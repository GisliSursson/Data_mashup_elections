import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Script servant à obtenir les numéros de département selon leur format habituel (deux chiffres)
# Ce script est utilisé pour pallier le fait que Dataiku considère les numéros de département inférieurs à 10 comme des nombres et
# les exprime comme décimaux, ce qui pose des problèmes pour joindre les datasets. 
# Auteur : Victor Meynaud
# -*- coding: utf-8 -*-

# On cible le dataset source
tour = dataiku.Dataset("2002_2t_nuancier")
tour_df = tour.get_dataframe()

try:
    for cell in tour_df["code_dep"]:
        print(cell)
        # Si le numéro de département est inférieur à 10, on l'exprime sous la forme "0X". On le met en str pour éviter que Dataiku
        # le convertisse en float.
        if float(cell) < 10:
            remp = "0" + str(int(cell))
            tour_df["code_dep"] = tour_df["code_dep"].replace(cell, remp)
        # Si le numéro de département est supérieur à 10, on le met en str. 
        elif int(cell) >= 10:
            remp = str(int(cell))
            tour_df["code_dep"] = tour_df["code_dep"].replace(cell, remp)
except ValueError: # Pour la Corse
    pass

# Write recipe outputs
sortie = dataiku.Dataset("2002_2t_nuancier_2")
sortie.write_with_schema(tour_df)