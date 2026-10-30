# Articles de la page Actualités / Insights

Un fichier Markdown **bilingue** par article. `py _tools/publish_article.py` régénère, à partir de tous les fichiers de ce dossier : la page de chaque article en FR et en EN, la liste de `actualites.html` / `en/insights.html` (avec les filtres par catégorie), le carrousel de l'accueil (3 dernières entrées) et le plan du site. Les trois cartes historiques de l'été 2026 (CTMS, eTMF, nouveau site) restent définies dans le générateur et n'ont pas de page.

Ce dossier commence par `_` : il n'est pas publié par GitHub Pages, mais il est versionné (comme `_notes/`).

## Format

```
slug: fin-de-mission-maat-pharma            # nom du fichier FR dans actualites/
slug_en: maat-pharma-end-of-assignment      # nom du fichier EN dans en/insights/
date: 2026-10-29                            # ISO ; sert au tri et à l'affichage
category: carnet                            # carnet | metier | outils | vie  (donne la couleur)
type: apprentissages                        # facultatif : fin-de-mission | apprentissages | offre | fond | reglementaire | outil | evenement | actualite  (donne l'icône)
linkedin: https://www.linkedin.com/posts/…  # lien du post LinkedIn correspondant (profil si inconnu)
title_fr: …                                 # ≤ 70 caractères une fois « | OKILYS » ajouté, sans tiret cadratin
title_en: …
description_fr: …                           # 70 à 160 caractères (Google)
description_en: …
excerpt_fr: …                               # chapeau de l'article, texte de la carte et du carrousel
excerpt_en: …
--- fr ---
Texte français : paragraphes séparés par une ligne vide, `## Sous-titre`, listes `- `, **gras**.
Blocs de structure (facultatifs, validés le 30/10/2026) : `::: contexte` … `:::` (épingle), `::: points` + liste `- ` (losanges),
`::: retenir` (ampoule, fond teinté), `::: resultat` (coche), `::: evenement` (calendrier), `::: conclusion` (flèche, liseré dégradé,
bouton « Parlons-en » vers la page Contact ajouté automatiquement) ; mots-clés anglais acceptés (context, insight, result, event).
--- en ---
English text, same conventions.
```

## Règles vérifiées par le générateur (il refuse sinon)

- Les deux langues dans le même fichier : jamais une page sans sa jumelle.
- `Lydie PARSUS` (nom en majuscules), `OKILYS` en majuscules, aucune adresse e-mail dans le texte.
- Pas de tiret cadratin dans les titres et sous-titres (la police Agne n'a pas ce glyphe).
- Catégories : `carnet` (Carnet de la fondatrice : missions, retours d'expérience, compétences, à la première personne), `metier` (Métier & réglementaire), `outils` (Outils OKILYS : CTMS, eTMF), `vie` (Vie d'OKILYS : site, événements, collaborations).

## Règles éditoriales du site (non vérifiables par script, à relire)

- Jamais de codes de modules du CTMS, jamais « OKILYS est une CRO », jamais de mention de freelance.okilys.com, OKILYS CTMS et eTMF toujours « à venir ».
- Sur une mission client : uniquement des informations publiques (intitulé, périmètre tel que sur LinkedIn et dans le CV, aire thérapeutique si le promoteur l'a communiquée). Jamais de nom d'étude, de chiffres, de contexte interne de l'entreprise.

## Publier

```
py _tools/publish_article.py --check     # valide les sources
py _tools/publish_article.py             # génère tout
py _notes/tests/site_audit.py --no-net   # audit du site (doit rester vert)
git add <fichiers de la section Actualites> ; git commit -F msg.txt ; git push   # jamais git add -A (depot partage)
```
