import pandas as pd
import os
import ast
import sys

os.makedirs('raw_statements_cleaned', exist_ok=True)

# define any necessary paths
observable_translated_statements = ['raw_statements/observable_gpt4o_ar.csv',
                        'raw_statements/observable_gpt4o_bn.csv',
                        'raw_statements/observable_gpt4o_es.csv',
                        'raw_statements/observable_gpt4o_fr.csv',
                        'raw_statements/observable_gpt4o_hi.csv',
                        'raw_statements/observable_gpt4o_ja.csv',
                        'raw_statements/observable_gpt4o_pt.csv',
                        'raw_statements/observable_gpt4o_ru.csv',
                        'raw_statements/observable_gpt4o_zh.csv',
]

observable_duplicate_statements = ['duplicate_statements/observable_gpt4o_ar_duplicates.csv', 
                        'duplicate_statements/observable_gpt4o_bn_duplicates.csv',
                        'duplicate_statements/observable_gpt4o_es_duplicates.csv',
                        'duplicate_statements/observable_gpt4o_fr_duplicates.csv',
                        'duplicate_statements/observable_gpt4o_hi_duplicates.csv',
                        'duplicate_statements/observable_gpt4o_ja_duplicates.csv',
                        'duplicate_statements/observable_gpt4o_pt_duplicates.csv',
                        'duplicate_statements/observable_gpt4o_ru_duplicates.csv',
                        'duplicate_statements/observable_gpt4o_zh_duplicates.csv'
]

email_translated_statements = ['raw_statements/email_statements_ar.csv',
                               'raw_statements/email_statements_bn.csv',
                               'raw_statements/email_statements_es.csv',
                               'raw_statements/email_statements_fr.csv',
                               'raw_statements/email_statements_hi.csv',
                               'raw_statements/email_statements_ja.csv',
                               'raw_statements/email_statements_pt.csv',
                               'raw_statements/email_statements_ru.csv',
                               'raw_statements/email_statements_zh.csv',
]

email_duplicate_statements = ['duplicate_statements/email_statements_ar_duplicates.csv',
                        'duplicate_statements/email_statements_bn_duplicates.csv',
                        'duplicate_statements/email_statements_es_duplicates.csv',
                        'duplicate_statements/email_statements_fr_duplicates.csv',
                        'duplicate_statements/email_statements_hi_duplicates.csv',
                        'duplicate_statements/email_statements_ja_duplicates.csv',
                        'duplicate_statements/email_statements_pt_duplicates.csv',
                        'duplicate_statements/email_statements_ru_duplicates.csv',
                        'duplicate_statements/email_statements_zh_duplicates.csv'
]

# helper function that removes indices of duplicate statements from the original CSV and their translations
def remove_duplicates(original_csv, duplicate_statements, translated_statements):
    indices_to_remove = set() # stores the indices of the rows to remove 
    original_df = pd.read_csv(original_csv)

    # iterate through each duplicate CSV corresponding to the original CSV
    for duplicate_csv in duplicate_statements:
        duplicate_df = pd.read_csv(duplicate_csv)

        # iterate through each group
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

            # add all indices except the index of the shortest statement to indices_to_remove
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

# call the function to standardize observable_gpt4o statements and across all their translations
remove_duplicates('raw_statements/observable_gpt4o.csv', 
                  observable_duplicate_statements, 
                  observable_translated_statements)

# call the function to standardize email statements and across all their translations
remove_duplicates('raw_statements/email_statements.csv', 
                  email_duplicate_statements, 
                  email_translated_statements)

"""
Test the number of lines is the same across all files and across their translations
"""

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

observable_translated_statements_cleaned = ['raw_statements_cleaned/observable_gpt4o_ar.csv',
                                            'raw_statements_cleaned/observable_gpt4o_bn.csv',
                        'raw_statements_cleaned/observable_gpt4o_es.csv',
                        'raw_statements_cleaned/observable_gpt4o_fr.csv',
                        'raw_statements_cleaned/observable_gpt4o_hi.csv',
                        'raw_statements_cleaned/observable_gpt4o_ja.csv',
                        'raw_statements_cleaned/observable_gpt4o_pt.csv',
                        'raw_statements_cleaned/observable_gpt4o_ru.csv',
                        'raw_statements_cleaned/observable_gpt4o_zh.csv'
]

email_translated_statements_cleaned = ['raw_statements_cleaned/email_statements_ar.csv',
                                       'raw_statements_cleaned/email_statements_bn.csv',
                                      'raw_statements_cleaned/email_statements_es.csv',
                                      'raw_statements_cleaned/email_statements_fr.csv',
                                      'raw_statements_cleaned/email_statements_hi.csv',
                                      'raw_statements_cleaned/email_statements_ja.csv',
                                      'raw_statements_cleaned/email_statements_pt.csv',
                                      'raw_statements_cleaned/email_statements_ru.csv',
                                      'raw_statements_cleaned/email_statements_zh.csv',
]

test_line_numbers('raw_statements_cleaned/observable_gpt4o.csv', observable_translated_statements_cleaned)
test_line_numbers('raw_statements_cleaned/email_statements.csv', email_translated_statements_cleaned)
