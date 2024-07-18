import pandas
import os
import sys
from string import punctuation
import re

def exit_error(message):
    print("Exiting:", message)
    sys.exit(1)

def clean_statement_regular(statement):
    # remove any leading/trailing punctuation and whitespace
    cleaned = statement.lstrip(punctuation).rstrip(punctuation).strip()

    # ensure only the first letter is capitalized
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:]

    # ensure the statement ends in a period
    if cleaned and not cleaned.endswith("."):
        cleaned += "."
    
    return cleaned

# might need to clean separately depending on the language
def clean_statements(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            try:
                df = pandas.read_csv(filepath)
                df['statement'] = df['statement'].apply(clean_statement_regular)

                # save the cleaned data back to the csv
                df.to_csv(filename, index=False)
                print(f"Processed and cleaned {filename}")
            except Exception as e:
                exit_error(f"Error processing {filename}: {e}")

    print("Finished cleaning")

if __name__ == "__main__":
    # res = clean_statement_regular("this IS a tEst sentence....,")
    # print(res)
    clean_statements("raw_statements")


