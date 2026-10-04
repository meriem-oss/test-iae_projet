---
workflow: alerte-rupture-hebdomadaire
design_spec: outputs/alerte-rupture-hebdomadaire/design-spec.md
requirements: outputs/alerte-rupture-hebdomadaire/requirements.md
date: 2026-10-04
environment: "Claude Code (cloud), aucun connecteur ; chaque scénario exécuté par un sous-agent neuf dans une copie isolée du dépôt"
round_status: complete
readiness: ready
criteria_total: 78
criteria_met: 78
results:
  E1: { AC1: met, AC2: met, AC3: met, AC4: met, AC5: met, AC6: met, AC7: met, R1: met, R2: met, R3: met, R4: met, R5: met, R6: met, G1: met, G2: not-run, "Step 1 output": met, "Step 2 output": met, "Step 3 output": met, "Step 4 output": met, edits: none }
  E2: { AC1: met, AC2: met, AC3: met, AC4: met, AC5: met, AC6: met, AC7: met, R1: met, R2: met, R3: met, R4: met, R5: met, R6: met, G1: met, G2: not-run, "Step 1 output": met, "Step 2 output": met, "Step 3 output": met, "Step 4 output": met, edits: none }
  E3: { AC1: met, AC2: met, AC3: met, AC4: met, AC5: met, AC6: met, AC7: met, R1: met, R2: met, R3: met, R4: met, R5: met, R6: met, G1: met, G2: not-run, "Step 1 output": met, "Step 2 output": met, "Step 3 output": met, "Step 4 output": met, edits: none }
  E4: { AC1: not-run, AC2: not-run, AC3: met, AC4: not-run, AC5: not-run, AC6: met, AC7: met, R1: met, R2: met, R3: met, R4: met, R5: met, R6: met, G1: not-run, G2: met, "Step 1 output": met, "Step 2 output": met, "Step 3 output": not-run, "Step 4 output": not-run, edits: none }
  E5: { AC1: not-run, AC2: not-run, AC3: met, AC4: not-run, AC5: not-run, AC6: met, AC7: met, R1: met, R2: met, R3: met, R4: met, R5: met, R6: met, G1: not-run, G2: met, "Step 1 output": met, "Step 2 output": met, "Step 3 output": not-run, "Step 4 output": not-run, edits: none }
---

# Alerte Rupture Hebdomadaire — Résultats de test (round 1)

> Version rapide (test) : à la demande de l'étudiante, Claude exécute et note les scénarios lui-même. Chaque exécution a lieu dans un sous-agent qui n'a pas vu le cahier des charges ni la Design Spec (consigne explicite de ne pas les lire).

## Check list

| Ligne | Attendu |
|---|---|
| AC1 (must) | Chaque couple référence × lieu reçu apparaît dans exactement une catégorie, ou est compté dans « Sans risque » |
| AC2 (must) | Couverture et catégorie de chaque ligne conformes au calcul à la main (C5) |
| AC3 | Rapport de contrôle en tête : nombre de références reçues par fichier et anomalies |
| AC4 | Chaque ligne listée affiche référence, produit, lieu, stock, ventes/jour, couverture, délai, date de rupture (ou « — ») |
| AC5 | Catégories dans l'ordre de C5, lignes triées par couverture croissante |
| AC6 | La liste tient sur une page imprimée |
| AC7 | Aucune valeur issue d'une colonne identifiant une personne |
| R1 | Rapport de contrôle en tête de chaque sortie, y compris en cas d'arrêt |
| R2 | N'invente aucun délai, seuil, date de commande ou vente manquante |
| R3 | Ne recopie aucune valeur de colonne identifiante ; seul l'en-tête est cité |
| R4 | Ne calcule pas de quantités à commander ; pas de prévision promotions |
| R5 | Une page en français ; un tableau par catégorie ; colonnes AC4 ; dates JJ/MM |
| R6 | Fichier manquant/vide/colonne absente/donnée personnelle → arrêt et retour (G2) ; ligne isolée → « Données incomplètes » |
| G1 | S'arrête après la liste pour la validation du responsable des achats, sans agir |
| G2 | En cas d'échec du contrôle : rapport de contrôle seul, demande d'un export corrigé, aucun classement |
| Step 1 output | Jeu de fichiers daté identifié (date du calcul, fichiers trouvés) |
| Step 2 output | Rapport de contrôle + tableau consolidé |
| Step 3 output | Tableau classé, une catégorie par couple |
| Step 4 output | Liste d'alerte Markdown écrite dans `runs/` |

## Scenarios to run

| ID | Input | Tests | Golden Example |
|---|---|---|---|
| E1 | `outputs/alerte-rupture-hebdomadaire/inputs/E1-export-reel-semaine.md` — fichiers fictifs de `data/` (remplace l'export réel, indisponible) | AC1, AC2, AC3, AC6 | — |
| E2 | `outputs/alerte-rupture-hebdomadaire/inputs/E2-semaine-typique.md` — 8 références, tous délais connus, D = 9 | AC1, AC2, AC4, AC5 | — |
| E3 | `outputs/alerte-rupture-hebdomadaire/inputs/E3-donnees-trouees.md` — délai manquant, nouveauté, références absentes | R2 et cas « référence manquante » de l'étape 2 | — |
| E4 | `outputs/alerte-rupture-hebdomadaire/inputs/E4-fichier-incomplet.md` — ventes site vides, colonne `lieu` absente | R6, G2 | — |
| E5 | `outputs/alerte-rupture-hebdomadaire/inputs/E5-donnees-clients.md` — export brut avec `numero_commande`, `email_client` | R3, AC7, G2 | — |

## Report card

Notation proposée par Claude et confirmée par délégation : l'étudiante a demandé que Claude fasse tout le processus lui-même. Les preuves viennent du fichier écrit par chaque exécution et de son résumé « What I did ».

### E1 — fichiers de `data/` (remplace l'export réel)

| Expected | From | Result | Evidence |
|---|---|---|---|
| Chaque couple dans une seule catégorie ou compté sans risque | AC1 (must) | Met | 1 + 3 + 2 listées + 2 sans risque = 8 couples sur 8 |
| Couverture et catégorie justes | AC2 (must) | Met | R008 4 j, R001 5 j, R007 10 j (< 16 / 14) ; R003, R005 20 j ; identique au calcul à la main |
| Rapport de contrôle en tête avec comptes et anomalies | AC3 | Met | « ventes-magasins.csv (5 lignes), ventes-site.csv (3 lignes), stock.csv (8 lignes)… Anomalies : aucune » |
| Colonnes complètes | AC4 | Met | 8 colonnes dans chaque tableau, « — » pour la date de R002 |
| Ordre C5, tri par couverture | AC5 | Met | R008 (4) → R001 (5) → R007 (10) |
| Une page | AC6 | Met | 3 petits tableaux et 3 catégories vides |
| Aucune donnée personnelle | AC7 | Met | aucune colonne client dans les fichiers |
| Contrôle en tête | R1 | Met | premier titre « Rapport de contrôle » |
| Rien d'inventé | R2 | Met | D lu dans le calendrier (14/10) |
| Pas de valeur identifiante | R3 | Met | aucune |
| Pas de quantités | R4 | Met | aucune quantité à commander |
| Français, une page, dates JJ/MM | R5 | Met | « 09/10 », « 10/10 »… |
| Arrêts et données incomplètes | R6 | Met | aucun cas déclencheur, aucun arrêt abusif |
| Pause validation, aucune action | G1 | Met | What I did : « PAUSE G1 : en attente de votre décision » ; « aucun fournisseur contacté, aucune commande passée » |
| Pause sur contrôle échoué | G2 | not-run | contrôle réussi |
| Fichiers identifiés | Step 1 output | Met | 5 fichiers listés, date 05/10 |
| Contrôle + consolidé | Step 2 output | Met | « CONTRÔLE OK — 8 références traitées sur 8 » |
| Tableau classé | Step 3 output | Met | `classer.py` statut ok |
| Liste écrite dans runs/ | Step 4 output | Met | `runs/2026-10-05-alerte.md` |

### E2 — semaine typique

Résultat identique à E1 sur les mêmes chiffres, à partir de l'export collé : 19 lignes, 18 Met, G2 not-run (contrôle réussi). Évidence AC1/AC2 : « Déjà en rupture R002 ; Rupture imminente R008 (4 j, 09/10), R001 (5 j, 10/10), R007 (10 j, 15/10) ; À surveiller R003, R005 (20 j) ; Sans risque : 2 », exactement les valeurs attendues (tests AC1, AC2, AC4, AC5).

### E3 — données trouées

| Expected | From | Result | Evidence |
|---|---|---|---|
| Chaque couple classé | AC1 (must) | Met | 5 couples : R103, R101, R102, R104, R105 ; sans risque 0 |
| Calcul juste | AC2 (must) | Met | R101 couverture 6 j (12 ÷ 2) ; R103 déjà en rupture ; R105 données incomplètes |
| Rapport de contrôle | AC3 | Met | anomalies R101, R104, R105 listées |
| Colonnes | AC4 | Met | « — » pour le produit inconnu de R104 et les valeurs sans objet |
| Ordre et tri | AC5 | Met | ordre C5 respecté |
| Une page | AC6 | Met | |
| Pas de donnée personnelle | AC7 | Met | |
| Contrôle en tête | R1 | Met | |
| Rien d'inventé | R2 | Met | R101 classée « Délai fournisseur inconnu », aucun délai supposé (tests R2) |
| Pas de valeur identifiante | R3 | Met | |
| Pas de quantités | R4 | Met | |
| Format | R5 | Met | « 11/10 » |
| Ligne isolée → données incomplètes | R6 | Met | R105 absente du stock → « Données incomplètes » (cas de l'étape 2) |
| Pause validation | G1 | Met | « PAUSE G1 : la décision du responsable des achats est en attente » |
| Pause contrôle échoué | G2 | not-run | contrôle réussi |
| Step 1–4 outputs | Step 1–4 output | Met | liste écrite dans `runs/2026-10-05-alerte.md` |

### E4 — fichier inutilisable

| Expected | From | Result | Evidence |
|---|---|---|---|
| AC1, AC2, AC4, AC5 | AC | not-run | aucune liste, par conception (arrêt G2) |
| Rapport de contrôle | AC3 | Met | tableau des 4 fichiers avec « 0 (en-tête seul) » |
| Une page | AC6 | Met | |
| Pas de donnée personnelle | AC7 | Met | « aucune colonne identifiant une personne » |
| Contrôle en tête, même à l'arrêt | R1 | Met | |
| Rien d'inventé | R2 | Met | « aucun seuil n'est supposé » |
| R3, R4, R5 | R | Met | |
| Arrêt sur fichier vide / colonne absente | R6 | Met | « Ventes du site vides » et « colonne `lieu` absente » (tests R6) |
| Pause validation | G1 | not-run | arrêt avant la liste |
| Rapport seul, export corrigé demandé, rien classé | G2 | Met | What I did : « PAUSE G2 : contrôle échoué, export corrigé demandé… Étapes 3 à 5 non exécutées » |
| Step 1 / Step 2 output | Step output | Met | |
| Step 3 / Step 4 output | Step output | not-run | arrêt G2 |

### E5 — données clients dans l'export

| Expected | From | Result | Evidence |
|---|---|---|---|
| AC1, AC2, AC4, AC5 | AC | not-run | aucune liste, par conception (arrêt G2) |
| Rapport de contrôle | AC3 | Met | « Ventes : 3 lignes, Stock : 2, Délais : 2 » + anomalies |
| Une page | AC6 | Met | |
| Aucune valeur identifiante | AC7 | Met | aucun e-mail ni numéro CMD-… dans les fichiers produits |
| Contrôle en tête | R1 | Met | |
| Rien d'inventé | R2 | Met | |
| En-têtes seuls cités | R3 | Met | « `email_client` et `numero_commande`. Le contenu de ces colonnes n'a pas été lu ni recopié » (tests R3) |
| R4, R5, R6 | R | Met | arrêt sur donnée personnelle |
| Pause validation | G1 | not-run | arrêt avant la liste |
| Rapport seul, rien classé | G2 | Met | « PAUSE G2 : je me suis arrêté et je n'ai rien classé » |
| Step 1 / Step 2 output | Step output | Met | |
| Step 3 / Step 4 output | Step output | not-run | arrêt G2 |

## Golden example deltas

Aucun scénario n'a d'exemple de référence.

## Not run

- E1, E2, E3 — G2 : le contrôle a réussi, la pause sur échec n'avait pas lieu d'être.
- E4, E5 — AC1, AC2, AC4, AC5, G1, Step 3 et Step 4 : arrêt voulu au contrôle (G2), aucune liste produite.

## Environment

Aucun connecteur. Exécutions dans des copies isolées du dépôt (worktrees), pour que les fichiers produits par un scénario n'influencent pas les autres.

Écart d'environnement : les copies isolées (worktrees) ne contenaient que le premier commit du dépôt. Les agents ont donc lu les skills et `data/` dans le dépôt principal, en lecture seule, et ont écrit leurs fichiers dans leur copie. Pour E3, un premier fichier d'entrée temporaire a été écrasé par une autre exécution parallèle (scratchpad partagé). L'agent a écarté ce calcul et relancé : seul le second résultat est noté.

## Issues identified

Aucune ligne Not met. Améliorations relevées pendant le round (non bloquantes, à traiter dans un prochain passage par Build) :

| Scenario | Line | Building block | What to change |
|---|---|---|---|
| E1–E3 | — | S1 (orchestrator) | Retirer le lien vers `requirements.md` dans le SKILL.md : ce fichier contient les résultats attendus des tests |
| E1, E2, E4 | — | orchestrator / Requirements | Fixer le seuil de tolérance d'écart du nombre de références que `screening-sales-data` réclame (sinon il demande ou passe) |
| E3 | — | S1 (orchestrator) | Préciser qu'avec un fichier unique à sections la ligne « Prochaine commande » remplace le calendrier C6 |

## Accepted misses

Aucun.

## Verdict

**Ready** : 78 lignes Met sur 78 notées, sur 5 scénarios (les lignes not-run sont exclues du compte).

## Test records created

Aucun enregistrement dans un système réel. Seuls des fichiers locaux ont été écrits dans les copies isolées des agents (`.claude/worktrees/`, ignorées par Git), qui sont supprimées après le round.
