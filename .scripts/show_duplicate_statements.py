import pandas as pd
import os

# Define the path to your CSV file
# csv_file_paths = ['raw_statements/email_statements.csv',
#                   'raw_statements/email_statements_ar.csv',
#                     'raw_statements/email_statements_bn.csv',
#                     'raw_statements/email_statements_es.csv',
#                     'raw_statements/email_statements_fr.csv',
#                     'raw_statements/email_statements_hi.csv',
#                     'raw_statements/email_statements_ja.csv',
#                     'raw_statements/email_statements_pt.csv',
#                     'raw_statements/email_statements_ru.csv',
#                     'raw_statements/email_statements_zh.csv',
# ]
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
]

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

all_duplicates = []

for csv_file_path in csv_file_paths:
    df = pd.read_csv(csv_file_path)

    # add a column for the line number
    df['line_number'] = df.index + 2  # +2 to account for the header row and 0-based index

    # find duplicates
    duplicates = df[df.duplicated('statement', keep=False)]

    if not duplicates.empty:
        print("\n---------------------\n")
        print(f"Duplicates found in {csv_file_path}:")
        grouped_duplicates = duplicates.groupby('statement') # group by the statement
        group_number = 1
        for statement, group in grouped_duplicates:
            group['source_file'] = csv_file_path  # add a column to indicate the source file
            group['group_number'] = group_number # add a column to indicate the group number
            group_number += 1
            all_duplicates.append(group[['source_file', 'group_number', 'line_number', 'statement']])
    
    if all_duplicates:
        result_df = pd.concat(all_duplicates)
        result_df.to_csv('observable_gpt4o_duplicates.csv', index=False)
        print("Grouped duplicates have been saved to grouped_duplicates.csv")

    else:
        print("No duplicates found.")
