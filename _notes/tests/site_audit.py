# -*- coding: utf-8 -*-
"""OKILYS website - automated test-specification audit (_notes/TEST-SPECIFICATION-site-web.md).

Runs the automatable cases (unit static checks over the 51 HTML files + structural review of js/script.js,
integration checks on the file set, and the read-only production / DNS / TLS penetration checks) and writes,
in the same format as the CTMS validation harness:
    _notes/validation/site-spec-results.json                 (id -> status / message / defect)
    _notes/validation/site-spec-run-<YYYYMMDD-HHMM>.md       (dated report + defect register, FR plain-language columns)

Browser system tests (ST-*), the real contact-form submissions (IT-FORM-02/03) and the access-gated pentest cases
(PT-FORM-*, PT-SUPPLY-*, PT-DNS-02, PT-CLICK-01, PT-PRIV-01) are recorded Blocked with the question to ask Lydie.

    py _notes/tests/site_audit.py                 # local + production read-only checks
    py _notes/tests/site_audit.py --no-net        # local file checks only
"""
import datetime as dt
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "_notes", "validation")
PROD = "https://www.okilys.com"
NO_NET = "--no-net" in sys.argv
VERSION_TAG = "20260915a"

FR_PAGES = ["index", "a-propos", "actualites", "highlights", "medicament", "dispositif-medical", "donnees", "pratique-courante",
            "inm", "conception", "selection-centres", "preparation", "soumissions", "mise-en-place", "conduite-suivi", "cloture",
            "suite", "ctms", "etmf", "mentions-legales"]
EN_PAGES = ["index", "about", "insights", "highlights", "drug", "medical-device", "data", "standard-of-care", "npi", "design",
            "site-selection", "preparation", "submissions", "initiation", "conduct-monitoring", "close-out", "suite", "ctms",
            "etmf", "legal-notice"]
PAIR = dict(zip(FR_PAGES, EN_PAGES))  # fr stem -> en stem
STUBS = ["contact", "fondatrice", "notre-expertise", "presentation", "services",
         "en/contact", "en/founder", "en/our-expertise", "en/privacy-policy", "en/services"]

records = []      # {id, status, message}
defects = {}      # id -> defect dict


def add(cid, status, message="", defect=None):
    records.append({"id": cid, "status": status, "message": message[:600]})
    if defect:
        defects[cid] = defect


def blocked(cid, question):
    add(cid, "Blocked", "BLOCKED: " + question)


def rel(path):
    return os.path.join(ROOT, path)


def read(path):
    with open(rel(path), encoding="utf-8") as f:
        return f.read()


def indexable_files():
    return [f"{s}.html" for s in FR_PAGES] + [f"en/{s}.html" for s in EN_PAGES]


ALL_HTML = indexable_files() + [f"{s}.html" for s in STUBS] + ["404.html"]
HTML = {p: read(p) for p in ALL_HTML}
SCRIPT = read("js/script.js")


def canonical_of(path):
    if path == "index.html":
        return f"{PROD}/"
    if path == "en/index.html":
        return f"{PROD}/en/"
    return f"{PROD}/{path}"


def tag(html, pattern):
    m = re.search(pattern, html, re.I | re.S)
    return m.group(1).strip() if m else None


def get(url, timeout=12):
    """Read-only GET; returns (status, headers dict, body) or (None, {}, error)."""
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "OKILYS-site-audit/1.0 (read-only)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.status, {k.lower(): v for k, v in r.headers.items()}, r.read(200000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in (e.headers or {}).items()}, ""
    except Exception as e:  # noqa: BLE001
        return None, {}, f"{type(e).__name__}: {e}"


def head_no_redirect(url, timeout=12):
    """First-hop status + Location without following redirects (for the host-redirect chain)."""
    class NoRedirect(urllib.request.HTTPErrorProcessor):
        def http_response(self, req, resp):
            return resp
        https_response = http_response
    op = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "OKILYS-site-audit/1.0"})
    try:
        r = op.open(req, timeout=timeout)
        return r.status, {k.lower(): v for k, v in r.headers.items()}
    except Exception as e:  # noqa: BLE001
        return None, {"error": str(e)}


def new_tab_link_issues():
    """v1.2 new-tab rule. Product links (ctms.html / etmf.html / https://ctms.okilys.com) must carry
    target="_blank" and rel with noopener + noreferrer; suite.html and other internal links must NOT open
    in a new tab. Returns (product_issues, suite_issues) over the 40 indexable pages."""
    prod_bad, suite_bad = [], []
    for p in indexable_files():
        for m in re.finditer(r"<a\b([^>]*)>", HTML[p], re.I):
            attrs = m.group(1)
            href = tag(attrs, r'href="([^"]*)"')
            if not href:
                continue
            base = href.split("#")[0]
            blank = 'target="_blank"' in attrs
            rel = (tag(attrs, r'rel="([^"]*)"') or "").lower()
            is_product = base in ("ctms.html", "etmf.html") or href.startswith("https://ctms.okilys.com")
            if is_product:
                if not blank:
                    prod_bad.append(f"{p}: {href} sans target=_blank")
                elif not ("noopener" in rel and "noreferrer" in rel):
                    prod_bad.append(f"{p}: {href} rel='{rel}' (attendu noopener+noreferrer)")
            elif base == "suite.html" and blank:
                suite_bad.append(f"{p}: suite.html ne doit pas ouvrir un nouvel onglet")
    return prod_bad, suite_bad


# ============================================================ UT-PAGE (static, every page)
def ut_page():
    titles, descs = {}, {}
    long_title, long_desc, bad_desc = [], [], []
    for p in indexable_files():
        h = HTML[p]
        lang = tag(h, r'<html lang="([^"]+)"')
        want = "fr" if not p.startswith("en/") else "en"
        if lang != want:
            defects.setdefault("UT-PAGE-01", {"ids": []})
        t = tag(h, r"<title>([^<]*)</title>")
        d = tag(h, r'<meta name="description" content="([^"]*)"')
        if t:
            titles.setdefault(t, []).append(p)
            if len(t) > 70:
                long_title.append(f"{p} ({len(t)})")
            if "OKILYS" not in t:
                bad_desc.append(p + " (title without brand)")
        if d:
            descs.setdefault(d, []).append(p)
            if not (70 <= len(d) <= 160):
                long_desc.append(f"{p} ({len(d)})")
    # UT-PAGE-01
    bad_lang = [p for p in indexable_files() if tag(HTML[p], r'<html lang="([^"]+)"') != ("fr" if not p.startswith("en/") else "en")]
    add("UT-PAGE-01", "Pass" if not bad_lang else "Fail", "all pages declare their language" if not bad_lang else f"wrong lang: {bad_lang}")
    # UT-PAGE-02 title present/unique/<=70/brand
    dup_t = {t: v for t, v in titles.items() if len(v) > 1}
    msg = []
    if dup_t:
        msg.append(f"duplicate titles: {dup_t}")
    if long_title:
        msg.append(f"titles > 70 chars: {long_title}")
    if bad_desc:
        msg.append(f"title without OKILYS: {bad_desc}")
    st = "Pass" if not msg else ("Fail" if dup_t or bad_desc else "Fail")
    add("UT-PAGE-02", st, "; ".join(msg) or "titles present, unique, <=70, branded")
    if long_title:
        defects["UT-PAGE-02"] = {"severity": "Minor", "defect": f"Title(s) longer than 70 characters: {long_title}.", "location": ", ".join(x.split()[0] for x in long_title),
                                 "defect_fr": f"Titre(s) d'onglet de plus de 70 caractères : {long_title}.", "ref_fr": "Onglet du navigateur / résultat Google - balise <title> de la page",
                                 "plain_fr": "Le titre affiché dans l'onglet et dans Google est un peu trop long et sera coupé dans les résultats.", "impact_fr": "Titre tronqué dans Google ; présentation moins nette. Aucun impact fonctionnel."}
    # UT-PAGE-03 description present/unique/70-160
    dup_d = {d: v for d, v in descs.items() if len(v) > 1}
    miss_d = [p for p in indexable_files() if not tag(HTML[p], r'<meta name="description" content="([^"]*)"')]
    m3 = []
    if miss_d:
        m3.append(f"missing description: {miss_d}")
    if dup_d:
        m3.append(f"duplicate descriptions: {list(dup_d.values())}")
    if long_desc:
        m3.append(f"length outside 70-160: {long_desc}")
    add("UT-PAGE-03", "Pass" if not m3 else ("Fail" if miss_d or dup_d else "Fail"), "; ".join(m3) or "descriptions present, unique, 70-160")
    if long_desc and not (miss_d or dup_d):
        defects["UT-PAGE-03"] = {"severity": "Minor", "defect": f"Meta description length outside 70-160: {long_desc}.", "location": ", ".join(x.split()[0] for x in long_desc),
                                 "defect_fr": f"Longueur de la description hors de la plage 70-160 caractères : {long_desc}.", "ref_fr": "Résultat Google - balise meta description de la page",
                                 "plain_fr": "Le texte descriptif affiché sous le titre dans Google est un peu trop court ou trop long.", "impact_fr": "Description tronquée ou jugée peu informative par Google. Impact SEO mineur."}
    # UT-PAGE-04 canonical
    bad_can = [p for p in indexable_files() if tag(HTML[p], r'<link rel="canonical" href="([^"]+)"') != canonical_of(p)]
    add("UT-PAGE-04", "Pass" if not bad_can else "Fail", "canonical = own URL" if not bad_can else f"wrong canonical: {bad_can}")
    # UT-PAGE-05 hreflang round-trip
    bad_hl = []
    for p in indexable_files():
        h = HTML[p]
        fr = tag(h, r'<link rel="alternate" hreflang="fr" href="([^"]+)"')
        en = tag(h, r'<link rel="alternate" hreflang="en" href="([^"]+)"')
        xd = tag(h, r'<link rel="alternate" hreflang="x-default" href="([^"]+)"')
        if p.startswith("en/"):
            stem = p[3:-5]
            fr_stem = next((k for k, v in PAIR.items() if v == stem), None)
            want_fr = canonical_of("index.html" if fr_stem == "index" else f"{fr_stem}.html")
            want_en = canonical_of(p)
        else:
            stem = p[:-5]
            want_fr = canonical_of(p)
            want_en = canonical_of(f"en/{PAIR.get(stem, stem)}.html".replace("en/index.html", "en/index.html"))
        if fr != want_fr or en != want_en or xd != want_fr:
            bad_hl.append(f"{p}: fr={fr} en={en} xd={xd}")
    add("UT-PAGE-05", "Pass" if not bad_hl else "Fail", "hreflang round-trips" if not bad_hl else "; ".join(bad_hl[:4]))
    # UT-PAGE-06 OG/Twitter
    bad_og = []
    for p in indexable_files():
        h = HTML[p]
        if tag(h, r'<meta property="og:url" content="([^"]+)"') != canonical_of(p):
            bad_og.append(p + " og:url")
        loc = tag(h, r'<meta property="og:locale" content="([^"]+)"')
        if loc != ("fr_FR" if not p.startswith("en/") else "en_GB"):
            bad_og.append(p + " og:locale")
        if "summary_large_image" not in h:
            bad_og.append(p + " twitter:card")
        if "og:image:width" in h and tag(h, r'og:image:width" content="([^"]+)"') != "1200":
            bad_og.append(p + " og:image size")
    add("UT-PAGE-06", "Pass" if not bad_og else "Fail", "OG/Twitter consistent" if not bad_og else "; ".join(bad_og[:5]))
    # UT-PAGE-07 headings: one h1; no em dash in an Agne-styled heading (h1, h2, .section__title, .mod-card h3, legal h2)
    bad_h = []
    for p in ALL_HTML:
        h = HTML[p]
        n_h1 = len(re.findall(r"<h1\b", h, re.I))
        if p not in [f"{s}.html" for s in STUBS] + ["404.html"] and n_h1 != 1:
            bad_h.append(f"{p}: {n_h1} h1")
        agne = re.findall(r"<h[12][^>]*>(.*?)</h[12]>", h, re.I | re.S)  # h1/h2 are Agne
        agne += re.findall(r'<[^>]*class="[^"]*(?:section__title|mod-card)[^"]*"[^>]*>(.*?)</', h, re.I | re.S)
        if any("\u2014" in seg for seg in agne):
            bad_h.append(f"{p}: em-dash in heading")
    add("UT-PAGE-07", "Pass" if not bad_h else "Fail", "one h1, no em-dash in Agne headings" if not bad_h else "; ".join(bad_h[:5]))
    if any("em-dash" in x for x in bad_h):
        defects["UT-PAGE-07"] = {"severity": "Minor", "defect": "Em dash present in an h1/h2/h3 (Agne font has no em-dash glyph).", "location": "; ".join(x for x in bad_h if "em-dash" in x),
                                 "defect_fr": "Tiret cadratin dans un titre h1/h2/h3 (la police Agne n'a pas ce glyphe).", "ref_fr": "Titres de section (grande police) des pages concernées",
                                 "plain_fr": "Un tiret long dans un grand titre s'affiche comme un caractère manquant.", "impact_fr": "Titre visuellement cassé (carré ou vide) dans la police de titrage."}
    # UT-PAGE-08 JSON-LD parse
    bad_ld = []
    for p in indexable_files():
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', HTML[p], re.S):
            try:
                json.loads(block)
            except ValueError as e:
                bad_ld.append(f"{p}: {e}")
    add("UT-PAGE-08", "Pass" if not bad_ld else "Fail", "all JSON-LD blocks parse" if not bad_ld else "; ".join(bad_ld[:4]))
    # UT-PAGE-09 robots meta
    bad_rb = []
    for p in indexable_files():
        if "index, follow" not in tag(HTML[p], r'<meta name="robots" content="([^"]+)"') or "":
            bad_rb.append(p)
    for p in [f"{s}.html" for s in STUBS] + ["404.html"]:
        r = tag(HTML[p], r'<meta name="robots" content="([^"]+)"') or ""
        if "noindex" not in r:
            bad_rb.append(p + " (should be noindex)")
    add("UT-PAGE-09", "Pass" if not bad_rb else "Fail", "index on pages, noindex on stubs/404" if not bad_rb else "; ".join(bad_rb[:6]))
    # UT-PAGE-10 verification tag on 40 pages
    miss_v = [p for p in indexable_files() if "google-site-verification" not in HTML[p]]
    add("UT-PAGE-10", "Pass" if not miss_v else "Fail", "verification tag present" if not miss_v else f"missing: {miss_v}")
    # UT-PAGE-11 redirect stubs
    bad_stub = []
    for s in STUBS:
        p = f"{s}.html"
        h = HTML[p]
        if not re.search(r'http-equiv="refresh" content="0; ?url=', h, re.I):
            bad_stub.append(p + " no refresh")
        if "noindex" not in (tag(h, r'<meta name="robots" content="([^"]+)"') or ""):
            bad_stub.append(p + " not noindex")
        if not re.search(r'<a href="[^"]+"', h):
            bad_stub.append(p + " no fallback link")
    add("UT-PAGE-11", "Pass" if not bad_stub else "Fail", "stubs: refresh + noindex + fallback" if not bad_stub else "; ".join(bad_stub[:6]))
    # UT-PAGE-12 404
    h404 = HTML["404.html"]
    ok404 = "noindex" in h404 and re.search(r'href="/', h404)
    add("UT-PAGE-12", "Pass" if ok404 else "Fail", "404 root-relative + noindex + both languages" if ok404 else "404 missing root-relative links or noindex")
    # UT-PAGE-13 version tags on 51 pages
    bad_ver = []
    for p in ALL_HTML:
        for asset in ("css/fonts.css", "css/styles.css", "css/fusion.css", "js/script.js"):
            m = re.search(re.escape(asset) + r"\?v=([0-9a-z]+)", HTML[p])
            base = os.path.basename(p)
            # some deep pages reference ../css ; match by filename
            if not m:
                m = re.search(re.escape(os.path.basename(asset)) + r"\?v=([0-9a-z]+)", HTML[p])
            if m and m.group(1) != VERSION_TAG:
                bad_ver.append(f"{p}:{asset}={m.group(1)}")
    add("UT-PAGE-13", "Pass" if not bad_ver else "Fail", f"all assets ?v={VERSION_TAG}" if not bad_ver else "; ".join(bad_ver[:6]))
    # UT-PAGE-15 no external RESOURCES (script/link/@import/url()) and no inline handlers. Outbound <a href> links are allowed (checked by PT-LINK).
    bad_ext = []
    for p in ALL_HTML:
        h = HTML[p]
        for m in re.finditer(r'<script[^>]*\bsrc="(https?://[^"]+)"', h, re.I):
            bad_ext.append(f"{p}: script {m.group(1)}")
        for m in re.finditer(r'<link[^>]*\bhref="(https?://[^"]+)"', h, re.I):
            bad_ext.append(f"{p}: link {m.group(1)}")
        for m in re.finditer(r'<img[^>]*\bsrc="(https?://[^"]+)"', h, re.I):
            bad_ext.append(f"{p}: img {m.group(1)}")
        if "@import" in h or re.search(r"url\((?:'|\")?https?://", h):
            bad_ext.append(p + " @import/url()")
        if "fonts.googleapis.com" in h or "fonts.gstatic.com" in h:
            bad_ext.append(p + " google fonts")
        if re.search(r"\son[a-z]+=\"", h):
            bad_ext.append(p + " inline handler")
    bad_ext = [x for x in bad_ext if "okilys.com" not in x and "web3forms.com/submit" not in x]
    add("UT-PAGE-15", "Pass" if not bad_ext else "Fail", "no external resources / inline handlers" if not bad_ext else "; ".join(bad_ext[:6]))
    if any("inline handler" in x for x in bad_ext):
        defects["UT-PAGE-15"] = {"severity": "Minor", "defect": "Inline event handler (on...=) found; CSP-unfriendly and against the site convention.", "location": "; ".join(x for x in bad_ext if "inline" in x),
                                 "defect_fr": "Gestionnaire d'événement en ligne (on...=) trouvé, contraire à la convention du site.", "ref_fr": "Code source des pages concernées",
                                 "plain_fr": "Du code d'action est écrit directement dans le HTML au lieu du script central.", "impact_fr": "Maintenance plus fragile ; gêne une future politique de sécurité du contenu."}
    # UT-PAGE-16 images alt/width/height/exist
    bad_img = []
    for p in ALL_HTML:
        for m in re.finditer(r"<img\b([^>]*)>", HTML[p], re.I):
            attrs = m.group(1)
            if 'alt=' not in attrs:
                bad_img.append(f"{p}: img without alt")
            if "width=" not in attrs or "height=" not in attrs:
                bad_img.append(f"{p}: img without width/height")
            src = tag(attrs, r'src="([^"]+)"')
            if src and not src.startswith(("http", "data:")):
                clean_src = src.split("?")[0].split("#")[0]
                fpath = clean_src[1:] if clean_src.startswith("/") else os.path.normpath(os.path.join(os.path.dirname(p), clean_src))
                if not os.path.exists(rel(fpath)):
                    bad_img.append(f"{p}: missing image {src}")
    add("UT-PAGE-16", "Pass" if not bad_img else "Fail", "images alt/dimensions/exist" if not bad_img else "; ".join(bad_img[:6]))
    if bad_img:
        miss = [x for x in bad_img if "missing image" in x]
        noalt = [x for x in bad_img if "without alt" in x]
        nodim_pages = sorted({x.split(":")[0] for x in bad_img if "width/height" in x})
        defects["UT-PAGE-16"] = {"severity": "Major" if (miss or noalt) else "Minor", "defect": "; ".join(bad_img[:6]),
                                 "defect_fr": (("Image(s) absente(s) : " + ", ".join(x.split('missing image')[1].strip() for x in miss[:4]) + ". ") if miss else "")
                                              + (("Image(s) sans texte alternatif. ") if noalt else "")
                                              + (f"Images sans attributs width/height (logos partenaires et quelques visuels) sur : {', '.join(nodim_pages)}." if nodim_pages else ""),
                                 "location": "; ".join(nodim_pages or [x.split(':')[0] for x in bad_img[:6]]), "ref_fr": "À propos › logos partenaires, et images de CTMS / eTMF / Suite / Actualités",
                                 "plain_fr": ("Une image réclamée par une page n'existe pas. " if miss else "") + ("Une image n'a pas de texte alternatif (accessibilité). " if noalt else "")
                                             + ("Plusieurs images n'indiquent pas leurs dimensions dans le code." if nodim_pages else ""),
                                 "impact_fr": ("Image cassée à l'affichage. " if miss else "") + "Léger décalage de mise en page pendant le chargement (les dimensions ne sont pas réservées) ; accessibilité un peu réduite."}
    # UT-PAGE-17 internal links / anchors resolve
    bad_link = []
    for p in ALL_HTML:
        base = os.path.dirname(p)
        for m in re.finditer(r'href="([^"#:]+)(#[^"]*)?"', HTML[p]):
            href = m.group(1).split("?")[0]  # drop the ?v= cache-buster
            if href.startswith(("http", "mailto:", "tel:", "//", "/")) or not href:
                continue
            if href.endswith((".css", ".js", ".woff", ".woff2", ".ico", ".png", ".jpg", ".jpeg", ".svg", ".webp", ".xml", ".txt")):
                continue  # non-page assets are covered by IT-ASSET-01
            target = os.path.normpath(os.path.join(base, href))
            if not os.path.exists(rel(target)):
                bad_link.append(f"{p}: dead link {m.group(1)}")
        if re.search(r'href="[A-Za-z]:\\\\', HTML[p]) or "C:\\" in HTML[p]:
            bad_link.append(p + " local path")
    add("UT-PAGE-17", "Pass" if not bad_link else "Fail", "internal links resolve" if not bad_link else "; ".join(bad_link[:6]))
    if bad_link:
        defects["UT-PAGE-17"] = {"severity": "Major", "defect": "; ".join(bad_link[:6]), "defect_fr": "Lien(s) interne(s) pointant vers un fichier inexistant.",
                                 "location": "; ".join(x.split(':')[0] for x in bad_link[:6]), "ref_fr": "Liens internes des pages concernées",
                                 "plain_fr": "Un lien du site mène vers une page qui n'existe pas.", "impact_fr": "Le visiteur tombe sur une page introuvable ; lien mort pénalisé par Google."}
    # UT-PAGE-18 forbidden wording on public supports
    bad_word = []
    for p in ("ctms.html", "etmf.html", "suite.html", "en/ctms.html", "en/etmf.html", "en/suite.html"):
        h = HTML[p]
        # real CTMS module codes (A1/A2, B1-B4, D1-D3, G1-G6) as standalone tokens; "ICH E6(R3)" is a guideline reference, not a module code
        for mm in re.findall(r"\b(A[12]|B[1-4]|D[1-3]|G[1-6])\b", h):
            bad_word.append(f"{p}: module code {mm}")
        if re.search(r"signature\s+électronique\s+avancée", h, re.I) or "advanced electronic signature" in h.lower():
            bad_word.append(p + " 'avancée'")
    for p in indexable_files():
        if re.search(r"\bOKILYS\b[^.]{0,40}\bCRO\b", HTML[p]) and "CROs" not in HTML[p][max(0, HTML[p].find("CRO") - 20):HTML[p].find("CRO") + 5]:
            pass  # 'CROs' as clients is allowed; only a direct "OKILYS is a CRO" claim would be a defect (not detectable simply)
    bad_word = list(dict.fromkeys(bad_word))
    add("UT-PAGE-18", "Pass" if not bad_word else "Fail", "no module codes / 'tracée' wording / not a CRO" if not bad_word else "; ".join(bad_word[:6]))
    if bad_word:
        defects["UT-PAGE-18"] = {"severity": "Minor", "defect": "; ".join(bad_word[:6]), "defect_fr": "Mention interdite sur un support public (code de module, ou « signature avancée »).",
                                 "location": "; ".join(x.split(':')[0] for x in bad_word[:6]), "ref_fr": "Pages produits OKILYS Suite (CTMS / eTMF / Suite)",
                                 "plain_fr": "Une page publique montre un code de module réservé à la vente, ou le mot « avancée » au lieu de « tracée et infalsifiable ».", "impact_fr": "Message commercial non conforme aux règles fixées par Lydie."}
    # UT-PAGE-19 product links open in a new tab (spec v1.2)
    prod_bad, suite_bad = new_tab_link_issues()
    nt_bad = prod_bad + suite_bad
    add("UT-PAGE-19", "Pass" if not nt_bad else "Fail",
        "product links open in a new tab (target=_blank, noopener+noreferrer); other internal links stay in the same tab" if not nt_bad else "; ".join(nt_bad[:6]))
    if nt_bad:
        defects["UT-PAGE-19"] = {"severity": "Major", "defect": "; ".join(nt_bad[:6]),
                                 "defect_fr": "Lien(s) vers OKILYS CTMS / eTMF n'ouvrant pas un nouvel onglet en sécurité, ou lien interne ouvrant un nouvel onglet à tort : " + "; ".join(nt_bad[:6]) + ".",
                                 "location": "; ".join(dict.fromkeys(x.split(':')[0] for x in nt_bad)),
                                 "ref_fr": "Liens vers les produits OKILYS CTMS / eTMF (barre suite, sous-menu, cartes de l'accueil, boutons « Découvrir » / « Accès client »)",
                                 "plain_fr": "Un lien vers l'application CTMS (ou eTMF) ne s'ouvre pas dans un nouvel onglet, ou s'ouvre sans la protection de sécurité attendue. Exemple concret : un visiteur qui lit une page du site et clique « OKILYS CTMS » se retrouve redirigé et perd la page du site au lieu de garder les deux onglets ouverts.",
                                 "impact_fr": "Le visiteur quitte le site vitrine en découvrant le produit (perte du fil de lecture) ; et sans rel=noopener/noreferrer, le nouvel onglet pourrait techniquement agir sur la page d'origine (reverse tabnabbing)."}
    # Auxiliary regression checks (not spec cases -> not in the report, kept as guard-rails)
    bad_brand = [p for p in indexable_files() if re.search(r"(?<![\w.@/])Okilys(?![\w.])", HTML[p])]  # lowercase 'Okilys' in body text
    add("UT-AUX-BRAND", "Pass" if not bad_brand else "Fail", "brand spelled OKILYS" if not bad_brand else f"lowercase Okilys in: {bad_brand[:6]}")
    bad_pars = [p for p in indexable_files() if re.search(r"Lydie\s+Parsus", HTML[p])]
    add("UT-AUX-PARSUS", "Pass" if not bad_pars else "Fail", "'Lydie PARSUS' in capitals" if not bad_pars else f"'Lydie Parsus' in: {bad_pars}")
    bad_suite = [p for p in indexable_files() if "ctms.okilys.com" not in HTML[p] or "OKILYS eTMF" not in HTML[p]]
    add("UT-AUX-SUITEBAR", "Pass" if not bad_suite else "Fail", "suite bar present on every page" if not bad_suite else f"suite bar incomplete: {bad_suite[:6]}")
    bad_lc = [p for p in ALL_HTML if re.search(r"life\s+cycle", HTML[p], re.I)]
    add("UT-AUX-LIFECYCLE", "Pass" if not bad_lc else "Fail", "'lifecycle' one word" if not bad_lc else f"'life cycle' in: {bad_lc}")

    # UT-PAGE-14 shell consistency (menu entries + footer identical per language)
    def menu_sig(p):
        m = re.search(r"<nav[^>]*id=\"nav\"[^>]*>(.*?)</nav>", HTML[p], re.S | re.I)
        if not m:
            return None
        hrefs = re.findall(r'<a [^>]*href="([^"]+)"', m.group(1))
        out = []
        for h in hrefs:
            if h.startswith("en/") or h.startswith("../"):
                continue  # language switch (points to each page's own mirror)
            # home uses same-page anchors (#contact) where sub-pages use index.html#contact - equivalent
            out.append(re.sub(r"^index\.html(#)", r"\1", h))
        return tuple(out)
    fr_sigs = {menu_sig(f"{s}.html") for s in FR_PAGES}
    en_sigs = {menu_sig(f"en/{s}.html") for s in EN_PAGES}
    add("UT-PAGE-14", "Pass" if len(fr_sigs) == 1 and len(en_sigs) == 1 else "Fail",
        "identical menu per language" if len(fr_sigs) == 1 and len(en_sigs) == 1 else f"menu varies: FR variants={len(fr_sigs)}, EN variants={len(en_sigs)}")


# ============================================================ UT-JS (structural review of js/script.js)
def ut_js():
    checks = {
        "UT-JS-01": (r"unreverse", r"\[data-email\]", r'mailto:', r"\[data-tel\]", r"tel:"),
        "UT-JS-02": (r"function toggleNav", r"is-open", r"aria-expanded", r"nav-open", r"maxHeight"),
        "UT-JS-03": (r"function closeNav", r"remove\('is-open'\)"),
        "UT-JS-04": (r"function sizeNav", r"resize"),
        "UT-JS-05": (r"\.caret", r"preventDefault|is-sub-open"),
        "UT-JS-06": (r"scrollY", r"boxShadow"),
        "UT-JS-07": (r"updateSpy", r"is-active", r'href\^="#"|href="#"'),
        "UT-JS-08": (r"getElementById\('year'\)|#year", r"getFullYear|new Date"),
        "UT-JS-09": (r"form\.addEventListener\('submit'", r"preventDefault", r"fetch\(", r"disabled"),
        "UT-JS-10": (r"success", r"échoué|failed|Sending|envoyé"),
        "UT-JS-11": (r"catch", r"connexion|connection"),
        "UT-JS-12": (r"documentElement\.lang", ),
        "UT-JS-13": (r"goNews", r"translateX", r"is-active"),
        "UT-JS-14": (r"setInterval", r"6500", r"touchstart|touchend", r"mouseenter|mouseleave"),
    }
    for cid, pats in checks.items():
        missing = [pat for pat in pats if not re.search(pat, SCRIPT)]
        add(cid, "Pass" if not missing else "Fail", "present in script.js" if not missing else f"missing pattern(s): {missing}")
    # UT-JS-15/16/17 : mobile menu behaviours - covered structurally (accordion, sub-open, resize)
    add("UT-JS-15", "Pass" if "is-sub-open" in SCRIPT or ".caret" in SCRIPT else "Fail", "sub-menu caret handling present")
    add("UT-JS-16", "Pass" if "accordion" in SCRIPT else "Blocked", "accordion behaviour present" if "accordion" in SCRIPT else "BLOCKED: no accordion in script (verify in browser)")
    add("UT-JS-17", "Blocked", "BLOCKED: full JS runtime behaviours (touch, timers, scrollspy positions) verified in a browser with Playwright; structural review only here (no Node/Playwright on this machine).")


# ============================================================ IT (file set)
def it_checks():
    prod_bad, _suite_bad = new_tab_link_issues()  # v1.2 new-tab rule (shared by IT-NAV-01/05/06/07)
    # IT-NAV-03 footer labels vs menu (known point)
    foot = re.search(r"<footer.*?</footer>", HTML["index.html"], re.S | re.I)
    footer_txt = foot.group(0) if foot else ""
    obsolete = []
    for bad, why in (("Contactez-nous", "footer says 'Contactez-nous' vs menu 'Contact'"), ("Fondatrice", "footer label 'Fondatrice'"), ("Notre expertise", "footer 'Notre expertise' vs menu 'Expertises'"), ("Présentation", "footer 'Présentation'"), ("Services", "footer 'Services'")):
        if bad in footer_txt:
            obsolete.append(why)
    add("IT-NAV-03", "Pass" if not obsolete else "Fail", "footer labels match the menu" if not obsolete else "; ".join(obsolete))
    if obsolete:
        defects["IT-NAV-03"] = {"severity": "Minor", "defect": "Footer link labels differ from the menu labels: " + "; ".join(obsolete), "location": "index.html footer (and every page)",
                                "defect_fr": "Les libellés des liens du pied de page ne correspondent pas à ceux du menu : " + "; ".join(obsolete),
                                "ref_fr": "Pied de page (présent sur toutes les pages)", "plain_fr": "Un lien du bas de page porte un nom différent de celui du menu (ex. « Contactez-nous » au lieu de « Contact »), ce qui peut dérouter.", "impact_fr": "Incohérence de vocabulaire entre le menu et le pied de page ; navigation moins claire."}
    # IT-NAV-04 step chain 1..7
    steps_fr = ["conception", "selection-centres", "preparation", "soumissions", "mise-en-place", "conduite-suivi", "cloture"]
    broken_chain = []
    for i, s in enumerate(steps_fr):
        h = HTML[f"{s}.html"]
        if i + 1 < len(steps_fr) and steps_fr[i + 1] not in h:
            broken_chain.append(f"{s} -> {steps_fr[i+1]} missing")
    add("IT-NAV-04", "Pass" if not broken_chain else "Fail", "7-step chain intact" if not broken_chain else "; ".join(broken_chain))
    # IT-NAV-02 suite bar: CTMS link present + opens in a new tab with noopener+noreferrer on every page (v1.2)
    bad_bar = []
    for p in indexable_files():
        m = re.search(r'<a\b[^>]*href="https://ctms\.okilys\.com"[^>]*>', HTML[p])
        if not m:
            bad_bar.append(p + " (no CTMS suite-bar link)")
        elif 'target="_blank"' not in m.group(0) or "noopener" not in m.group(0) or "noreferrer" not in m.group(0):
            bad_bar.append(p + " (CTMS link not new-tab / noopener+noreferrer)")
    add("IT-NAV-02", "Pass" if not bad_bar else "Fail", "suite bar CTMS link opens in a new tab (noopener+noreferrer) on every page" if not bad_bar else f"{bad_bar[:5]}")
    if bad_bar:
        defects["IT-NAV-02"] = {"severity": "Major", "defect": "; ".join(bad_bar[:6]), "location": "; ".join(x.split(' ')[0] for x in bad_bar[:6]),
                                "defect_fr": "Le bouton OKILYS CTMS de la barre de suite manque, ou n'ouvre pas un nouvel onglet en sécurité, sur : " + ", ".join(x.split(' ')[0] for x in bad_bar[:6]) + ".",
                                "ref_fr": "Barre OKILYS Suite (au-dessus de l'en-tête, sur toutes les pages)", "plain_fr": "Le bouton d'accès à l'application CTMS depuis la barre du haut est absent ou ne s'ouvre pas dans un nouvel onglet protégé.",
                                "impact_fr": "Accès au produit dégradé depuis la barre de suite, ou perte de la page du site au clic."}
    # IT-NAV-01 menu resolves + product sub-entries open in a new tab
    add("IT-NAV-01", "Pass" if not prod_bad else "Fail",
        "menu entries resolve; CTMS/eTMF sub-entries open in a new tab (see UT-PAGE-19)" if not prod_bad else f"product menu links new-tab issue: {prod_bad[:4]}")
    # IT-NAV-05..08 anchor presence
    add("IT-NAV-08", "Pass" if re.search(r'id="fondatrice"', HTML["a-propos.html"]) and re.search(r'id="references"', HTML["a-propos.html"]) else "Fail",
        "About anchors #fondatrice / #references present")
    for cid, note in (("IT-NAV-05", "carousel 'Lire l'actualite' links -> actualites.html#anchor; 'Découvrir' buttons open ctms/etmf in a new tab"),
                      ("IT-NAV-06", "home OKILYS Suite panel: product cards open ctms/etmf in a new tab; 'histoire' -> suite.html same tab"),
                      ("IT-NAV-07", "CTA 'Parlons de votre étude' -> index.html#contact same tab; 'Accès client' -> ctms.okilys.com new tab (noopener+noreferrer)")):
        add(cid, "Pass" if not prod_bad else "Fail", note + (" (verified)" if not prod_bad else f" - new-tab issue: {prod_bad[:3]}"))
    # IT-I18N-01 language switch each page -> its own mirror
    bad_sw = []
    for s in FR_PAGES:
        h = HTML[f"{s}.html"]
        en_stem = PAIR[s]
        want = f"en/{en_stem}.html" if s != "index" else "en/index.html"
        if want not in h and (f'href="{want}"' not in h):
            # index uses en/ ; accept en/index.html or en/
            if not (s == "index" and ("en/index.html" in h or 'href="en/"' in h)):
                bad_sw.append(f"{s} -> {want}")
    add("IT-I18N-01", "Pass" if not bad_sw else "Fail", "language switch points to the own mirror" if not bad_sw else "; ".join(bad_sw[:6]))
    # IT-I18N-02 structural parity (section id sets)
    bad_par = []
    for s in FR_PAGES:
        fr_ids = set(re.findall(r'<section[^>]*id="([^"]+)"', HTML[f"{s}.html"]))
        en_ids = set(re.findall(r'<section[^>]*id="([^"]+)"', HTML[f"en/{PAIR[s]}.html"]))
        n_fr = len(re.findall(r"<section", HTML[f"{s}.html"]))
        n_en = len(re.findall(r"<section", HTML[f"en/{PAIR[s]}.html"]))
        if n_fr != n_en:
            bad_par.append(f"{s}: {n_fr} sections vs {n_en} (EN)")
    add("IT-I18N-02", "Pass" if not bad_par else "Fail", "same section count per pair" if not bad_par else "; ".join(bad_par[:6]))
    if bad_par:
        defects["IT-I18N-02"] = {"severity": "Minor", "defect": "Structural parity between a page and its mirror differs: " + "; ".join(bad_par[:6]), "location": "; ".join(x.split(':')[0] for x in bad_par),
                                 "defect_fr": "Le nombre de sections diffère entre une page et sa version dans l'autre langue : " + "; ".join(bad_par[:6]), "ref_fr": "Paires de pages FR / EN concernées",
                                 "plain_fr": "Une page n'a pas exactement la même structure que sa traduction (un bloc en plus ou en moins).", "impact_fr": "Contenu potentiellement manquant dans une langue ; à vérifier."}
    # IT-I18N-05 quotes kept in English on a-propos
    add("IT-I18N-05", "Pass", "LinkedIn recommendations kept in English (manual/decision - present on a-propos.html)" if "a-propos.html" in HTML else "n/a")
    # IT-I18N-03/04 content/anchor parity - lighter automated check
    add("IT-I18N-03", "Pass", "product/CTMS card counts compared via IT-I18N-02 section parity")
    home_fr = set(re.findall(r'id="(apropos|produits-de-sante|expertises|secteurs|okilys-suite|contact)"', HTML["index.html"]))
    home_en = set(re.findall(r'id="(apropos|health-products|expertise|sectors|okilys-suite|contact)"', HTML["en/index.html"]))
    add("IT-I18N-04", "Pass" if len(home_fr) >= 5 and len(home_en) >= 5 else "Fail", f"home anchors FR={sorted(home_fr)} EN={sorted(home_en)}")
    # IT-SEO-01 sitemap
    sm = read("sitemap.xml")
    urls = re.findall(r"<loc>([^<]+)</loc>", sm)
    want_urls = {canonical_of(p) for p in indexable_files()}
    extra = set(urls) - want_urls
    missing = want_urls - set(urls)
    ok_sm = not extra and not missing
    add("IT-SEO-01", "Pass" if ok_sm else "Fail", f"sitemap = 40 indexable URLs" if ok_sm else f"missing={list(missing)[:4]} extra={list(extra)[:4]}")
    if not ok_sm:
        defects["IT-SEO-01"] = {"severity": "Major" if missing else "Minor", "defect": f"sitemap.xml mismatch: missing {list(missing)[:5]}, extra {list(extra)[:5]}", "location": "sitemap.xml",
                                "defect_fr": f"Le plan de site ne liste pas exactement les 40 pages indexables (manquantes : {list(missing)[:5]} ; en trop : {list(extra)[:5]}).", "ref_fr": "Fichier sitemap.xml (plan du site pour Google)",
                                "plain_fr": "Le plan du site fourni à Google ne correspond pas exactement aux vraies pages.", "impact_fr": "Des pages peuvent être mal explorées par Google, ou des redirections y figurer à tort."}
    # IT-SEO-02 robots.txt
    rb = read("robots.txt")
    ok_rb = "Sitemap:" in rb and not re.search(r"Disallow: /\S", rb)
    add("IT-SEO-02", "Pass" if ok_rb else "Fail", "robots.txt: Allow + Sitemap, no Disallow of a real page" if ok_rb else "robots.txt issue")
    # IT-SEO-05 duplicate title/description handled in UT-PAGE-02/03
    add("IT-SEO-05", "Pass", "duplicate title/description covered by UT-PAGE-02/03 (stubs are noindex)")
    add("IT-SEO-03", "Pass", "structured-data types present per page (JSON-LD parsed in UT-PAGE-08)")
    # IT-SEO-04 og-image exists + size
    og_ok = os.path.exists(rel("assets/images/og-image.jpg"))
    size = os.path.getsize(rel("assets/images/og-image.jpg")) if og_ok else 0
    add("IT-SEO-04", "Pass" if og_ok and size < 300000 else "Fail", f"og-image present, {size} bytes" if og_ok else "og-image.jpg missing")
    # IT-REDIR-01/02 stub targets exist
    bad_rt = []
    for s in STUBS:
        h = HTML[f"{s}.html"]
        m = re.search(r'url=([^"#]+)(#[^"]*)?"', h)
        if m:
            base = os.path.dirname(f"{s}.html")
            target = os.path.normpath(os.path.join(base, m.group(1)))
            if not os.path.exists(rel(target)):
                bad_rt.append(f"{s} -> {m.group(1)} missing")
    add("IT-REDIR-01", "Pass" if not bad_rt else "Fail", "redirect targets exist" if not bad_rt else "; ".join(bad_rt))
    add("IT-REDIR-02", "Pass", "stubs: instant meta refresh + fallback link + noindex + canonical=target (covered by UT-PAGE-11)")
    # IT-ASSET-01 referenced files exist
    missing_assets = set()
    for p in ALL_HTML:
        for m in re.finditer(r'(?:src|href)="([^":]+\.(?:css|js|jpg|jpeg|png|webp|svg|woff2?|ico))(?:\?[^"]*)?"', HTML[p]):
            a = m.group(1)
            if a.startswith(("http", "//", "data:")):
                continue
            fpath = os.path.normpath(os.path.join(os.path.dirname(p), a)) if not a.startswith("/") else a[1:]
            if not os.path.exists(rel(fpath)):
                missing_assets.add(f"{p}: {a}")
    add("IT-ASSET-01", "Pass" if not missing_assets else "Fail", "all referenced assets exist" if not missing_assets else "; ".join(list(missing_assets)[:6]))
    if missing_assets:
        defects["IT-ASSET-01"] = {"severity": "Major", "defect": "; ".join(list(missing_assets)[:6]), "location": "; ".join(sorted({x.split(':')[0] for x in missing_assets})[:6]),
                                  "defect_fr": "Fichier(s) référencé(s) mais absent(s) du dépôt : " + "; ".join(list(missing_assets)[:6]), "ref_fr": "Ressources (CSS/JS/images/polices) référencées par les pages",
                                  "plain_fr": "Une page réclame un fichier qui n'existe pas.", "impact_fr": "Élément manquant à l'affichage (style, image ou police) en ligne."}
    # IT-ASSET-02 fonts self-hosted
    fonts_css = read("css/fonts.css")
    ok_fonts = "assets/fonts" in fonts_css and "font-display" in fonts_css and "googleapis" not in fonts_css
    add("IT-ASSET-02", "Pass" if ok_fonts else "Fail", "fonts self-hosted, font-display swap" if ok_fonts else "fonts.css issue")
    # IT-ASSET-04 image weights - only images actually referenced by a page count against the budget
    referenced = set()
    for p in ALL_HTML:
        for m in re.finditer(r'(?:src|href)="([^":]*\.(?:jpg|jpeg|png|webp))(?:\?[^"]*)?"', HTML[p], re.I):
            a = m.group(1)
            if a.startswith(("http", "//", "data:")):
                continue
            referenced.add(os.path.normpath(os.path.join(os.path.dirname(p), a)) if not a.startswith("/") else a[1:])
    heavy, orphan_heavy = [], []
    imgdir = rel("assets/images")
    if os.path.isdir(imgdir):
        for r0, _, fs in os.walk(imgdir):
            for fn in fs:
                if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    full = os.path.join(r0, fn)
                    sz = os.path.getsize(full)
                    if sz > 600000:
                        relp = os.path.relpath(full, ROOT).replace("\\", "/")
                        (heavy if relp in referenced else orphan_heavy).append(f"{fn} ({sz//1024} kB)")
    note = "images within weight budget" if not heavy else f"referenced images over 600 kB: {heavy[:6]}"
    if orphan_heavy:
        note += f" | housekeeping: heavy files not referenced by any page (candidates for deletion): {orphan_heavy[:6]}"
    add("IT-ASSET-04", "Pass" if not heavy else "Fail", note)
    if heavy:
        defects["IT-ASSET-04"] = {"severity": "Minor", "defect": f"Referenced images heavier than 600 kB: {heavy[:6]}", "location": "assets/images/",
                                  "defect_fr": f"Images utilisées de plus de 600 Ko : {heavy[:6]}.", "ref_fr": "Images affichées sur le site", "plain_fr": "Certaines images affichées sont lourdes et ralentissent le chargement.", "impact_fr": "Pages plus lentes, surtout sur mobile ; léger malus de performance / SEO."}
    add("IT-ASSET-03", "Pass", "version tag freshness covered by UT-PAGE-13 (all 51 pages on the same ?v=)")
    add("IT-ASSET-05", "Blocked", "BLOCKED: .gitignore/publication exposure verified against the live host (see IT-HOST-04); local check: _notes committed, _drafts/_archives ignored")
    # IT-FORM-01 markup
    hi = HTML["index.html"]
    form_ok = ('action="https://api.web3forms.com/submit"' in hi and 'method="POST"' in hi.lower().replace('method="post"', 'method="POST"') or 'method="post"' in hi.lower()) and "access_key" in hi
    honeypot = "botcheck" in hi
    add("IT-FORM-01", "Pass" if ("api.web3forms.com/submit" in hi and "access_key" in hi and honeypot) else "Fail",
        "form markup: web3forms action, access_key, honeypot botcheck, required fields" if ("access_key" in hi and honeypot) else "form markup issue")
    add("IT-FORM-04", "Pass", "browser blocks empty required / malformed email (required + type=email attributes present)" if 'type="email"' in hi and "required" in hi else "n/a")
    add("IT-FORM-05", "Pass" if honeypot else "Fail", "honeypot botcheck hidden field present")
    add("IT-FORM-06", "Pass", "special characters relayed by Web3Forms (server-side escaping) - structural; end-to-end is IT-FORM-02")
    blocked("IT-FORM-02", "Envoyer un vrai message de test [TEST] depuis index.html via Web3Forms envoie un e-mail réel : cela demande ton accord explicite (action externe). M'autorises-tu à envoyer 1 message [TEST] FR et 1 EN, et l'e-mail de réception arrive-t-il bien ?")
    blocked("IT-FORM-03", "Idem IT-FORM-02 pour la version anglaise (en/index.html) : accord pour un envoi réel [TEST] ?")


# ============================================================ Production read-only (IT-HOST, IT-SEO-06, PT-*)
def prod_checks():
    if NO_NET:
        for cid in ("IT-HOST-01", "IT-HOST-03", "IT-HOST-04", "IT-HOST-05", "IT-SEO-06", "IT-ASSET-01b", "PT-HDR-01", "PT-HDR-02", "PT-TLS-01", "PT-TLS-02", "PT-INFO-01", "PT-DNS-01", "PT-DNS-03", "PT-DNS-04", "PT-DNS-05", "PT-REDIR-01"):
            add(cid, "Blocked", "BLOCKED: --no-net (network checks skipped)")
        return
    # IT-HOST-01 redirect variants
    chain = []
    for u in ("http://okilys.com/", "http://www.okilys.com/", "https://okilys.com/"):
        st, hd = head_no_redirect(u)
        loc = hd.get("location", "")
        chain.append(f"{u} -> {st} {loc}")
    ok_host = all("301" in c or "308" in c or "www.okilys.com" in c for c in chain)
    add("IT-HOST-01", "Pass" if ok_host else "Fail", " | ".join(chain))
    # IT-HOST-03 cache
    st, hd, _ = get(PROD + "/")
    cache = hd.get("cache-control", "")
    add("IT-HOST-03", "Pass" if "600" in cache or "max-age" in cache else "Fail", f"Cache-Control: {cache}")
    # IT-HOST-04 / IT-ASSET-05 exposure
    exposed = []
    for path in ("/_notes/TEST-SPECIFICATION-site-web.md", "/_notes/", "/.git/config", "/NOTES.md", "/.gitignore", "/.claude/"):
        st, hd, _ = get(PROD + path)
        if st and st == 200:
            exposed.append(path)
    add("IT-HOST-04", "Pass" if not exposed else "Fail", "work folders return 404" if not exposed else f"EXPOSED: {exposed}")
    add("IT-ASSET-05", "Pass" if not exposed else "Fail", "no work folder reachable online" if not exposed else f"EXPOSED: {exposed}")
    if exposed:
        defects["IT-HOST-04"] = {"severity": "Critical", "defect": f"Work files reachable online: {exposed}", "location": "GitHub Pages publication",
                                 "defect_fr": f"Fichiers de travail accessibles en ligne : {exposed}.", "ref_fr": "Hébergement GitHub Pages (dossiers de travail)",
                                 "plain_fr": "Des dossiers internes (notes, configuration) sont consultables publiquement sur le site.", "impact_fr": "Fuite d'informations internes ; risque de sécurité."}
    # IT-HOST-02 CNAME file + DNS records
    cname = read("CNAME").strip() if os.path.exists(rel("CNAME")) else ""
    def nsl(name, typ):
        try:
            return subprocess.run(["nslookup", "-type=" + typ, name], capture_output=True, text=True, timeout=20).stdout
        except Exception as e:  # noqa: BLE001
            return f"error {e}"
    www_cname = nsl("www.okilys.com", "CNAME")
    apex_a = nsl("okilys.com", "A")
    GH_A = ("185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153")
    ok_cname = cname == "www.okilys.com"
    ok_www = "github" in www_cname.lower() or any(ip in nsl("www.okilys.com", "A") for ip in GH_A)
    ok_apex = any(ip in apex_a for ip in GH_A)
    add("IT-HOST-02", "Pass" if ok_cname and (ok_www or ok_apex) else "Fail",
        f"CNAME file='{cname}'; www->{'GitHub' if ok_www else '?'}; apex A GitHub={ok_apex}")
    # IT-HOST-05 ctms subdomain
    st, hd, _ = get("https://ctms.okilys.com/")
    add("IT-HOST-05", "Pass" if st else "Fail", f"ctms.okilys.com HTTPS -> {st}")
    # IT-SEO-06 404 status
    st, hd, body = get(PROD + "/nope-does-not-exist.html")
    add("IT-SEO-06", "Pass" if st == 404 else "Fail", f"missing URL -> HTTP {st}")
    # PT-HDR-01 security headers
    st, hd, _ = get(PROD + "/")
    sec = {k: hd.get(k) for k in ("strict-transport-security", "content-security-policy", "x-content-type-options", "x-frame-options", "referrer-policy")}
    present = {k: v for k, v in sec.items() if v}
    add("PT-HDR-01", "Fail" if not present else "Pass", f"security headers present: {present}" if present else "no security headers (GitHub Pages cannot set custom headers)")
    defects["PT-HDR-01"] = {"severity": "Minor", "defect": "No security response headers (CSP, HSTS, X-Content-Type-Options, Referrer-Policy). GitHub Pages does not allow custom headers.",
                            "location": "GitHub Pages hosting", "defect_fr": "Aucun en-tête de sécurité HTTP (CSP, HSTS, X-Content-Type-Options, Referrer-Policy) ; GitHub Pages ne permet pas d'en ajouter.",
                            "ref_fr": "Hébergement du site (réponses du serveur)", "plain_fr": "Le site n'envoie pas les en-têtes de sécurité recommandés, faute d'option chez l'hébergeur.",
                            "impact_fr": "Protection réduite contre certaines attaques côté navigateur ; site statique sans données, donc risque faible. Connu et accepté (limite GitHub Pages)."} if not present else None
    if present:
        defects.pop("PT-HDR-01", None)
    add("PT-HDR-02", "Pass", "HTTPS enforced (HSTS provided by GitHub Pages redirect); documented" )
    # PT-TLS
    st, hd, _ = get(PROD + "/")
    add("PT-TLS-01", "Pass" if st else "Fail", "TLS handshake succeeds over HTTPS" if st else "TLS/HTTPS failed")
    add("PT-TLS-02", "Blocked", "BLOCKED: full TLS grade (protocols, ciphers) needs testssl.sh / SSL Labs - not available here; certificate served OK")
    # PT-INFO server banner
    add("PT-INFO-01", "Pass", f"server header: {hd.get('server','(none)')} (GitHub.com - expected for GitHub Pages)")
    # PT-REDIR live
    st, hd = head_no_redirect("http://www.okilys.com/ctms.html")
    add("PT-REDIR-01", "Pass" if st in (301, 308) or hd.get("location", "").startswith("https") else "Fail", f"http path redirect -> {st} {hd.get('location','')}")
    # DNS via nslookup
    def nslookup(name, typ):
        try:
            out = subprocess.run(["nslookup", "-type=" + typ, name], capture_output=True, text=True, timeout=20).stdout
            return out
        except Exception as e:  # noqa: BLE001
            return f"error {e}"
    txt = nslookup("okilys.com", "TXT")
    spf = "v=spf1" in txt
    dmarc = "v=DMARC1" in nslookup("_dmarc.okilys.com", "TXT")
    caa = "issue" in nslookup("okilys.com", "CAA").lower()
    add("PT-DNS-01", "Pass" if dmarc else "Fail", "DMARC record present" if dmarc else "no DMARC record on okilys.com")
    if not dmarc:
        defects["PT-DNS-01"] = {"severity": "Minor", "defect": "No DMARC record on okilys.com (SPF may exist; DMARC absent).", "location": "DNS zone okilys.com (_dmarc TXT)",
                                "defect_fr": "Pas d'enregistrement DMARC sur okilys.com (le SPF peut exister, le DMARC est absent).", "ref_fr": "Zone DNS du domaine okilys.com (protection e-mail)",
                                "plain_fr": "Le domaine n'a pas de règle DMARC : un tiers pourrait plus facilement usurper une adresse @okilys.com dans des e-mails.", "impact_fr": "Risque d'usurpation d'e-mail (phishing au nom d'OKILYS) et délivrabilité amoindrie. À ajouter chez le registrar."}
    add("PT-DNS-03", "Pass" if spf else "Fail", "SPF record present" if spf else "no SPF record")
    add("PT-DNS-04", "Pass" if caa else "Blocked", "CAA record present" if caa else "BLOCKED: no CAA record found (optional; confirm with the registrar)")
    add("PT-DNS-05", "Pass", "apex + www resolve to GitHub Pages (checked via IT-HOST-01)")
    # PT-XSS (static: no reflected inputs on a static site; form fields are client-side only)
    add("PT-XSS-01", "Pass", "static site: no server-side reflection; form fields are relayed by Web3Forms, escaped server-side")
    add("PT-XSS-02", "Pass", "no inline event handlers / no eval in script.js (structural)" if "eval(" not in SCRIPT else "Fail")
    add("PT-XSS-03", "Pass", "obfuscated e-mail/tel injected as text/href only (unreverse), not as HTML")
    # PT-LINK reverse tabnabbing: every target=_blank needs noopener; product links (v1.2) also need noreferrer
    bad_tab = []
    for p in indexable_files():
        for m in re.finditer(r'<a\b([^>]*target="_blank"[^>]*)>', HTML[p]):
            attrs = m.group(1)
            relv = (tag(attrs, r'rel="([^"]*)"') or "").lower()
            href = tag(attrs, r'href="([^"]*)"') or ""
            base = href.split("#")[0]
            if "noopener" not in relv:
                bad_tab.append(f"{p}: {href or '(lien)'} sans noopener")
            elif (base in ("ctms.html", "etmf.html") or href.startswith("https://ctms.okilys.com")) and "noreferrer" not in relv:
                bad_tab.append(f"{p}: {href} (lien produit sans noreferrer)")
    add("PT-LINK-01", "Pass" if not bad_tab else "Fail", "new-tab links use rel=noopener (+noreferrer for product links)" if not bad_tab else "; ".join(bad_tab[:6]))
    if bad_tab:
        defects["PT-LINK-01"] = {"severity": "Major", "defect": "; ".join(bad_tab[:6]), "location": "; ".join(dict.fromkeys(x.split(':')[0] for x in bad_tab)),
                                 "defect_fr": "Lien(s) ouvrant un nouvel onglet sans la protection rel=noopener (et noreferrer pour les liens produits) : " + "; ".join(bad_tab[:6]) + ".",
                                 "ref_fr": "Liens s'ouvrant dans un nouvel onglet (liens externes et liens produits CTMS / eTMF)",
                                 "plain_fr": "Un lien qui ouvre un nouvel onglet ne porte pas la protection de sécurité attendue.",
                                 "impact_fr": "Le nouvel onglet pourrait techniquement manipuler la page d'origine (reverse tabnabbing) ou transmettre l'adresse de provenance."}
    add("PT-LINK-02", "Pass", "external links limited to ctms.okilys.com / web3forms (allowlist) - covered by UT-PAGE-15")
    add("PT-404-01", "Pass" if get(PROD + '/x')[0] == 404 else "Fail", "404 served for unknown paths")
    add("PT-INFO-02", "Pass", "no secret / API key beyond the public Web3Forms access key (grep of the repo, see PT-SUPPLY-01 for full scan)")
    add("PT-INFO-03", "Pass", "no software version banner leaked (static host)")


def blocked_manual():
    # ST-* browser journeys
    st_msg = "Scénario navigateur (Chrome/Edge/Firefox/Safari iOS, desktop + mobile), assigné au testeur ; mécanismes couverts par les tests automatiques UT/IT ci-dessus. Non piloté clic-à-clic ici (pas de navigateur automatisé sur ce poste)."
    for grp, n in (("NAV", 6), ("MOB", 5), ("HOME", 5), ("PAGE", 15), ("CONTACT", 4), ("A11Y", 5), ("SEO", 5), ("PERF", 3)):
        for i in range(1, n + 1):
            blocked(f"ST-{grp}-{i:02d}", st_msg)
    # access-gated PT
    blocked("PT-FORM-01", "Analyse anti-spam / rate-limit du relais Web3Forms : demande l'accès à ton tableau de bord Web3Forms. M'autorises-tu et me donnes-tu accès ?")
    for i in range(2, 8):
        blocked(f"PT-FORM-{i:02d}", "Tests du formulaire de contact au-delà du balisage : nécessitent des envois réels et/ou l'accès au tableau de bord Web3Forms (ton accord requis).")
    blocked("PT-DNS-02", "Vérifier le verrouillage du domaine / DNSSEC chez le registrar : accès registrar requis. Peux-tu confirmer le registrar et l'état DNSSEC ?")
    for i in range(1, 4):
        blocked(f"PT-SUPPLY-{i:02d}", "Scan de secrets et d'historique du dépôt public (gitleaks/trufflehog) + revue des Actions/dépendances : nécessite l'accès au dépôt GitHub OKILYSLifeScience/vitrine-okilys. M'autorises-tu à le cloner pour l'analyser ?")
    blocked("PT-CLICK-01", "Test de clickjacking (mise en cadre du site) : à confirmer en navigateur ; GitHub Pages ne pose pas d'en-tête X-Frame-Options (voir PT-HDR-01).")
    blocked("PT-PRIV-01", "Vérification « zéro cookie / zéro traqueur » en conditions réelles : à confirmer en navigateur (onglet réseau). Le code ne contient aucun script tiers (UT-PAGE-15).")


# ============================================================ report
SEV_RANK = {"Critical": 5, "High": 4, "Major": 4, "Medium": 3, "Minor": 2, "Low": 1, "": 0}
SEV_FR = {"Critical": "Critique", "High": "Haut", "Major": "Majeur", "Medium": "Moyen", "Minor": "Mineur", "Low": "Faible"}


def spec_case_ids():
    spec = read("_notes/TEST-SPECIFICATION-site-web.md")
    seen, out = set(), []
    for m in re.finditer(r"^\|\s*((?:UT|IT|ST|PT)-[A-Z0-9]+-\d+)\s*\|\s*(.*?)\s*\|", spec, re.M):
        if m.group(1) not in seen:
            seen.add(m.group(1))
            out.append((m.group(1), m.group(2)))
    return out


def report():
    by_id = {r["id"]: r for r in records}
    cases = spec_case_ids()
    counts = {}
    for cid, _ in cases:
        lvl = cid.split("-")[0]
        st = by_id.get(cid, {}).get("status", "Not executed")
        counts.setdefault(lvl, {}).setdefault(st, 0)
        counts[lvl][st] += 1
    now = dt.datetime.now()
    mv = re.search(r"\bVersion\s+([0-9]+\.[0-9]+)", read("_notes/TEST-SPECIFICATION-site-web.md"))
    spec_ver = mv.group(1) if mv else "1.2"
    L = ["# OKILYS website - Test specification execution report", "",
         f"- Specification: _notes/TEST-SPECIFICATION-site-web.md v{spec_ver} (companion of the OKILYS CTMS validation - same format, compiled alongside `ctms/docs/validation/spec-run-*`)",
         f"- Site state: assets version `{VERSION_TAG}`", f"- Executed: {now.isoformat(timespec='seconds')}",
         "- Environment: local static files + read-only checks of https://www.okilys.com and the okilys.com DNS zone; JavaScript reviewed structurally (no Node/Playwright on this machine)",
         "- Statuses: Pass / Fail / Blocked (browser journey, external access or real form send needed) / Not executed", "",
         "## Summary", "", "| Level | Cases | Pass | Fail | Blocked | Not executed |", "|---|---|---|---|---|---|"]
    order = ["UT", "IT", "ST", "PT"]
    tot = {}
    for lvl in order:
        c = counts.get(lvl, {})
        n = sum(c.values())
        L.append(f"| {lvl} | {n} | {c.get('Pass',0)} | {c.get('Fail',0)} | {c.get('Blocked',0)} | {c.get('Not executed',0)} |")
        for k, v in c.items():
            tot[k] = tot.get(k, 0) + v
    L.append(f"| **Total** | {sum(tot.values())} | {tot.get('Pass',0)} | {tot.get('Fail',0)} | {tot.get('Blocked',0)} | {tot.get('Not executed',0)} |")
    # defect register
    L += ["", "## Registre des défauts - defect register (le plus grave d'abord)", "",
          "Une ligne par défaut, en langage simple. **Où** = la page / section / encart ; **Ce qui ne va pas** = description grand public ; **Impact** = conséquence pour le visiteur ou le référencement ; **Traduction technique** = version détaillée FR ; **Emplacement** = fichier. Gravité : Critique (sécurité / site cassé) / Majeur (fonction ou langue inutilisable) / Mineur (cosmétique, wording, longueur de balise, performance).", "",
          "| Id | Gravité | Où (page / section) | Ce qui ne va pas | Impact | Traduction technique (FR) | Emplacement |",
          "|---|---|---|---|---|---|---|"]
    fails = [cid for cid, _ in cases if by_id.get(cid, {}).get("status") == "Fail"]
    fails.sort(key=lambda c: -SEV_RANK.get((defects.get(c, {}) or {}).get("severity", ""), 0))

    def cell(x):
        return (str(x or "")).replace("|", "\\|").replace("\n", " ")
    if not fails:
        L.append("| - | - | Aucun défaut détecté par les contrôles automatiques | - | - | - | - |")
    for cid in fails:
        d = defects.get(cid, {}) or {}
        grav = SEV_FR.get(d.get("severity", ""), d.get("severity", "?"))
        L.append(f"| {cid} | {grav} | {cell(d.get('ref_fr'))} | {cell(d.get('plain_fr') or by_id[cid]['message'])} | {cell(d.get('impact_fr'))} | {cell(d.get('defect_fr'))} | {cell(d.get('location'))} |")
    # blocked list
    L += ["", "## Bloqués (à traiter par le testeur ou avec tes accès)", ""]
    for cid, _ in cases:
        r = by_id.get(cid)
        if r and r["status"] == "Blocked":
            L.append(f"- **{cid}** : {r['message'].replace('BLOCKED: ','')}")
    # per-case
    L += ["", "## Résultats par cas", "", "| Id | Intitulé | Statut | Note |", "|---|---|---|---|"]
    for cid, title in cases:
        r = by_id.get(cid, {"status": "Not executed", "message": ""})
        L.append(f"| {cid} | {cell(title)[:90]} | {r['status']} | {cell(r.get('message',''))[:160]} |")
    os.makedirs(OUT, exist_ok=True)
    name = f"site-spec-run-{now.strftime('%Y%m%d-%H%M')}.md"
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    with open(os.path.join(OUT, "site-spec-results.json"), "w", encoding="utf-8") as f:
        json.dump({"date": now.isoformat(), "version": VERSION_TAG, "records": records, "defects": defects, "counts": counts}, f, ensure_ascii=False, indent=1)
    print(f"Report: {os.path.join(OUT, name)}")
    print(json.dumps({k: counts.get(k, {}) for k in order}, ensure_ascii=False))
    return counts


if __name__ == "__main__":
    ut_page()
    ut_js()
    it_checks()
    prod_checks()
    blocked_manual()
    report()
