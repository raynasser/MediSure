import pandas as pd

import os

from transformers import pipeline

import requests
import json
import openai


import re




def lower(text):
    try:
        return text.lower()
    except:
        return text






def extract_medication_info(med_str):
    # Updated regular expression to capture the name (with special characters), optional dosage, and form
    # pattern = r'^([a-zA-Z\s]+)\s([\dmg/]+)\s*(.*)$'
    pattern = r'^([a-zA-Z\s\-]+)\s*(\d*mg)?\s*(.*)$'
    # pattern = r'^([\w\s\-\u00C0-\u02AF]+)\s*(\d*mg|\d+)?\s*(.*)$'
    match = re.match(pattern, med_str)

    if match:
        name = match.group(1).strip()
        dosage = match.group(2).strip() if match.group(2) else ""
        form = match.group(3).strip()
        return pd.Series([name, dosage, form])
    return pd.Series([None, None, None])





def clean_name():

    raw = '/Users/raynasser/code/raynasser/MediSure/data/raw_data/'


    medi = pd.read_csv(os.path.join(raw, 'medicine_dataset.csv'))#, index_col='id')


    medi.applymap(lower)


    medi = medi.drop_duplicates(subset='name', keep='last').reset_index(drop=True)

    # medi = medi.head(7)

    medi[['name_', 'dosage', 'form']] = medi['name'].apply(extract_medication_info)

    # df[['SMILES', 'InChI', 'InChIKey']] = df['drug'].apply(lambda x: pd.Series(fetch_chemical_info(x)))


    output_path = os.path.join(raw,'medi_name.csv')
    medi.to_csv(output_path, index=False)

    return medi






def ddi_drugs_key():

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




    # all_ddi = all_ddi.head(7)
    print("Start fetching chemical identifiers...")
    all_ddi[['Drug_A_SMILES', 'Drug_A_InChI', 'Drug_A_InChIKey']] = all_ddi['Drug_A'].apply(lambda x: pd.Series(fetch_chemical_info(x)))
    all_ddi[['Drug_B_SMILES', 'Drug_B_InChI', 'Drug_B_InChIKey']] = all_ddi['Drug_B'].apply(lambda x: pd.Series(fetch_chemical_info(x)))
    # Save the updated dataframe with new columns
    output_path = os.path.join(ddi, 'drugsKey_results.csv')
    all_ddi.to_csv(output_path, index=False)
    print(f"Done")

    return all_ddi





def main(file_path):
    drugs_key = uniq_drugs_key()
    # drugs_key_ddi = ddi_drugs_key()
    print(drugs_key)
    # print(drugs_key_ddi)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process drug data and fetch chemical information.")
    parser.add_argument('--file', type=str, help='Path to the unique drugs CSV file', required=False)
    args = parser.parse_args()

    main(args.file)
