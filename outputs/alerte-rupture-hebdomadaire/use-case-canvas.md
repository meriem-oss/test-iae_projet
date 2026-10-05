# Use case canvas — Alerte Rupture Hebdomadaire

*Synthèse sur une page · Meriem · 05/10/2026*

| **PROBLÈME** | **UTILISATEURS** | **VALEUR** |
|---|---|---|
| Ruptures découvertes trop tard · commandes passées tous les 15 jours à date fixe, sans regarder les ventes réelles | Responsable des achats (lance, valide) · contrôle de gestion / e-commerce (exports) · directeurs de magasin (destinataires) | Savoir chaque lundi ce qui va manquer avant la prochaine commande et agir avant la rupture · plus de produits disponibles en magasin et sur le site |
| **PROCESSUS ET ACTEURS** | **DONNÉES** | **IRRITANTS** |
| Rassembler les exports → contrôler les données → calculer et classer (IA) → rédiger la liste (IA) → valider (responsable des achats) | Ventes 28 j magasins et site · stock par lieu · délais fournisseurs *(à créer)* · calendrier des commandes *(à créer)* · règles de classement | Exports manuels CSV · délais fournisseurs « dans la tête » des acheteurs · aucun contrôle des données aujourd'hui |
| **RÈGLES** | **RISQUES** | **INDICATEURS DE RÉUSSITE** |
| Rapport de contrôle en tête (R1) · ne jamais inventer un délai ou une vente (R2) · aucune donnée client recopiée (R3) · validation humaine avant toute action (G1) | Données incomplètes ou fausses · donnée personnelle dans un export (arrêt, G2) · sources modifiées · commande ou contact fournisseur (interdits) | Ruptures / semaine (départ *à mesurer*) · ≥ 80 % des ruptures signalées à l'avance et −30 % de ruptures *(à vérifier)* · aucune référence perdue, calcul juste (AC1, AC2) |

*Chaque case se retrouve, en détail, dans [requirements.md](requirements.md).*

## Points à vérifier
- Le porteur du workflow (responsable des achats) est une hypothèse.
- Le niveau de départ des ruptures est inconnu : à mesurer avant la mise en service.
- Les objectifs chiffrés (80 %, −30 %) sont des hypothèses.
- Les fichiers des délais fournisseurs et du calendrier des commandes restent à créer.
