<!-- Ce fichier est versionne dans le depot pour suivre Lydie d un poste a l autre,
     mais le dossier commence par un souligne : GitHub Pages construit le site avec
     Jekyll, qui exclut de la publication tout dossier prefixe par « _ ».
     A verifier apres la premiere publication : https://www.okilys.com/_notes/REPRISE-session.md
     doit repondre 404. Si ce n est pas le cas, retirer le fichier du depot. -->
# Note de reprise — vitrine-okilys

*Rédigée le 2026-08-11, fin de session sur le PC portable. À coller dans la nouvelle session Claude du PC fixe.*

**Emplacement du dossier local (depuis le 12/09/2026)** : `C:\Users\lydie\Documents\Claude\Site Web OKILYS` (anciennement `vitrine-fusion-OKILYS` dans `Documents`). Sur le PC portable, relocaliser le dépôt dans GitHub Desktop (« Locate ») si besoin.

---

## Où en est le projet

Site vitrine OKILYS Life Science, statique (HTML/CSS/JS), publié par GitHub Pages sur **www.okilys.com**. Version française à la racine, version anglaise miroir dans `en/` — **toute modification doit être répercutée dans les deux**.

Le dépôt est à jour et poussé. Le site en ligne correspond au dernier commit.

### Ce qui a été fait dans cette session

**Référencement** — `robots.txt`, `sitemap.xml` bilingue (30 URLs), page `404.html`, adresses canoniques, liens entre versions FR/EN (hreflang), balises de partage social + image `og-image.jpg`, fiches Google (JSON-LD : Organization, Person, WebSite, FAQPage, BreadcrumbList, Service), titres et descriptions réécrits autour des rôles et des activités.

**Cohérence des textes** — audit complet, puis correction : 6 rôles clés (et non 7, le poste de Clinical Project Manager n'a pas été tenu), harmonisation des intitulés de rôles, page Réalisations passée au « nous », périmètre géographique aligné, 5 catégories d'essais assumées partout.

**Nouvelles pages** — `pratique-courante.html` et `inm.html` (+ `en/standard-of-care.html`, `en/npi.html`), sur le modèle des pages produits.

**Références** — mur de logos cliquables (11 sociétés), bloc « Parcours salarié, jusqu'en 2019 », 4 recommandations LinkedIn en anglais d'origine.

**Technique** — polices Manrope rapatriées (plus aucun appel à Google, donc aucun bandeau cookies nécessaire), alternance des fonds de section rétablie, portrait réduit d'un tiers, numéros de version sur les feuilles de style.

---

## Ce qui reste à faire

### 1. Champ d'action OKILYS sur les 5 pages produits
Les pages Médicament, Dispositif médical, Données, Pratique courante et INM se limitent aujourd'hui à : définition, parcours en infographie, liste « Cadres réglementaires ». **Toutes les mentions du champ d'action d'OKILYS en ont été retirées** — Lydie doit préciser, parcours par parcours, où OKILYS intervient. Un encadré sera ensuite ajouté sur le modèle de ceux des pages d'étape.

Un bloc détaillé « Trois cadres, un même essai » (nomenclature internationale ICH, Règlement UE 536/2014, loi Jardé) avait été écrit pour la page Médicament puis retiré, jugé trop détaillé. Il est archivé dans `_drafts/cadres-reglementaires-medicament-FR.html` et `-EN.html`.

### 2. Vérification expertises / rôles sur les 7 pages d'étapes
Contrôler que la liste « Ce que nous faisons à cette étape » correspond bien aux rôles décrits plus bas sur la même page.

### 3. Références réglementaires belges — ✅ vérifiées le 15/08/2026
Les quatre lois belges ont été confirmées en ligne (Moniteur belge / AFMPS / APD) : loi du 7 mai 2017 (essais cliniques de médicaments, application du règlement 536/2014, AFMPS point de contact national + Comité d'éthique agréé), loi du 22 décembre 2020 (dispositifs médicaux) + arrêté royal du 18 mai 2021 (investigations cliniques), loi du 7 mai 2004 (expérimentations sur la personne humaine — couvre interventionnel et non interventionnel, opt-out possible pour le non interventionnel), loi du 30 juillet 2018 (protection des données, application du RGPD, APD).
Les listes « Cadres réglementaires » des 5 pages produits (FR + EN) ont été enrichies à **4 zones : Monde / Union européenne / France / Belgique**, à partir du document de fond `_notes/produits-de-sante/produits-de-sante-et-recherche-clinique.md` (Monde/UE/France) et des vérifications ci-dessus (Belgique). Restent des formulations générales et non des avis juridiques : à relire une dernière fois par Lydie.

### 4. Google Search Console — ✅ FAIT le 20/08/2026
Propriété https://www.okilys.com/ validée (balise HTML posée sur les 31 pages, commit 079d434) et sitemap.xml envoyé — Google a répondu « Sitemap envoyé ». Reste à surveiller le rapport « Indexation des pages » d'ici 1 à 2 semaines. Bing Webmasters : ✅ fait le 20/08/2026 — propriété importée depuis Search Console, sitemap repris (30 pages). Référencement entièrement en place sur Google et Bing ; il ne reste qu'à surveiller les rapports d'indexation. Procédure d'origine conservée ci-dessous pour mémoire.

#### Procédure (archivée)
Le sitemap est en ligne et accessible mais **n'a jamais été déclaré à Google**. C'est l'action qui déclenche la prise en compte de tout le travail de référencement. Gratuit, une dizaine de minutes.

**a. Créer le compte** — `search.google.com/search-console`, connexion avec un compte Google durable (c'est lui qui recevra les alertes de Google sur le site).

**b. Déclarer le site** — choisir le type **« Préfixe de l'URL »** (colonne de droite) et saisir exactement `https://www.okilys.com/`
*L'autre option, « Domaine », couvre aussi okilys.com sans www mais exige d'ajouter un enregistrement DNS chez le fournisseur du nom de domaine. À préférer si ces accès sont disponibles.*

**c. Prouver la propriété** — choisir la méthode **« Balise HTML »**. Google affiche une ligne du type :
`<meta name="google-site-verification" content="AbC123...xyz" />`
→ **Coller cette ligne à Claude**, qui l'ajoute au `<head>` des pages. Publier, **puis seulement** revenir cliquer sur *Valider* dans Google. Ne pas fermer la page Google entre-temps, et ne pas valider avant publication : Google ne trouverait pas la balise.

**d. Déposer le plan du site** — menu de gauche, **Sitemaps**. Le champ est précédé de `https://www.okilys.com/`, il suffit d'y taper `sitemap.xml` puis *Envoyer*. Google doit répondre « Réussite » et annoncer une trentaine d'URL découvertes.

**Délais réels** : quelques heures pour la lecture du sitemap, quelques jours à deux semaines pour l'apparition des pages dans les résultats, 2 à 3 jours minimum avant que le rapport *Performances* affiche des chiffres (vide au début, c'est normal). Rapport à surveiller ensuite : **Indexation des pages**.

**Bonus, 2 minutes** : `bing.com/webmasters` propose d'importer la configuration depuis Search Console en un clic. Bing pèse peu en France mais alimente les réponses de plusieurs assistants d'IA.

### 5. Mission de Magdalena
Son témoignage affiche « Mission OKILYS » sans précision du rôle, contrairement aux trois autres. Lydie doit indiquer lequel.

---

## Décisions prises, à ne pas défaire

- **Six rôles clés**, pas sept. Le certificat Clinical Project Manager reste affiché — c'est une qualification, pas un poste tenu.
- **Les citations des recommandations restent en anglais d'origine**, y compris sur le site français. Traduire ferait dire à ces personnes des phrases qu'elles n'ont pas écrites.
- **Section Contact orientée candidature** : Lydie est candidate à un poste, elle ne développe plus une société de conseil.
- **Les logos et noms de sociétés** du mur de références : à ne pas transformer en « clients », la distinction avec le parcours salarié est volontaire.
- **La page INM assume l'absence d'expérience** sur ce champ. Ne pas la lisser.

---

## Conventions de travail

- **Committer et pousser automatiquement**, sans redemander. Messages de commit en français **sans accents** (cohérence avec l'historique). Ne jamais mettre de guillemets doubles dans un message passé en here-string PowerShell : PowerShell 5.1 casse la commande.
- **`git push` en ligne de commande échoue** sur le PC portable : le trousseau Windows ne contient qu'un jeton `api.github.com` posé par GitHub Desktop. Lydie publie avec le bouton Push de GitHub Desktop. À vérifier sur le PC fixe : si `git push` fonctionne, tant mieux.
- **Langage non technique.** Lydie n'est pas développeuse : dire ce que ça change avant de nommer la technique, bannir le jargon web (canonical, hreflang, JSON-LD, CLS…). Son vocabulaire métier — CTIS, ISO 14155, ARC, oversight, TMF — est le sien, l'utiliser normalement.
- **Après toute modification de CSS ou de JS**, incrémenter le `?v=` des liens vers `css/*.css` et `js/script.js` dans les 31 pages (format AAAAMMJJ). GitHub Pages renvoie `Cache-Control: max-age=600` : sans changement d'adresse, le navigateur ressert sa copie pendant 10 minutes et la modification semble ne pas être partie.
- **Ne rien laisser à la racine du dépôt** qui ne doive pas être publié : tout ce qui s'y trouve devient accessible sur okilys.com. Le dossier `_drafts/` est exclu de git et de la publication.

---

## Contenu de `_drafts/` (non transféré par git)

| Fichier | Quoi |
|---|---|
| `cadres-reglementaires-medicament-FR.html` / `-EN.html` | bloc « Trois cadres » retiré de la page Médicament |
| `Lydie PARSUS _ LinkedIn References.pdf` | export des 10 recommandations LinkedIn |
| `REPRISE-session.md` | ce document |

À copier manuellement si tu veux les retrouver sur l'autre poste. Le PDF est ré-exportable depuis LinkedIn à tout moment.

---

## Ajout du 16/08/2026 — photos de section et valeurs HOME

- **Photos** (toutes issues de « Photos Site Okilys », libres de droits Unsplash/Pexels/Pixabay, recadrées 21:9 et allégées dans `assets/images/sections/`) : `apropos.jpg` (succulente), `produits.jpg` (fleurs blanches), `expertises.jpg` (arbre lumière), `references.jpg` (enfants forêt), `contact.jpg` (gouttes sur feuille) + 5 alternatives `alt-*.jpg` non utilisées.
- **Quatre styles panachés, pas de voile bleu** (le gingko reste le seul bandeau voilé) : A = photo en vis-à-vis du texte (À propos) · B = bandeau naturel + carte-titre chevauchante (Références sur l'accueil ; bandeau de toutes les sous-pages : fleurs pour les 5 pages produits, arbre pour les 7 pages étapes) · C = photo en filigrane sous voile blanc 88 % (Contact) · D = vignette ronde à côté du titre (Produits de santé). Classes `.split`, `.band`/`.band--sub`/`.band__card`, `.wash`, `.thumb-head` dans fusion.css. L'ancre `#references` est maintenant sur le `div.band` : scrollspy et scroll-margin étendus à `.band[id]`.
- **Valeurs HOME** en 4 tuiles (`.home-values`) sous À propos, en remplacement de l'encadré pointillé (la phrase « santé des générations futures » est conservée sous les tuiles). Textes validés par Lydie : Humain / Objectivité / Maîtrise / Engagement — EN : Human / Objectivity / Mastery / Engagement (le mot HOME se lit dans les deux langues). Le H ne parle plus du bien-être des salariés mais de la finalité humaine ; O remplace Outsourcing ; E remplace Éco-responsable et insiste sur le chemin autant que le résultat.
- Les gabarits des pages étapes (scratchpad tpl-fr/tpl-en) intègrent le bandeau.

---

## Ajout du 12/09/2026 — OKILYS suite (barre produits) et page OKILYS CTMS

- **Barre « OKILYS suite »** au-dessus de l'en-tête sur les 31 pages, harmonisée avec la barre du CTMS (option 4 côté CTMS) : OKILYS website (courant, dégradé) · OKILYS CTMS (→ ctms.html) · OKILYS eTMF (badge à venir / coming soon) + phrase « Une suite d'outils pour conduire vos essais cliniques de A à Z ». Elle remplace l'ancienne topbar (phrase d'accroche + email) — l'email reste dans le pied de page et la section Contact. Styles `.suite-bar__*` dans fusion.css (copie de ceux du CTMS). Côté CTMS : labels de `core.suite_tools()` et marque de la barre alignés (consigne consignée dans le CLAUDE.md du projet CTMS).
- **Page produit `ctms.html` + `en/ctms.html`** : contenu repris de `Claude\CTMS Like\commercial\Okilys-CTMS-plaquette-FR.html` / `brochure-EN.html` (hero, pourquoi remplacer Excel, modules à la carte A1→K, 4 outils autonomes, sécurité/conformité, pour qui, comment ça se passe, offre). Habillage complet du site, JSON-LD SoftwareApplication, sitemap passé à 32 URLs. Accessible uniquement par la barre suite (pas d'entrée de menu — choix de Lydie, menu déjà chargé). CTA → index#contact ; accès client → https://ctms.okilys.com.
- **Pied de page** : « Basée secteur Dijon · Besançon · Lyon » → « Secteur Dijon · Besançon · Lyon » (EN : « Dijon · Besançon · Lyon area (France) »), aligné sur le footer du CTMS.
- Décision de Lydie (12/09/2026, même jour) : présentation en produits assumée. **Encart « OKILYS suite »** sur l'accueil (bandeau sombre `.suite-panel`, une carte par produit) et **page produit `etmf.html` + `en/etmf.html`** créée dès maintenant, clairement badgée « à venir » (contenu prospectif : dépôts automatiques, vérification humaine, complétude, revue ISF, TMF Reference Model, restitution ZIP — issu du module I du CTMS). Bouton eTMF de la barre suite cliquable sur toutes les pages. Sitemap : 34 URLs. Côté CTMS : URL par défaut de l'entrée eTMF de la barre = okilys.com/etmf.html.

## 2026-09-12 (session CTMS) — bouton de menu « OKILYS Suite », barre = passage entre les sites

- Consigne de Lydie : les boutons de la barre du haut servent à passer d'un site à l'autre (OKILYS website · OKILYS CTMS → https://ctms.okilys.com · OKILYS eTMF « à venir » sans lien), pas à ouvrir les pages descriptives. Sur toutes les pages (y compris ctms.html / etmf.html), « OKILYS website » est l'outil courant.
- Nouveau bouton de menu **« OKILYS Suite »** (pastille teal, distinct du reste du menu, classe `.nav__suite`, `.nav-item--suite`) avec sous-menu : « La suite : notre histoire » (`suite.html` / `en/suite.html`, page mère : genèse des outils à partir de l'expérience CTM, la suite, principes communs), « OKILYS CTMS » (`ctms.html`), « OKILYS eTMF » (`etmf.html`, badge à venir). Actif sur les trois pages.
- Menu sur une seule ligne : « Contactez-nous » → « Contact » (EN « Contact us » → « Contact »), bouton plus compact et rapproché du sélecteur de langue, tagline « Make People… » resserrée (letter-spacing 0.04em, 0.02em entre 1321 et 1500 px). Vérifié à 1366 px FR et EN.
- Accueil FR/EN : bouton « Comment ces outils sont nés → » sous les deux cartes de la suite. Sitemap : 36 URLs. Version des feuilles de style : `20260912c`. Non poussé : Lydie publie (git push).

## 12/09/2026 (soir) - pages produit CTMS / eTMF avec photos et icônes
- `ctms.html`, `etmf.html`, `en/ctms.html`, `en/etmf.html` : `<main>` régénéré par le script `site_product_pages.py` (scratchpad de la session CTMS) - contenu aligné sur OKILYS CTMS 1.20 ; photos et icônes dans `assets/images/suite/` (issues des dossiers Communication d'OKILYS sur X:) ; CSS ajouté en fin de `css/fusion.css` (`.product-*`, `.mod-card--ico`) ; version `?v=20260913a` sur toutes les pages. Ne pas mettre de tiret cadratin « — » dans les titres (police Agne sans ce glyphe).

## Ajout du 12/09/2026 (soir) — rubrique Actualités / Insights

- **Pages** `actualites.html` + `en/insights.html` (entrée de menu « Actualités » / « Insights » après Réalisations/Highlights sur toutes les pages, 404 comprise ; menu vérifié sur une ligne à 1366 px). 3 articles au lancement : lancement CTMS (#lancement-ctms / #ctms-launch), eTMF en préparation (#etmf-a-venir / #etmf-coming), nouveau site (#nouveau-site / #new-website). Sitemap : 38 URLs.
- **Diaporama accueil** (`.news-band`, entre le bandeau de chiffres et À propos) : glissement droite-gauche automatique (6,5 s), flèches, points, glissement tactile sur mobile, bouton teal « Lire l'actualité » vers l'ancre de l'article. Slides à mettre à jour à la main dans index.html / en/index.html quand on ajoute une actualité (garder les 3-4 dernières).
- **Procédure « nouvelle actualité »** (ex. nouveau contrat : courte présentation du client + pathologie) : 1) ajouter l'article en haut de actualites.html et en/insights.html avec une ancre ; 2) mettre à jour les slides du diaporama (FR+EN) ; 3) sitemap lastmod ; 4) publier ; 5) poster sur la page LinkedIn OKILYS avec le lien https://www.okilys.com/actualites.html#ancre.

## Ajout du 13/09/2026 — restructuration Accueil / À propos

- **Menu** : « À propos » (ancre accueil) devient **« Accueil »** (lien vers index.html) ; les entrées « Fondatrice » et « Références » sont remplacées par **« À propos »** → nouvelle page `a-propos.html` / `en/about.html` (l'ancien stub de redirection en/about.html est devenu la vraie page). Menu final : Accueil · Produits de santé · Expertises · Secteurs · Réalisations · Actualités · À propos · OKILYS Suite · Contact — identique FR/EN, vérifié sur une ligne à 1366 px, tagline forcée sur une ligne (white-space nowrap).
- **Page À propos** = sections Fondatrice + Références déplacées depuis l'accueil (l'accueil s'arrête maintenant à Secteurs puis Contact). Ancres conservées (#fondatrice, #references) : tous les liens du site mis à jour (nav, footers, 404, stubs fondatrice/presentation/en-founder, bouton de highlights, JSON-LD Person). Sitemap : 40 URLs.
