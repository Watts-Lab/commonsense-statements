import pandas as pd
import os

# define the paths to CSV files
csv_file_paths = ['raw_statements/observable_gpt4o.csv',
                'raw_statements/observable_gpt4o_ar.csv',
                'raw_statements/observable_gpt4o_bn.csv',
                'raw_statements/observable_gpt4o_es.csv',
                'raw_statements/observable_gpt4o_fr.csv',
                'raw_statements/observable_gpt4o_hi.csv',
                'raw_statements/observable_gpt4o_ja.csv',
                'raw_statements/observable_gpt4o_pt.csv',
                'raw_statements/observable_gpt4o_ru.csv',
                'raw_statements/observable_gpt4o_zh.csv',
                'raw_statements/email_statements.csv',
                'raw_statements/email_statements_ar.csv',
                'raw_statements/email_statements_bn.csv',
                'raw_statements/email_statements_es.csv',
                'raw_statements/email_statements_fr.csv',
                'raw_statements/email_statements_hi.csv',
                'raw_statements/email_statements_ja.csv',
                'raw_statements/email_statements_pt.csv',
                'raw_statements/email_statements_ru.csv',
                'raw_statements/email_statements_zh.csv',
]

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

os.makedirs('duplicate_statements', exist_ok=True)

def show_groups_of_duplicates(csv_file_paths):
    for csv_file_path in csv_file_paths:
        df = pd.read_csv(csv_file_path)
        csv_file_name = os.path.basename(csv_file_path).split('.')[0]

        # add a column for the line number
        df['line_number'] = df.index + 2  # +2 to account for the header row and 0-based index
        df['lng'] = os.path.basename(csv_file_path).split('_')[-1].split('.')[0]  # add a column for the language

        # find duplicates
        duplicates = df[df.duplicated('statement', keep=False)]

        if not duplicates.empty:
            print("\n---------------------\n")
            print(f"Duplicates found in {csv_file_path}:")

            grouped_duplicates = duplicates.groupby('statement') # group by the statement
            print(f'number of groups: {len(grouped_duplicates)}')
            group_number = 1
            all_duplicates = []

            for statement, group in grouped_duplicates:
                group['source_file'] = csv_file_path  # add a column to indicate the source file
                group['group_number'] = group_number # add a column to indicate the group number
                group_number += 1
                all_duplicates.append(group[['source_file', 'group_number', 'lng', 'line_number', 'statement']])
        
            if all_duplicates:
                result_df = pd.concat(all_duplicates)

                # group by group number and merge line_number and statement columns into a dictionary
                result_df = result_df.groupby(['source_file', 'group_number', 'lng']).apply(
                    lambda x: x.set_index('line_number')['statement'].to_dict(), include_groups=False # reference: https://stackoverflow.com/questions/77969964/deprecation-warning-with-groupby-apply
                ).reset_index().rename(columns={0: 'line_and_statement'})

                # convert result dataframe to a csv
                result_df.to_csv(f'duplicate_statements/{csv_file_name}_duplicates.csv', index=False)
                print("Grouped duplicates have been saved to grouped_duplicates.csv")
        else:
            print("No duplicates found.")

# invoke the function to show groups of duplicates -- each row is a unique group
show_groups_of_duplicates(csv_file_paths)
