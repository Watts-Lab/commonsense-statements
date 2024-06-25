import os
import pandas as pd
import boto3

# set up authentication key and endpoint
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
region_name = 'us-east-1' 

# initialize amazon translate client
translate_client = boto3.client(
    service_name='translate', 
    aws_access_key_id=aws_access_key_id, 
    aws_secret_access_key=aws_secret_access_key, 
    region_name=region_name
)

# define the supported languages
languages = ['ar','bn','es','fr','hi','ja','pt','ru','zh']

# define paths
files = [
    'raw_statements/email_statements.csv'
]

# translate text via a call to AWS API 
# api doc: https://docs.aws.amazon.com/translate/latest/APIReference/API_TranslateText.html
def translate_text(text, tgt_lng):
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=tgt_lng
    )
    print('TranslatedText: ' + result.get('TranslatedText'))
    return result['TranslatedText']

# translate each file
for file in files:
    df = pd.read_csv(file)
    for lng in languages:
        translated_statements = df['statement'].apply(lambda x: translate_text(x, lng))
        translated_df = df.copy()
        translated_df['statement'] = translated_statements
        translated_df['elicitation'] = 'amazon translate'
        translated_df['committer'] = 'Dan'

        filename = os.path.splitext(file)[0]
        translated_file = f'{filename}_{lng}.csv'
        translated_df.to_csv(translated_file, index=False)

        print(f'Translated {file} to {lng} and saved as {translated_file}')
