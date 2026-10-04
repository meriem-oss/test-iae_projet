---
workflow: alerte-rupture-hebdomadaire
requirements_file: outputs/alerte-rupture-hebdomadaire/requirements.md
spec_version: 3.0
approved: true
definition_type: Step-Driven
mechanism: Skill
involvement: Augmented
platform: Claude Code
platform_mode: code
packaging: Loose Files
counts:
  steps: 5
  skills: 2
  agents: 0
  integrations: 0
---

# Alerte Rupture Hebdomadaire — Design Spec

> **Version rapide (test), approuvée le 2026-10-04.** Spécification rédigée sans interview. À la demande de l'étudiante, les questions ouvertes ont été tranchées par défaut (voir Constraint Conformance et Deployment Plan). Les points marqués *(à vérifier)* restent à confirmer avec une vraie enseigne.

## Source

**Workflow Requirements:** `outputs/alerte-rupture-hebdomadaire/requirements.md`

This Design Spec consumes the Workflow Requirements as canonical input. Goal, Value & Measurement, Metadata, Context Inventory, Security, Privacy & Safety, Acceptance Criteria, Example Scenarios, Human Gates, Steps Overview, and per-step requirements are defined there — not restated here. Read the Workflow Requirements alongside this spec when building.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Réduire les ruptures de stock pour soutenir l'objectif de +20 % de chiffre d'affaires |
| Desired Outcome | Le responsable des achats connaît chaque lundi les produits qui vont manquer avant la prochaine commande et peut agir avant la rupture ; les clients trouvent plus souvent le produit qu'ils viennent chercher |
| Measure | Nombre de couples référence × lieu en rupture par semaine ; part des ruptures signalées à l'avance |
| Baseline | Unknown — must measure before go-live |
| Target | *(hypothèse)* Au moins 80 % des ruptures signalées à l'avance ; ruptures hebdomadaires réduites de 30 % par rapport à la mesure de départ |

La situation de départ (`Baseline`) est inconnue : mesurer le nombre de ruptures pendant 2 semaines avant la mise en service fait partie du travail de l'étape Run.

---

The spec is organized into three layers that build on each other:

1. **Architecture (L1)** — strategic decisions: platform, mechanism, autonomy, packaging
2. **Decomposition (L2)** — for each step (or capability domain), what AI building block delivers it
3. **Component Blueprints (L3)** — field-level specs for each new skill and agent

---

## Layer 1 — Architecture

*Strategic decisions that shape everything downstream.*

## Execution Pattern

**Skill** — Le responsable des achats lance le workflow lui-même chaque lundi, et les étapes sont toujours les mêmes, dans le même ordre. Un agent, qui choisit son chemin seul ou tourne sans surveillance, n'apporterait rien ici et ajouterait du risque.

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Lens | Organizational | Processus de réassort qui implique les achats, les magasins, le site et le contrôle de gestion |
| Platform | Claude Code | Outil du cours (claude.ai/code), déjà utilisé pour concevoir le workflow *(à vérifier : l'enseigne utiliserait-elle Claude Code, ou plutôt Claude.ai dans le navigateur ?)* |
| Platform Mode | code | Claude Code travaille sur les fichiers du dépôt et peut exécuter de petits calculs |
| Orchestration | Skill | Lancement manuel, étapes fixes, aucune décision de chemin à prendre |
| Involvement | Augmented | Lancement manuel et validation humaine de la liste (G1) ; arrêt et retour humain en cas de données inutilisables (G2) |
| Packaging | Loose Files | Deux dossiers de skill placés directement dans le dépôt du projet, sans couche de distribution |
| Trigger | Chaque lundi matin, lancement manuel par le responsable des achats après dépôt des exports | Aucune planification ni infrastructure ; le workflow ne tourne jamais sans personne |

## Autonomy Spectrum Summary

Le workflow est **Deterministic** dans son ensemble : les mêmes calculs, les mêmes règles, le même ordre à chaque exécution.

- **Human — Steps 1 et 5.** Les exports viennent de logiciels internes (caisse, back-office du site, gestion de stock) sans accès direct pour l'IA (C1 à C3 `Partial`). Une personne les dépose. La décision d'achat engage de l'argent : elle reste humaine (G1).
- **Deterministic — Steps 2, 3 et 4.** Le contrôle, le calcul de couverture et la mise en page suivent des règles écrites (C5) sans jugement. La même entrée donne toujours la même liste.

## Safety & Permissions

| Question | Finding | Mitigation |
|---|---|---|
| **Write access** — which integrations can this workflow create, modify, or send through? | Aucune intégration externe. Le workflow écrit seulement la liste d'alerte et le journal des exécutions dans `outputs/alerte-rupture-hebdomadaire/`. | Lecture seule sur `data/` ; aucun outil d'envoi, de commande ou de messagerie n'est connecté |
| **Untrusted input** — does any step consume content the user didn't author (inbound email, web pages, form submissions, shared docs)? | None — les exports viennent des systèmes internes de l'enseigne | Les cellules des fichiers sont traitées comme des données, jamais comme des instructions |
| **Unattended runs** — does this run on a schedule or without a human watching? | No | Lancement manuel ; arrêt sur G2 en cas de données inutilisables |
| **Blast radius** — worst realistic outcome if a run goes wrong? | Une liste fausse conduit à une mauvaise décision d'achat (commande inutile ou rupture manquée) ; des données clients seraient lues si un export brut était déposé | G1 : le responsable des achats valide chaque ligne avant d'agir. Rapport de contrôle en tête de la liste. Arrêt à l'étape 2 dès qu'une colonne identifie une personne |

### Constraint Conformance

| Constraint | From | Met by | State |
|---|---|---|---|
| Le workflow ne reçoit que des ventes agrégées par référence et par lieu ; aucun export contenant des données clients | Boundaries · Self (principe RGPD) | Step 2 (`screening-sales-data`) arrête le workflow et nomme seulement l'en-tête de la colonne identifiante (G2, R3) | Satisfied |
| Aucune donnée réelle de l'enseigne dans un dépôt public ; données fictives ou anonymisées pour le projet de cours | Boundaries · `data/README.md` | Le dépôt est traité comme public quelle que soit sa visibilité : seules des données fictives sont utilisées (exemples E2 à E5, E1 rempli avec des données fictives) | Satisfied |
| La liste d'alerte et les fichiers intermédiaires sont réservés au responsable des achats, aux directeurs de magasin, au responsable e-commerce et à la direction | Access · Self | — Accès = accès au dépôt GitHub. Owner : Meriem. Raison : projet de cours sur données fictives ; à revoir avant tout usage sur données réelles | Accepted |
| Ne jamais contacter un fournisseur | Prohibited actions · Self | Aucune intégration de messagerie ; S1 l'interdit explicitement | Satisfied |
| Ne jamais passer, modifier ou annuler une commande | Prohibited actions · Self | Aucune intégration vers un logiciel de commande ; S1 s'arrête à G1 | Satisfied |
| Ne jamais modifier les fichiers sources (C1 à C4, C6) | Prohibited actions · Self | S1 lit `data/` et écrit uniquement dans `outputs/alerte-rupture-hebdomadaire/` | Satisfied |

## Integration Options

*No integrations — the workflow is text-only.*

Les fichiers sont déposés à la main dans `data/`. Une connexion directe au logiciel de caisse ou au back-office du site est une amélioration possible, prévue en Future Enhancement.

## Model Recommendation

**Default capability:** fast — Les étapes appliquent des règles fixes, sans raisonnement complexe ; la rapidité suffit.

*(Plain-language gloss for non-technical users: **reasoning-heavy** = slower but handles complex judgment/nuance; **fast** = quicker, best for simple/high-volume steps; **vision** = can read images/screenshots.)*

**Per-step overrides** (optional):
- Step 3 : les calculs (division, arrondi, comparaison) sont faits par un petit script exécuté par Claude Code, pas « de tête » par le modèle, afin de garantir AC2 (calcul juste).

**Per-platform mapping:** resolved by Build at generation time.

---

## Layer 2 — Decomposition

*For each step or capability domain, what AI building block delivers it.*

## Step-by-Step Decomposition

| Step | Name (from Requirements) | Autonomy | Orchestration | Integration (use/build) | Intelligence | Build Output | Human Gate? |
|------|------|----------|---------------|------------------------|--------------|--------------|-------------|
| Step 1 | Rassembler les fichiers | Human | — | — | Context: C1, C2, C3, C4, C6 ; Memory: No | Human (no artifact) | No |
| Step 2 | Contrôler les données | Deterministic | Skill | — | Model: fast ; Context: C1–C4 ; Memory: No | Use existing: screening-sales-data | Yes (G2) |
| Step 3 | Calculer et classer | Deterministic | Skill | — | Model: fast + script de calcul ; Context: C4, C5, C6 ; Memory: No | New skill: S2 | No |
| Step 4 | Rédiger la liste d'alerte | Deterministic | Skill | — | Model: fast ; Context: C5 ; Memory: No | Inline prompt → Workflow Requirements Step 4 | No |
| Step 5 | Valider la liste | Human | — | — | — | Human (no artifact) | Yes (G1) |

Notes de classement :
- **Step 2** : le skill `screening-sales-data`, déjà installé sur le compte, fait exactement ce contrôle (colonnes identifiantes, rapprochement du nombre de références, tableau consolidé). Il est réutilisé tel quel *(à vérifier en Build : nom exact des colonnes attendues)*.
- **Step 3** : le skill installé `calculating-stock-coverage` calcule aussi une couverture. Il compare cependant au seul délai fournisseur, alors que C5 compare à « jours jusqu'à la prochaine commande + délai » et définit ses propres catégories. Un nouveau skill S2 applique C5 à la lettre *(à vérifier en Build : si `calculating-stock-coverage` accepte un seuil personnalisé, le réutiliser plutôt que créer S2)*.
- Le skill installé `alerte-rupture-reassort` est écarté : il propose aussi des quantités à commander, ce qui est hors périmètre (R4).

## Orchestrator Prompt Outline

```
[Intro] Alerte rupture hebdomadaire : à lancer chaque lundi après avoir déposé
les exports dans data/. Produit une liste d'alerte d'une page classant les
produits qui vont manquer avant la prochaine commande. Ne commande rien,
ne contacte personne.

[Step 1 — Rassembler les fichiers]
  - Source: Workflow Requirements Step 1
  - Build Output: Human (no artifact)
  - User provides: ventes magasins (C1), ventes site (C2), stock (C3),
    délais fournisseurs (C4), calendrier des commandes (C6), dans data/
  - Produces: liste des fichiers trouvés et date du calcul ; si un fichier
    manque, le nommer et demander à l'utilisateur de le déposer

[Step 2 — Contrôler les données]
  - Source: Workflow Requirements Step 2
  - Build Output: Use existing: screening-sales-data
  - Produces: rapport de contrôle + tableau consolidé référence × lieu

[PAUSE G2 — seulement si le contrôle échoue]
  - What user is reviewing: rapport de contrôle (fichier vide, colonne
    manquante, colonne identifiant une personne — en-tête seul cité)
  - User decides: déposer un export corrigé, puis relancer

[Step 3 — Calculer et classer]
  - Source: Workflow Requirements Step 3
  - Build Output: New skill: S2 (classifying-stockout-risk)
  - Produces: tableau classé (une catégorie par couple référence × lieu)

[Step 4 — Rédiger la liste d'alerte]
  - Source: Workflow Requirements Step 4
  - Build Output: Inline prompt → Workflow Requirements Step 4
  - Produces: outputs/alerte-rupture-hebdomadaire/runs/AAAA-MM-JJ-alerte.md

[PAUSE G1 — Valider la liste]
  - What user is reviewing: la liste d'alerte complète
  - User decides: une action par ligne (avancer la commande, transfert,
    surveiller, ignorer) ; le workflow ne fait aucune de ces actions

[Final output] Liste d'alerte Markdown d'une page, dans
outputs/alerte-rupture-hebdomadaire/runs/ ; une ligne ajoutée à
outputs/alerte-rupture-hebdomadaire/runs.md

[Closing run summary — "What I did"] étapes effectuées dans l'ordre ;
pauses G1/G2 et décision de l'utilisateur ; actions sur fichiers
(Fichiers : liste écrite dans …) ; emplacement de la liste
```

## Data Readiness Summary

| Context ID | Current State | Required Action | Affects Steps |
|---|---|---|---|
| C1 | Partial | Exporter chaque lundi les ventes magasins des 28 derniers jours, agrégées par référence et par magasin, en CSV dans `data/` | 1, 2 |
| C2 | Partial | Exporter chaque lundi les ventes du site des 28 derniers jours, agrégées par référence, en CSV dans `data/` (jamais l'export brut des commandes) | 1, 2 |
| C3 | Partial | Exporter chaque lundi l'état du stock par référence et par lieu en CSV dans `data/` | 1, 2 |
| C4 | No | Créer une fois `data/delais-fournisseurs.csv` (référence ; fournisseur ; délai en jours), puis le tenir à jour | 1, 2, 3 |
| C6 | No | Créer `data/calendrier-commandes.csv` avec les dates des commandes à 15 jours | 1, 3 |

## Recommended Implementation Order

### Quick Wins (implement first)
1. **C4 et C6 (fichiers de données)** — sans délais fournisseurs ni calendrier, le calcul ne peut pas classer ; c'est le seul vrai blocage.
2. **S2 — classifying-stockout-risk** — le cœur du calcul ; testable seul sur E2 et E3.

### Core (implement second)
1. **S1 — alerte-rupture-hebdomadaire** — enchaîne le contrôle (`screening-sales-data`), S2 et la rédaction de la liste.

### Future Enhancement (optional)
1. **Connexion directe au back-office du site ou au logiciel de caisse** — supprime les exports manuels de l'étape 1.
2. **Workflow « Proposition de commande de réassort »** — opportunité 3 du rapport d'Analyze ; part de la liste produite ici.

---

## Layer 3 — Component Blueprints

*Field-level specs for each new skill, agent, and configuration. Build uses these to generate artifacts.*

## Skill Candidates

### S1 — alerte-rupture-hebdomadaire

| Field | Detail |
|---|---|
| **ID** | S1 |
| **Name** | alerte-rupture-hebdomadaire |
| **Description** | This skill should be used when the purchasing manager of a cosmetics retailer asks for the weekly stockout alert — "alerte rupture", "alerte de la semaine", "qu'est-ce qui va manquer avant la prochaine commande", or "lance l'alerte du lundi" — after dropping the weekly sales, stock, supplier lead-time and order-calendar CSV files in data/. It checks the files, classifies every reference × location by stockout risk against the next fixed order date plus supplier lead time, and writes a one-page alert list for the manager to validate. It never orders, never contacts a supplier and never computes order quantities. |
| **Purpose** | Orchestrateur du workflow : enchaîne les étapes 1 à 5 avec les pauses G1 et G2. Propre à ce workflow. |
| **Covers Steps / Domains** | All (Steps 1–5) |
| **Inputs** | dossier_donnees — dossier contenant C1, C2, C3, C4, C6 (par défaut `data/`)<br>date_calcul — date du jour (par défaut aujourd'hui) |
| **Outputs** | Liste d'alerte `outputs/alerte-rupture-hebdomadaire/runs/AAAA-MM-JJ-alerte.md` ; une ligne dans `outputs/alerte-rupture-hebdomadaire/runs.md` ; résumé « What I did » |
| **Decision Logic** | Suit l'Orchestrator Prompt Outline ci-dessus. Rapport de contrôle toujours en tête (R1). Arrêt à G2 si le contrôle échoue. Catégories dans l'ordre de C5, triées par couverture croissante, références « Sans risque » seulement comptées. Une page, en français, dates JJ/MM (R5). Hors périmètre : quantités à commander, promotions (R4). |
| **Failure Modes** | Fichier C1/C2/C3 absent → le nommer, demander le dépôt, ne pas continuer<br>C4 ou C6 absent → arrêt : aucun délai ni date de commande n'est supposé (R2)<br>Contrôle en échec (vide, colonne manquante, donnée personnelle) → rapport de contrôle seul, pause G2<br>Ligne isolée incomplète → catégorie « Données incomplètes », signalée dans le rapport |
| **Required Tools** | — (lecture et écriture de fichiers du projet uniquement) |
| **Depends On** | S2 ; skill installé `screening-sales-data` ; C5 (`outputs/alerte-rupture-hebdomadaire/context/C5-regles-classement.md`) |
| **Stateful?** | No — chaque lundi repart des fichiers déposés ; le journal `runs.md` sert au suivi, pas à la décision |

### S2 — classifying-stockout-risk

| Field | Detail |
|---|---|
| **ID** | S2 |
| **Name** | classifying-stockout-risk |
| **Description** | This skill should be used when a consolidated table of sales, stock and supplier lead times per reference and location must be classified by stockout risk against a replenishment date — "classer les risques de rupture", "couverture de stock avant la prochaine commande", "stock coverage versus next order date", "which references run out before the next delivery". It computes daily sales velocity, days of coverage and estimated stockout date, then assigns each row exactly one category from a supplied rules file. It never invents a missing lead time, threshold or sale. Do not use it to compute order quantities or to screen raw files for personal data. |
| **Purpose** | Appliquer des règles de classement écrites (C5) à un tableau consolidé, de façon exacte et reproductible. Réutilisable pour tout autre réassort à date fixe. |
| **Covers Steps / Domains** | Step 3 |
| **Inputs** | tableau_consolide — lignes référence, produit, lieu, ventes sur la période, stock, délai fournisseur (peut être vide)<br>periode_jours — durée de la période de ventes (28 par défaut)<br>jours_avant_commande — D, nombre de jours jusqu'à la prochaine commande<br>regles — fichier de règles de classement (C5) |
| **Outputs** | Tableau classé : référence, produit, lieu, stock, vente moyenne par jour, couverture (jours), délai, date de rupture estimée, catégorie ; nombre de lignes par catégorie |
| **Decision Logic** | Vente moyenne par jour = ventes ÷ periode_jours ; couverture = stock ÷ vente moyenne par jour, arrondie à l'entier inférieur ; date de rupture = date du calcul + couverture. Catégories appliquées dans l'ordre de priorité du fichier de règles (première règle vraie l'emporte) : Données incomplètes, Pas d'historique, Déjà en rupture, Délai inconnu, Rupture imminente (couverture < D + L), À surveiller (D + L ≤ couverture < D + L + 7), Sans risque. Calculs faits par un script, pas estimés. Contrôle final : nombre de lignes en sortie = nombre de lignes en entrée (AC1). |
| **Failure Modes** | Fichier de règles absent → arrêt, ne pas appliquer de seuils par défaut<br>D absent → arrêt et le signaler<br>Valeur non numérique dans une ligne → catégorie « Données incomplètes »<br>Nombre de lignes en sortie ≠ entrée → arrêt et signaler l'écart |
| **Required Tools** | — (exécution d'un petit script de calcul sur la plateforme) |
| **Depends On** | None |
| **Stateful?** | No |

## Prerequisites

1. Ouvrir le dépôt du projet dans Claude Code (claude.ai/code).
2. Le skill `screening-sales-data` est disponible dans la session (skills du compte).
3. `data/delais-fournisseurs.csv` (C4) et `data/calendrier-commandes.csv` (C6) existent.
4. Les exports C1, C2 et C3 de la semaine sont déposés dans `data/`, agrégés et sans donnée client. Pour le projet de cours, utiliser uniquement des données fictives.
5. Les nouveaux skills sont rangés dans `outputs/alerte-rupture-hebdomadaire/skill/`, car le `CLAUDE.md` du projet demande de ne pas modifier `.claude/skills/`. Pour les lancer par leur nom, l'enseignante pourra les copier dans `.claude/skills/` si elle le souhaite.

## Deployment Plan

| Artifact | Target Location | Deployment Steps |
|---|---|---|
| S1 — `alerte-rupture-hebdomadaire` | `outputs/alerte-rupture-hebdomadaire/skill/alerte-rupture-hebdomadaire/SKILL.md` | Build écrit le SKILL.md (`disable-model-invocation: true`), commit ; lancement en demandant à Claude de suivre ce fichier (ou par `/alerte-rupture-hebdomadaire` après copie dans `.claude/skills/`) |
| S2 — `classifying-stockout-risk` | `outputs/alerte-rupture-hebdomadaire/skill/classifying-stockout-risk/SKILL.md` | Build écrit le SKILL.md et le script de calcul, commit |
| `screening-sales-data` | Déjà installé (skills du compte) | Aucun ; vérifier sa présence au lancement |

**Packaging note:** Les deux skills sont des dossiers placés directement dans le dépôt du projet. Pas de plugin ni de marketplace : le dépôt GitHub est le moyen de partage.

**Orchestrator artifact (primary-loop platforms):** S1 est le point d'entrée lancé par l'utilisateur (skill, pas commande slash séparée) et porte le nom du workflow ; S2 porte un nom de capacité.

**Run Logging:** À la fin de chaque exécution, S1 ajoute une ligne à `outputs/alerte-rupture-hebdomadaire/runs.md` (date, fichiers reçus, résultat, nombre de lignes par catégorie, corrections nécessaires), en créant le fichier avec son en-tête s'il n'existe pas.

**Recommended for frequent use:** Un rappel de calendrier chaque lundi matin pour déposer les exports et taper `/alerte-rupture-hebdomadaire`.

---

## Cross-Layer Sections

*These sections apply across all three layers — handoff and metadata that doesn't belong to a single layer.*

## Evaluation Inputs

**Acceptance Criteria, Example Scenarios (including Golden Examples), and Human Gates are sourced from the Workflow Requirements file** (`outputs/alerte-rupture-hebdomadaire/requirements.md`). Do not duplicate them here. Step 5 (Test) reads them from that file directly.

## Deferred to Build

- [ ] Shareability (file vs code distribution mode) — partage via le dépôt GitHub par défaut
- [ ] Exact model version per platform (mapping above is guidance; Build verifies current names)
- [ ] Format exact des colonnes attendues par `screening-sales-data`, et réutilisation éventuelle de `calculating-stock-coverage` à la place de S2
- [ ] Langage du script de calcul de S2

## Stakeholders

| Rôle | Étapes | Ce qu'il fait |
|---|---|---|
| Contrôle de gestion / responsable e-commerce | Step 1 | Produit les exports C1, C2, C3 |
| Responsable des achats (porteur) | Steps 1, 5 ; G1, G2 | Dépose les fichiers, lance le workflow, valide la liste et décide |
| Workflow IA | Steps 2, 3, 4 | Contrôle, calcule, rédige |
| Directeurs de magasin, responsable e-commerce | Après Step 5 | Reçoivent les décisions (transferts, surveillance) |

Swimlane : Contrôle de gestion / e-commerce (1) → Responsable des achats (lancement) → IA (2 → 3 → 4) → Responsable des achats (5).

## Self-Test Summary

**Structure**
- ✓ Frontmatter is present with workflow, requirements_file, spec_version (`3.0`), approved (`false`), definition_type, mechanism, involvement, platform, platform_mode, packaging, and counts
- ✓ Frontmatter `counts` match the body — skills = 2, agents = 0, integrations = 0
- ✓ Source section names the Workflow Requirements file path
- ✓ All mandatory template sections are present in template order
- ✓ `Architecture Decisions` table has Lens, Platform, Platform Mode, Orchestration, Involvement, Packaging, and Trigger rows
- ✓ Every step in the decomposition table has separate Orchestration, Integration, Intelligence, and Build Output columns
- ✓ Step IDs in the decomposition table match the Step IDs in the Workflow Requirements
- ✓ Every step uses canonical autonomy terms
- ✓ Every Integration column entry includes the block type, tool name, and use/build tag — all entries are "—" (no integrations)
- ✓ Every Build Output value is one of the canonical forms
- ✓ Packaging value is one of the canonical forms (`Loose Files`)
- ✓ Mechanism is one of `Skill | Agent`

**Skill Candidates**
- ✓ Every `New skill: SN` reference has a matching Skill Candidates entry
- ✓ Every Skill Candidate has all 12 fields
- ✓ Every Skill Candidate's Name conforms to format rules and is capability-named, except the orchestrator S1
- ✓ Every Skill Candidate's Description starts with "This skill should be used when...", is ≤1024 chars, is third-person, and names at least two concrete trigger keywords/contexts
- ✓ No two Skill Candidates describe the same capability at different steps
- ✓ For a `Skill` mechanism, S1 is the orchestrator skill, named with the workflow slug, Covers Steps: all
- ✓ Every `Extend existing: [name]` cell carries the `(also used by: …)` parenthetical — none present

**Agent Configuration**
- ✓ Every `New agent: AN` reference has a matching Agent Configuration entry — none present
- ✓ Every Agent Configuration has all 14 fields — not applicable (agents: 0)
- ✓ Every Agent Configuration's Description starts with "Use this agent when..." — not applicable
- ✓ Every Agent Configuration's Tools list is consistent with Safety & Permissions — not applicable
- ✓ Multi-Agent Configuration present if more than one agent — not applicable

**Cross-references**
- ✓ Every tool in the Integration column has a matching Integration Options entry — no tools; Integration Options is the single text-only line
- ✓ Every skill `Depends On` reference points to a defined skill ID (S2) or an installed skill / artifact

**Mechanism-specific**
- ✓ Orchestrator Prompt Outline section is present (mechanism = Skill)
- ✓ Orchestrator Prompt Outline names the closing **What I did** run summary
- ✓ `agents: 0` is set and orchestration logic is documented in the Orchestrator Prompt Outline and Deployment Plan

**Safety**
- ✓ Safety & Permissions section is present — all four questions answered with mitigations
- ✓ Constraint Conformance table lists every constraint in a recorded state — 5 Satisfied, 1 Accepted (owner : Meriem, raison indiquée), 0 Open
- ✓ Value & Measurement restates objective, outcome, measure, baseline and target ; `Baseline: Unknown` carried through
- ✓ Requirements do not predate these sections — no Design-sourced constraints
- ✓ Untrusted input AND write access — not applicable (no untrusted input, no external write)

**Completeness**
- ✓ Model Recommendation section is present with a default capability and per-platform mapping
- ✓ Data Readiness Summary is present and references Context IDs
- ✓ Deployment Plan is present with target location and deployment steps for each artifact, plus a Packaging note
- ✓ Evaluation Inputs section points to the Workflow Requirements file
- ✓ Deferred to Build section lists what Build will resolve
- ✓ Self-Test Summary section is present, enumerating every checklist item
