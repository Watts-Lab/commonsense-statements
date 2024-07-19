import os
import pandas as pd
import requests
import uuid
import sys

# set up authentication key and endpoint
azure_key = os.environ['AZURE_TRANSLATE_SERVICE_KEY']
endpoint = 'https://api.cognitive.microsofttranslator.com/'
location = 'eastus' 

# define the supported languages
languages = ['ar','bn','es','fr','hi','ja','pt','ru','zh']

# translate text via the Microsoft Translator's REST API 
# api doc: https://learn.microsoft.com/en-us/azure/ai-services/translator/quickstart-text-rest-api?tabs=python
def translate_text(text, tgt_lng):
    path = '/translate?api-version=3.0'
    params = '&to=' + tgt_lng
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': azure_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-Type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    response = requests.post(constructed_url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()
    return result[0]['translations'][0]['text']

# translate each file
def translate_files(files, elicitation, committer):
    for file in files:
        df = pd.read_csv(file)
        for lng in languages:
            translated_statements = df['statement'].apply(lambda x: translate_text(x, lng))
            translated_df = df.copy()
            translated_df['statement'] = translated_statements
            translated_df['elicitation'] = elicitation
            translated_df['committer'] = committer

            filename = os.path.splitext(file)[0]
            translated_file = f'{filename}_{lng}.csv'
            translated_df.to_csv(translated_file, index=False)

            print(f'Translated {file} to {lng} and saved as {translated_file}')

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python translate.py <comma-separated list of files> <elicitation> <committer>")
        sys.exit(1)

    files = sys.argv[1]
    files = files[0].split(',')
    files = [file.strip() for file in files]
    elicitation = sys.argv[2]
    committer = sys.argv[3]

    translate_files(files, elicitation, committer)
