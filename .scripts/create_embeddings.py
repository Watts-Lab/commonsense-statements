import pandas as pd
from openai import OpenAI
import os

# docs: https://platform.openai.com/docs/guides/embeddings/use-cases

# set up openai authentication credentials
client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)

# define paths
files = [
    'raw_statements/observable_gpt4o.csv',
    'raw_statements/news_statements_amir.csv', 
    'raw_statements/email_statements.csv'
]

# helper function for creating an embedding
def create_embedding(text, model='text-embedding-3-small'):
    response = client.embeddings.create(input = [text], model=model)
    return response.data[0].embedding

# embed the statement column for each file
for file in files:
    df = pd.read_csv(file)
    filename = os.path.splitext(file)[0]
    df['embedding'] = df['statement'].apply(lambda x: create_embedding(x, model='text-embedding-3-small'))
    df.to_csv(f'{filename}_embedding.csv', index=False)
    print('embedding created for', file)