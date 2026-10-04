# Alerte Rupture Hebdomadaire — Workflow Requirements

> **Version rapide (test).** Ce document a été rédigé sans interview complète, à partir du rapport d'Analyze et d'hypothèses réalistes pour une enseigne de cosmétiques (magasins + site). Tout est **à vérifier** avec l'enseigne, en particulier les points marqués *(hypothèse)*.

## Goal

Chaque lundi, le workflow produit une **liste d'alerte d'une page**. Elle classe par risque les couples référence × lieu (magasin ou site) dont le stock sera épuisé avant l'arrivée de la marchandise de la prochaine commande. Elle commence par un rapport de contrôle des données. Le responsable des achats l'utilise pour avancer une commande, déclencher un transfert ou surveiller un produit avant la prochaine commande à date fixe (tous les 15 jours).

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Réduire les ruptures de stock pour soutenir l'objectif de +20 % de chiffre d'affaires |
| Desired Outcome | Le responsable des achats connaît chaque lundi les produits qui vont manquer avant la prochaine commande et peut agir avant la rupture ; les clients trouvent plus souvent en magasin et sur le site le produit qu'ils viennent chercher |
| Measure | Nombre de couples référence × lieu en rupture par semaine ; part des ruptures signalées dans une alerte avant de se produire |
| Baseline | Unknown — must measure before go-live |
| Target | *(hypothèse)* Au moins 80 % des ruptures signalées à l'avance ; nombre de ruptures hebdomadaires réduit de 30 % par rapport à la mesure de départ |
| Readable When | 8 semaines après la mise en service (4 cycles de commande de 15 jours) |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Alerte Rupture Hebdomadaire |
| Description | Repère chaque semaine les produits qui vont manquer avant la prochaine commande, en comparant les ventes réelles au stock et aux délais fournisseurs |
| Trigger | Chaque lundi matin, lancement manuel par le responsable des achats après dépôt des exports |
| Owner | Responsable des achats / approvisionnement *(hypothèse)* |
| Lens | Organizational |
| Definition Type | Step-Driven |
| Stakeholders | Responsable des achats (porteur), directeurs de magasin, responsable e-commerce, contrôle de gestion (export des données) |

---

## Steps Overview

1. Rassembler les fichiers — réunir les exports de ventes, de stock, les délais fournisseurs et la date de la prochaine commande
2. Contrôler les données — vérifier que les fichiers sont complets, utilisables et sans donnée personnelle
3. Calculer et classer — calculer la couverture de chaque couple référence × lieu et lui attribuer une catégorie de risque
4. Rédiger la liste d'alerte — produire la page d'alerte, rapport de contrôle en tête
5. Valider la liste — le responsable des achats relit et décide des actions

## Step Details

### Step 1 — Rassembler les fichiers
- **Goal:** Disposer, au même endroit, de toutes les données nécessaires au calcul de la semaine.
- **Inputs:** C1 (ventes magasins), C2 (ventes site), C3 (stock), C4 (délais fournisseurs), C6 (calendrier des commandes).
- **Outputs:** Un jeu de fichiers daté (date du calcul) transmis à l'étape 2.
- **External Action:** None (read-only).
- **Rules & Edge Cases:**
  - Les ventes couvrent exactement les 28 jours précédant la date du calcul.
  - Les ventes sont agrégées par référence et par lieu ; aucun export ligne à ligne de commandes.
  - Un fichier absent est signalé à l'étape 2 et n'est jamais remplacé par une estimation.
- **Context Needed:** C1, C2, C3, C4, C6
- **Role:** Contrôle de gestion ou responsable e-commerce (exports) ; responsable des achats (dépôt et lancement)

### Step 2 — Contrôler les données
- **Goal:** Garantir que le calcul repose sur des données complètes et sans donnée personnelle.
- **Inputs:** Jeu de fichiers de l'étape 1.
- **Outputs:** Un rapport de contrôle (nombre de références reçues par fichier, colonnes refusées, lignes incomplètes) et un tableau consolidé référence × lieu × ventes × stock × délai.
- **External Action:** None (read-only).
- **Rules & Edge Cases:**
  - Si une colonne identifie une personne (nom, e-mail, téléphone, adresse, numéro de commande individuel, identifiant de fidélité) : arrêt immédiat, nommer l'en-tête de colonne seulement, ne jamais recopier ses valeurs (G2).
  - Si un fichier de ventes est vide ou qu'une colonne obligatoire manque (`reference`, `lieu`, `quantite_vendue_28j`, `stock_disponible`) : arrêt, rapport de contrôle seul (G2).
  - Une référence présente dans les ventes mais absente du stock passe en catégorie « Données incomplètes ».
  - Une référence présente dans le stock mais absente des ventes est comptée avec 0 vente.
  - Le rapport compare le nombre de références reçues dans chaque fichier et signale les écarts.
- **Context Needed:** C1, C2, C3, C4
- **Role:** Workflow (IA)

### Step 3 — Calculer et classer
- **Goal:** Attribuer à chaque couple référence × lieu une seule catégorie de risque.
- **Inputs:** Tableau consolidé de l'étape 2 ; D (jours jusqu'à la prochaine commande, depuis C6) ; règles C5.
- **Outputs:** Tableau classé : référence, produit, lieu, stock, vente moyenne par jour, couverture en jours, délai fournisseur, date de rupture estimée, catégorie.
- **External Action:** None (read-only).
- **Rules & Edge Cases:**
  - Vente moyenne par jour = ventes 28 jours ÷ 28 ; couverture = stock ÷ vente moyenne par jour, arrondie à l'entier inférieur.
  - Les catégories et leur ordre de priorité sont ceux de C5, sans modification.
  - Un délai fournisseur manquant donne la catégorie « Délai fournisseur inconnu » ; aucun délai n'est supposé.
  - Aucune vente sur 28 jours donne la catégorie « Pas d'historique de vente » ; aucune couverture n'est calculée.
- **Context Needed:** C4, C5, C6
- **Role:** Workflow (IA)

### Step 4 — Rédiger la liste d'alerte
- **Goal:** Présenter le résultat sur une page lisible en moins de 5 minutes.
- **Inputs:** Tableau classé de l'étape 3 ; rapport de contrôle de l'étape 2.
- **Outputs:** Liste d'alerte en Markdown : rapport de contrôle, puis un tableau par catégorie dans l'ordre de C5, puis le nombre de références « Sans risque ».
- **External Action:** None (read-only) — le fichier est produit dans `outputs/alerte-rupture-hebdomadaire/runs/`.
- **Rules & Edge Cases:**
  - Une catégorie vide affiche « Aucune référence ».
  - Les références « Sans risque » sont seulement comptées, pas listées.
  - Rédaction en français, sans jargon.
- **Context Needed:** C5
- **Role:** Workflow (IA)

### Step 5 — Valider la liste
- **Goal:** Transformer l'alerte en décisions humaines.
- **Inputs:** Liste d'alerte de l'étape 4.
- **Outputs:** Liste validée, annotée d'une action par ligne (avancer la commande, transfert, surveiller, ignorer).
- **External Action:** None — toute commande ou tout contact fournisseur se fait hors du workflow.
- **Rules & Edge Cases:**
  - Le workflow s'arrête à la présentation de la liste ; il n'agit pas sur la décision.
- **Context Needed:** —
- **Role:** Responsable des achats (G1)

## Sequence

- **Sequential steps:** 1 → 2 → 3 → 4 → 5
- **Parallel steps:** Au sein de l'étape 1, les exports C1, C2 et C3 sont produits en parallèle.
- **Critical path:** 1 → 2 → 3 → 4 → 5
- **Role swimlane:** Contrôle de gestion / e-commerce (étape 1, exports) → Workflow IA (étapes 2 à 4) → Responsable des achats (étape 5)

---

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Export des ventes magasins (28 jours) | 1, 2 | Exists *(hypothèse)* | Confidential | Authored | Partial | Logiciel de caisse — export manuel CSV vers `data/` | Référence, produit, magasin, quantité vendue sur 28 jours |
| C2 | Export des ventes du site (28 jours) | 1, 2 | Exists *(hypothèse)* | Confidential | Authored | Partial | Back-office du site — export manuel CSV vers `data/` | Référence, produit, « Site », quantité vendue sur 28 jours |
| C3 | État du stock par référence et par lieu | 1, 2 | Exists *(hypothèse)* | Internal | Authored | Partial | Logiciel de gestion de stock — export manuel CSV vers `data/` | Référence, lieu, stock disponible |
| C4 | Table des délais fournisseurs | 1, 2, 3 | Needs Creation | Internal | Authored | No | Create as `data/delais-fournisseurs.csv` | Référence, fournisseur, délai de livraison en jours |
| C5 | Règles de classement | 3, 4 | Exists | Internal | Authored | Yes | `outputs/alerte-rupture-hebdomadaire/context/C5-regles-classement.md` | Formules, catégories, ordre d'affichage |
| C6 | Calendrier des commandes à date fixe | 1, 3 | Needs Creation | Internal | Authored | No | Create as `data/calendrier-commandes.csv` | Dates des prochaines commandes (tous les 15 jours) |

Notes de préparation des données (pour Design) :
- C1, C2 et C3 demandent aujourd'hui un export manuel ; leur format exact (noms de colonnes, séparateur) est à confirmer avec l'enseigne.
- C4 se trouve aujourd'hui dans la tête des acheteurs ou dans les conditions fournisseurs. Il faut le rédiger une fois, puis le tenir à jour.
- C5 est une hypothèse de test ; les seuils sont à valider par le responsable des achats.

## Acceptance Criteria

1. **AC1 (must)** — Chaque couple référence × lieu reçu apparaît dans exactement une catégorie, ou est compté dans « Sans risque » ; aucun ne disparaît.
2. **AC2 (must)** — La couverture et la catégorie de chaque ligne correspondent au calcul fait à la main avec les formules de C5.
3. **AC3** — Le rapport de contrôle figure en tête et indique le nombre de références reçues par fichier et les anomalies détectées.
4. **AC4** — Chaque ligne listée affiche la référence, le produit, le lieu, le stock, la vente moyenne par jour, la couverture, le délai fournisseur et la date de rupture estimée (ou « — » quand elle n'a pas de sens).
5. **AC5** — Les catégories apparaissent dans l'ordre de C5, et les lignes sont triées par couverture croissante dans chaque catégorie.
6. **AC6** — La liste tient sur une page imprimée.
7. **AC7** — La sortie ne contient aucune valeur issue d'une colonne qui identifie une personne.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Export réel de la semaine (real) | `outputs/alerte-rupture-hebdomadaire/inputs/E1-export-reel-semaine.md` — export réel de l'enseigne, à coller avant l'étape 5 | Liste complète et juste sur des données réelles ; tests AC1, AC2, AC3, AC6 | — |
| E2 | Semaine typique (proposed) | `outputs/alerte-rupture-hebdomadaire/inputs/E2-semaine-typique.md` — 8 références, 2 magasins + site, tous les délais connus, D = 9 | Déjà en rupture : R002. Rupture imminente, dans l'ordre : R008 (4 j, 09/10), R001 (5 j, 10/10), R007 (10 j, 15/10). À surveiller : R003 et R005 (20 j). Sans risque : 2 (R004, R006) ; tests AC1, AC2, AC4, AC5 | — |
| E3 | Données trouées (proposed) | `outputs/alerte-rupture-hebdomadaire/inputs/E3-donnees-trouees.md` — délai manquant, nouveauté sans vente, référence absente du stock, référence absente des ventes | Déjà en rupture : R103. Délai fournisseur inconnu : R101 (couverture 6 j, aucun délai inventé). Pas d'historique : R102, R104. Données incomplètes : R105 (absente du stock) ; tests R2 and the Step 2 missing-reference edge cases | — |
| E4 | Fichier inutilisable (proposed) | `outputs/alerte-rupture-hebdomadaire/inputs/E4-fichier-incomplet.md` — ventes du site vides, colonne `lieu` absente du stock | Le workflow s'arrête après le rapport de contrôle, nomme les deux problèmes et ne produit aucune liste ; tests R6, G2 | — |
| E5 | Données clients dans l'export (proposed) | `outputs/alerte-rupture-hebdomadaire/inputs/E5-donnees-clients.md` — export brut avec `numero_commande` et `email_client` | Le workflow s'arrête, nomme uniquement les en-têtes `numero_commande` et `email_client`, ne recopie aucune valeur ; tests R3, AC7, G2 | — |

## Rules & Constraints

| ID | Type | Rule |
|---|---|---|
| R1 | Must do | Placer le rapport de contrôle en tête de chaque sortie, y compris quand le workflow s'arrête |
| R2 | Must never do | Inventer un délai fournisseur, un seuil, une date de commande ou une vente manquante |
| R3 | Must never do | Recopier la valeur d'une colonne qui identifie une personne ; seul l'en-tête est cité |
| R4 | Scope | Le workflow signale les risques de rupture ; il ne calcule pas de quantité à commander et ne fait pas de prévision liée aux promotions (workflows distincts) |
| R5 | Tone / format / length | Une page en français ; un tableau par catégorie ; colonnes de AC4 ; dates au format JJ/MM |
| R6 | Fallback | Fichier manquant, vide, colonne obligatoire absente ou donnée personnelle : arrêt et retour au responsable des achats (G2). Ligne isolée incomplète : classement en « Données incomplètes » et signalement dans le rapport de contrôle |

## Human Gates

| ID | Where | What requires human input |
|---|---|---|
| G1 | Step 5 | Le responsable des achats valide la liste et décide d'une action par ligne |
| G2 | Step 2 | En cas d'arrêt du contrôle (fichier inutilisable ou donnée personnelle), le responsable des achats fournit un export corrigé avant toute reprise |

## Security, Privacy & Safety

*Scope: handles data you would be uncomfortable seeing outside the company (C1, C2 : chiffres de ventes confidentiels). Read-only ; aucun contenu externe.*

### Boundaries
| Constraint | Source |
|---|---|
| Le workflow ne reçoit que des ventes agrégées par référence et par lieu ; aucun export contenant des données clients | Self *(hypothèse)* — principe de minimisation du RGPD |
| Aucune donnée réelle de l'enseigne n'est déposée dans un dépôt public ; pour le projet de cours, seules des données fictives ou anonymisées sont utilisées | `data/README.md` du dépôt |

### Access
| Constraint | Source |
|---|---|
| La liste d'alerte et les fichiers intermédiaires sont réservés au responsable des achats, aux directeurs de magasin, au responsable e-commerce et à la direction | Self *(hypothèse)* |

### Prohibited actions
| Constraint | Source |
|---|---|
| Ne jamais contacter un fournisseur | Self *(hypothèse)* |
| Ne jamais passer, modifier ou annuler une commande | Self *(hypothèse)* |
| Ne jamais modifier les fichiers sources (C1 à C4, C6) | Self *(hypothèse)* |

### Governing regime
None — aucune donnée personnelle n'est traitée. Les exports contenant des données clients sont refusés à l'étape 2, conformément au RGPD.

## Optimization Notes

- **Ajouté :** l'étape 2 (Contrôler les données). Le processus humain actuel ne contrôle rien ; l'IA a besoin d'une vérification explicite des données personnelles et des lignes manquantes.
- **Fusionné :** calcul de la vente moyenne, calcul de la couverture et comparaison au délai fournisseur ne forment plus qu'une seule étape (Step 3). L'IA les fait en un seul passage, là où un humain les ferait colonne par colonne dans Excel.
- **Fusionné :** la consolidation des ventes magasins et site se fait dans l'étape 2, sans fichier intermédiaire préparé à la main.
- **En parallèle :** les trois exports de l'étape 1 n'ont pas de dépendance entre eux.
- **Conservé :** la validation humaine (G1). La liste déclenche des décisions d'achat qui engagent de l'argent.
- **Hors périmètre, gardé pour plus tard :** la proposition de quantités à commander (opportunité 3 du rapport d'Analyze). Elle s'appuiera sur la sortie de ce workflow.
