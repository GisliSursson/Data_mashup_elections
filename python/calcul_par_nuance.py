import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import random

# Script servant à calcul le total des voix par nuance politique
# Auteur : Victor Meynaud
# -*- coding: utf-8 -*-

# Read recipe inputs
tour = dataiku.Dataset("2002_2t_nuancier_2")
tour_df = tour.get_dataframe()

# On récupère tous les intitulés de colonne
liste_col = tour_df.keys()
liste_nuance = []
liste_resul = []

# Nuances selon Wikipédia
set_nuance = ['extrême gauche','communisme - gauche radicale','socialisme','divers gauche',
                'centre', 'droites','extrême droite', 'divers droite']

# On ne garde que les colonnes où on trouve le mot "nuance"
for element in liste_col:
    if "nuance" in element:
        liste_nuance.append(element)
 
# On cible les colonnes où sont indiqués les résultats       
for element in liste_col:
    if "Voix/Exp" in element:
        liste_resul.append(element)

# On insère une colonne par nuance
for element in set_nuance:
    tour_df.insert(0, element, None)

for count, col in enumerate(liste_nuance):
    cible = tour_df[col]
    for index, cell in enumerate(cible):
        # Pour chaque nuance
        for element in set_nuance:
            # On cherche la mention de la nuance dans les colonnes de résultat
            if cell == element:
                col_resul = tour_df[liste_resul[count]]
                resul = float(col_resul[index])
                # Si la nuance n'a pas été rencontrée, on l'inscrit une 1ere fois
                if tour_df[element][index] is None:
                    tour_df[element][index] = resul
                # Si la nuance a déjà été rencontrée, on l'additionne avec le chiffre existant
                else:
                    tour_df[element][index] += resul
    

# Write recipe outputs
sortie = dataiku.Dataset("2002_2t_par_nuance")
sortie.write_with_schema(tour_df)