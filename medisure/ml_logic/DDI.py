import pandas as pd

import os

from transformers import pipeline

import requests
import json
import openai







def lower(text):
    try:
        return text.lower()
    except:
        return text











def ddi_data():

    ddi = '/Users/raynasser/code/raynasser/MediSure/data/raw_data/drugs_allergic_interaction'


    ddi_a = pd.read_csv(os.path.join(ddi, 'A_alimentary_tract_metabolism_drugs.csv'))#, index_col='id')
    ddi_b = pd.read_csv(os.path.join(ddi, 'B_blood_drugs.csv'))#, index_col='id')
    ddi_d = pd.read_csv(os.path.join(ddi, 'D_dermatologicals_drugs.csv'))#, index_col='id')
    ddi_h = pd.read_csv(os.path.join(ddi, 'H_hormonal_drugs.csv'))#, index_col='id')
    ddi_l = pd.read_csv(os.path.join(ddi, 'L_antineoplastic_immunomodulating_agents_drugs.csv'))#, index_col='id')
    ddi_p = pd.read_csv(os.path.join(ddi, 'P_antiparasitic_insecticides_repellents_drugs.csv'))#, index_col='id')
    ddi_r = pd.read_csv(os.path.join(ddi, 'P_antiparasitic_insecticides_repellents_drugs.csv'))#, index_col='id')
    ddi_v = pd.read_csv(os.path.join(ddi, 'P_antiparasitic_insecticides_repellents_drugs.csv'))#, index_col='id')


    all_ddi = pd.concat([ddi_a, ddi_b, ddi_d, ddi_h, ddi_l, ddi_p, ddi_r, ddi_v], ignore_index=True)


    all_ddi.drop_duplicates(inplace=True)

    all_ddi = all_ddi.applymap(lower)

    ......


    return all_ddi
