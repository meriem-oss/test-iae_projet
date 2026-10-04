# Rapport d'opportunités IA : ruptures de stock dans une enseigne de cosmétiques

| | |
|---|---|
| **Nom** | Meriem |
| **Rôle** | Étudiante IAE : étude de cas d'une enseigne de cosmétiques (magasins + site en ligne) |
| **Date** | 2026-10-04 |
| **Lens** | Organisationnel |
| **Opportunités identifiées** | 5 |
| **Recommandation n° 1** | **Alerte rupture hebdomadaire** : c'est le moyen le plus simple et le plus rapide de ne plus découvrir les ruptures trop tard, alors qu'aujourd'hui on recommande tous les 15 jours sans regarder les ventes. |

> **Statut : interview interrompue (version test).** L'interview s'est arrêtée après 2 questions sur 7, à la demande de l'étudiante.
> Les éléments marqués *(hypothèse)* sont des suppositions fréquentes dans le commerce de cosmétiques. Ils restent **à vérifier** lors d'une prochaine séance :
> qui passe les commandes (siège ou magasins), quels outils et quelles données de ventes existent, si le stock du site est partagé avec celui des magasins.

## Ce que l'on sait du cas

- **Objectifs de l'entreprise :**
  1. augmenter le chiffre d'affaires (CA) de **20 %** ;
  2. **réduire les ruptures de stock**, qui font perdre des ventes.
- **Fonctionnement actuel du réassort :** les commandes sont passées **tous les 15 jours, à date fixe, sans tenir compte des ventes réelles ni de la demande des clients.**
- **Diagnostic :** un produit qui se vend vite peut être épuisé bien avant la commande suivante, ce qui entraîne des jours de rupture et des ventes perdues. Un produit qui se vend peu est recommandé alors qu'il en reste en réserve, ce qui immobilise de l'argent. Le problème vient donc du **processus** (une commande au calendrier, pas au besoin), plus que d'une personne.

## Tableau de synthèse

| # | Opportunité | Autonomie | Implication humaine | Impact |
|---|---|---|---|---|
| 1 | Alerte rupture hebdomadaire | Déterministe | Augmentée | Élevé |
| 2 | Tableau de bord des ventes perdues | Déterministe | Automatisée | Moyen |
| 3 | Proposition de commande de réassort | Guidée | Augmentée | Élevé |
| 4 | Répartition du stock magasins / site | Guidée | Augmentée | Moyen |
| 5 | Prévision des pics de demande | Guidée | Augmentée | Moyen |

## Recommandations prioritaires

1. **Alerte rupture hebdomadaire** : elle s'attaque directement à la cause principale (on ne regarde pas les ventes). Elle est simple à construire avec un export des ventes et un fichier de stock, et c'est un bon premier workflow pour apprendre la méthode.
2. **Proposition de commande de réassort** : c'est l'étape suivante logique. Après avoir repéré les produits à risque, on calcule combien en commander. C'est l'impact le plus fort sur l'objectif de +20 % de CA.
3. **Tableau de bord des ventes perdues** : sans mesure, impossible de prouver que les ruptures diminuent. Il donne les chiffres de départ et de suivi.

## Fiches détaillées des opportunités

### Autonomie déterministe

---

**1. Alerte rupture hebdomadaire**

**Autonomie :** Déterministe
**Implication humaine :** Augmentée

**Pourquoi c'est un bon candidat :**
Le calcul est répétitif et suit des règles claires : ventes moyennes par jour, stock restant, nombre de jours de stock, comparaison avec le délai de livraison du fournisseur. Les entrées (ventes, stock) et la sortie (liste de produits à risque) sont bien définies.

**Problème actuel :**
On recommande tous les 15 jours sans regarder les ventes. Les ruptures sont découvertes en rayon ou sur le site, quand il est déjà trop tard.

**Comment l'IA aide :**
Chaque semaine, l'IA reçoit l'export des ventes (magasins + site) et le fichier de stock. Elle calcule, produit par produit, la **couverture de stock**, c'est-à-dire le nombre de jours avant d'être à zéro au rythme actuel des ventes. Elle produit ensuite une liste classée : produits déjà en rupture, rupture imminente (couverture inférieure au délai fournisseur), produits à surveiller. Le responsable des achats relit la liste et décide quoi faire.

**Pour démarrer :**
Prendre un export Excel des ventes des 4 dernières semaines et un état du stock pour une seule catégorie (par exemple les rouges à lèvres), et faire calculer la couverture par Claude.

**Objectif de l'entreprise :** réduire les ruptures, et donc soutenir les +20 % de CA.
**Parties prenantes :** responsable achats / approvisionnement *(hypothèse : porteur du processus)*, directeurs de magasin, responsable e-commerce.
**Indicateurs de succès :** nombre de produits en rupture par semaine, nombre de ruptures signalées avant qu'elles arrivent, nombre de jours de rupture par produit.

---

**2. Tableau de bord des ventes perdues**

**Autonomie :** Déterministe
**Implication humaine :** Automatisée

**Pourquoi c'est un bon candidat :**
Il s'agit d'agréger des données et de calculer toujours les mêmes indicateurs, toujours de la même façon. Il n'y a pas de jugement à porter.

**Problème actuel :**
L'entreprise sait que les ruptures « font perdre des ventes », mais *(hypothèse)* elle ne les chiffre pas. Sans mesure, on ne peut ni prioriser ni prouver un progrès.

**Comment l'IA aide :**
Chaque semaine, l'IA estime les ventes perdues : jours de rupture × ventes moyennes par jour × prix, par produit et par canal (magasin / site). Elle produit une page de synthèse : top 10 des produits qui coûtent le plus cher en ruptures, et évolution sur les semaines précédentes.

**Pour démarrer :**
Pour 5 produits connus pour manquer souvent, estimer à la main le CA perdu le mois dernier avec la formule ci-dessus.

**Objectif de l'entreprise :** piloter la réduction des ruptures et mesurer leur effet sur le CA.
**Parties prenantes :** direction commerciale, contrôle de gestion, responsable achats.
**Indicateurs de succès :** CA perdu estimé par semaine, taux de rupture (part des produits en rupture), part du CA perdu dans le CA total.

---

### Autonomie guidée

---

**3. Proposition de commande de réassort**

**Autonomie :** Guidée
**Implication humaine :** Augmentée

**Pourquoi c'est un bon candidat :**
Plusieurs facteurs sont à combiner (ventes récentes, stock, délai fournisseur, quantité minimum de commande, date de péremption des cosmétiques). L'IA peut proposer, mais une personne doit valider avant d'engager de l'argent.

**Problème actuel :**
Les quantités commandées tous les 15 jours ne suivent pas les ventes : trop peu sur les produits qui marchent, trop sur ceux qui ne marchent pas.

**Comment l'IA aide :**
À partir de l'alerte rupture (opportunité 1), l'IA propose pour chaque produit à risque une quantité à commander, en respectant le délai fournisseur, la quantité minimum et la durée de vie du produit. La liste est regroupée par fournisseur. Le responsable des achats valide, modifie ou refuse chaque ligne avant envoi. L'IA ne contacte jamais un fournisseur elle-même.

**Pour démarrer :**
Lors de la prochaine commande, comparer pour 10 produits la quantité réellement commandée avec une quantité calculée « ventes des 15 derniers jours + marge de sécurité ».

**Objectif de l'entreprise :** +20 % de CA (moins de ventes perdues) et réduction des ruptures.
**Parties prenantes :** responsable achats (porteur du processus), fournisseurs, contrôle de gestion (budget).
**Indicateurs de succès :** taux de rupture, valeur du stock dormant, part des propositions de l'IA acceptées sans modification.

---

**4. Répartition du stock magasins / site**

**Autonomie :** Guidée
**Implication humaine :** Augmentée

**Pourquoi c'est un bon candidat :**
Il faut comparer le stock et les ventes de plusieurs lieux et proposer des mouvements de marchandise. C'est un travail de croisement d'informations, avec une décision humaine à la fin.

**Problème actuel :**
*(Hypothèse)* Un produit peut être en rupture sur le site ou dans un magasin alors qu'il dort en réserve dans un autre magasin.

**Comment l'IA aide :**
Chaque semaine, l'IA repère les produits en surplus à un endroit et en manque à un autre. Elle propose des transferts entre magasins, ou vers le stock du site, avec les quantités. Le responsable logistique valide.

**Pour démarrer :**
Vérifier avec l'enseigne si le site a son propre stock ou s'il puise dans celui des magasins, et si les transferts entre magasins sont possibles.

**Objectif de l'entreprise :** réduire les ruptures sans racheter de stock, et donc augmenter le CA.
**Parties prenantes :** responsable logistique, directeurs de magasin, responsable e-commerce.
**Indicateurs de succès :** nombre de ruptures évitées grâce à un transfert, stock dormant par magasin.

---

**5. Prévision des pics de demande**

**Autonomie :** Guidée
**Implication humaine :** Augmentée

**Pourquoi c'est un bon candidat :**
Les ventes de cosmétiques varient avec les événements : fêtes, soldes, promotions, publications d'influenceurs, saison. L'IA est douée pour rassembler ces signaux et les traduire en besoins de stock.

**Problème actuel :**
Une commande à date fixe ne prévoit pas les pics. Les produits mis en avant par une promotion ou un influenceur partent en quelques jours.

**Comment l'IA aide :**
Chaque mois, l'IA prend le calendrier commercial (promotions prévues, fêtes) et les ventes des années précédentes. Elle produit la liste des produits qui risquent un pic, avec une estimation du volume supplémentaire à prévoir. L'équipe marketing et les achats valident.

**Pour démarrer :**
Lister les 3 dernières promotions ou opérations marketing et regarder si elles ont provoqué des ruptures.

**Objectif de l'entreprise :** +20 % de CA (capter les pics de demande).
**Parties prenantes :** marketing, responsable achats, responsable e-commerce.
**Indicateurs de succès :** ruptures pendant les opérations commerciales, écart entre ventes prévues et ventes réelles.

---

## Candidats de workflow (à confirmer)

> L'étudiante n'a pas encore choisi ses candidats : le tableau détaillé « Workflow Candidate Summary » sera rempli à la prochaine séance.
> **Proposition :** commencer par **Alerte rupture hebdomadaire**. Il compte 3 à 5 étapes (importer les ventes, importer le stock, calculer la couverture, classer, faire valider), une seule source de données et un lancement manuel.
> L'opportunité au plus fort impact (**Proposition de commande de réassort**) est aussi plus complexe. Elle reste sur la liste comme deuxième workflow, et elle s'appuie directement sur le premier.

## Prochaines étapes

1. Terminer l'interview : savoir qui commande, avec quels outils, et quelles données de ventes existent.
2. Choisir les candidats et compléter le tableau des candidats.
3. Étape suivante du cours : **Deconstruct** du workflow choisi.
4. Plus tard : l'angle **individuel** (le travail quotidien d'une personne, par exemple le responsable des achats) peut faire apparaître d'autres opportunités. Il mérite une séance à part.

## Annexe : définitions des classements

**Autonomie : combien l'IA décide seule ?**

- **Déterministe** : l'IA suit des règles fixes, sans jugement. La même entrée donne toujours le même résultat.
- **Guidée** : l'IA prend des décisions encadrées. L'humain fixe la direction, l'IA choisit comment faire dans ces limites.
- **Autonome** : l'IA planifie, décide et s'adapte seule selon ce qu'elle trouve.

**Implication humaine : un humain intervient-il pendant le déroulement ?**

- **Augmentée** : l'humain participe pendant le déroulement (il relit, oriente, décide aux étapes clés).
- **Automatisée** : l'IA travaille seule du début à la fin. L'humain ne regarde que le résultat final.
