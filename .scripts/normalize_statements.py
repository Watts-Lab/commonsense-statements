import pandas as pd
import os
from string import punctuation, whitespace
import en_core_web_sm
import zh_core_web_sm
import fr_core_news_sm
import ja_core_news_sm
import pt_core_news_sm
import ru_core_news_sm
import es_core_news_sm

# load spaCy models for each supported language
nlp_en = en_core_web_sm.load(disable=['parser', 'ner', 'textcat', 'lemmatizer'])
nlp_zh = zh_core_web_sm.load(disable=['parser', 'ner', 'textcat', 'lemmatizer'])
nlp_fr = fr_core_news_sm.load(disable=['parser', 'ner', 'textcat', 'lemmatizer'])
nlp_ja = ja_core_news_sm.load(disable=['parser', 'ner', 'textcat', 'lemmatizer'])
nlp_pt = pt_core_news_sm.load(disable=['parser', 'ner', 'textcat', 'lemmatizer'])
nlp_ru = ru_core_news_sm.load(disable=['parser', 'ner', 'textcat', 'lemmatizer'])
nlp_es = es_core_news_sm.load(disable=['parser', 'ner', 'textcat', 'lemmatizer'])

language_models = {
    'en': nlp_en,
    'zh': nlp_zh,
    'fr': nlp_fr,
    'ja': nlp_ja,
    'pt': nlp_pt,
    'ru': nlp_ru,
    'es': nlp_es
}

def extract_quoted_substrings(text, lng):
    """
    Extracts all substrings enclosed in quotation marks from the input text
    
    Parameters:
    - text (str): the input text from which to extract quoted substrings
    - lng (str): the language code to indicate which spaCy model to use
    
    Returns:
    - quoted_substrings (list of str): a list of substrings that were enclosed in quotation marks
    """
    if lng in language_models:
        doc = language_models[lng](text) # tokenize text based on selected language
        quoted_substrings = [] # stores quoted substrings
        in_quote = False # flag to track whether the current position is inside a quote
        quote_char = None # stores the type of quote character
        current_quote = [] # list to accumulate tokens inside a quote

        for token in doc:
            if token.text in ["'", '"', '‘', '’', '“', '”']:
                # handle the opening of a quote
                if not in_quote:
                    in_quote = True
                    quote_char = token.text
                    current_quote = []
                # handle the closing of a quote
                elif in_quote and token.text == quote_char:
                    in_quote = False
                    quoted_substrings.append(''.join(current_quote).strip())
                    current_quote = []
            elif in_quote:
                current_quote.append(token.text_with_ws)
        
        return quoted_substrings
    else:
        # basic tokenization for unsupported languages
        quoted_substrings = []
        in_quote = False
        quote_char = None
        current_quote = []
        
        for char in text:
            if char in ["'", '"', '‘', '’', '“', '”']:
                if not in_quote:
                    in_quote = True
                    quote_char = char
                    current_quote = []
                elif in_quote and char == quote_char:
                    in_quote = False
                    quoted_substrings.append(''.join(current_quote).strip())
                    current_quote = []
            elif in_quote:
                current_quote.append(char)
        
        return quoted_substrings

def normalize_statement(statement, lng):
    """
    Function that standardizes a statement:
    - Capitalizes first word (if capitalization applies)
    - Removes leading/trailing punctuation
    - Ends statement in appropriate full-stop punctuation
    
    Parameters:
    - statement (str): the input statement to be normalized
    - lng (str): The language code indicating which spaCy model to use
    
    Returns:
    - cleaned (str): the normalized statement
    """
    # extract any and all substrings enclosed in quotation marks
    quoted_substrings = extract_quoted_substrings(statement, lng)
    quotes_map = {match: f'QUOTE{index}' for index, match in enumerate(quoted_substrings)}

    # replace quoted substrings with placeholders
    for quote, placeholder in quotes_map.items():
        statement = statement.replace(f'"{quote}"', placeholder).replace(f"'{quote}'", placeholder)

    # remove leading/trailing punctuation and excess whitespace
    cleaned = statement.strip(whitespace + punctuation) 
    
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

    # replace placeholders back with the original quoted substrings
    for quote, placeholder in quotes_map.items():
        cleaned = cleaned.replace(placeholder, f'"{quote}"')

    # ensure correct capitalization for the initial character if it was quoted
    if cleaned[0] == '"' and len(cleaned) > 1 and lng not in ['ar', 'bn', 'hi', 'ja', 'zh']:
        cleaned = cleaned[0] + cleaned[1].upper() + cleaned[2:]
    
    return cleaned

def process_files(directory):
    """
    Function that processes all files in the raw_statements directory
    
    Parameters:
    - directory (str): the directory containing the CSV files to be processed
    """
    files_cleaned = set()
    count = 0
    for filename in os.listdir(directory):
        count += 1
        if filename.endswith('.csv') and (filename.split('.')[0].split('_')[-1] == 'cleaned'):
            files_cleaned.add(filename)
    
    if count == len(files_cleaned):
        print("All files have already been cleaned.")
        return
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv") and filename not in files_cleaned:
            lng = filename.split("_")[-1].split(".")[0]
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            df['statement'] = df['statement'].apply(lambda x: normalize_statement(x, lng))

            df.to_csv(filepath, index=False)
            cleaned_filename = f"{os.path.splitext(filename)[0]}_cleaned.csv"
            cleaned_filepath = os.path.join(directory, cleaned_filename)
            os.rename(filepath, cleaned_filepath)
            print(f"Cleaned statements saved back to {filepath} and renamed file to {cleaned_filepath}")

    print("Finished cleaning statements")

if __name__ == "__main__":
    process_files("raw_statements")
