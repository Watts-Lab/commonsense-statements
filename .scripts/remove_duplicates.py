import pandas as pd
import os
import ast
import sys

"""
Function to remove duplicate statements across files and their corresponding translation files

Parameters:
- original_csv: path to the original CSV file containing statements
- duplicate_statements: list of paths to CSV files containing duplicate statements information
- translated_statements: list of paths to translated CSV files corresponding to the original file
"""
def remove_duplicates(original_csv, duplicate_statements, translated_statements):
    indices_to_remove = set() 
    original_df = pd.read_csv(original_csv)

    for duplicate_csv in duplicate_statements:
        if not os.path.exists(duplicate_csv):
            continue

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
    
    if indices_to_remove:
        # remove the duplicate indices from the translated CSVs
        for translated_csv in translated_statements:
            translated_df = pd.read_csv(translated_csv)
            translated_df = translated_df.drop(list(indices_to_remove))
            translated_df.reset_index(drop=True)
            translated_output_file = f'raw_statements/{os.path.basename(translated_csv)}'
            translated_df.to_csv(translated_output_file, index=False)
            print(f"Cleaned original file has been saved to {translated_output_file}")
            print(f"removed {len(indices_to_remove)} duplicates")
            print('-----------------')

        # drop duplicate indices from the original CSV
        original_df = original_df.drop(list(indices_to_remove))
        original_df.reset_index(drop=True)
        original_output_file = f'raw_statements/{os.path.basename(original_csv)}'
        original_df.to_csv(original_output_file, index=False)
        print(f"Cleaned original file has been saved to {original_output_file}")
        print(f"removed {len(indices_to_remove)} duplicates")
        print('-----------------')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ./.scripts/remove_duplicates.py <comma-separated list of files>")
        sys.exit(1)

    files = sys.argv[1]
    files = files.split(',')
    files = [file.strip().split('.')[0] for file in files]
    print(f'files: {files}')
    languages = ['ar','bn','es','fr','hi','ja','pt','ru','zh']

    for file in files:
        translated_statements = [f'raw_statements/{file}_{language}.csv' for language in languages]
        duplicate_statements = [f'duplicate_statements/{file}_{language}_duplicates.csv' for language in languages]

        if any(os.path.exists(dup_file) for dup_file in duplicate_statements): # only remove duplicates if the duplicate files exist
            remove_duplicates(f'raw_statements/{file}.csv', duplicate_statements, translated_statements)
        else:
            print(f"No duplicate files found for {file}, skipping removal.")
