import os
import pandas as pd
import requests
import uuid
import argparse

# set up authentication key and endpoint
azure_key = os.environ.get('AZURE_TRANSLATE_SERVICE_KEY')
endpoint = 'https://api.cognitive.microsofttranslator.com/'
location = 'eastus' 

# define the supported languages
languages = ['ar','bn','es','fr','hi','ja','pt','ru','zh']

"""
Function that translates text to the given target language

Parameters:
- text: the text to be translated
- tgt_lng: the target language code

Returns: the translated text

API reference: https://learn.microsoft.com/en-us/azure/ai-services/translator/quickstart-text-rest-api?tabs=python
"""
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

"""
Function to translate each statement in multiple CSV files and save them to raw_statements folder

Parameters: 
- files: list of CSV files to be translated
- elicitation: the elicitation method
- committer: the committer's name

Returns: the total number of characters translated (for API cost calculation)
"""
def translate_files(files, elicitation, committer):
    total_characters = 0

    for file in files:
        df = pd.read_csv(file)
        for lng in languages:
            translated_statements = df["statement"].swifter.progress_bar(enable=True).apply(lambda x: translate_text(x, lng))
            total_characters += df['statement'].apply(len).sum() # accumluate the total number of characters translated
            translated_df = df.copy()
            translated_df['statement'] = translated_statements
            translated_df['elicitation'] = elicitation
            translated_df['committer'] = committer

            basename = os.path.basename(file) # ie. raw_statements/email_statements_en.csv --> email_statements_en.csv
            match = re.search(r'(.*)_[a-z]{2}(?:_cleaned)?\.csv', basename) # extract the part before the language code
            if match:
                filename = match.group(1)
            else:
                filename = None
            translated_file = f'raw_statements/{filename}_{lng}.csv' # e.g. raw_statements/email_statements_ar.csv
            translated_df.to_csv(translated_file, index=False)
            print(f"Translated {file} to {lng} and saved as {translated_file}")

    return total_characters

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Translate statements to multiple languages using AWS Translate')
    parser.add_argument('files', type=str, help='comma-separated list of files')
    parser.add_argument('elicitation', type=str, help='the elicitation method')
    parser.add_argument('committer', type=str, help='the committer\'s name')

    args = parser.parse_args()
    files = args.files
    files = files.split(',')
    files = [f'raw_statements/{file.strip()}' for file in files]
    elicitation = args.elicitation
    committer = args.committer

    print(f"File: {files}") 
    print(f"Elicitation: {elicitation}")
    print(f"Committer: {committer}")

    total_characters = translate_files(files, elicitation, committer)
    total_cost = (total_characters / 1000000) * 15.00
    print(f"Total characters translated: {total_characters}")
    print(f"Total cost for translation: ${total_cost:.2f}")