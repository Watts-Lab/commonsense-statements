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
        print(len(grouped_duplicates))
        group_number = 1
        for statement, group in grouped_duplicates:
            group['source_file'] = csv_file_path  # add a column to indicate the source file
            group['group_number'] = group_number # add a column to indicate the group number
            group_number += 1
            all_duplicates.append(group[['source_file', 'group_number', 'line_number', 'statement']])
    
    # if all_duplicates:
    #     result_df = pd.concat(all_duplicates)
    #     result_df.to_csv('observable_gpt4o_duplicates.csv', index=False)
    #     print("Grouped duplicates have been saved to grouped_duplicates.csv")

    # else:
    #     print("No duplicates found.")



# import pandas as pd

# # Define the path to your original and translated CSV files
# email_csv_files = {
#     'raw_statements/email_statements_ar.csv': 'raw_statements/email_statements.csv',
#     'raw_statements/email_statements_bn.csv': 'raw_statements/email_statements.csv',
#     'raw_statements/email_statements_es.csv': 'raw_statements/email_statements.csv',
#     'raw_statements/email_statements_fr.csv': 'raw_statements/email_statements.csv',
#     'raw_statements/email_statements_hi.csv': 'raw_statements/email_statements.csv',
#     'raw_statements/email_statements_ja.csv': 'raw_statements/email_statements.csv',
#     'raw_statements/email_statements_pt.csv': 'raw_statements/email_statements.csv',
#     'raw_statements/email_statements_ru.csv': 'raw_statements/email_statements.csv',
#     'raw_statements/email_statements_zh.csv': 'raw_statements/email_statements.csv',
# }

# observable_csv_files = {
#     'raw_statements/observable_gpt4o_ar.csv': 'raw_statements/observable_gpt4o.csv',
#     'raw_statements/observable_gpt4o_bn.csv': 'raw_statements/observable_gpt4o.csv',
#     'raw_statements/observable_gpt4o_es.csv': 'raw_statements/observable_gpt4o.csv',
#     'raw_statements/observable_gpt4o_fr.csv': 'raw_statements/observable_gpt4o.csv',
#     'raw_statements/observable_gpt4o_hi.csv': 'raw_statements/observable_gpt4o.csv',
#     'raw_statements/observable_gpt4o_ja.csv': 'raw_statements/observable_gpt4o.csv',
#     'raw_statements/observable_gpt4o_pt.csv': 'raw_statements/observable_gpt4o.csv',
#     'raw_statements/observable_gpt4o_ru.csv': 'raw_statements/observable_gpt4o.csv',
#     'raw_statements/observable_gpt4o_zh.csv': 'raw_statements/observable_gpt4o.csv',
# }

# news_csv_files = {
#     'raw_statements/news_statements_amir_ar.csv': 'raw_statements/news_statements_amir.csv',
#     'raw_statements/news_statements_amir_bn.csv': 'raw_statements/news_statements_amir.csv',
#     'raw_statements/news_statements_amir_es.csv': 'raw_statements/news_statements_amir.csv',
#     'raw_statements/news_statements_amir_fr.csv': 'raw_statements/news_statements_amir.csv',
#     'raw_statements/news_statements_amir_hi.csv': 'raw_statements/news_statements_amir.csv',
#     'raw_statements/news_statements_amir_ja.csv': 'raw_statements/news_statements_amir.csv',
#     'raw_statements/news_statements_amir_pt.csv': 'raw_statements/news_statements_amir.csv',
#     'raw_statements/news_statements_amir_ru.csv': 'raw_statements/news_statements_amir.csv',
#     'raw_statements/news_statements_amir_zh.csv': 'raw_statements/news_statements_amir.csv',
# }

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.width', None)

# for translated_file, original_file in email_csv_files.items():
#     all_duplicates = []
#     translated_df = pd.read_csv(translated_file)
#     original_df = pd.read_csv(original_file)

#     # add a column for the line number
#     translated_df['translated_line_number'] = translated_df.index + 2  # +2 to account for the header row and 0-based index
#     original_df['original_line_number'] = original_df.index + 2  # +2 to account for the header row and 0-based index

#     # find duplicates in the translated file
#     duplicates = translated_df[translated_df.duplicated('statement', keep=False)]

#     if not duplicates.empty:
#         print("\n---------------------\n")
#         print(f"Duplicates found in {translated_file}:")
#         grouped_duplicates = duplicates.groupby('statement')  # group by the statement
#         group_number = 1
#         for statement, group in grouped_duplicates:
#             group['source_file'] = translated_file  # add a column to indicate the source file
#             group['group_number'] = group_number  # add a column to indicate the group number
#             group_number += 1
#             # find original line numbers for the statement
#             original_lines = original_df[original_df['statement'] == statement][['original_line_number']]
#             for _, translated_row in group.iterrows():
#                 for _, original_row in original_lines.iterrows():
#                     print('hello')
#                     all_duplicates.append({
#                         'translated_source_file': translated_file,
#                         'translated_line_number': translated_row['translated_line_number'],
#                         'original_source_file': original_file,
#                         'original_line_number': original_row['original_line_number'],
#                         'statement': statement
#                     })

#         if all_duplicates:
#             result_df = pd.concat(all_duplicates)
#             result_df.to_csv('email_duplicates.csv', index=False)
#             print("Original and translated duplicates have been saved to email_duplicates.csv")

#         else:
#             print("No duplicates found.")

