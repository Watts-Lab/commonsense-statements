import pandas as pd
import os

languages = ['ar','bn','en','es','fr','hi','ja','pt','ru','zh']

"""
Function that removes duplicates caused after running the normalize_statements.py script

input: the directory to process the files where duplicates occur
"""
def remove_duplicates_after_normalization(directory):
    base_names = set()
    for filename in os.listdir(directory):
        if filename.endswith('_cleaned.csv'):
            base = '_'.join(filename.split('.')[0].split('_')[:-2])
            base_names.add(base)
    
    # process files with the same base
    for base in base_names:
        files = [f'{base}_{lng}_cleaned.csv' for lng in languages]

        # identify indices to drop
        indices_to_drop = set()
        for filename in files:
            filepath = os.path.join(directory, filename)
            print(f'Checking for duplicates in {filename}...')
            df = pd.read_csv(filepath)
            duplicates = df.duplicated(keep='first')
            dropped_indices = df.index[duplicates]
            indices_to_drop.update(dropped_indices.tolist())

        # drop the indices across all files with the same base name
        if indices_to_drop:
            for filename in files:
                filepath = os.path.join(directory, filename)
                df = pd.read_csv(filepath)
                df.drop(list(indices_to_drop), inplace=True)
                df.reset_index(drop=True, inplace=True)
                df.to_csv(filepath, index=False)
                print(f'dropped {list(indices_to_drop)} in {filename}')
        else:
            print(f'No duplicates found in {base}_en.csv and corresponding translation files.')


if __name__ == '__main__':
    remove_duplicates_after_normalization('raw_statements')