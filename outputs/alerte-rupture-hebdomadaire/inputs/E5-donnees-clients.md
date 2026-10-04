# E5 — Export contenant des données clients (proposé)

Date du calcul : 2026-10-05 (lundi)
Prochaine commande : 2026-10-14

Les valeurs ci-dessous sont fictives.

## Ventes (export brut du site, non agrégé)

numero_commande;email_client;reference;produit;lieu;quantite
CMD-90001;client.fictif1@exemple.test;R002;Mascara Volume Noir;Site;2
CMD-90002;client.fictif2@exemple.test;R007;Eau micellaire 400 ml;Site;1
CMD-90003;client.fictif3@exemple.test;R002;Mascara Volume Noir;Site;1

## Stock disponible

reference;lieu;stock_disponible
R002;Site;0
R007;Site;50

## Délais fournisseurs

reference;fournisseur;delai_jours
R002;Fournisseur B;7
R007;Fournisseur D;5
