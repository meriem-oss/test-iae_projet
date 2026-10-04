---
workflow: alerte-rupture-hebdomadaire
design_spec: outputs/alerte-rupture-hebdomadaire/design-spec.md
requirements: outputs/alerte-rupture-hebdomadaire/requirements.md
date: 2026-10-04
environment: "Claude Code (cloud), aucun connecteur ; chaque scénario exécuté par un sous-agent neuf dans une copie isolée du dépôt"
round_status: in-progress
criteria_total: 0
criteria_met: 0
results: {}
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

## Golden example deltas

Aucun scénario n'a d'exemple de référence.

## Not run

## Environment

Aucun connecteur. Exécutions dans des copies isolées du dépôt (worktrees), pour que les fichiers produits par un scénario n'influencent pas les autres.
