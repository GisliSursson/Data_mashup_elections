# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
tour = dataiku.Dataset("2017_1t_prepared")
tour_df = tour.get_dataframe()

tour_df.columns = tour_df.columns.str.replace('ok_', '')



# Write recipe outputs
sortie = dataiku.Dataset("2017_1t_renamed_prepared")
sortie.write_with_schema(tour_df)
