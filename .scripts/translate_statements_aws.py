import os
import pandas as pd
import boto3
import sys

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

# translate text via a call to AWS API 
# api doc: https://docs.aws.amazon.com/translate/latest/APIReference/API_TranslateText.html
def translate_text(text, tgt_lng):
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=tgt_lng
    )
    return result['TranslatedText']

# function that translates each file
def translate_files(files, elicitation, committer):
    total_characters = 0
    for file in files:
        df = pd.read_csv(file)
        for lng in languages:
            translated_statements = df['statement'].apply(lambda x: translate_text(x, lng))
            total_characters += df['statement'].apply(len).sum() # accumluate the total number of characters translated
            translated_df = df.copy()
            translated_df['statement'] = translated_statements
            translated_df['elicitation'] = elicitation
            translated_df['committer'] = committer

            filename = os.path.splitext(file)[0]
            translated_file = f'{filename}_{lng}.csv'
            translated_df.to_csv(translated_file, index=False)

            print(f'Translated {file} to {lng} and saved as {translated_file}')

    return total_characters

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python ./.scripts/translate_statements_aws.py <comma-separated list of files> <elicitation> <committer>")
        sys.exit(1)

    files = sys.argv[1]
    files = files.split(',')
    files = [f'raw_statements/{file.strip()}' for file in files]
    elicitation = sys.argv[2]
    committer = sys.argv[3]

    print(f"File: {files}")
    print(f"Elicitation: {elicitation}")
    print(f"Committer: {committer}")

    total_characters = translate_files(files, elicitation, committer)
    total_cost = (total_characters / 1000000) * 15.00
    print(f"Total characters translated: {total_characters}")
    print(f"Total cost for translation: ${total_cost:.2f}")