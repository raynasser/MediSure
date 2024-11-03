import pandas as pd

import os

import json
import openai







def lower(text):
    try:
        return text.lower()
    except:
        return text







def ddi_tau_score(drug_a, drug_b, level):

    API_KEY = os.environ.get("API_KEY")


    client = openai.OpenAI(api_key=API_KEY)


    prompt = f"""
    You are tasked with determining the interaction mechanism between two drugs.
    The drugs are:
    - Drug A: {drug_a}
    - Drug B: {drug_b}

    The level of interaction is: {level}

    Based on this information, describe the interaction mechanism (inhibition, synergy, antagonism, etc.), and return a tau score that reflects the strength of the interaction. Return the result as a JSON object in the following format:
        {{
            "drug_a": "{drug_a}",
            "drug_b": "{drug_b}",
            "mechanism": "",
            "tau": 0
        }}
    Only return the JSON object.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )


        response_content = completion.choices[0].message.content
        print(f"Response for {drug_a} and {drug_b}: {response_content}")


        response_content = response_content.strip('```json').strip('```').strip()

        # Check if response is empty or invalid
        if not response_content.strip():
            print(f"Empty response for {drug_a} and {drug_b}")
            return {
                "drug_a": drug_a,
                "drug_b": drug_b,
                "mechanism": "unknown",
                "tau": 0
            }

        # Try to load the JSON response
        return json.loads(response_content)

    except (json.JSONDecodeError, KeyError) as e:
        # Handle JSON decode errors or missing keys
        print(f"Error processing response for {drug_a} and {drug_b}: {e}")
        return {
            "drug_a": drug_a,
            "drug_b": drug_b,
            "mechanism": "unknown",
            "tau": 0
        }

    except Exception as e:
        # Catch all other errors (e.g., connection issues)
        print(f"An error occurred: {e}")
        return {
            "drug_a": drug_a,
            "drug_b": drug_b,
            "mechanism": "unknown",
            "tau": 0
        }






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




    # # all_ddi50 = all_ddi.head(7)
    # print("Start getting ddi...")
    # all_ddi['Interaction_Details'] = all_ddi.apply(
    # lambda row: ddi_tau_score(row['Drug_A'],
    #                           row['Drug_B'],
    #                           row['Level']),
    # axis=1)



    # all_ddi[['drug_a_', 'drug_b_', 'mechanism', 'tau']] = all_ddi['Interaction_Details'].apply(pd.Series)
    # all_ddi.drop(columns= 'Interaction_Details', inplace= True)

    # output_path = os.path.join(ddi, 'ddi_results.csv')
    # all_ddi.to_csv(output_path, index=False)
    # print("Done")


    return all_ddi
