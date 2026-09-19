# -*- coding: utf-8 -*-
"""Build ONE consolidated results workbook for the OKILYS website, from the last audit run.

    py _notes/tests/build_site_full_report.py

Output: _notes/validation/resultats-tests-site-web-<version>.xlsx with four sheets:
    Synthese / Defauts (a decider) / Cas non reussis / Tous les cas - same layout as the CTMS consolidated workbook.
"""
import glob
import json
import os
import re

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VAL = os.path.join(ROOT, "_notes", "validation")
NAVY, TEAL, YELLOW = "1A2333", "21778A", "FFF2CC"
FILL = {"Pass": "E2EFDA", "Fail": "F8CBAD", "Blocked": "FFF2CC", "Not executed": "D9D9D9"}
STATUT_FR = {"Pass": "Réussite", "Fail": "Échec (défaut)", "Blocked": "Bloqué", "Not executed": "Non exécuté"}
AREA_FR = {"UT": "Test unitaire", "IT": "Test d'intégration", "ST": "Test système (navigateur)", "PT": "Test d'intrusion"}
SEV_RANK = {"Critical": 5, "High": 4, "Major": 4, "Medium": 3, "Minor": 2, "Low": 1, "": 0}
SEV_FR = {"Critical": "Critique", "High": "Haut", "Major": "Majeur", "Medium": "Moyen", "Minor": "Mineur", "Low": "Faible"}
ACTIONS = '"Corriger,Corriger plus tard,Ne pas corriger,A decider"'


def spec_cases():
    spec = open(os.path.join(ROOT, "_notes", "TEST-SPECIFICATION-site-web.md"), encoding="utf-8").read()
    seen, out = set(), []
    for m in re.finditer(r"^\|\s*((?:UT|IT|ST|PT)-[A-Z0-9]+-\d+)\s*\|\s*(.*?)\s*\|", spec, re.M):
        if m.group(1) not in seen:
            seen.add(m.group(1))
            out.append((m.group(1), m.group(2)))
    return out


def who(cid, status, note):
    n = (note or "").lower()
    if status == "Fail":
        return "Défaut - voir l'onglet Défauts (à corriger ou non)"
    if any(w in n for w in ("web3forms", "registrar", "dnssec", "dépôt", "depot", "github", "accès", "acces", "accord", "autorises", "envoi réel", "envoi reel")):
        return "Toi (accès ou accord requis)"
    if cid.startswith("ST"):
        return "Testeur (navigateur : Chrome / Edge / Firefox / Safari iOS)"
    return "Testeur / navigateur"


# Catalogue FR des cas non joués (bloqués) du site : les DEUX colonnes de texte doivent être en français
# (explication grand public + traduction technique), jamais d'anglais brut ni de traduction vide.
BLOCKED_FR = {
    "st_browser": (
        "Test à faire à la main dans un navigateur (Chrome, Edge, Firefox, Safari iOS ; ordinateur et mobile) : c'est un "
        "parcours visuel de bout en bout. Il n'est pas rejoué automatiquement ici (le contrôle automatique lit le code des "
        "pages, pas leur rendu à l'écran). À réaliser par le testeur. Le détail du parcours est en colonne « Où ».",
        "Test système (ST) — scénario navigateur multi-appareils. Nécessite un vrai navigateur ; hors du périmètre du "
        "contrôle automatique du code source.",
        "Aucun défaut détecté : parcours à jouer manuellement pour confirmation."),
    "web3forms": (
        "Envoi réel du formulaire de contact via le relais Web3Forms : nécessite ton accord (un vrai message part) et/ou "
        "l'accès au compte Web3Forms. À faire ensemble, pas en automatique.",
        "Envoi/relais Web3Forms de bout en bout (anti-spam, limitation d'envois) : demande l'accès au service et l'accord "
        "pour un envoi réel.",
        "Aucun défaut détecté : à vérifier avec un envoi de test contrôlé."),
    "dns": (
        "Réglages du nom de domaine à contrôler chez le bureau d'enregistrement (registrar) : verrouillage du domaine, "
        "signature DNSSEC, enregistrement CAA. Nécessite l'accès au compte du domaine.",
        "DNS/registrar : verrou de transfert, DNSSEC, enregistrement CAA (optionnel). Nécessite l'accès au registrar.",
        "Aucun défaut détecté : à confirmer côté registrar."),
    "tls": (
        "Note complète du chiffrement HTTPS (versions, algorithmes) : se mesure avec un outil externe (SSL Labs) sur le "
        "domaine en ligne, pas dans ce contrôle automatique.",
        "Grade TLS complet (protocoles, ciphers) : nécessite testssl.sh / SSL Labs sur le domaine public.",
        "Aucun défaut détecté : à mesurer sur le domaine en ligne."),
    "supply": (
        "Recherche de secrets et d'historique sensible dans le dépôt public du site : nécessite un outil dédié "
        "(gitleaks/trufflehog) et l'accès au dépôt.",
        "Scan de secrets / historique du dépôt public (gitleaks/trufflehog) et revue de la chaîne d'approvisionnement. "
        "Nécessite l'accès au dépôt.",
        "Aucun défaut détecté : audit à lancer sur le dépôt."),
    "privacy": (
        "Vérification « zéro cookie / zéro traqueur » en conditions réelles : à confirmer dans un navigateur en naviguant "
        "sur le site en ligne.",
        "Absence de cookies / traqueurs en conditions réelles : à confirmer via les outils du navigateur sur le site "
        "déployé.",
        "Aucun défaut détecté : à confirmer en navigation réelle."),
    "clickjacking": (
        "Test de « mise en cadre » du site (clickjacking) : à confirmer dans un navigateur ; GitHub Pages ne permet pas "
        "d'ajouter l'en-tête de protection habituel.",
        "Clickjacking (framing) : à confirmer en navigateur ; en-têtes X-Frame-Options/CSP non modifiables sur GitHub "
        "Pages.",
        "Aucun défaut détecté : à confirmer en navigateur."),
    "publication": (
        "Contrôle de ce qui est réellement publié en ligne (fichiers ignorés, exposition) : se vérifie sur le site "
        "déployé, pas seulement dans les sources.",
        "Exposition/publication (.gitignore, fichiers servis) : à vérifier sur l'hôte en ligne.",
        "Aucun défaut détecté : à vérifier sur le site déployé."),
    "jsruntime": (
        "Comportements JavaScript complets (tactile, minuteurs, défilement) : se vérifient à l'exécution dans un "
        "navigateur, pas par lecture du code.",
        "Comportements JS à l'exécution (touch, timers, scrollspy) : vérifiables uniquement en navigateur.",
        "Aucun défaut détecté : à confirmer en navigateur."),
    "generic": (
        "Ce test n'a pas pu être joué automatiquement : il demande une action manuelle ou un accès externe. À exécuter "
        "par le testeur.",
        "Cas non automatisable dans le contrôle actuel (action manuelle ou accès externe requis).",
        "Aucun défaut détecté : reste à exécuter."),
}
_OU_FR = [
    ("End-to-end browser business scenario", "Scénario métier de bout en bout dans le navigateur"),
    ("assigned to the Okilys tester", "assigné au testeur OKILYS"), ("(spec ", "(spéc. "),
]


def classify_blocked(cid, note):
    n = (note or "").lower()
    if "web3forms" in n or (cid.startswith("IT-FORM") and "message" in n) or cid.startswith("PT-FORM"):
        return "web3forms"
    if cid.startswith("PT-DNS") or "dnssec" in n or "registrar" in n or "caa" in n:
        return "dns"
    if cid.startswith("PT-TLS") or "tls" in n or "ssl labs" in n or "testssl" in n:
        return "tls"
    if cid.startswith("PT-SUPPLY") or "gitleaks" in n or "trufflehog" in n or "secret" in n:
        return "supply"
    if cid.startswith("PT-PRIV") or "cookie" in n or "traqueur" in n or "tracker" in n:
        return "privacy"
    if cid.startswith("PT-CLICK") or "clickjack" in n or "framing" in n or "cadre" in n:
        return "clickjacking"
    if cid.startswith("IT-ASSET") or "publication" in n or "gitignore" in n:
        return "publication"
    if cid.startswith("UT-JS") or "runtime" in n:
        return "jsruntime"
    if cid.startswith("ST"):
        return "st_browser"
    return "generic"


def ou_fr(title):
    t = title or ""
    for en, fr in _OU_FR:
        t = t.replace(en, fr)
    return t


def _hdr(ws, heads, widths, row=1):
    ws.append(heads)
    for c in ws[row]:
        c.fill, c.font = PatternFill("solid", fgColor=TEAL), Font(bold=True, color="FFFFFF")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for col, w in zip("ABCDEFGHIJ", widths):
        ws.column_dimensions[col].width = w


def prior_choices(current_name):
    """Report la revue de Lydie ('Action souhaitee' + 'Vos notes') de TOUS les classeurs site (y compris le
    fichier de meme nom qui va etre reecrit : on le lit avant de l'ecraser), pour ne jamais perdre sa revue."""
    out = {}
    for f in sorted(glob.glob(os.path.join(VAL, "resultats-tests-site-web-*.xlsx"))):
        try:
            ws = __import__("openpyxl").load_workbook(f).worksheets[0]
        except Exception:
            continue
        heads = [c.value for c in ws[4]] if ws.max_row >= 4 else []
        if "Action souhaitee" not in heads:
            continue
        ia = heads.index("Action souhaitee")
        inn = heads.index("Vos notes") if "Vos notes" in heads else None
        for r in ws.iter_rows(min_row=5, values_only=True):
            if r and r[0] and len(r) > ia and (r[ia] or (inn is not None and len(r) > inn and r[inn])):
                out[r[0]] = (r[ia], r[inn] if inn is not None and len(r) > inn else None)
    return out


def build():
    data = json.load(open(os.path.join(VAL, "site-spec-results.json"), encoding="utf-8"))
    version = data.get("version", "site")
    date = data.get("date", "?")
    defects = data.get("defects", {})
    st = {r["id"]: r for r in data["records"]}
    # Manual overlay: browser / system tests executed by hand (the automated audit cannot drive a browser, so it marks
    # them Blocked). Recorded as Pass with evidence in site-manual-results.json so the compiled workbook reflects that
    # they were actually run. The contact-form real-send tests are deliberately NOT in the overlay (they await Lydie's go-ahead).
    _mp = os.path.join(VAL, "site-manual-results.json")
    if os.path.exists(_mp):
        for cid, rec in (json.load(open(_mp, encoding="utf-8")).get("results", {}) or {}).items():
            st[cid] = {"id": cid, "status": rec.get("status", "Pass"), "message": rec.get("message", "")}
            if rec.get("status") == "Fail" and rec.get("defect"):  # a defect surfaced by a manual test carries its own metadata
                defects[cid] = rec["defect"]
    cases = spec_cases()  # (id, title) in spec order
    counts = {}
    per = []
    for cid, title in cases:
        status = st.get(cid, {}).get("status", "Not executed")
        note = st.get(cid, {}).get("message", "")
        per.append({"id": cid, "title": title, "status": status, "note": note})
        lvl = cid.split("-")[0]
        counts.setdefault(lvl, {}).setdefault(status, 0)
        counts[lvl][status] += 1
    def who(cid, status, note):
        n = (note or "").lower()
        if any(w in n for w in ("web3forms", "registrar", "dnssec", "dépôt", "depot", "github", "accès", "acces", "accord", "autorises", "envoi réel", "envoi reel")):
            return "Toi (accès ou accord requis)"
        if cid.startswith("ST"):
            return "Testeur (navigateur : Chrome / Edge / Firefox / Safari iOS)"
        return "Testeur / navigateur"

    review = [p for p in per if p["status"] in ("Fail", "Blocked", "Not executed")]
    order = {"Fail": 0, "Blocked": 1, "Not executed": 2}
    review.sort(key=lambda p: (order.get(p["status"], 3), -SEV_RANK.get((defects.get(p["id"], {}) or {}).get("severity", ""), 0), p["id"]))
    n_fail = sum(1 for p in review if p["status"] == "Fail")
    n_block = sum(1 for p in review if p["status"] == "Blocked")
    prior = prior_choices(f"resultats-tests-site-web-{version}.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.title = "A revoir"
    ws["A1"] = f"OKILYS site web (www.okilys.com) - Cas a revoir (version {version}) - execute le {date}"
    ws["A1"].font = Font(bold=True, size=14, color=NAVY)
    ws["A2"] = (f"Un seul onglet, {n_fail} defauts (echecs) + {n_block} bloques + les points deja traites (trace conservee). "
                "Le classeur s'ouvre FILTRE sur l'ETAT REEL (colonne 'Gravite') : il montre ce qui attend encore quelque chose - "
                "les defauts ouverts et les cas encore bloques (y compris ceux qui attendent une action ou un accord de votre part, meme si vous avez deja ecrit 'Corriger') - "
                "et masque les points resolus ou deja executes. Une decision ecrite ne ferme pas un point tant qu'il n'est pas corrige. "
                "Pour revoir tout l'historique (points resolus / tests deja joues au navigateur), enlevez le filtre de la colonne 'Gravite'. "
                "Les defauts sont en haut, puis les cas bloques (Gravite='Bloque' : test non joue - la colonne 'Ce qui ne va pas' dit pourquoi), puis les points resolus. "
                "Remplissez 'Action souhaitee' (menu deroulant) ; cellules a remplir en jaune. Les cas en reussite ne sont pas listes.")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:J2")
    ws.row_dimensions[2].height = 72
    ws.append([])
    _hdr(ws, ["Id", "Gravite", "Domaine", "Ou (page / section)", "Ce qui ne va pas (langage simple)", "Impact", "Traduction technique (FR)", "Emplacement", "Action souhaitee", "Vos notes"],
         (13, 13, 22, 32, 52, 34, 44, 30, 22, 24), row=4)
    for p in review:
        d = defects.get(p["id"], {}) or {}
        if p["status"] == "Fail":
            grav = SEV_FR.get(d.get("severity", ""), d.get("severity") or "?")
            ou = d.get("ref_fr") or p["title"]
            quoi = d.get("plain_fr") or p["note"]
            impact = d.get("impact_fr") or ""
            trad = d.get("defect_fr") or ""
            empl = d.get("location") or ""
        else:  # Bloque / Non execute - tout en francais (deux colonnes), jamais d'anglais brut ni de traduction vide
            grav = STATUT_FR.get(p["status"], p["status"])
            ou = ou_fr(p["title"])
            plain_fr, tech_fr, impact_fr = BLOCKED_FR[classify_blocked(p["id"], p["note"])]
            quoi = plain_fr
            impact = impact_fr
            trad = tech_fr
            empl = who(p["id"], p["status"], p["note"])
        act, notes = prior.get(p["id"], (None, None))
        ws.append([p["id"], grav, AREA_FR.get(p["id"][:2], ""), ou, quoi[:500], impact, trad[:400], empl, act, notes])
        rr = ws.max_row
        for c in ws[rr]:
            c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=rr, column=9).fill = PatternFill("solid", fgColor=YELLOW)
        ws.cell(row=rr, column=10).fill = PatternFill("solid", fgColor=YELLOW)
        if p["status"] != "Fail":
            ws.cell(row=rr, column=2).fill = PatternFill("solid", fgColor=FILL.get(p["status"], "FFFFFF"))
        # Default view = what STILL needs Lydie's attention (real state), NOT "has a decision been written".
        # A written "Corriger" does not close a point: an open defect / blocked case that still waits for her (e.g. the
        # DMARC record to create, the contact-form sends to authorise) stays visible; only a declined point is hidden here.
        # Genuinely settled points (resolved / executed) leave the review list above (their status is Pass) or fall in the
        # resolved-trace section below (hidden). This fixes the workbook opening visually empty when every row was decided.
        if (act or "").strip().lower().startswith("ne pas"):  # "Ne pas corriger" = declined -> hidden by default
            ws.row_dimensions[rr].hidden = True
    # Trace des defauts deja traites qui ne ressortent plus (corriges ou plus detectes) : on garde la ligne
    current_ids = {p["id"] for p in review}
    for cid in sorted(k for k in prior if k not in current_ids):
        act, notes = prior[cid]
        ws.append([cid, "Résolu", AREA_FR.get(cid[:2], ""), "(déjà traité lors d'un test précédent)",
                   "Ce point avait été signalé et vous aviez indiqué une action ; il n'apparaît plus dans les résultats (corrigé ou plus détecté). Ligne conservée pour la trace.",
                   "", "", "", act, notes])
        rr = ws.max_row
        for c in ws[rr]:
            c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=rr, column=2).fill = PatternFill("solid", fgColor=FILL["Pass"])
        ws.cell(row=rr, column=9).fill = PatternFill("solid", fgColor=YELLOW)
        ws.cell(row=rr, column=10).fill = PatternFill("solid", fgColor=YELLOW)
        ws.row_dimensions[rr].hidden = True  # deja traite -> masque par defaut
    if ws.max_row >= 5:
        dv = DataValidation(type="list", formula1=ACTIONS, allow_blank=True)
        dv.add(f"I5:I{ws.max_row}")
        ws.add_data_validation(dv)
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:J{max(ws.max_row, 4)}"
    # Filtre par ETAT REEL (colonne "Gravite", col B = index 1), pas par presence d'une decision : on montre les defauts
    # ouverts (leur gravite) et les cas encore bloques ("Bloque"), on masque la trace des points resolus ("Resolu").
    # Ainsi le classeur ne s'ouvre jamais vide et ne cache jamais un point qui attend une action de Lydie (ex. le DMARC,
    # les envois de formulaire a autoriser), meme si elle a deja ecrit "Corriger". Enlever le filtre = tout l'historique.
    show_gravs = sorted({ws.cell(row=r, column=2).value for r in range(5, ws.max_row + 1)
                         if ws.cell(row=r, column=2).value and ws.cell(row=r, column=2).value != "Résolu"})
    if show_gravs:
        ws.auto_filter.add_filter_column(1, show_gravs, blank=False)
    path = os.path.join(VAL, f"resultats-tests-site-web-{version}.xlsx")
    wb.save(path)
    print(f"Workbook: {path} - 1 onglet, {len(review)} lignes ({n_fail} defauts, {n_block} bloques)")
    return path


if __name__ == "__main__":
    build()
