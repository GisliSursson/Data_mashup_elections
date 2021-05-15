# Script servant à associer un politique avec son orientation politque
# Auteur : Victor Meynaud
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import random

# Read recipe inputs
tour = dataiku.Dataset("2002_1t_prepared")
tour_df = tour.get_dataframe()
nuancier_csv = dataiku.Dataset("nuancier_csv")
nuancier_csv_df = nuancier_csv.get_dataframe()


# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

# On récupère tous les intitulés de colonne
liste_col = tour_df.keys()
liste_noms = []


# On ne garde que les intitulés qui contiennent la str "Nom"
for element in liste_col:
    if "Nom" in element:
        liste_noms.append(element)
        
# Attention à alterner entre les upper et les lower selon le tableau du tour en entrée

# On crée une liste des uniques de tous les noms dans le DF
set_noms = []
for col in liste_noms:
    col_cible = tour_df[col]
    for nom in col_cible:
        set_noms.append(nom.lower())
set_noms = set(set_noms)

# On remplace chaque nom par nom + nuance dans tout le DF
for nom in set_noms:
    # Syntaxe permettant d'obtenir la 1ere cellule d'une colonne
    remp = nuancier_csv_df[nom].iloc[0] + ";" + nom
    tour_df = tour_df.replace(nom.upper(), remp)

# Pour toutes les colonnes avec "Nom" dans leur intitulé
for col in liste_noms:
    cible = tour_df[col]
    # Chaque colonne ciblée est splitée sur ";" (ce qui donne 2 colonnes)
    nouv = cible.str.split(";", n = 1, expand=True)
    # Noms des nouvelles colonnes
    nouv_col_zero = col + "_nuance"
    nouv_col_un = col + "_traite"
    # On insère la 1ere colonne splitée (nuance) dans le dataframe à côté de la colonne originale pour plus de clarté
    tour_df.insert(tour_df.columns.get_loc(col) + 1, nouv_col_zero, nouv[0], allow_duplicates=True)
    # Idem avec la 2e colonne splitée (nom) 
    tour_df.insert(tour_df.columns.get_loc(nouv_col_zero) + 1, nouv_col_un, nouv[1], allow_duplicates=True)
    # On supprime la colonne originale split qui est devenue inutile
    tour_df.drop(columns = col, inplace = True) 
    

# Write recipe outputs
sortie = dataiku.Dataset("2002_1t_nuancier")
sortie.write_with_schema(tour_df)
