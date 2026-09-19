<!-- Dossier _notes : versionne dans le depot mais exclu de la publication GitHub Pages (prefixe _). -->
# OKILYS website (www.okilys.com) - Test specification

Version 1.6 - 19 September 2026 - two decisions of Lydie PARSUS closed on 19/09: (a) **no phone number will be published on the site**, so every `tel:` / `data-tel` expectation is removed from ST-CONTACT-04, ST-MOB-04 and UT-JS-01 (the dormant helper stays in `js/script.js`); (b) **the Azeolys logo deliberately carries no link** - 13 of the 14 logos are clickable and that is the expected state, not a defect. Also recorded: the real `[TEST]` sends of 19/09 (3 authorised by Lydie in chat) closed IT-FORM-02/03, ST-CONTACT-01, PT-FORM-02, PT-INPUT-01 and PT-XSS-03 in Pass, and **confirmed PT-FORM-01 as a genuine failure**: the public Web3Forms key is accepted from an origin other than okilys.com, so the domain restriction is not enabled - correction is a Web3Forms dashboard setting, an action for Lydie. ST-CONTACT-02 (English send) stays blocked: the third send was spent on PT-FORM-01.

(Version 1.5 - 19 September 2026 - site state: stylesheet / script version `20260919a`, commit `157a3d6`. Two decisions and five corrections:
- **OKILYS CTMS is now announced as "à venir" / "coming soon" everywhere** (decision of Lydie PARSUS, 19/09), exactly like eTMF: in the suite bar it is a non-clickable `<span class="suite-bar__tool is-soon" title="ctms.okilys.com">` with the badge, and the badge is added in the menu drop-down, the home suite cards, the suite comparison and the `ctms.html` hero (FR + EN). **The single remaining link to the application is the "Accès client" on `ctms.html` / `en/ctms.html`** (new tab, `noopener noreferrer`); the duplicate on `suite.html` was removed. IT-NAV-02 rewritten accordingly; the harness now fails if any suite bar still links to the application, if either tool lacks its badge, or if the client access is missing or unsafe.
- **Register corrections** (Lydie's decisions, run of 17/09): UT-PAGE-02 `suite.html` title 72 -> 51 characters and aligned with the menu; UT-PAGE-03 descriptions brought back into 70-160 (`dispositif-medical`, `inm`, `preparation`); UT-PAGE-16 50 images given their intrinsic `width`/`height` across 10 pages; IT-NAV-03 footer aligned with the menu (the duplicate "Fondatrice" entry removed, shortest label kept - the `#fondatrice` anchor stays reachable from the About page, `highlights.html`, the 404 and the stubs); PT-HDR-01 addressed by **meta-tag compensating controls on all 51 pages** (`Content-Security-Policy` via `http-equiv` + `referrer=strict-origin-when-cross-origin`), GitHub Pages allowing no HTTP headers. Residual and documented: HSTS and `X-Frame-Options`/`frame-ancestors` cannot be set by meta (see PT-CLICK-01). **PT-DNS-01 (DMARC) remains open**: it needs a DNS record at the registrar, outside the repository.
- **Findings from the browser test run of 19/09** (fixed the same day): heading hierarchy on the home page (the news band title was a `<p class="eyebrow">` producing an h1 -> h3 skip; now an `<h2>` with the same class, visually identical); carousel dots had a 9x9 px hit area, below the WCAG 2.2 AA minimum of 24 px (SC 2.5.8) - now 25x25 px via `padding` + `background-clip: content-box`, the visible dot unchanged at 9 px.
- Verified in the browser after the CSP was added: styles, self-hosted fonts (11 loaded), JavaScript, key injection, JSON-LD parsing, 15 images and all 3 stylesheets load with an empty console - no CSP violation.)

(Version 1.4 - 17 September 2026 - site state: stylesheet / script version bumped to `20260917a`, commit `292f8cb`. Requirement added by Lydie PARSUS: **protect the contact form, the e-mail addresses and the phone number from robots (scrapers and spam bots)**. Measures on 17/09: (a) e-mail and phone already obfuscated - stored reversed in `data-email` / `data-tel`, rebuilt with `textContent` at render, never in clear in the raw HTML or JSON-LD; (b) the Web3Forms access key removed from the raw HTML (stored reversed in `data-key`, injected into the hidden field only at render) so a bot reading the source cannot reuse it; (c) two spam traps on submit - the hidden `botcheck` honeypot (already present) plus a minimum 4-second delay between page display and submission - which yield a fake success and send nothing. New cases: UT-PAGE-21 (key absent from raw HTML, obfuscation coverage), PT-FORM-04 (honeypot + time-trap behaviour, key not scrapable) and PT-INFO-04 (no clear e-mail / phone / key in the published source). To retest without new text: UT-JS-01 (the render also injects the key), UT-JS-09 (a legit submission still works after 4 s). Verified locally on 17/09: key absent from raw HTML, injected at render; submission within 4 s blocked with no Web3Forms request; e-mail links rebuilt.)

(Version 1.3 - 17 September 2026 - requirement added by Lydie PARSUS: **every user input field must be protected against SQL injection and other attacks**. The site's only input fields are the four contact-form fields (name, e-mail, organisation, message) on `index.html` / `en/index.html`; the site is static with **no database**, so no SQL can be injected into the site itself, and messages travel as inert text through the Web3Forms relay to the mailbox. Hardening added on 17/09: `maxlength` caps on the four fields (100 / 254 / 150 / 5000), `autocomplete` hints, `inputmode="email"`; the script already displays everything with `textContent` (never `innerHTML`) and the e-mail field is `type="email" required`. New cases: UT-PAGE-20 (form hardening attributes) and PT-INPUT-01 (injection sweep - SQL, script, CRLF, oversized, control characters - on every field); PT-XSS-03 and PT-FORM-01 unchanged and still applicable.)

(v1.2 - 16 September 2026 - site state: stylesheet / script version `20260915a`, commit `d733834` (v1.0: 15 September 2026, commit `4a8ce3e`, 40 indexable pages + 10 redirect stubs + 404; v1.1: 15 September 2026, readable home anchors + footer alignment). Changes in v1.2: every link to the OKILYS Suite products - suite bar button to `https://ctms.okilys.com`, menu sub-entries and home / suite / insights buttons to `ctms.html` and `etmf.html`, "Accès client" - now opens in a **new tab** with `target="_blank" rel="noopener noreferrer"` (86 links, FR + EN; new case UT-PAGE-19, updated IT-NAV-01/02/05/06/07, new ST-NAV-06); the `ctms.html` module map and its JSON-LD gained the sponsor-oversight thematic module (ICH E6(R3)) on 15/09 (covered by UT-PAGE-08/18 and IT-I18N-02, no new case).) Author: assistant, on request of Lydie PARSUS (OKILYS). Companion document of the OKILYS CTMS test specification (`OKILYS CTMS\ctms\docs\TEST-SPECIFICATION.md`): same four levels, same conventions, same reporting format (dated run report, defect register with severity and French plain-language columns), so that the results of both products can be compiled together.

## 1. Purpose, scope and references

This document specifies the tests of the OKILYS showcase website at four levels: **unit tests** (the JavaScript behaviours of `js/script.js` and the per-file static checks of every page), **integration tests** (pages working together: menus, language pairs, sitemap, redirects, assets, the contact-form relay, the hosting), **system tests** (end-to-end visitor journeys in real browsers, desktop and mobile, on the live site) and **penetration testing** (security assessment of the live site, its DNS and its public repository). It covers every function of the site as published on 15/09/2026.

The site is static (HTML, CSS, vanilla JavaScript), built by GitHub Pages from the public repository `OKILYSLifeScience/vitrine-okilys`, served at https://www.okilys.com (French at the root, English mirror in `en/`). It has no backend, no database, no cookie, no tracker and no third-party script; fonts are self-hosted. The only external call is the contact form, relayed by Web3Forms (`https://api.web3forms.com/submit`) with a public access key. Everything in `_notes/`, `_drafts/` and `_archives/` is excluded from publication (Jekyll ignores folders prefixed by `_`; `_drafts/` and `_archives/` are also outside git).

References: WCAG 2.2 level AA; OWASP Web Security Testing Guide 4.2 (information gathering, configuration, client-side testing); OWASP Top 10 2021; Google Search Essentials and the Rich Results guidelines; schema.org; RFC 7208 (SPF), RFC 7489 (DMARC), RFC 8659 (CAA); Mozilla Observatory; GitHub Pages documentation (custom domains, HTTPS enforcement, no custom response headers, 10-minute cache).

Risk-based approach: the contact form and the external links carry the only security exposure and are tested at all four levels; the bilingual navigation and the search-engine metadata carry the business risk (a lost prospect, a page badly indexed) and are tested by automated checks on every page plus visitor journeys; purely visual sections are covered by system tests only.

## 2. Test strategy and organisation

### 2.1 Levels, tools and environments

| Level | Object | Tool / technique | Environment | Data |
|---|---|---|---|---|
| Unit (UT) | The functions of `js/script.js` (contact obfuscation, mobile menu, scrollspy, footer year, contact-form handler, news carousel) and the per-file checks of every HTML page (metadata, headings, links, structured data, version tags) | Playwright (Chromium) evaluating the functions on a locally served page, with `fetch` mocked for the form; Python script for the static checks (the `audit.py` pattern: regex over the 51 HTML files + `sitemap.xml`) | Local static server (`python -m http.server 8090`, config `vitrine` in `.claude/launch.json`) | The published pages themselves |
| Integration (IT) | Pages working together: menu → pages, FR ↔ EN pairs, sitemap ↔ files, redirect stubs → targets, assets referenced ↔ files present, form → Web3Forms, hosting behaviour (redirects, 404, exposure) | Python `requests` + parsing on the local server, then the same on https://www.okilys.com; one real form submission with a `[TEST]` marker | Local server, then production (read-only, static) | Test message marked `[TEST]` |
| System (ST) | End-to-end visitor journeys in the browser (Chrome, Edge, Firefox, Safari iOS), desktop 1366 and 1440 px, tablet 768 px, mobile 390 px; accessibility, performance and search-engine checks | Manual scripted tests with screenshots; Playwright for the regression subset (R); Lighthouse, axe, Google Rich Results test, hreflang validator | Production https://www.okilys.com (static site: no data risk) | None |
| Penetration (PT) | The live site, its DNS zone (`okilys.com`), its TLS, the public repository and its history, the contact-form relay as used by the site | OWASP WSTG methodology; testssl.sh, dig / nslookup, Mozilla Observatory, ZAP baseline, gitleaks / trufflehog on the repository, manual client-side review | Production (static) and the public repository | Test messages marked `[TEST]` only; **no load, no flooding of the form relay, no test against Web3Forms or GitHub infrastructure themselves** |

### 2.2 Conventions

- Test identifiers: `UT-JS-<nn>`, `UT-PAGE-<nn>`, `IT-<area>-<nn>`, `ST-<journey or area>-<nn>`, `PT-<category>-<nn>`. Each case: preconditions, steps or input, expected result, evidence, status (Pass / Fail / Blocked / Not applicable).
- Expected results derive from the site as specified in `_notes/REPRISE-session.md` (conventions and decisions), the memory notes of the site session and this document.
- Severity for a showcase site: **Critical** = security exposure (form, secret, external link hijack, DNS) or the site unreachable or a page broken in both languages; **Major** = a function unusable on one page or one language (broken link, wrong redirect, missing language pair, form not sending, menu unusable on mobile); **Minor** = cosmetic, wording, metadata length, performance below target.
- Every defect is logged as in the CTMS register: id, test id, severity, `defect` (English), `location` (file and line), `defect_fr` (translation), `ref_fr` (where: page › section › block, in plain words), `plain_fr` (what is wrong, for a non-specialist), `impact_fr` (consequence for a visitor or for the search ranking). Fixed defects are retested on the next publication.
- Regression: the automated set (UT-PAGE + IT) runs after every publication; the ST regression subset (R) runs after any change to the menu, the stylesheet or the script; PT runs after any change to the contact form, the DNS or the external links, and at least once a year.
- Acceptance: 100 % of Critical and Major cases Pass, no open Critical or Major defect, every Minor defect listed with a decision; PT: no open High or Critical finding.

### 2.3 Test data and fixtures

- Page inventory: 20 French indexable pages at the root (`index`, `a-propos`, `actualites`, `highlights`, `medicament`, `dispositif-medical`, `donnees`, `pratique-courante`, `inm`, `conception`, `selection-centres`, `preparation`, `soumissions`, `mise-en-place`, `conduite-suivi`, `cloture`, `suite`, `ctms`, `etmf`, `mentions-legales`) and their 20 English mirrors in `en/` (`index`, `about`, `insights`, `highlights`, `drug`, `medical-device`, `data`, `standard-of-care`, `npi`, `design`, `site-selection`, `preparation`, `submissions`, `initiation`, `conduct-monitoring`, `close-out`, `suite`, `ctms`, `etmf`, `legal-notice`); 10 redirect stubs (`contact`, `fondatrice`, `notre-expertise`, `presentation`, `services`, `en/contact`, `en/founder`, `en/our-expertise`, `en/privacy-policy`, `en/services`); `404.html`.
- Menu (identical on every page, FR / EN): Accueil / Home · Produits de santé / Health products (5 entries) · Expertises / Expertise (7 numbered steps) · Secteurs / Sectors · Réalisations / Highlights · Actualités / Insights · À propos / About us · OKILYS Suite (teal pill, 3 entries) · Contact · language switch.
- Suite bar (above the header on every page): OKILYS website (current) · OKILYS CTMS → https://ctms.okilys.com · OKILYS eTMF badged *à venir / coming soon* (no link yet).
- **New-tab rule (since 16/09/2026)**: every link pointing to an OKILYS Suite product — `ctms.html`, `etmf.html` (menu sub-entries, home suite cards, insights buttons, suite-page buttons) or `https://ctms.okilys.com` (suite bar, "Accès client") — carries `target="_blank" rel="noopener noreferrer"`. Links to `suite.html` (the story page) and all other internal links stay in the same tab. When the eTMF badge becomes a real link, it must follow the same rule.
- Contact form: fields name (`maxlength=100`), email (`type=email`, `maxlength=254`), organisation (optional, `maxlength=150`), message (`maxlength=5000`); name / email / message `required`; hidden `access_key`, `subject`, `from_name`; honeypot checkbox `botcheck`; messages FR / EN for sending, sent, failed, network error, always displayed with `textContent`. These four fields are the **only** user inputs of the whole site (no search box, no comment, no URL parameter read by the script).
- Test message: name `Test OKILYS`, organisation `[TEST] spec run <date>`, message `[TEST] automated check, please ignore`.

## 3. Function inventory and traceability

| Area | Functions (pages / behaviours) | Unit | Integration | System | Pentest |
|---|---|---|---|---|---|
| Shell | Suite bar, header (logo, tagline), main menu with 3 drop-downs, language switch, burger menu on mobile, sticky header shadow, footer (links, e-mail, LinkedIn, year, legal link) | UT-JS-02..06, UT-PAGE-14 | IT-NAV, IT-I18N | ST-NAV, ST-MOB | PT-LINK |
| Home (FR / EN) | Hero, figures band, news carousel, À propos + HOME values tiles, Produits de santé (5 cards), Expertises (7 steps), Secteurs, OKILYS Suite panel, Contact (form + e-mail / phone) | UT-JS-01, 07..14, UT-PAGE-20 | IT-FORM | ST-HOME, ST-CONTACT | PT-FORM, PT-XSS, PT-INPUT |
| Product pages (×5) | Band photo + title card, definition, journey infographic, "Cadres réglementaires" in 4 zones (Monde / UE / France / Belgique) | UT-PAGE | IT-NAV, IT-I18N | ST-PAGE-01 | - |
| Step pages (×7) | Band, "Ce que nous faisons à cette étape", roles held, links to previous / next step | UT-PAGE | IT-NAV, IT-I18N | ST-PAGE-02 | - |
| À propos / About | Fondatrice (portrait, roles, certificate), Références (14 logos, 13 clickable, "Parcours salarié" block, 4 LinkedIn recommendations in English) | UT-PAGE | IT-NAV | ST-PAGE-03 | PT-LINK |
| Réalisations / Highlights, Actualités / Insights | Articles with anchors, links from the home carousel | UT-PAGE | IT-NAV | ST-PAGE-04 | - |
| OKILYS Suite pages | `suite` (story), `ctms` (positioning, differentiators, core / modules / tools, overview, workspace, roles, security, process), `etmf` (coming soon) | UT-PAGE | IT-NAV | ST-PAGE-05 | PT-LINK |
| Legal, 404, redirect stubs | Mentions légales / Legal notice, custom 404, 10 stubs with meta refresh | UT-PAGE-11, 12 | IT-REDIR, IT-HOST | ST-PAGE-06 | PT-REDIR, PT-INFO |
| Search-engine layer | title, description, canonical, hreflang pairs, Open Graph / Twitter tags, JSON-LD (Organization, Person, WebSite, FAQPage, BreadcrumbList, Service, SoftwareApplication), robots.txt, sitemap.xml (40 URLs), Google / Bing verification | UT-PAGE-01..10 | IT-SEO | ST-SEO | PT-INFO |
| Assets and delivery | Self-hosted fonts (Manrope, Agne) with preload, images with dimensions and lazy loading, `?v=AAAAMMJJx` version on CSS / JS, 10-minute cache on GitHub Pages | UT-PAGE-13, 15 | IT-ASSET | ST-PERF | PT-SUPPLY |
| Hosting and domain | CNAME, HTTP → HTTPS, apex → www, TLS certificate, DNS (SPF, DMARC, CAA, subdomains ctms / etmf) | - | IT-HOST | - | PT-TLS, PT-DNS, PT-INFO |

## 4. Unit test specification

### 4.1 UT-JS (`js/script.js`, evaluated with Playwright on the local server)

| Id | Function | Input / action | Expected | Traduction FR (où, quoi) |
|---|---|---|---|---|
| UT-JS-01 | `unreverse` + `[data-email]` initialisation | page loaded | every element with `data-email` gets `href="mailto:<address>"` and shows the address; `data-tel` gets `href="tel:<number>"` and shows the label; the raw HTML never contains the address in clear | Accueil › Contact et pied de page : l'adresse e-mail et le téléphone s'affichent correctement et sont cliquables, alors qu'ils sont masqués dans le code source (anti-robots) |
| UT-JS-02 | `toggleNav` | click on `#burger` at 390 px | `#nav`, `#nav-overlay`, `#burger` get `is-open`; `aria-expanded="true"`; `body.nav-open`; `nav.style.top` = bottom of the header; `maxHeight` = viewport height minus header | Menu mobile : le bouton ☰ ouvre le panneau juste sous l'en-tête, à la bonne hauteur |
| UT-JS-03 | `closeNav` | overlay click, or click on any menu link, after UT-JS-02 | every `is-open` removed, `aria-expanded="false"`, inline `top` / `maxHeight` cleared | Menu mobile : toucher le fond grisé ou un lien referme le menu |
| UT-JS-04 | `sizeNav` on resize | open menu, change viewport height | `maxHeight` recomputed | Menu mobile : le panneau reste défilable quand la barre d'adresse du téléphone apparaît ou disparaît |
| UT-JS-05 | sub-menu caret on mobile | click on `.caret` of "Produits de santé" at 390 px | `nav-item.is-sub-open` toggled, no navigation (default prevented); at 1366 px the click follows the link | Menu mobile : la petite flèche déplie le sous-menu sans changer de page ; sur ordinateur elle mène à la page |
| UT-JS-06 | sticky header shadow | `window.scrollY` 0 → 20 | `#header` box-shadow none → set | En-tête : une ombre apparaît sous le bandeau dès qu'on descend dans la page |
| UT-JS-07 | scrollspy `updateSpy` (home only) | scroll to each `main section[id]` and `.band[id]` | the menu link pointing to that anchor gets `is-active`, the others lose it; the CTA "Contact" is never highlighted | Accueil : l'entrée de menu de la section visible est surlignée pendant le défilement |
| UT-JS-08 | footer year | page loaded | `#year` = current year | Pied de page : l'année du copyright est l'année en cours |
| UT-JS-09 | form handler, success | `fetch` mocked → `{success:true}`; submit with valid fields | `preventDefault`, button disabled during the call, note = "Envoi en cours…" then "Message envoyé…" (EN: "Sending…" / "Message sent…"), fields reset, button re-enabled | Accueil › Contact : après « Envoyer », le bouton se grise, puis le message de confirmation s'affiche et le formulaire se vide |
| UT-JS-10 | form handler, relay refusal | `fetch` mocked → `{success:false}` | note = "L'envoi a échoué…" (EN equivalent), fields kept, button re-enabled | Contact : si le relais refuse, le message d'échec s'affiche et le texte saisi n'est pas perdu |
| UT-JS-11 | form handler, network error | `fetch` mocked → rejected promise | note = "L'envoi a échoué (connexion)…", button re-enabled | Contact : sans connexion, le message d'échec « connexion » s'affiche |
| UT-JS-12 | form handler, language | same on `en/index.html` | English messages selected from `document.documentElement.lang` | Contact (EN) : les messages sont en anglais |
| UT-JS-13 | carousel `goNews`, dots, arrows | 3 slides; click next ×3, prev ×1, dot 2 | index wraps 0→1→2→0; `translateX(-100 %·index)`; active dot follows; timer restarted after each interaction | Accueil › Actualités : les flèches et les points font défiler les actualités en boucle |
| UT-JS-14 | carousel timer and touch | wait 6.5 s; hover; swipe of 60 px left / right; swipe of 20 px | auto-advance every 6.5 s; paused on hover, resumed on leave; swipe ≥ 40 px changes slide in the right direction; shorter swipe ignored | Accueil › Actualités : défilement automatique, pause au survol, glissement au doigt |

### 4.2 UT-PAGE (static checks, every HTML file; run by script)

| Id | Check | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| UT-PAGE-01 | `<html lang>` | `fr` at the root, `en` in `en/` | Chaque page annonce sa langue |
| UT-PAGE-02 | `<title>` | present, unique across the site, ≤ 70 characters, ends with the OKILYS brand | Titre d'onglet présent, unique, court, avec la marque |
| UT-PAGE-03 | `meta description` | present, unique, 70–160 characters, consistent with the page content | Description Google présente, unique, de bonne longueur, fidèle à la page |
| UT-PAGE-04 | canonical | `https://www.okilys.com/<path>` equal to the file's own URL (`/` for `index.html`, `/en/` for `en/index.html`) | L'adresse officielle déclarée est bien celle de la page |
| UT-PAGE-05 | hreflang | `fr` = own French URL, `en` = own English URL, `x-default` = French URL; the target file exists and points back | Chaque page désigne sa jumelle dans l'autre langue, et réciproquement |
| UT-PAGE-06 | Open Graph / Twitter | `og:url` = canonical, `og:locale` fr_FR / en_GB, `og:title` and `og:description` present, `og:image` 1200×630 existing, `twitter:card` summary_large_image | Balises de partage (LinkedIn, etc.) complètes et cohérentes |
| UT-PAGE-07 | headings | exactly one `h1`; no skipped level (`h2` before `h3`); no em dash "—" inside `h1`/`h2`/`h3` styled with the Agne font (`.section__title`, `.mod-card h3`, legal `h2`) | Un seul titre principal, hiérarchie propre, pas de tiret long dans les titres (la police ne l'a pas) |
| UT-PAGE-08 | JSON-LD | every block parses; `WebPage.url` and `@id` = canonical; `BreadcrumbList` present on sub-pages; `inLanguage` matches; site-level `Organization` / `WebSite` / `Person` on home and About | Fiches Google valides et cohérentes avec l'adresse de la page |
| UT-PAGE-09 | robots meta | `index, follow…` on the 40 pages; `noindex, follow` on the 10 stubs and on `404.html` | Les vraies pages sont indexables, les redirections et la 404 ne le sont pas |
| UT-PAGE-10 | Google verification tag | present on the 40 indexable pages (same content value) | Balise de vérification Search Console présente partout |
| UT-PAGE-11 | redirect stubs | `meta http-equiv="refresh" content="0; url=<target>"`, target existing, canonical = target, `noindex`, a visible fallback link | Les anciennes adresses renvoient vers la bonne page, sans être indexées |
| UT-PAGE-12 | 404 page | root-relative links (`/…`) so that it works from any depth; `noindex`; both languages offered | La page « introuvable » fonctionne quel que soit l'endroit où on tombe |
| UT-PAGE-13 | CSS / JS version tags | `css/fonts.css`, `css/styles.css`, `css/fusion.css`, `js/script.js` referenced with the same `?v=` value on all 51 pages; the value is the latest (format `AAAAMMJJ` + letter) | Les 51 pages appellent la même version des feuilles de style et du script |
| UT-PAGE-14 | shell consistency | same suite bar, same menu entries and order, same footer links on every page of a language; language switch present | Barre, menu et pied de page identiques sur toutes les pages |
| UT-PAGE-15 | no external resources | no `<script src>` / `<link>` / `@import` / `url()` to another domain; no `fonts.googleapis.com`; no inline event handlers (`onclick=`) | Aucun appel à un service extérieur (pas de bandeau cookies nécessaire) |
| UT-PAGE-16 | images | every `<img>` has `alt` (empty allowed for decorative), `width` and `height`; `loading="lazy"` below the fold; file exists | Toutes les images ont une description, des dimensions et existent |
| UT-PAGE-17 | internal links and anchors | every relative `href` resolves to a file; every `#anchor` exists in the target page; no `C:\` or local path | Aucun lien mort, aucune ancre manquante |
| UT-PAGE-18 | forbidden wording (public supports) | no module code (`A1`, `B1`… `K`) on `ctms`, `etmf`, `suite`; "signature électronique tracée et infalsifiable" (never "avancée"); OKILYS never called a CRO; "Lydie PARSUS" in capitals everywhere (title, meta, alt included); "lifecycle" in one word | Règles de rédaction : pas de codes de modules, signature « tracée », pas « CRO », nom en majuscules |
| UT-PAGE-19 | product links open in a new tab | every `<a>` whose `href` is `ctms.html`, `etmf.html` or starts with `https://ctms.okilys.com` (any page, FR and EN) carries `target="_blank"` **and** `rel` containing `noopener` and `noreferrer`; conversely no link to `suite.html` or to any other internal page carries `target="_blank"` | Tous les liens vers les produits OKILYS CTMS / eTMF s'ouvrent dans un nouvel onglet, en toute sécurité ; les autres pages du site restent dans le même onglet |
| UT-PAGE-21 | contact info and key hidden from robots | in the raw HTML of every page (as served, before JavaScript): no clear e-mail address (`@okilys.com`), no clear phone number, and no Web3Forms key (`72f439e6…`); the address / phone are held reversed in `data-email` / `data-tel` and the key reversed in `data-key`; no `email` / `telephone` in clear inside JSON-LD; after render, the `mailto:` and `tel:` links and the hidden `access_key` field are correctly rebuilt | Les adresses e-mail, le téléphone et la clé du formulaire n'apparaissent jamais en clair dans le code source des pages (un robot qui lit le code ne les voit pas) ; ils sont reconstruits uniquement quand un vrai navigateur affiche la page |
| UT-PAGE-20 | contact-form input hardening | on `index.html` and `en/index.html`: name `type=text required maxlength=100`, email `type=email required maxlength=254`, organisation `maxlength=150`, message `required maxlength=5000`; honeypot `botcheck` present and hidden; `js/script.js` contains no `innerHTML`, no `eval`, no `document.write` - the form note and every dynamic text use `textContent`; no other `<input>` / `<textarea>` / `<select>` exists anywhere on the site | Les quatre champs du formulaire de contact sont bornés (longueur maximale, format e-mail imposé, champs obligatoires) et rien de ce qu'un visiteur tape ne peut être exécuté par la page ; aucun autre champ de saisie n'existe sur le site |

## 5. Integration test specification

### 5.1 IT-NAV (menus and links between pages)

| Id | Test | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| IT-NAV-01 | every main-menu entry on every page | Accueil → `index.html`; Produits de santé → `index.html#produits-de-sante` (EN `#health-products`) + 5 sub-entries → the 5 product pages; Expertises → `index.html#expertises` (EN `#expertise`) + 7 steps in order; Secteurs → `#secteurs` (EN `#sectors`); Réalisations → `highlights.html`; Actualités → `actualites.html`; À propos → `a-propos.html`; OKILYS Suite → `suite.html` (same tab) + `ctms.html` + `etmf.html` (badge à venir) both in a new tab; Contact → `index.html#contact`; all targets exist | Menu : chaque entrée mène à la bonne page ou section ; les entrées CTMS et eTMF ouvrent un nouvel onglet |
| IT-NAV-02 | suite bar on every page | OKILYS website marked current (no link); OKILYS CTMS → `https://ctms.okilys.com` in a new tab with `rel="noopener noreferrer"`; OKILYS eTMF badge *à venir / coming soon* with no external link; tagline present | Barre OKILYS Suite : le bouton CTMS ouvre l'application dans un nouvel onglet, eTMF annoncé à venir |
| IT-NAV-03 | footer links on every page | each link resolves; the footer entries name the same destinations as the menu (no obsolete label such as "Contactez-nous" vs "Contact", "Fondatrice" pointing to `a-propos.html#fondatrice`); legal link → `mentions-legales.html` / `en/legal-notice.html`; LinkedIn → company or founder profile with `noopener` | Pied de page : liens à jour et cohérents avec le menu |
| IT-NAV-04 | previous / next step links on the 7 step pages | chain 1 → 7 in order, both languages | Pages Expertises : les liens « étape précédente / suivante » suivent l'ordre |
| IT-NAV-05 | home carousel buttons "Lire l'actualité" | each → `actualites.html#<anchor>` existing (EN: `insights.html#<anchor>`), same tab; on the news page itself, the buttons "Découvrir OKILYS CTMS / eTMF" open `ctms.html` / `etmf.html` in a new tab | Accueil › Actualités : le bouton ouvre le bon article ; sur la page Actualités, les boutons « Découvrir » ouvrent les pages produits dans un nouvel onglet |
| IT-NAV-06 | OKILYS Suite panel on the home page | 2 cards → `ctms.html`, `etmf.html`, each in a new tab; button "Comment ces outils sont nés" → `suite.html` in the same tab | Accueil › encart OKILYS Suite : les cartes produits ouvrent un nouvel onglet, le bouton « histoire » reste dans l'onglet |
| IT-NAV-07 | CTA buttons | "Parlons de votre étude" (ctms, etmf, suite) → `index.html#contact` same tab; "Accès client" → `https://ctms.okilys.com` in a new tab with `rel="noopener noreferrer"` | Boutons d'appel à l'action : contact dans le même onglet, accès client dans un nouvel onglet |
| IT-NAV-08 | About page anchors | `#fondatrice` and `#references` exist and are reachable from the menu, the footer, the 404 page, the stubs and JSON-LD `Person.url` | Page À propos : les ancres Fondatrice et Références répondent depuis partout |

### 5.2 IT-I18N (French / English pairs)

| Id | Test | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| IT-I18N-01 | language switch on each of the 40 pages | FR page → its own EN mirror (never the EN home), and back | Bouton EN / FR : on tombe sur la même page dans l'autre langue |
| IT-I18N-02 | structural parity | same number of `<section>` and same `id` set between a page and its mirror; same menu structure; same number of cards in each grid | Les deux versions ont la même structure |
| IT-I18N-03 | content parity of the last changes | the differentiators, the core / modules / tools cards, the Overview and Workspace sections of `ctms` have the same items in both languages; product pages have the 4 regulatory zones in both languages | Les derniers ajouts existent dans les deux langues |
| IT-I18N-04 | anchors per language | home sections: FR `#apropos`, `#produits-de-sante`, `#expertises`, `#secteurs`, `#okilys-suite`, `#contact` ↔ EN `#apropos`, `#health-products`, `#expertise`, `#sectors`, `#okilys-suite`, `#contact` (renamed 15/09/2026 for readable addresses); `#fondatrice`, `#references` identical; old names `#developpement`, `#domaines` (and FR `#expertise`) redirected by the script to the new ones | Les repères de sections sont lisibles dans chaque langue ; les anciennes adresses sont rattrapées |
| IT-I18N-05 | quotes kept in English | the 4 LinkedIn recommendations on `a-propos.html` are in their original English | Page À propos : les recommandations restent en anglais d'origine (décision) |

### 5.3 IT-SEO (search-engine files and consistency)

| Id | Test | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| IT-SEO-01 | `sitemap.xml` | valid XML with `xhtml:link` alternates; exactly the 40 indexable URLs (`/` and `/en/` for the two homes); no stub, no 404; every `lastmod` ≥ the file's last git commit date; every hreflang in the sitemap equals the page's own tags | Plan du site complet, à jour et cohérent avec les pages |
| IT-SEO-02 | `robots.txt` | `Allow: /`, `Sitemap:` line, no `Disallow` of a real page | Fichier robots correct |
| IT-SEO-03 | structured-data types per page | home: Organization, WebSite, FAQPage (if FAQ present), BreadcrumbList; About: Person; product / step pages: Service + BreadcrumbList; `ctms`: SoftwareApplication with provider = Organization; `etmf`: SoftwareApplication or WebPage with the "coming soon" wording | Fiches Google du bon type sur chaque page |
| IT-SEO-04 | `og:image` | `assets/images/og-image.jpg` exists, 1200×630, < 300 kB | Image de partage présente et légère |
| IT-SEO-05 | duplicate content | no two pages with identical `title` or `description`; stubs carry `noindex` so they never compete | Pas de doublon de titres ou de descriptions |
| IT-SEO-06 | 404 status | GitHub Pages returns HTTP 404 with the custom page for a missing URL (`/nope.html`, `/en/nope.html`) | Une adresse inexistante renvoie bien la page « introuvable » avec le bon code |

### 5.4 IT-REDIR (10 redirect stubs)

| Id | Test | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| IT-REDIR-01 | targets | `contact` → `index.html#contact`; `fondatrice` → `a-propos.html#fondatrice`; `notre-expertise` → `index.html#expertises`; `presentation` → `index.html#apropos` (or `a-propos.html`); `services` → `index.html#expertises`; EN equivalents; `en/privacy-policy` → `en/legal-notice.html` | Les anciennes adresses redirigent vers la bonne section |
| IT-REDIR-02 | behaviour | HTTP 200 + instant `meta refresh`; visible link if JavaScript / refresh disabled; `noindex`; canonical = target | Redirection immédiate, avec lien de secours |

### 5.5 IT-ASSET (files, fonts, images, versions)

| Id | Test | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| IT-ASSET-01 | every referenced file (CSS, JS, images, fonts, favicon, og-image, CNAME) | exists in the repository and answers 200 on the live site | Aucun fichier manquant en ligne |
| IT-ASSET-02 | fonts | `css/fonts.css` declares Manrope 400 / 600 / 800 and Agne from `assets/fonts/`; `<link rel="preload">` matches the files; `font-display: swap`; no request leaves the domain | Polices hébergées sur le site, chargées en priorité |
| IT-ASSET-03 | version tag freshness | after a CSS or JS change, the `?v=` value changed on all 51 pages (compare with `git log` of `css/` and `js/`) | Après une modification de style ou de script, la version a été incrémentée partout |
| IT-ASSET-04 | image weight | no image > 400 kB except the portrait and band photos ≤ 600 kB; section photos in 21:9, suite photos 4:3 | Images allégées |
| IT-ASSET-05 | `.gitignore` and publication | `_drafts/`, `_archives/`, `NOTES.md`, `.claude/` ignored; `_notes/` committed but unreachable online (404) | Rien de non publiable n'est en ligne |

### 5.6 IT-FORM (contact form relay)

| Id | Test | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| IT-FORM-01 | markup | `action="https://api.web3forms.com/submit"`, `method="POST"`, hidden `access_key` / `subject` / `from_name`, honeypot `botcheck` hidden and unchecked, `required` on name / email / message, `type="email"`, labels bound to inputs, `role="status"` on the note | Formulaire correctement construit et accessible |
| IT-FORM-02 | real submission FR | send the test message from `index.html` | relay answers `success:true`; the e-mail reaches the OKILYS address within 5 minutes with subject "Nouveau message depuis okilys.com", all fields, sender e-mail usable for reply | Contact : un message envoyé depuis le site arrive bien dans la boîte OKILYS |
| IT-FORM-03 | real submission EN | same from `en/index.html` | same, with the English subject if configured | Contact (EN) : idem |
| IT-FORM-04 | validation | submit with empty required field / malformed e-mail | browser blocks before sending; no request made | Le navigateur refuse un formulaire incomplet |
| IT-FORM-05 | honeypot | submit with `botcheck` checked (script) | relay rejects or silently drops; no e-mail received | Un robot qui coche la case cachée est ignoré |
| IT-FORM-06 | special characters | message with accents, apostrophes, `<b>`, `&`, line breaks | arrives intact and escaped (no HTML interpreted in the e-mail) | Les caractères spéciaux arrivent correctement, sans code interprété |

### 5.7 IT-HOST (domain and GitHub Pages)

| Id | Test | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| IT-HOST-01 | redirects | `http://okilys.com`, `http://www.okilys.com`, `https://okilys.com` → 301 → `https://www.okilys.com/`, path preserved | Toutes les variantes d'adresse mènent au site sécurisé |
| IT-HOST-02 | CNAME | file content `www.okilys.com`; DNS `www` CNAME to GitHub Pages, apex A / AAAA records to GitHub | Domaine correctement branché |
| IT-HOST-03 | cache | `Cache-Control: max-age=600` observed; documented consequence: versioned CSS / JS | Mise en cache de 10 minutes connue et gérée |
| IT-HOST-04 | exposure | `/_notes/`, `/_drafts/`, `/_archives/`, `/.git/`, `/.gitignore`, `/NOTES.md`, `/.claude/` → 404 | Les dossiers de travail ne sont pas accessibles en ligne |
| IT-HOST-05 | sub-domains | `ctms.okilys.com` answers over HTTPS with a valid certificate; `etmf.okilys.com` either absent or pointing to something OKILYS controls (no dangling record) | Les sous-domaines CTMS / eTMF sont sains |

## 6. System test specification (end-to-end)

Executed on https://www.okilys.com in Chrome, Edge and Firefox (current versions) and Safari on iOS; desktop 1366 px (the reference width for the one-line menu) and 1440 px, tablet 768 px, mobile 390 px. Screenshots as evidence. (R) = Playwright regression subset.

### 6.1 ST-NAV (navigation, desktop)

| Id | Scenario | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| ST-NAV-01 (R) | at 1366 px, every page | the menu fits on one line (no wrap, no overflow), tagline "Make People Health & Wellness our Priority" on one line, language switch and Contact button visible | Menu sur une seule ligne à 1366 px |
| ST-NAV-02 (R) | drop-downs | hover and keyboard (Tab / Enter / Escape) open and close Produits de santé, Expertises, OKILYS Suite; entries clickable; the parent link itself navigates | Sous-menus utilisables à la souris et au clavier |
| ST-NAV-03 | scrollspy | scrolling the home page highlights the matching entry (Accueil, Produits, Expertises, Secteurs, Contact) including the Références band | L'entrée de menu suit la section affichée |
| ST-NAV-04 (R) | language switch | from each of 6 sampled pages (home, a product, a step, About, Actualités, CTMS) the switch lands on the mirror, same scroll position when anchored | Changement de langue sans perdre la page |
| ST-NAV-05 | back / forward | browser history works with anchors and stubs (no loop on the redirect stubs) | Les boutons Précédent / Suivant fonctionnent, sans boucle |
| ST-NAV-06 (R) | product links open a new tab | clicking OKILYS CTMS in the suite bar, in the menu drop-down, on a home suite card, on a "Découvrir" button (Actualités) or on "Accès client" (page CTMS) opens the product page or `ctms.okilys.com` in a **new tab**; the website tab stays on its page (scroll position kept); same for the eTMF page links; the new tab has no `window.opener` access back (check in the console); also verified on mobile Safari / Chrome (new tab, not a popup blocked) | Cliquer sur OKILYS CTMS ou OKILYS eTMF (barre, menu, cartes, boutons) ouvre un nouvel onglet : le site reste ouvert derrière, on ne perd pas sa lecture ; vérifié aussi sur téléphone |

### 6.2 ST-MOB (mobile 390 px and tablet 768 px)

| Id | Scenario | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| ST-MOB-01 (R) | burger menu | opens below the header, scrollable to the last entry (Contact, language), overlay closes it, sub-menu carets expand in place, no page scroll behind the panel | Menu mobile complet, défilable, refermable |
| ST-MOB-02 (R) | layout | no horizontal scroll on any of the 40 pages; images and bands fit; text ≥ 16 px; tap targets ≥ 44 px | Aucun débordement horizontal, textes lisibles, boutons assez grands |
| ST-MOB-03 | carousel | swipe left / right changes the news; arrows and dots usable; "Lire l'actualité" reachable | Diaporama utilisable au doigt |
| ST-MOB-04 | contact | form usable, keyboard types match fields (`type=email` + `inputmode=email` on the e-mail field), fields and button >= 44 px, no overflow at 375 px, sending works | Formulaire utilisable sur mobile avec le bon clavier |
| ST-MOB-05 | tablet 768 px | menu behaviour (burger) and grids (2 columns) correct | Affichage tablette correct |

### 6.3 ST-HOME (home page, FR then EN)

| Id | Scenario | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| ST-HOME-01 | hero and figures band | portrait, title, CTA, figures displayed; no layout shift when fonts load | En-tête d'accueil stable au chargement |
| ST-HOME-02 (R) | news carousel | slides = the 3 or 4 latest news, in the same order as `actualites.html`; automatic 6.5 s; pause on hover | Diaporama à jour et automatique |
| ST-HOME-03 | À propos + HOME tiles | 4 tiles Humain / Objectivité / Maîtrise / Engagement (EN: Human / Objectivity / Mastery / Engagement); sentence about future generations kept below | Valeurs HOME conformes aux textes validés |
| ST-HOME-04 | Produits de santé and Expertises | 5 product cards → 5 pages; 7 steps in order → 7 pages; the infographic renders | Cartes et frise complètes |
| ST-HOME-05 | Secteurs, OKILYS Suite panel, Contact | sectors listed; dark suite panel with 2 cards; contact section with form, e-mail and phone visible (obfuscation resolved) | Bas de page d'accueil complet |

### 6.4 ST-PAGE (page families)

| Id | Scenario | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| ST-PAGE-01 | 5 product pages | band photo (flowers) with title card; definition; journey infographic; "Cadres réglementaires" in 4 zones Monde / Union européenne / France / Belgique with the Belgian laws (7 May 2017, 22 Dec 2020 + RD 18 May 2021, 7 May 2004, 30 July 2018); INM page keeps its honest "no experience yet" wording | Pages produits : 4 zones réglementaires, page INM sans lissage |
| ST-PAGE-02 | 7 step pages | band photo (tree); "Ce que nous faisons à cette étape" list consistent with the roles described lower on the same page; 6 key roles overall (never 7); Clinical Project Manager shown as a certificate only | Pages étapes : liste cohérente avec les rôles, 6 rôles clés |
| ST-PAGE-03 | About page | portrait reduced size; **14 logos in the wall, of which 13 are clickable** (new tab, `noopener noreferrer`); **the 14th (Azeolys) deliberately carries no link** - decision of Lydie PARSUS, 19/09/2026, expected behaviour and not a defect; not labelled "clients"; "Parcours salarié, jusqu'en 2019" block; 4 recommendations in English; Magdalena's testimonial role (open point) | Page À propos conforme aux décisions |
| ST-PAGE-04 | Réalisations and Actualités | articles readable, anchors reachable from the home carousel and from LinkedIn-style links; dates and order descending | Réalisations et Actualités lisibles, ancres fonctionnelles |
| ST-PAGE-05 (R) | Suite, CTMS, eTMF | `ctms`: hero with the extended side follow-ups (trackers, calls, training, team allocation, system access register); sections in the order differentiators → core / modules / tools → overview → workspace → roles → security → process; backgrounds alternating; no module code; `etmf`: "à venir / coming soon" badge everywhere; `suite`: "Conçu par OKILYS, développé par INFRARCH" card | Pages Suite / CTMS / eTMF conformes au positionnement et à l'ordre validés |
| ST-PAGE-06 | Legal and 404 | legal notice mentions the host (GitHub Pages), the form relay (Web3Forms) as a processor, the absence of cookies; numbered headings render (no missing dash); 404 offers both languages and the main links | Mentions légales complètes, page 404 utile |

### 6.5 ST-CONTACT

| Id | Scenario | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| ST-CONTACT-01 (R) | send a `[TEST]` message from the live FR site | confirmation shown, e-mail received, reply-to = visitor address | Envoi réel depuis le site en ligne (FR) |
| ST-CONTACT-02 | same from EN | idem | Envoi réel (EN) |
| ST-CONTACT-03 | offline (devtools) | network message shown, text kept | Message d'erreur clair hors connexion |
| ST-CONTACT-04 | e-mail links | `mailto:` opens the mail client with the right address; the address is never visible in the page source (reversed in `data-email`, rebuilt at render). **By decision of Lydie PARSUS (19/09/2026) no phone number is published on the site**, so no `tel:` link is expected anywhere; the dormant `data-tel` helper is kept in `js/script.js` in case that changes. | Liens e-mail fonctionnels et adresse masquée aux robots. Aucun numéro de téléphone n'est publié, c'est un choix de Lydie |

### 6.6 ST-A11Y (accessibility, WCAG 2.2 AA)

| Id | Scenario | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| ST-A11Y-01 (R) | axe / Lighthouse accessibility on 8 sampled pages | score ≥ 95, no critical issue | Audit accessibilité automatique sans erreur bloquante |
| ST-A11Y-02 | keyboard only | every interactive element reachable in order, visible focus, drop-downs and burger operable (Enter / Space / Escape), carousel controls labelled | Site utilisable au clavier seul |
| ST-A11Y-03 | screen reader (NVDA) on the home | landmarks (header, nav, main, footer), one h1, form labels announced, status message read after sending | Lecture d'écran cohérente |
| ST-A11Y-04 | contrast and zoom | text contrast ≥ 4.5:1 (teal on white checked), page usable at 200 % zoom and at 320 px width | Contrastes et zoom conformes |
| ST-A11Y-05 | motion | carousel stops on hover / focus; `prefers-reduced-motion` respected if animations exist | Animations réductibles |

### 6.7 ST-SEO and ST-PERF (search engines and performance)

| Id | Scenario | Expected | Traduction FR (où, quoi) |
|---|---|---|---|
| ST-SEO-01 (R) | Lighthouse SEO on 8 sampled pages | 100 | Note SEO maximale |
| ST-SEO-02 | Google Rich Results test on home, About, a product page, `ctms` | structured data valid, no error | Fiches Google validées par l'outil Google |
| ST-SEO-03 | Search Console and Bing Webmaster | sitemap accepted, 40 URLs discovered, no "excluded by noindex" on a real page, no crawl error; coverage report reviewed | Rapports d'indexation sans erreur |
| ST-SEO-04 | hreflang validator (e.g. Merkle / Sistrix) on 6 pages | all pairs reciprocal | Paires de langues validées |
| ST-SEO-05 | snippet preview | title and description not truncated on Google desktop / mobile previews for the 10 most important pages | Aperçu Google lisible |
| ST-PERF-01 (R) | Lighthouse performance mobile on home, a product page, `ctms` | ≥ 90; LCP < 2.5 s; CLS < 0.1; total transfer < 1.5 MB | Pages rapides sur mobile |
| ST-PERF-02 | fonts | preload effective, no flash of invisible text longer than 100 ms | Polices chargées sans texte invisible |
| ST-PERF-03 | cache behaviour after a publication | within 10 minutes the new CSS / JS is served thanks to the `?v=` change; a hard refresh not needed | Après publication, la nouvelle version s'affiche sans manipulation |

## 7. Penetration testing specification

### 7.1 Scope and rules of engagement

- **Target**: https://www.okilys.com and the apex `okilys.com` (static site on GitHub Pages), the DNS zone `okilys.com` (records for `@`, `www`, `ctms`, `etmf`, mail), the TLS configuration, the public repository `OKILYSLifeScience/vitrine-okilys` and its history, and the contact-form relay **as used by the site** (our access key, our honeypot). Out of scope: GitHub's and Web3Forms' own infrastructure, the CTMS application (covered by its own specification), social engineering, denial of service, any flooding of the form relay.
- **Approach**: black-box on the live site plus white-box review of the repository (source available). Automated: Mozilla Observatory, ZAP baseline (passive), testssl.sh, gitleaks / trufflehog on the repository history, DNS enumeration (dig, dnsdumpster). Manual: client-side review of `js/script.js`, redirect stubs, external links, form abuse scenarios limited to a handful of `[TEST]` submissions.
- **Severity**: CVSS 3.1; Critical ≥ 9.0, High 7.0–8.9, Medium 4.0–6.9, Low < 4.0, Informational. Exit criteria: no Critical / High open; Medium with a recorded decision (`_notes/REPRISE-session.md`, section "Décisions").
- **Known constraints to record as accepted or mitigated**: GitHub Pages sends no custom security headers (no CSP, HSTS only if "Enforce HTTPS" is on and the domain is on the preload list, no X-Frame-Options); the Web3Forms access key is public by design (protection = honeypot + Web3Forms spam filtering + domain restriction if enabled); the repository is public (no secret may ever be committed).
- **Deliverables**: findings with evidence and reproduction steps, remediation, severity; retest report; decisions recorded.

### 7.2 Test cases

| Id | Category (WSTG) | Test | Expected secure behaviour | Traduction FR (où, quoi) |
|---|---|---|---|---|
| PT-INFO-01 | Information gathering | fingerprint headers, error pages, `robots.txt`, `sitemap.xml`; probe `/.git/`, `/.gitignore`, `/_notes/`, `/_drafts/`, `/_archives/`, `/NOTES.md`, `/.claude/`, backup / editor files (`*.bak`, `*~`, `.DS_Store`), directory listing on `/assets/`, `/css/`, `/js/` | only intended files served; work folders 404; no listing | Rien d'autre que le site n'est visible en ligne |
| PT-INFO-02 | Repository hygiene | gitleaks / trufflehog on the full history; grep for e-mails, phone numbers, keys, local paths (`C:\Users`), personal data in `_notes/` | no secret; the only key is the public Web3Forms key; personal data limited to what is published on the site; local paths absent from published files | Aucun secret ni donnée privée dans le dépôt public |
| PT-INFO-04 | Contact data harvesting | grep the **published** pages (as served) and the JSON-LD for any clear e-mail (`@okilys.com`), phone number or the Web3Forms key; check they appear only reversed in `data-*` attributes | none in clear; e-mail, phone and key are reconstructed by JavaScript only, invisible to a source-reading scraper | Un robot qui aspire le code des pages ne récolte ni adresse e-mail, ni numéro, ni clé exploitable |
| PT-INFO-03 | Metadata leakage | EXIF / XMP in images (GPS, author, software), PDF metadata if any | no geolocation or private metadata | Les photos ne contiennent pas de données cachées |
| PT-TLS-01 | Transport | testssl.sh on `www.okilys.com` and `okilys.com`: protocols, ciphers, certificate chain, expiry, OCSP, HTTP → HTTPS 301 on every path | TLS 1.2 / 1.3 only, strong ciphers, valid certificate auto-renewed by GitHub, no mixed content | Connexion chiffrée correcte, certificat valide |
| PT-TLS-02 | HSTS | header `Strict-Transport-Security` present after "Enforce HTTPS"; preload eligibility | present, or documented as a GitHub Pages limitation with the risk accepted | Forçage du HTTPS par le navigateur |
| PT-HDR-01 | Security headers | Mozilla Observatory: CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, X-Frame-Options | absent headers cannot be set on GitHub Pages: evaluate a `<meta http-equiv="Content-Security-Policy">` (script-src 'self', connect-src api.web3forms.com, img-src 'self' data:, style-src 'self' 'unsafe-inline' if inline styles kept) and `<meta name="referrer" content="strict-origin-when-cross-origin">`; decision recorded | En-têtes de sécurité : compenser par des balises dans les pages, décision à prendre |
| PT-XSS-01 | Client-side | review every DOM sink in `js/script.js` (`setAttribute('href')`, `textContent`, `style.transform`) and their sources (`data-*` attributes authored in HTML only; no URL parameter, no `location.hash` use, no `innerHTML`) | no user-controlled source reaches a sink; form note uses `textContent` | Aucun point d'injection dans le script du site |
| PT-XSS-02 | Reflected input | append `?q=<script>`, `#<img onerror>`, encoded payloads to every page and to the 404 | nothing reflected; the 404 page does not echo the requested path | Le site ne renvoie jamais ce qu'on tape dans l'adresse |
| PT-XSS-03 | Form relay | submit `[TEST]` messages containing HTML / script in each field | the e-mail received shows the payload as text; no execution in the mailbox; headers not injectable (CRLF in name / e-mail rejected) | Un message piégé arrive inoffensif dans la boîte |
| PT-INPUT-01 | Input validation (WSTG-INPV) | injection sweep on **each** of the four form fields, one field at a time: SQL payloads (`' OR 1=1--`, `"; DROP TABLE`, `1; SELECT`), script payloads (`<script>`, `<img onerror>`, event handlers), CRLF / header injection (`%0d%0aBcc:`), template / expression payloads (`{{7*7}}`, `${7*7}`), oversized input (beyond `maxlength`, and a direct POST bypassing the browser cap), control and unicode characters; at most 5 `[TEST]`-marked submissions actually sent | the page never executes or interprets any payload (static site, no database: SQL has nothing to reach - documented); the browser blocks over-length and malformed e-mail input; a direct POST with oversized or malicious content is accepted or rejected **by Web3Forms** but in every case reaches the mailbox as inert text, never executed, headers not injectable; the site itself stores and evaluates nothing | Tout ce qu'on peut taper dans les champs (code SQL, script, contenu piégé ou démesuré) reste du texte inoffensif : le site n'a pas de base de données à attaquer, la page n'exécute rien, et le message arrive neutralisé dans la boîte |
| PT-FORM-04 | Bot / spam traps and key scraping | (a) tick the hidden `botcheck` honeypot and submit -> fake success, **no** Web3Forms request; (b) submit less than 4 s after page display (simulating an auto-fill bot) -> fake success, **no** request; (c) submit legitimately after 4 s with the honeypot untouched -> real request sent; (d) fetch the raw page source and confirm the key `72f439e6…` is absent, so it cannot be scraped and reused from another origin | Les pièges anti-robots fonctionnent : un envoi trop rapide ou déclenchant la case cachée fait croire au robot que c'est parti mais rien n'est envoyé ; un vrai visiteur passe normalement ; la clé du formulaire n'est pas récupérable dans le code source |
| PT-FORM-01 | Form abuse | honeypot check; Web3Forms domain restriction (key usable only from okilys.com) and spam filter settings; behaviour of the key when called from another origin (one request) | requests from another origin refused or flagged; honeypot effective; spam settings enabled in the Web3Forms dashboard | La clé publique du formulaire ne peut pas servir à envoyer du spam depuis ailleurs |
| PT-FORM-02 | Rate and quota | check the Web3Forms plan quota and what happens when exceeded (message to the visitor) | visitor gets the failure message with the fallback e-mail; the OKILYS address remains reachable | Si le quota est dépassé, le visiteur a quand même l'adresse e-mail |
| PT-FORM-03 | Privacy of submissions | data path visitor → Web3Forms → OKILYS mailbox; retention at Web3Forms; mention in the legal notice / privacy section | processor named, retention known, lawful basis stated (legitimate interest / consent) | Le traitement des messages est décrit dans les mentions légales |
| PT-LINK-01 | External links and new-tab links | every `target="_blank"` — external links **and** the internal product links to `ctms.html` / `etmf.html` added on 16/09/2026 — has `rel` containing `noopener` (and `noreferrer` for the product links); every external domain (LinkedIn, ctms.okilys.com, infrarch.fr, client sites, cnil.fr, github.com) resolves to the intended organisation over HTTPS; no typosquatted or expired domain | no reverse-tabnabbing from any new tab; no link to an expired domain that could be re-registered | Aucun lien ouvert dans un nouvel onglet ne peut manipuler la page d'origine ; aucun lien vers un domaine abandonné |
| PT-LINK-02 | Mixed content | no `http://` resource or link inside the pages | none | Aucun contenu non chiffré |
| PT-REDIR-01 | Open redirect | the 10 stubs use fixed targets; no parameter-driven redirect anywhere | none | Aucune redirection manipulable |
| PT-DNS-01 | Mail authentication | SPF (`v=spf1 include:spf.protection.outlook.com -all` observed), DMARC at `_dmarc.okilys.com` (none observed on 15/09/2026), DKIM selectors for Microsoft 365 | SPF `-all`; **DMARC published** (at least `p=quarantine; rua=`), DKIM enabled | Les e-mails « @okilys.com » ne peuvent pas être usurpés (DMARC à ajouter) |
| PT-DNS-02 | Zone hygiene | CAA record (`letsencrypt.org` for GitHub Pages), DNSSEC status, no wildcard, no dangling CNAME on `etmf`, `ctms`, `www`; registrar lock and 2FA at the registrar | no takeover possible; CAA present or decision recorded | Aucun sous-domaine abandonné, nom de domaine verrouillé |
| PT-DNS-03 | Sub-domain takeover | for each sub-domain with a CNAME: the target still belongs to OKILYS / provider and is claimed | none unclaimed | Aucun sous-domaine récupérable par un tiers |
| PT-CLICK-01 | Clickjacking | frame the site from another origin | GitHub Pages cannot send X-Frame-Options; static site with no authenticated action: risk Informational, recorded | Le site peut être encadré ailleurs : sans conséquence, à consigner |
| PT-PRIV-01 | Privacy | inspect requests, storage, cookies on every page family | no cookie, no localStorage, no third-party request except the form POST; legal notice consistent ("no cookie banner needed") | Aucun traceur, promesse de confidentialité tenue |
| PT-SUPPLY-01 | Supply chain | list every external dependency (Web3Forms endpoint only; no CDN, no analytics, no fonts service); GitHub Actions / Pages build settings; branch protection and 2FA on the GitHub organisation; who can push | minimal dependencies; 2FA enforced; only OKILYS accounts can publish | Seuls les comptes OKILYS peuvent publier ; aucune dépendance extérieure |
| PT-SUPPLY-02 | Publication integrity | verify that the live HTML equals the `main` branch (hash comparison on 5 pages) | identical | Ce qui est en ligne est bien ce qui est dans le dépôt |
| PT-404-01 | Error handling | malformed paths (`%00`, very long, unicode, `..%2f`) | custom 404, no stack trace, no path echo | Adresses tordues : page « introuvable » propre |

### 7.3 Tooling and evidence

| Tool | Use |
|---|---|
| Mozilla Observatory, securityheaders.com | headers and TLS overview |
| testssl.sh | transport details |
| OWASP ZAP (baseline, passive) | automated client-side and configuration findings on the 40 pages |
| gitleaks / trufflehog, `git log -p` grep | repository history |
| dig / nslookup, dnsdumpster, MXToolbox (SPF / DMARC / DKIM / CAA) | DNS |
| exiftool | image metadata |
| Browser devtools, Playwright | client-side review, storage, requests, payload sweep on the form (≤ 5 `[TEST]` submissions) |

Evidence: raw outputs, request / response pairs, screenshots, DNS records dump, repository scan report, retest results.

## 8. Execution plan and reporting

| Phase | When | Who | Output |
|---|---|---|---|
| 1. Automated set (UT-PAGE, UT-JS, IT-*) as scripts under `_notes/tests/` (not published) | now, then after every publication | assistant | dated run report `_notes/validation/spec-run-<date>.md` + `spec-baseline.json` for regression |
| 2. System tests (§6) on the live site | now, then the (R) subset after menu / CSS / JS changes | assistant for automation and audits; Lydie for the visitor journeys on her devices | protocol with screenshots, defect register |
| 3. Penetration test (§7) | now; after any change to the form, DNS or external links; yearly | assistant, with Lydie for the registrar / GitHub / Web3Forms dashboards (PT-FORM-01, PT-DNS-02, PT-SUPPLY-01 need her access) | findings, decisions recorded |
| 4. Compilation | after each run | assistant | one register for the site, compiled with the previous site runs (first run = baseline) and presented alongside the CTMS register in the same format |

Reporting format (identical to the CTMS runs): per case Id · Title · Preconditions · Steps · Expected · Actual · Pass / Fail / Blocked · Evidence · Date; defect register with `severity`, `defect`, `location`, `defect_fr`, `ref_fr`, `plain_fr`, `impact_fr`, and the Excel decision workbook with the "Action souhaitée" column for Lydie.

Test protocol template (one line per case): Id · Title · Preconditions · Steps · Expected · Actual · Pass / Fail · Evidence reference · Tester · Date · Defect id.

## 9. Open points to decide with OKILYS

- DMARC (and DKIM) for `okilys.com`: to publish at the DNS provider (PT-DNS-01) - the single most useful security action for a site whose purpose is to be contacted by e-mail.
- Content-Security-Policy and referrer policy as `<meta>` tags (PT-HDR-01): decide, then add to the 51 pages with a `?v=` bump if CSS / JS change.
- Web3Forms dashboard: confirm domain restriction and spam settings (PT-FORM-01), quota (PT-FORM-02), and mention Web3Forms as a processor in the legal notice (PT-FORM-03, ST-PAGE-06).
- Footer labels still showing the pre-13/09 menu wording on some pages (IT-NAV-03): align with the current menu (Accueil · À propos page · Contact).
- **CAA DNS record absent** (PT-DNS-02): recommendation to add a `CAA` record authorising `letsencrypt.org` (the authority GitHub Pages uses), so that no other authority can issue a certificate for okilys.com. Registrar access required.
- Magdalena's testimonial role (ST-PAGE-03) and the OKILYS field of action on the 5 product pages (ST-PAGE-01): content decisions still pending in `_notes/REPRISE-session.md`.
- Where to keep the site test scripts and reports: `_notes/tests/` and `_notes/validation/` (versioned, not published) is proposed.
