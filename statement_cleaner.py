import os
import pandas as pd
import openai

# Set up constants (input and output filenames)
INPUT_CSV = "./extracted_statements/election_emails/extracted_statements.csv"
OUTPUT_CSV = "input_out.csv"

openai.api_key = os.environ["OPENAI_API_KEY"]


def process_line(line):
    """Process a line of text using the OpenAI API."""
    print("Processing line:", line)
    return


df = pd.read_csv(INPUT_CSV)


df["processed"] = df["statements"].apply(process_line)


df.to_csv(OUTPUT_CSV, index=False)

print(f"Processed data saved to {OUTPUT_CSV}")
