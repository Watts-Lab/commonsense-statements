import pandas as pd
import os
import ast
import sys

# create a new directory to store the cleaned statements
os.makedirs('raw_statements_cleaned', exist_ok=True)

# function that removes duplicate statements across files and their corresponding translation files
def remove_duplicates(original_csv, duplicate_statements, translated_statements):
    indices_to_remove = set() 
    original_df = pd.read_csv(original_csv)

    for duplicate_csv in duplicate_statements:
        duplicate_df = pd.read_csv(duplicate_csv)

        for i in range(0, len(duplicate_df)): 
            group = ast.literal_eval(duplicate_df.at[i, 'line_and_statement'])
            min_length = sys.maxsize
            index_to_not_remove = -1

            # remove the longest statements, keep the shortest one
            for line_number in group.keys():
                original_statement = original_df.at[int(line_number) - 2, 'statement']
                if len(original_statement) < min_length:
                    min_length = len(original_statement)
                    index_to_not_remove = int(line_number) - 2

            for line_number in group.keys():
                if int(line_number) - 2 != index_to_not_remove:
                    indices_to_remove.add(int(line_number) -2)
    
    # remove the duplicate indices from the translated CSVs
    for translated_csv in translated_statements:
        translated_df = pd.read_csv(translated_csv)
        translated_df = translated_df.drop(list(indices_to_remove))
        translated_df.reset_index(drop=True)
        translated_output_file = 'raw_statements_cleaned/' + os.path.basename(translated_csv)
        translated_df.to_csv(translated_output_file, index=False)
        print(f"Cleaned original file has been saved to {translated_output_file}")
        print(f"removed {len(indices_to_remove)} duplicates")
        print('-----------------')

    # drop duplicate indices from the original CSV
    original_df = original_df.drop(list(indices_to_remove))
    original_df.reset_index(drop=True)
    original_output_file = 'raw_statements_cleaned/' + os.path.basename(original_csv)
    original_df.to_csv(original_output_file, index=False)
    print(f"Cleaned original file has been saved to {original_output_file}")
    print(f"removed {len(indices_to_remove)} duplicates")
    print('-----------------')

# function that tests the number of lines across files is the same
def test_line_numbers(original_csv, translated_statements):
    original_df = pd.read_csv(original_csv)
    original_lines = len(original_df)

    for translated_csv in translated_statements:
        translated_df = pd.read_csv(translated_csv)
        translated_lines = len(translated_df)
        if (translated_lines != original_lines):
            print(f"Error: {translated_csv} has a different number of lines compared to {original_csv}")
            return False
    print("All files have the same number of lines")
    return True

if __name__ == "__main__":
    languages = ['ar','bn','es','fr','hi','ja','pt','ru','zh']

    observable_translated_statements = [f'raw_statements/observable_gpt4o_{language}.csv' for language in languages]
    observable_duplicate_statements = [f'duplicate_statements/observable_gpt4o_{language}_duplicates.csv' for language in languages]

    email_translated_statements = [f'raw_statements/email_statements_{language}.csv' for language in languages]
    email_duplicate_statements = [f'duplicate_statements/email_statements_{language}_duplicates.csv' for language in languages]

    remove_duplicates('raw_statements/observable_gpt4o.csv', 
                  observable_duplicate_statements, 
                  observable_translated_statements)

    remove_duplicates('raw_statements/email_statements.csv', 
                    email_duplicate_statements, 
                    email_translated_statements)
    
    observable_translated_statements_cleaned = [f'raw_statements_cleaned/observable_gpt4o_{language}.csv' for language in languages]
    email_translated_statements_cleaned = [f'raw_statements_cleaned/email_statements_{language}.csv' for language in languages]

    test_line_numbers('raw_statements_cleaned/observable_gpt4o.csv', observable_translated_statements_cleaned)
    test_line_numbers('raw_statements_cleaned/email_statements.csv', email_translated_statements_cleaned)
