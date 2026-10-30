# -*- coding: utf-8 -*-
"""Actualites / Insights generator for www.okilys.com (static site, FR + EN).

Source of truth: one Markdown file per article in `_articles/` (bilingual, see README.md there).
Running this script regenerates, from ALL sources, in both languages:
  - one page per article:            actualites/<slug>.html   and   en/insights/<slug_en>.html
  - the news list with category filters, between the NEWS:LIST markers of
                                      actualites.html          and   en/insights.html
  - the home carousel (3 latest),     between the NEWS:CAROUSEL markers of index.html and en/index.html
  - the sitemap entries,              between the NEWS:ARTICLES markers of sitemap.xml
The page shell (suite bar, header, menu, footer) is taken live from actualites.html / en/insights.html,
so article pages always match the site. No JavaScript is added: the category filter is CSS-only.

    py _tools/publish_article.py            # regenerate everything
    py _tools/publish_article.py --check    # parse and validate the sources only (no file written)

Rules enforced here (from the site's CLAUDE.md and test specification): bilingual output in the same run,
title <= 70 chars with the brand, description 70-160 chars, no em dash in headings, founder written
`Lydie PARSUS`, brand written `OKILYS`, no e-mail address in page source, product links in a new tab.
"""
import datetime as dt
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_articles")
PROD = "https://www.okilys.com"
CHECK = "--check" in sys.argv

CATS = {
    "carnet": {"fr": "Carnet de la fondatrice", "en": "Founder's notebook"},
    "metier": {"fr": "Métier & réglementaire", "en": "Practice & regulatory"},
    "outils": {"fr": "Outils OKILYS", "en": "OKILYS tools"},
    "vie": {"fr": "Vie d'OKILYS", "en": "Life at OKILYS"},
}
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

T = {
    "fr": {"index": "actualites.html", "dir": "actualites", "home": "index.html", "lang": "fr", "locale": "fr_FR", "alt_locale": "en_GB",
           "inlang": "fr-FR", "home_name": "Accueil", "index_name": "Actualités", "author_line": "Lydie PARSUS, fondatrice d'OKILYS",
           "all": "Tout", "read": "Lire l'article →", "read_news": "Lire l'actualité", "back": "← Toutes les actualités",
           "linkedin": "Lire sur LinkedIn ↗", "filter_label": "Filtrer par catégorie", "author": "Lydie PARSUS",
           "site_root": PROD + "/"},
    "en": {"index": "en/insights.html", "dir": "en/insights", "home": "en/index.html", "lang": "en", "locale": "en_GB", "alt_locale": "fr_FR",
           "inlang": "en-GB", "home_name": "Home", "index_name": "Insights", "author_line": "Lydie PARSUS, founder of OKILYS",
           "all": "All", "read": "Read the article →", "read_news": "Read the news", "back": "← All insights",
           "linkedin": "Read on LinkedIn ↗", "filter_label": "Filter by category", "author": "Lydie PARSUS",
           "site_root": PROD + "/en/"},
}

# The three historical cards (summer 2026) are kept as they were written; they have no article page.
LEGACY = [
    {"sort": "2026-09-19", "cat": "outils", "new_tab": True,
     "fr": {"id": "lancement-ctms", "date": "À venir", "title": "OKILYS CTMS arrive",
            "text": "OKILYS prépare son premier outil, né d'une expertise terrain transversale : faisabilité, sélection et activation des centres, visites et rapports signés électroniquement, actions de suivi. Pensé pour les biotechs, promoteurs et CROs, il s'activera module par module — et vos données vous seront restituées à tout moment.",
            "slide": "OKILYS prépare son premier outil de pilotage des essais cliniques, en modules à la carte.",
            "cta": "ctms.html", "cta_label": "Découvrir OKILYS CTMS →"},
     "en": {"id": "ctms-launch", "date": "Coming soon", "title": "OKILYS CTMS is coming",
            "text": "OKILYS is preparing its first tool, born from cross-cutting field expertise: site feasibility, selection and activation, visits and electronically signed reports, follow-up actions. Designed for biotechs, sponsors and CROs, it will be switched on module by module — with your data handed back at any time.",
            "slide": "OKILYS is preparing its first clinical trial management tool, with modules on demand.",
            "cta": "ctms.html", "cta_label": "Discover OKILYS CTMS →"}},
    {"sort": "2026-09-18", "cat": "outils", "new_tab": True,
     "fr": {"id": "etmf-a-venir", "date": "À venir", "title": "OKILYS eTMF en préparation",
            "text": "Le deuxième produit de la suite est en développement : un Trial Master File structuré selon le TMF Reference Model, alimenté automatiquement par le CTMS et vérifié par vos équipes. L'ambition : un TMF qui se remplit pendant l'étude, pas après.",
            "slide": "Un Trial Master File qui se remplit pendant l'étude, connecté au CTMS.",
            "cta": "etmf.html", "cta_label": "Découvrir OKILYS eTMF →"},
     "en": {"id": "etmf-coming", "date": "Coming soon", "title": "OKILYS eTMF in preparation",
            "text": "The second product of the suite is under development: a Trial Master File structured per the TMF Reference Model, fed automatically by the CTMS and verified by your teams. The ambition: a TMF that fills itself during the study, not after.",
            "slide": "A Trial Master File that fills itself during the study, connected to the CTMS.",
            "cta": "etmf.html", "cta_label": "Discover OKILYS eTMF →"}},
    {"sort": "2026-07-01", "cat": "vie", "new_tab": False,
     "fr": {"id": "nouveau-site", "date": "Été 2026", "title": "Le nouveau site okilys.com est en ligne",
            "text": "Un site bilingue qui présente toute l'offre : les cinq catégories de produits de santé et leurs cadres réglementaires, les sept étapes d'une étude couvertes de la conception à la clôture, les réalisations — et les valeurs HOME qui guident chaque mission.",
            "slide": "Toute l'offre OKILYS — expertises, produits de santé, outils — dans un site bilingue.",
            "cta": "index.html", "cta_label": "Parcourir le site →"},
     "en": {"id": "new-website", "date": "Summer 2026", "title": "The new okilys.com is online",
            "text": "A bilingual website presenting the whole offer: the five categories of health products and their regulatory frameworks, the seven steps of a study covered from design to close-out, the highlights — and the HOME values guiding every assignment.",
            "slide": "The full OKILYS offer — expertise, health products, tools — on a bilingual website.",
            "cta": "index.html", "cta_label": "Browse the website →"}},
]


# ------------------------------------------------------------------ helpers
def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def write(p, s):
    if CHECK:
        return
    full = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def esc(s):
    """Escape for HTML text and double-quoted attributes. Apostrophes are kept as such: the site's SEO audit
    measures the length of the title / description as written in the file, and &#x27; would inflate it."""
    return html.escape(s, quote=False).replace('"', "&quot;")


def inline(s):
    """Inline markdown: **bold**, escaped text. Links are not allowed in body text (kept simple and safe)."""
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s


def md_to_html(md):
    out, para, ul = [], [], []

    def flush_p():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    def flush_ul():
        if ul:
            out.append("<ul>" + "".join("<li>" + inline(x) + "</li>" for x in ul) + "</ul>")
            ul.clear()

    for line in md.splitlines():
        st = line.strip()
        if not st:
            flush_p(); flush_ul(); continue
        if st.startswith("## "):
            flush_p(); flush_ul()
            head = st[3:].strip()
            if "—" in head:
                raise SystemExit("em dash in heading (Agne font has no glyph): " + head)
            out.append("<h2>" + inline(head) + "</h2>")
        elif st.startswith("- "):
            flush_p(); ul.append(st[2:].strip())
        else:
            flush_ul(); para.append(st)
    flush_p(); flush_ul()
    return "\n".join(out)


def date_label(iso, lang):
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {MONTHS_FR[d.month-1]} {d.year}" if lang == "fr" else f"{d.day} {MONTHS_EN[d.month-1]} {d.year}"


def parse(path):
    raw = open(path, encoding="utf-8").read()
    head, _, rest = raw.partition("\n--- fr ---\n")
    fr, _, en = rest.partition("\n--- en ---\n")
    meta = {}
    for line in head.splitlines():
        if ":" in line and not line.startswith("#"):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    need = ["slug", "slug_en", "date", "category", "title_fr", "title_en", "description_fr", "description_en", "excerpt_fr", "excerpt_en"]
    missing = [k for k in need if not meta.get(k)]
    if missing:
        raise SystemExit(f"{os.path.basename(path)}: missing {missing}")
    if meta["category"] not in CATS:
        raise SystemExit(f"{os.path.basename(path)}: unknown category {meta['category']}")
    dt.date.fromisoformat(meta["date"])
    for lang in ("fr", "en"):
        t = meta[f"title_{lang}"] + " | OKILYS"
        if len(t) > 70:
            raise SystemExit(f"{os.path.basename(path)}: title_{lang} too long ({len(t)} > 70 with brand)")
        if "—" in meta[f"title_{lang}"]:
            raise SystemExit(f"{os.path.basename(path)}: em dash in title_{lang}")
        d = meta[f"description_{lang}"]
        if not 70 <= len(d) <= 160:
            raise SystemExit(f"{os.path.basename(path)}: description_{lang} length {len(d)} outside 70-160")
    for txt in (fr, en):
        if re.search(r"[A-Za-z0-9._%+-]+@okilys\.com", txt):
            raise SystemExit("e-mail address in article body: not allowed on the public site")
        if re.search(r"Lydie\s+Parsus", txt):
            raise SystemExit("write 'Lydie PARSUS' (surname in capitals)")
        if re.search(r"(?<![\w.@/])Okilys(?![\w.])", txt):
            raise SystemExit("write 'OKILYS' in capitals")
    meta["body_fr"], meta["body_en"] = fr.strip(), en.strip()
    meta["linkedin"] = meta.get("linkedin") or "https://www.linkedin.com/in/lydieparsus/"
    return meta


def relocate(shell):
    """Prefix every relative href/src of the shell with ../ (article pages live one folder deeper)."""
    def fix(m):
        attr, q, v = m.group(1), m.group(2), m.group(3)
        if v.startswith(("http", "#", "data:", "mailto:", "tel:", "/")) or not v:
            return m.group(0)
        return f'{attr}={q}../{v}{q}'
    return re.sub(r'\b(href|src)=(")([^"]*)(")', lambda m: fix(m) if m.group(2) == m.group(4) else m.group(0), shell)


def jsonld_article(a, lang):
    t = T[lang]
    url = f"{PROD}/{t['dir']}/{a['slug' if lang == 'fr' else 'slug_en']}.html"
    import json
    data = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": url + "#article", "url": url, "mainEntityOfPage": url,
         "headline": a[f"title_{lang}"], "description": a[f"description_{lang}"],
         "datePublished": a["date"], "dateModified": a["date"], "inLanguage": t["inlang"],
         "articleSection": CATS[a["category"]][lang],
         "author": {"@type": "Person", "name": "Lydie PARSUS", "url": PROD + "/a-propos.html#fondatrice"},
         "publisher": {"@id": PROD + "/#organization"},
         "image": PROD + "/assets/images/og-image.jpg",
         "isPartOf": {"@id": t["site_root"] + "#website"}},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": t["home_name"], "item": t["site_root"]},
            {"@type": "ListItem", "position": 2, "name": t["index_name"], "item": f"{PROD}/{t['index']}"},
            {"@type": "ListItem", "position": 3, "name": a[f"title_{lang}"]}]}]}
    return json.dumps(data, ensure_ascii=False, indent=2)


def article_page(a, lang):
    t = T[lang]
    other = "en" if lang == "fr" else "fr"
    slug = a["slug"] if lang == "fr" else a["slug_en"]
    slug_other = a["slug_en"] if lang == "fr" else a["slug"]
    url = f"{PROD}/{t['dir']}/{slug}.html"
    url_fr = f"{PROD}/actualites/{a['slug']}.html"
    url_en = f"{PROD}/en/insights/{a['slug_en']}.html"
    shell = read(t["index"])
    head, body = shell.split("</head>", 1)
    before_main, rest = body.split("<main>", 1)
    _, after_main = rest.split("</main>", 1)
    # ---- head
    title = esc(a[f"title_{lang}"]) + " | OKILYS"
    desc = esc(a[f"description_{lang}"])
    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head)
    head = re.sub(r'<link rel="alternate" hreflang="fr" href="[^"]*">', f'<link rel="alternate" hreflang="fr" href="{url_fr}">', head)
    head = re.sub(r'<link rel="alternate" hreflang="en" href="[^"]*">', f'<link rel="alternate" hreflang="en" href="{url_en}">', head)
    head = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', f'<link rel="alternate" hreflang="x-default" href="{url_fr}">', head)
    head = re.sub(r'<meta name="author" content="[^"]*">', '<meta name="author" content="Lydie PARSUS">', head)
    head = re.sub(r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="article">', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(a[f"title_{lang}"])}">', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', head)
    head = re.sub(r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{esc(a[f"title_{lang}"])}">', head)
    head = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{esc(a[f"title_{lang}"])}">', head)
    head = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{desc}">', head)
    head = re.sub(r'<meta property="og:image:height" content="630">',
                  f'<meta property="og:image:height" content="630">\n<meta property="article:published_time" content="{a["date"]}">\n<meta property="article:author" content="Lydie PARSUS">\n<meta property="article:section" content="{esc(CATS[a["category"]][lang])}">', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">\n' + jsonld_article(a, lang) + "\n</script>", head, flags=re.S)
    head = relocate(head)
    # ---- shell (menu, footer, script) with ../ paths; language switch -> the mirror article
    before_main = relocate(before_main)
    after_main = relocate(after_main)
    mirror_idx = "../" + T[other]["index"] if lang == "fr" else "../../actualites.html"
    mirror = f"../en/insights/{slug_other}.html" if lang == "fr" else f"../../actualites/{slug_other}.html"
    before_main = before_main.replace(f'href="{mirror_idx}"', f'href="{mirror}"')
    # ---- main
    cat = CATS[a["category"]][lang]
    body_html = md_to_html(a[f"body_{lang}"])
    main = f"""<main>

  <article class="post">
    <div class="container post__container">
      <p class="post__meta"><a class="news-badge" href="../{t['index'].split('/')[-1]}">{esc(cat)}</a><span class="post__sep">·</span><time datetime="{a['date']}">{date_label(a['date'], lang)}</time><span class="post__sep">·</span>{esc(t['author_line'])}</p>
      <h1 class="post__title">{esc(a[f'title_{lang}'])}</h1>
      <p class="post__lead">{inline(a[f'excerpt_{lang}'])}</p>
      <div class="post__body">
{body_html}
      </div>
      <p class="post__links"><a class="news-article__cta" href="{esc(a['linkedin'])}" target="_blank" rel="noopener noreferrer">{t['linkedin']}</a><span class="post__sep">·</span><a class="news-article__cta" href="../{t['index'].split('/')[-1]}">{t['back']}</a></p>
    </div>
  </article>

</main>"""
    return head + "</head>" + before_main + main + after_main


def card(item, lang, is_article):
    t = T[lang]
    if is_article:
        slug = item["slug"] if lang == "fr" else item["slug_en"]
        href = f"{t['dir'].split('/')[-1]}/{slug}.html"
        return f"""      <article class="news-article cat-{item['category']}" id="{esc(slug)}">
        <p class="news-article__meta"><span class="news-slide__date"><time datetime="{item['date']}">{date_label(item['date'], lang)}</time></span><span class="news-badge">{esc(CATS[item['category']][lang])}</span></p>
        <h2><a href="{href}">{esc(item[f'title_{lang}'])}</a></h2>
        <p>{inline(item[f'excerpt_{lang}'])}</p>
        <a class="news-article__cta" href="{href}">{t['read']}</a>
      </article>"""
    L = item[lang]
    nt = ' target="_blank" rel="noopener noreferrer"' if item["new_tab"] else ""
    return f"""      <article class="news-article cat-{item['cat']}" id="{L['id']}">
        <p class="news-article__meta"><span class="news-slide__date">{L['date']}</span><span class="news-badge">{esc(CATS[item['cat']][lang])}</span></p>
        <h2>{L['title']}</h2>
        <p>{L['text']}</p>
        <a class="news-article__cta" href="{L['cta']}"{nt}>{L['cta_label']}</a>
      </article>"""


def news_list(entries, lang):
    t = T[lang]
    chips = [f'      <input type="radio" name="news-cat" id="cat-all" class="news-filter__input" checked>']
    labels = [f'        <label for="cat-all" class="news-filter__chip">{t["all"]}</label>']
    for key, names in CATS.items():
        chips.append(f'      <input type="radio" name="news-cat" id="cat-{key}" class="news-filter__input">')
        labels.append(f'        <label for="cat-{key}" class="news-filter__chip">{esc(names[lang])}</label>')
    cards = "\n\n".join(card(e["item"], lang, e["article"]) for e in entries)
    return ("\n".join(chips) + f'\n      <div class="news-filter" role="group" aria-label="{t["filter_label"]}">\n' + "\n".join(labels)
            + '\n      </div>\n      <div class="news-items">\n' + cards + "\n      </div>")


def slide(entry, lang):
    t = T[lang]
    item = entry["item"]
    if entry["article"]:
        slug = item["slug"] if lang == "fr" else item["slug_en"]
        return f"""            <div class="news-slide">
              <p class="news-slide__date">{date_label(item['date'], lang)}</p>
              <h3>{esc(item[f'title_{lang}'])}</h3>
              <p>{inline(item[f'excerpt_{lang}'])}</p>
              <a href="{t['dir'].split('/')[-1]}/{slug}.html" class="btn btn--step">{t['read'].rstrip(' →')}</a>
            </div>"""
    L = item[lang]
    return f"""            <div class="news-slide">
              <p class="news-slide__date">{L['date']}</p>
              <h3>{L['title']}</h3>
              <p>{L['slide']}</p>
              <a href="{t['index'].split('/')[-1]}#{L['id']}" class="btn btn--step">{t['read_news']}</a>
            </div>"""


def replace_between(text, start, end, new, where):
    i, j = text.find(start), text.find(end)
    if i < 0 or j < 0 or j < i:
        raise SystemExit(f"markers {start} / {end} not found in {where}")
    return text[: i + len(start)] + "\n" + new + "\n" + text[j:]


def sitemap_entries(articles):
    today = dt.date.today().isoformat()
    out = []
    for a in articles:
        fr = f"{PROD}/actualites/{a['slug']}.html"
        en = f"{PROD}/en/insights/{a['slug_en']}.html"
        for loc in (fr, en):
            out.append(f"""  <url>
    <loc>{loc}</loc>
    <xhtml:link rel="alternate" hreflang="fr" href="{fr}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{fr}"/>
    <lastmod>{max(a['date'], '2026-01-01')}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.6</priority>
  </url>""")
    return "\n".join(out)


def main():
    files = sorted(f for f in os.listdir(SRC) if f.endswith(".md") and f[0].isdigit())  # README.md is not an article
    articles = [parse(os.path.join(SRC, f)) for f in files]
    slugs = [a["slug"] for a in articles] + [a["slug_en"] for a in articles]
    if len(set(slugs)) != len(slugs):
        raise SystemExit("duplicate slug")
    entries = [{"article": True, "item": a, "sort": a["date"]} for a in articles] + [{"article": False, "item": L, "sort": L["sort"]} for L in LEGACY]
    entries.sort(key=lambda e: e["sort"], reverse=True)
    print(f"{len(articles)} article(s), {len(LEGACY)} legacy card(s)" + (" [check only]" if CHECK else ""))
    for a in articles:
        write(f"actualites/{a['slug']}.html", article_page(a, "fr"))
        write(f"en/insights/{a['slug_en']}.html", article_page(a, "en"))
        print(f"  {a['date']}  {a['slug']}  /  {a['slug_en']}")
    for lang in ("fr", "en"):
        t = T[lang]
        idx = read(t["index"])
        idx = replace_between(idx, "<!-- NEWS:LIST:START -->", "<!-- NEWS:LIST:END -->", news_list(entries, lang), t["index"])
        write(t["index"], idx)
        home = read(t["home"])
        home = replace_between(home, "<!-- NEWS:CAROUSEL:START -->", "<!-- NEWS:CAROUSEL:END -->", "\n".join(slide(e, lang) for e in entries[:3]), t["home"])
        write(t["home"], home)
    sm = read("sitemap.xml")
    sm = replace_between(sm, "<!-- NEWS:ARTICLES:START -->", "<!-- NEWS:ARTICLES:END -->", sitemap_entries(articles), "sitemap.xml")
    write("sitemap.xml", sm)
    print("done" if not CHECK else "sources valid")


if __name__ == "__main__":
    main()
