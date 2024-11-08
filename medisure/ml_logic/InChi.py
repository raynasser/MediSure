import pandas as pd

import os

import requests

import argparse





def lower(text):
    try:
        return text.lower()
    except:
        return text








# def fetch_chemical_info(drug_name):
#     base_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{drug_name}/property/IsomericSMILES,InChI,InChIKey/JSON"

#     try:
#         # Set a timeout of 10 seconds for the request
#         response = requests.get(base_url, timeout=10)

#         # Check if the request was successful
#         if response.status_code == 200:
#             try:
#                 data = response.json()
#                 properties = data['PropertyTable']['Properties'][0]
#                 smiles = properties.get('IsomericSMILES', 'Not Found')
#                 inchi = properties.get('InChI', 'Not Found')
#                 inchikey = properties.get('InChIKey', 'Not Found')
#                 return smiles, inchi, inchikey
#             except (KeyError, IndexError):
#                 return 'Not Found', 'Not Found', 'Not Found'
#         else:
#             # Handle non-200 status codes
#             print(f"Error: Unable to fetch data for {drug_name}. Status code: {response.status_code}")
#             return 'Not Found', 'Not Found', 'Not Found'

#     except requests.exceptions.Timeout:
#         print(f"Error: Request timed out for {drug_name}")
#         return 'Not Found', 'Not Found', 'Not Found'

#     except requests.exceptions.RequestException as e:
#         print(f"Error: An error occurred while fetching data for {drug_name}: {e}")
#         return 'Not Found', 'Not Found', 'Not Found'




base_url = "https://cactus.nci.nih.gov/chemical/structure/{}/inchikey"


def fetch_chemical_info(drug_name):
    try:

        drug_encoded = drug_name.replace(' ', '%20')


        response = requests.get(base_url.format(drug_encoded))

        if response.status_code == 200:
            inchi_key = response.text.strip().replace('InChIKey=', '')
            return pd.Series([None, None, inchi_key])
        else:
            return pd.Series([None, None, None])

    except Exception as e:
        print(f"{drug_name}: Error - {e}")
        return pd.Series([None, None, None])





def uniq_drugs_key():

    raw = '/Users/raynasser/code/raynasser/MediSure/data/raw_data/'
    foodrug = '/Users/raynasser/code/raynasser/MediSure/data/raw_data/FooDru'


    uniq_drugs = pd.read_csv(os.path.join(foodrug, 'fdi_drugs.csv'))
    # uniq_drugs.drop(columns=['Unnamed: 0', 'ID'], inplace=True)

    uniq_drugs = uniq_drugs.applymap(lower)


    df = uniq_drugs.drop_duplicates()

    # df = df.head(7)

    df[['SMILES', 'InChI', 'InChIKey']] = df['drug'].apply(lambda x: pd.Series(fetch_chemical_info(x)))


    output_path = '/Users/raynasser/code/raynasser/MediSure/data/raw_data/fdi_drugs_key.csv'
    df.to_csv(output_path, index=False)

    return df






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
