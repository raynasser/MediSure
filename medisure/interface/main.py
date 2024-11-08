# VM


import pandas as pd
import os
from transformers import pipeline
import json
import openai
from google.cloud import storage


def lower(text):
    try:
        return text.lower()
    except:
        return text


def summarize(text):
    pipe = pipeline('summarization', model='sshleifer/distilbart-xsum-12-6')

    try:
        summary = pipe(text)
        return summary[0]['summary_text']
    except:
        return ""


def tau_score(text):

    API_KEY = os.environ.get("API_KEY")


    client = openai.OpenAI(api_key=API_KEY)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "assistant", "content": """
            You are tasked with elevating interaction between food and drugs from a summary from a study document.
            Analyze and identify the food and the drug in the text and the kind of relationship between the two of them (improving health, neutral, degrading health).
            Return a tau score that will reflect the power of the interaction between the 2 elements and also if it's negative or positive.
            Return the result through a JSON object in the following format:
                {
                    "food": "",
                    "drug": "",
                    "relationship": "",
                    "tau": 0
                }
            Return only the JSON object.
            """},
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(completion.choices[0].message.content)





def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def get_summarization():
    bucket_name = 'foodrug'
    local_foodrug_tm = 'TM_interactions.csv'
    local_foodrug_texts = 'texts.csv'


    download_blob(bucket_name, 'TM_interactions.csv', local_foodrug_tm)
    download_blob(bucket_name, 'texts.csv', local_foodrug_texts)


    foodrug_TM_interactions = pd.read_csv(local_foodrug_tm, index_col='Unnamed: 0')
    foodrug_texts = pd.read_csv(local_foodrug_texts, index_col='Unnamed: 0')
    foodrug_texts.drop(columns=['link', 'citation'], inplace=True)



    fdi_pre = foodrug_texts.merge(foodrug_TM_interactions, on="texts_ID")
    fdi_pre["food"] = fdi_pre.food.map(lower)
    fdi_pre["drug"] = fdi_pre.drug.map(lower)
    fdi_pre["clean_text"] = fdi_pre.apply(lambda x: x["document"][int(x["start_index"]):int(x["end_index"])], axis=1)
    fdi_map = fdi_pre.groupby(by="texts_ID").agg({
        "food": lambda x: x.mode()[0],
        "drug": lambda x: x.mode()[0],
        "clean_text": lambda x: '. '.join(x)
    }).reset_index()



    print("Start Summarization...")
    fdi_map["summarize"] = fdi_map.clean_text.map(summarize)


    output_path = 'fdi_summarization_results.csv'
    fdi_map.to_csv(output_path, index=False)
    upload_blob(bucket_name, output_path, 'fdi_summarization_results.csv')
    print("Done")

    return fdi_map






def get_tau_score(fdi_map):
    bucket_name = 'foodrug'
    output_path = 'fdi_tau_results.csv'

    print("Start TAU scoring...")
    fdi_map["tau"] = fdi_map.summarize.map(tau_score)
    fdi_map[['food_', 'drug_', 'relationship', 'tau_score']] = fdi_map['tau'].apply(pd.Series)
    fdi_map.drop(columns='tau', inplace=True)

    fdi_map.to_csv(output_path, index=False)
    upload_blob(bucket_name, output_path, 'fdi_tau_results.csv')
    print("Done")

    return fdi_map


if __name__ == '__main__':
    fdi_map = get_summarization()
    #get_tau_score(fdi_map)
