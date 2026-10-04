#!/usr/bin/env python3
"""Classe chaque couple référence x lieu par risque de rupture (règles de references/regles-classement.md).

Deux façons de fournir les données :
  1. Des fichiers CSV (séparateur ;) :
     classer.py --ventes data/ventes-magasins.csv data/ventes-site.csv --stock data/stock.csv \
                --delais data/delais-fournisseurs.csv --calendrier data/calendrier-commandes.csv \
                --date 2026-10-05
  2. Un seul fichier Markdown qui contient des sections « ## Ventes… », « ## Stock… », « ## Délais… »
     et les lignes « Date du calcul : AAAA-MM-JJ » et « Prochaine commande : AAAA-MM-JJ » :
     classer.py --md outputs/alerte-rupture-hebdomadaire/inputs/E2-semaine-typique.md

Sortie : JSON sur la sortie standard. Code retour 2 = arrêt (données inutilisables ou données personnelles).
"""
import argparse
import csv
import io
import json
import math
import re
import sys
from datetime import date, timedelta

PERIODE_DEFAUT = 28
MARGE_SURVEILLANCE = 7
ENTETES_PERSONNELLES = re.compile(
    r"(e-?mail|courriel|nom_client|client|prenom|t[ée]l[ée]phone|adresse|numero_commande|n°_commande|commande_id|fidelit[ée]|carte_fid)",
    re.IGNORECASE,
)
COLONNES_VENTES = {"reference", "lieu", "quantite_vendue_28j"}
COLONNES_STOCK = {"reference", "lieu", "stock_disponible"}
COLONNES_DELAIS = {"reference", "delai_jours"}

ORDRE = [
    "Déjà en rupture",
    "Rupture imminente",
    "À surveiller",
    "Délai fournisseur inconnu",
    "Pas d'historique de vente",
    "Données incomplètes",
]


class Arret(Exception):
    pass


def lire_csv(texte, nom):
    lignes = [l for l in texte.strip().splitlines() if l.strip()]
    if not lignes:
        raise Arret(f"Fichier « {nom} » vide.")
    lecteur = csv.DictReader(io.StringIO("\n".join(lignes)), delimiter=";")
    entetes = [h.strip() for h in (lecteur.fieldnames or [])]
    perso = [h for h in entetes if ENTETES_PERSONNELLES.search(h)]
    if perso:
        raise Arret(
            f"Fichier « {nom} » : colonne(s) identifiant une personne : {', '.join(perso)}. "
            "Fournir un export agrégé par référence et par lieu, sans donnée client."
        )
    rows = [{k.strip(): (v or "").strip() for k, v in r.items() if k} for r in lecteur]
    return entetes, rows


def verifier_colonnes(entetes, attendues, nom):
    manquantes = sorted(attendues - set(entetes))
    if manquantes:
        raise Arret(f"Fichier « {nom} » : colonne(s) obligatoire(s) absente(s) : {', '.join(manquantes)}.")


def parse_md(chemin):
    texte = open(chemin, encoding="utf-8").read()
    sections, courant = {}, None
    for ligne in texte.splitlines():
        if ligne.startswith("## "):
            courant = ligne[3:].strip()
            sections[courant] = []
        elif courant is not None:
            sections[courant].append(ligne)
    m_date = re.search(r"Date du calcul\s*:\s*(\d{4}-\d{2}-\d{2})", texte)
    m_cmd = re.search(r"Prochaine commande\s*:\s*(\d{4}-\d{2}-\d{2})", texte)
    ventes = [(k, "\n".join(v)) for k, v in sections.items() if k.lower().startswith("ventes")]
    stock = [(k, "\n".join(v)) for k, v in sections.items() if k.lower().startswith("stock")]
    delais = [(k, "\n".join(v)) for k, v in sections.items() if "lais" in k.lower()]
    return ventes, stock, delais, m_date and m_date.group(1), m_cmd and m_cmd.group(1)


def nombre(v):
    try:
        x = float(v.replace(",", "."))
        return x if x >= 0 else None
    except (ValueError, AttributeError):
        return None


def classer(ventes_src, stock_src, delais_src, date_calcul, prochaine_commande, periode):
    controle = {"fichiers": [], "anomalies": []}
    if not ventes_src:
        raise Arret("Aucun fichier de ventes fourni.")
    if not stock_src:
        raise Arret("Aucun fichier de stock fourni.")
    if not delais_src:
        raise Arret("Aucun fichier de délais fournisseurs fourni : aucun délai n'est supposé.")
    if not prochaine_commande:
        raise Arret("Date de la prochaine commande inconnue : aucune date n'est supposée.")

    erreurs = []

    def charger(nom, texte, attendues, vide_interdit=False):
        try:
            entetes, rows = lire_csv(texte, nom)
            verifier_colonnes(entetes, attendues, nom)
            if vide_interdit and not rows:
                raise Arret(f"Fichier « {nom} » : aucune ligne (fichier vide).")
        except Arret as e:
            if "identifiant une personne" in str(e):
                raise
            erreurs.append(str(e))
            return []
        controle["fichiers"].append({"fichier": nom, "lignes": len(rows)})
        return rows

    charges = [("v", n, charger(n, t, COLONNES_VENTES, True)) for n, t in ventes_src]
    charges += [("s", n, charger(n, t, COLONNES_STOCK)) for n, t in stock_src]
    charges += [("d", n, charger(n, t, COLONNES_DELAIS)) for n, t in delais_src]
    if erreurs:
        raise Arret(" | ".join(erreurs))

    ventes, produits = {}, {}
    for _, nom, rows in [c for c in charges if c[0] == "v"]:
        for r in rows:
            cle = (r["reference"], r["lieu"])
            ventes[cle] = r["quantite_vendue_28j"]
            produits[r["reference"]] = r.get("produit", "")

    stock = {}
    for _, nom, rows in [c for c in charges if c[0] == "s"]:
        for r in rows:
            stock[(r["reference"], r["lieu"])] = r["stock_disponible"]

    delais = {}
    for _, nom, rows in [c for c in charges if c[0] == "d"]:
        for r in rows:
            delais[r["reference"]] = r["delai_jours"]

    d_calc = date.fromisoformat(date_calcul)
    D = (date.fromisoformat(prochaine_commande) - d_calc).days
    if D < 0:
        raise Arret("La prochaine commande est antérieure à la date du calcul.")

    cles = sorted(set(ventes) | set(stock))
    lignes = []
    for ref, lieu in cles:
        l = {"reference": ref, "produit": produits.get(ref, ""), "lieu": lieu,
             "stock": None, "vente_jour": None, "couverture_jours": None,
             "delai_jours": None, "date_rupture": None, "categorie": None}
        q = nombre(ventes.get((ref, lieu), "0"))
        s = nombre(stock[(ref, lieu)]) if (ref, lieu) in stock else None
        L = nombre(delais[ref]) if delais.get(ref, "") != "" else None
        l["stock"], l["delai_jours"] = s, L
        if (ref, lieu) not in stock:
            l["categorie"] = "Données incomplètes"
            controle["anomalies"].append(f"{ref} ({lieu}) : présente dans les ventes, absente du stock.")
        elif q is None or s is None:
            l["categorie"] = "Données incomplètes"
            controle["anomalies"].append(f"{ref} ({lieu}) : valeur vide ou non numérique.")
        elif q == 0:
            l["categorie"] = "Pas d'historique de vente"
            if (ref, lieu) not in ventes:
                controle["anomalies"].append(f"{ref} ({lieu}) : présente dans le stock, absente des ventes (comptée à 0 vente).")
        else:
            v = q / periode
            l["vente_jour"] = round(v, 2)
            if s == 0:
                l["categorie"], l["couverture_jours"] = "Déjà en rupture", 0
            else:
                c = math.floor(s / v)
                l["couverture_jours"] = c
                l["date_rupture"] = (d_calc + timedelta(days=c)).strftime("%d/%m")
                if L is None:
                    l["categorie"] = "Délai fournisseur inconnu"
                    controle["anomalies"].append(f"{ref} : aucun délai fournisseur.")
                elif c < D + L:
                    l["categorie"] = "Rupture imminente"
                elif c < D + L + MARGE_SURVEILLANCE:
                    l["categorie"] = "À surveiller"
                else:
                    l["categorie"] = "Sans risque"
        lignes.append(l)

    if len(lignes) != len(cles):
        raise Arret("Contrôle final : le nombre de lignes en sortie ne correspond pas à l'entrée.")

    par_cat = {c: sorted([l for l in lignes if l["categorie"] == c],
                         key=lambda x: (x["couverture_jours"] is None, x["couverture_jours"] or 0, x["reference"]))
               for c in ORDRE}
    return {
        "statut": "ok",
        "date_calcul": date_calcul,
        "prochaine_commande": prochaine_commande,
        "D": D,
        "periode_jours": periode,
        "controle": controle,
        "nb_lignes": len(lignes),
        "comptes": {c: len(par_cat[c]) for c in ORDRE} | {"Sans risque": sum(1 for l in lignes if l["categorie"] == "Sans risque")},
        "categories": par_cat,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--md")
    p.add_argument("--ventes", nargs="*", default=[])
    p.add_argument("--stock", nargs="*", default=[])
    p.add_argument("--delais", nargs="*", default=[])
    p.add_argument("--calendrier")
    p.add_argument("--date")
    p.add_argument("--prochaine-commande")
    p.add_argument("--periode", type=int, default=PERIODE_DEFAUT)
    a = p.parse_args()
    try:
        if a.md:
            ventes, stock, delais, d, cmd = parse_md(a.md)
            d = a.date or d
            cmd = a.prochaine_commande or cmd
        else:
            lire = lambda fs: [(f, open(f, encoding="utf-8").read()) for f in fs]
            ventes, stock, delais = lire(a.ventes), lire(a.stock), lire(a.delais)
            d = a.date or date.today().isoformat()
            cmd = a.prochaine_commande
            if not cmd and a.calendrier:
                _, rows = lire_csv(open(a.calendrier, encoding="utf-8").read(), a.calendrier)
                futures = sorted(r["date_commande"] for r in rows if r.get("date_commande", "") >= d)
                cmd = futures[0] if futures else None
        if not d:
            raise Arret("Date du calcul inconnue.")
        res = classer(ventes, stock, delais, d, cmd, a.periode)
    except Arret as e:
        print(json.dumps({"statut": "arret", "raison": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(2)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
