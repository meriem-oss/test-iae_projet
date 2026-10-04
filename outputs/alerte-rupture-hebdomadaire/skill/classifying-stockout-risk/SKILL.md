---
name: classifying-stockout-risk
description: This skill should be used when a consolidated table of sales, stock and supplier lead times per reference and location must be classified by stockout risk against a replenishment date — "classer les risques de rupture", "couverture de stock avant la prochaine commande", "stock coverage versus next order date", "which references run out before the next delivery". It computes daily sales velocity, days of coverage and estimated stockout date, then assigns each row exactly one category from a supplied rules file. It never invents a missing lead time, threshold or sale. Do not use it to compute order quantities or to screen raw files for personal data.
---

# Classer les risques de rupture

Attribue à chaque couple **référence × lieu** une seule catégorie de risque, selon les règles de `references/regles-classement.md`.

## Entrées

- **Ventes** : une ou plusieurs tables `reference;produit;lieu;quantite_vendue_28j`
- **Stock** : `reference;lieu;stock_disponible`
- **Délais fournisseurs** : `reference;fournisseur;delai_jours`
- **Date du calcul** et **date de la prochaine commande** (ou un calendrier `date_commande` d'où la tirer)
- **Durée de la période de ventes** : 28 jours par défaut

## Méthode

Ne calcule jamais de tête. Exécute toujours le script, qui applique les règles à la lettre :

```bash
# Fichiers CSV (séparateur ;)
python3 <dossier-du-skill>/scripts/classer.py \
  --ventes data/ventes-magasins.csv data/ventes-site.csv \
  --stock data/stock.csv --delais data/delais-fournisseurs.csv \
  --calendrier data/calendrier-commandes.csv --date AAAA-MM-JJ

# Ou un fichier Markdown à sections (« ## Ventes… », « ## Stock… », « ## Délais… »)
python3 <dossier-du-skill>/scripts/classer.py --md <fichier.md>
```

Le script renvoie du JSON : `statut`, `D` (jours jusqu'à la prochaine commande), `controle` (fichiers lus, anomalies), `comptes` par catégorie, et `categories` (lignes triées par couverture croissante).

Règles appliquées (détail dans `references/regles-classement.md`) :
- vente moyenne par jour = ventes ÷ période ; couverture = stock ÷ vente par jour, arrondie à l'entier inférieur ; date de rupture = date du calcul + couverture ;
- catégories, première règle vraie l'emporte : Données incomplètes → Pas d'historique de vente → Déjà en rupture → Délai fournisseur inconnu → Rupture imminente (couverture < D + L) → À surveiller (< D + L + 7) → Sans risque.

## Cas d'arrêt

- `statut: arret` (code retour 2) → ne produis **aucun** classement ; rapporte la raison telle quelle.
- Fichier de règles, délais ou date de prochaine commande absents → arrêt ; ne suppose jamais une valeur.
- Valeur vide ou non numérique sur une ligne → la ligne passe en « Données incomplètes ».
- Le script vérifie que le nombre de lignes en sortie égale le nombre de couples reçus ; sinon arrêt.

## Ce que ce skill ne fait pas

- Il ne calcule pas de quantité à commander.
- Il ne recherche pas les données personnelles de façon exhaustive : ce contrôle appartient à `screening-sales-data`. Le script refuse seulement, par sécurité, les en-têtes manifestement personnels.
