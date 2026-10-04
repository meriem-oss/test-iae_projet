# C5 — Règles de classement des références

> Statut : **hypothèse de test, à valider** par le responsable des achats avant la mise en service.

## Définitions

| Terme | Définition |
|---|---|
| Période d'analyse | Les 28 derniers jours de ventes (4 semaines complètes) |
| Vente moyenne par jour | Quantité vendue sur 28 jours ÷ 28 |
| Couverture (jours) | Stock disponible ÷ vente moyenne par jour, arrondi à l'entier inférieur |
| D | Nombre de jours entre la date du calcul et la prochaine date de commande (lu dans C6) |
| L | Délai de livraison du fournisseur, en jours (lu dans C4) |
| Date de rupture estimée | Date du calcul + couverture |

## Catégories (une seule par couple référence × lieu)

Les règles s'appliquent dans cet ordre ; la première qui s'applique l'emporte.

| Ordre | Catégorie | Règle |
|---|---|---|
| 1 | Données incomplètes | La référence est absente du fichier de stock, ou une valeur est vide / non numérique |
| 2 | Pas d'historique de vente | Aucune vente sur les 28 jours (nouveauté ou produit dormant) |
| 3 | Déjà en rupture | Stock disponible = 0 et au moins une vente sur 28 jours |
| 4 | Délai fournisseur inconnu | Aucun délai L dans C4 pour cette référence (la couverture est quand même affichée) |
| 5 | Rupture imminente | Couverture < D + L (le stock sera épuisé avant l'arrivée de la marchandise de la prochaine commande) |
| 6 | À surveiller | D + L ≤ couverture < D + L + 7 |
| 7 | Sans risque | Couverture ≥ D + L + 7 — **non listée** dans l'alerte, seulement comptée |

## Ordre d'affichage

1. Rapport de contrôle
2. Déjà en rupture
3. Rupture imminente
4. À surveiller
5. Délai fournisseur inconnu
6. Pas d'historique de vente
7. Données incomplètes

Dans chaque catégorie : tri par couverture croissante.
