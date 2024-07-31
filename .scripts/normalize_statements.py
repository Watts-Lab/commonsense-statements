import pandas as pd
import os
from string import punctuation, whitespace
import re

def normalize_statement(statement, lng):
    # extract any and all substrings enclosed in quotation marks
    quoted_pattern = re.compile(r'["](.*?)["]') 
    quoted_substrings = quoted_pattern.findall(statement)

    # remove the quoted substrings from all substrings before cleaning
    cleaned = re.sub(quoted_pattern, lambda m: m.group(1), statement)

    # remove leading/trailing punctuation and excess whitespace
    cleaned = cleaned.strip(whitespace + punctuation) 
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # capitalize first letter for languages that use capitalization
    if cleaned and lng not in ['ar', 'bn', 'hi', 'ja', 'zh']:
        cleaned = cleaned[0].upper() + cleaned[1:]

    # ensure the statement ends with the appropriate punctuation
    if lng == 'ar':
        if cleaned and not cleaned.endswith('۔'): 
            cleaned += '۔'
    elif lng in ['bn', 'hi']:
        if cleaned and not cleaned.endswith('।'): 
            cleaned += '।'
    elif lng in ['ja', 'zh']:
        if cleaned and not cleaned.endswith('。'): 
            cleaned += '。'
    else:
        if cleaned and not cleaned.endswith('.'):
            cleaned += '.'

    # replace quoted substrings (if any) back into their original positions after cleaning
    for quoted_substring in quoted_substrings:
        print(f'quoted substring: {quoted_substring}\n')
        cleaned = re.sub(re.escape(quoted_substring.strip(whitespace + punctuation)), f'\"{quoted_substring}\"', cleaned) 
    
    print(f'cleaned: {cleaned}\n')
    return cleaned

# might need to clean separately depending on the language
def normalize_statements(directory):
    for filename in os.listdir(directory):
        if not filename.endswith(".csv"):
            continue

        lng = filename.split("_")[-1].split(".")[0]
        filepath = os.path.join(directory, filename)
        
        df = pd.read_csv(filepath)
        df['statement'] = df['statement'].apply(lambda x: normalize_statement(x, lng))
        df.to_csv(filepath, index=False)
        print(f"Processed and cleaned {filepath}")

    print("Finished cleaning statements")

if __name__ == "__main__":
    normalize_statements("raw_statements")


