# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
nom_coor_insee_filtre_corse = dataiku.Dataset("nom_coor_insee_filtre_corse_prepared")
df = nom_coor_insee_filtre_corse.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

# Obtention de tous les codes Insee
liste_insee = []
for element in df["num_insee"]:
    liste_insee.append(element)
set_insee = set(liste_insee)

for element in set_insee:
    element_str = str(element)
    # Extraction du code postal (valable aussi pour la Corse) et traitement particulier pour l'Outre-Mer
    if element_str[:2] != "97":
        cible = element_str[:2]
    # Traitement particulier pour l'Outre-Mer
    else:
        cible = element_str[:3]
    # Modification du DF par rechercher/remplacer
    df = df.replace(element, cible)


# Write recipe outputs
nom_coor_corse_dep = dataiku.Dataset("nom_coor_corse_dep")
nom_coor_corse_dep.write_with_schema(df)

