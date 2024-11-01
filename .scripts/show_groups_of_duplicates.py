import pandas as pd
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

os.makedirs('duplicate_statements', exist_ok=True)

"""
Function to find and group duplicate statements found in each CSV file

Parameters:
- directory: the directory containing the CSV files to be processed
"""
def show_groups_of_duplicates(directory):
    for filename in os.listdir(directory):
        if not filename.endswith(".csv"):
            continue
        
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        df['line_number'] = df.index + 2  # +2 to account for the header row and 0-based index

        duplicates = df[df.duplicated('statement', keep=False)] # filter duplicate statements found in each file

        if not duplicates.empty:
            print("\n---------------------\n")
            print(f"Duplicates found in {filename}:")

            grouped_duplicates = duplicates.groupby('statement') 
            print(f'number of groups: {len(grouped_duplicates)}')
            group_number = 1
            all_duplicates = []

            for statement, group in grouped_duplicates:
                group['source_file'] = filename  
                group['group_number'] = group_number
                group_number += 1
                all_duplicates.append(group[['source_file', 'group_number', 'line_number', 'statement']])
        
            if all_duplicates:
                result_df = pd.concat(all_duplicates)

                # group by group number and merge line_number and statement columns into a dictionary
                result_df = result_df.groupby(['source_file', 'group_number']).apply(
                    lambda x: x.set_index('line_number')['statement'].to_dict(), include_groups=False 
                ).reset_index().rename(columns={0: 'line_and_statement'})

                result_df.to_csv(f"duplicate_statements/{filename.split('.')[0]}_duplicates.csv", index=False)
                print(f"Grouped duplicates have been saved to duplicate_statements/{filename.split('.')[0]}_duplicates.csv")
        else:
            print("No duplicates found.")


if __name__ == "__main__":
    show_groups_of_duplicates("raw_statements")
