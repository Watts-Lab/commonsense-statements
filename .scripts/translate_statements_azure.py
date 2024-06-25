import os
import pandas as pd
import requests
import uuid

# set up authentication key and endpoint
azure_key = os.environ['AZURE_TRANSLATE_SERVICE_KEY']
endpoint = 'https://api.cognitive.microsofttranslator.com/'
location = 'eastus' 

# define the supported languages
languages = ['ar','bn','es','fr','hi','ja','pt','ru','zh']

# define paths
files = [
    'raw_statements/news_statements_amir.csv', 
    'raw_statements/observable_gpt4o.csv'
]

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
for file in files:
    df = pd.read_csv(file)
    for lng in languages:
        translated_statements = df['statement'].apply(lambda x: translate_text(x, lng))
        translated_df = df.copy()
        translated_df['statement'] = translated_statements
        translated_df['elicitation'] = 'microsoft azure text translation'
        translated_df['committer'] = 'Dan'

        filename = os.path.splitext(file)[0]
        translated_file = f'{filename}_{lng}.csv'
        translated_df.to_csv(translated_file, index=False)

        print(f'Translated {file} to {lng} and saved as {translated_file}')
