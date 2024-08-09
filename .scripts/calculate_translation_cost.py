import os
import pandas as pd
import json
import boto3
from botocore.config import Config
import sys

# define the supported languages
languages = ['ar','bn','es','fr','hi','ja','pt','ru','zh']

# set up credentials
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

# set up configuration details
my_config = Config(
    region_name = 'us-east-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10
    }
)

# set up boto3 client
client = boto3.client(
        'pricing', 
        config=my_config,
        aws_access_key_id=aws_access_key_id, 
        aws_secret_access_key=aws_secret_access_key 
)

def exit_error(message):
    print("Exiting:", message)
    sys.exit(1)

"""
Function that retrieves up-to-date pricing information dynamically via the AWS Price List Query API

Returns: price per character (float)
"""
def get_price_per_character():
    response = client.get_products(
        ServiceCode='translate',
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'productFamily',
                'Value': 'Text Translation'
            }
        ],
        FormatVersion='aws_v1'
    )

    for price_item in response['PriceList']:
        price_item_json = json.loads(price_item)
        for term in price_item_json['terms']['OnDemand'].values():
            for price_dimension in term['priceDimensions'].values():
                if price_dimension['unit'] == 'Character':
                    price_per_character = float(price_dimension['pricePerUnit']['USD'])
                    return price_per_character

    raise Exception("Unable to find the price for Amazon Translate.")


"""
Function to compute the cost of translating each non-translated CSV file in raw_statements 

Parameters: 
- directory: represents raw_statements directory
"""
def total_cost(directory): 
    files_translated = set()
    count = 0
    for filename in os.listdir(directory):
        count += 1
        if filename.endswith('.csv') and (filename.split('.')[0].split('_')[-1] in languages or filename.split('.')[0].split('_')[-2] in languages):
            files_translated.add('_'.join(filename.split('.')[0].split('_')[:-1]) + '.csv')
            files_translated.add(filename)
    
    if count == len(files_translated):
        print("All files have been translated in all languages.")
        return

    for filename in os.listdir(directory):
        if filename.endswith('.csv') and (filename not in files_translated):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            
            # Amazon Translate pricing: https://aws.amazon.com/translate/pricing/
            total_characters_for_file = df['statement'].apply(len).sum() * len(languages)
            
            try:
                cost_per_character = get_price_per_character()
                total_cost = total_characters_for_file * cost_per_character
                print(f"{filename} still needs to be translated in 9 new languages. This would require translating {total_characters_for_file} characters." )
                print(f"It will cost approximately ${total_cost:.2f} to complete these translations.")
                print('-----------------')
            except Exception as e:
                exit_error(f"Error: {e}")

if __name__ == "__main__":
    total_cost("raw_statements")
    