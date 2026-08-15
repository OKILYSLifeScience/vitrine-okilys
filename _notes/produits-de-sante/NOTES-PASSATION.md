# Notes de passation — dossier « Produits de santé »

*Dernière mise à jour : 11 août 2026 (session Claude Code, PC principal)*
*À lire en premier quand on reprend le travail depuis un autre PC ou une autre session.*

## Objectif du projet

Structurer, pour le **site web Okilys**, un contenu pédagogique qui :
1. définit et catégorise les produits de santé faisant l'objet d'études cliniques ;
2. décrit le parcours de recherche clinique de chacun ;
3. couvre trois cadres pour chaque catégorie : **international / européen / français**.

Ton attendu : non technique, expliquer l'effet avant la règle (voir mémoire `lydie-langage-non-technique`).

## Fichiers du dossier

| Fichier | Rôle | État |
|---|---|---|
| `produits-de-sante-et-recherche-clinique.md` | **Document de fond** — tout le contenu rédigé, structuré par catégorie, avec sources | Version 3, complète |
| `infographies-parcours.html` | Les **5 infographies** (SVG intégrés), une par catégorie — version pour publication artefact Claude | Version 1 |
| `infographies-parcours-standalone.html` | Même contenu, avec squelette HTML complet — **s'ouvre par double-clic** dans n'importe quel navigateur | Version 1 |
| `NOTES-PASSATION.md` | Ce fichier | — |

Lien artefact publié (privé, compte Lydie) : https://claude.ai/code/artifact/2c3dd9df-7a3a-47d5-8b81-36a27c02be06

## Décisions de structure prises (à ne pas défaire)

La structure retenue par Lydie est en **5 catégories**, dans cet ordre :

1. **Médicament** — avec un **encart dédié MTI / ATMP** (thérapies innovantes) à l'intérieur, pas une catégorie séparée.
2. **Dispositif médical, dont DMDIV** — le diagnostic in vitro est une sous-partie du DM.
3. **Produits d'origine humaine** — sang, tissus, cellules, organes ; insister sur la *qualification* (plasma fractionné → médicament ; cellules très manipulées → MTI).
4. **HPS** = recherches **hors produits de santé** (sens ANSM) : compléments alimentaires, cosmétiques, physiologie/nutrition/sport. Les compléments et cosmétiques sont rangés ici (et non plus en « produits frontières »).
5. **INM** = interventions non médicamenteuses (sens NPIS / HAS 2011) : APA, psychothérapies protocolisées, kiné, ETP…

Chaque catégorie suit le même gabarit : *définition → sous-catégories → parcours clinique → cadres monde / Europe / France*.

Points de contenu validés :
- Le vocabulaire « phases I-IV » est **réservé au médicament**. DM = pilote → pivot → PMCF ; DMDIV = études de performances (validité scientifique / analytique / clinique) ; HPS = études contrôlées ciblées ; INM = faisabilité → contrôlée → implémentation (NPIS Model).
- Panorama mondial en annexe : ICH/IMDRF/OMS = fond harmonisé ; ce qui varie = guichets (CTIS, IND/IDE, CTN…) et frontières de catégories (compléments : aliments en UE, PSN au Canada, dietary supplements USA ; quasi-drugs Japon…).

## Charte visuelle des infographies

- Une teinte par catégorie : médicament bleu `#2F6CB3` · MTI violet `#7A54BD` · DM vert-bleu `#0F7D70` · origine humaine rouge `#B34743` · HPS ambre `#A87A22` · INM vert `#4C8B50` (variantes plus claires en thème sombre).
- Lecture gauche → droite ; **l'étape colorée = le « sésame »** (AMM, marquage CE, allégation autorisée, référencement).
- Sous chaque schéma : 3 encadrés Monde / Europe / France.
- Les couleurs ne sont **pas encore alignées sur la charte Okilys** — à faire si intégration au site.

## Pistes ouvertes (non commencées)

- Découper le document en pages prêtes pour le site (une page par catégorie + page « qui protège les participants » + page « dans le monde »).
- Aligner les couleurs des infographies sur la charte du site vitrine-okilys.
- Éventuelle export PNG des schémas.
- Vérifier deux points de contenu si besoin de précision juridique : date d'application exacte du règlement SoHO 2024/1938 (indiquée : août 2027) ; libellé précis des catégories ANSM d'investigations DM (1, 2, 3, 4.1–4.4).

## Comment reprendre depuis l'autre PC

Ce dossier **n'est pas un dépôt git** : il faut le copier tel quel (clé USB, OneDrive, ou l'ajouter au dépôt vitrine-okilys). Une fois copié, ouvrir ce fichier puis le `.md` de fond ; Claude Code retrouvera le contexte grâce à ces notes et à sa mémoire (`okilys-produits-de-sante`).
