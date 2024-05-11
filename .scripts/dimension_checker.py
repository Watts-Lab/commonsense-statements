import hashlib
import pandas as pd
import os
import sys

# Define dimensions
DIMENSIONS = [
    "behavior",
    "everyday",
    "figure_of_speech",
    "judgment",
    "opinion",
    "reasoning",
]


def exit_error(message):
    print("Exiting:", message)
    sys.exit(1)


def calculate_hash(statement):
    hash_object = hashlib.sha256(statement.encode())
    return hash_object.hexdigest()[:10]


def process_files(input_folder, output_folder, save_combined=False):
    """
    Process files in the input folder, calculate hash for each statement, and save the output to the output folder.

    Args:
        input_folder (str): Path to the folder containing input files.
        output_folder (str): Path to the folder where the output files will be saved.
        save_combined (bool, optional): Whether to save a combined output file. Defaults to False.

    Returns:
        pandas.DataFrame: Combined dataframe containing the 'statement' and 'hash' columns.

    Raises:
        Exception: If there is an error processing the files.

    """
    all_dataframes = []

    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(input_folder):
            file_path = os.path.join(input_folder, filename)
            if os.path.isfile(file_path):
                df = pd.read_csv(file_path)

                # Ensure the 'statement' column exists in the dataframe
                if "statement" in df.columns:
                    # Calculate hash for each statement
                    df["hash"] = df["statement"].apply(calculate_hash)

                    output_df = df[["statement", "hash"]]

                    output_filename = filename.split(".")[0] + "_properties.csv"
                    output_file_path = os.path.join(output_folder, output_filename)

                    if save_combined:
                        output_df.to_csv(output_file_path, index=False)
                        print(f"Processed {filename} and saved to {output_filename}")

                    all_dataframes.append(output_df)

                else:
                    print(f"No 'statement' column in {filename}")

        # Combine all dataframes into one
        combined_df = pd.concat(all_dataframes)
        return combined_df

    except Exception as e:
        exit_error(f"Error processing files: {e}")


def get_unique_rows_by_hash(df1, df2):
    """
    Returns rows from df1 whose 'hash' values are not present in the hash column of df2.

    Parameters:
    df1 (pd.DataFrame): DataFrame containing a 'hash' column.
    df2 (pd.DataFrame): DataFrame containing a 'hash' column to compare against.

    Returns:
    pd.DataFrame: A DataFrame consisting of rows from df1 that have unique hash values not found in df2.
    """
    if "hash" not in df1.columns or "hash" not in df2.columns:
        raise ValueError("Both DataFrames should have a 'hash' column.")

    hashes_in_df2 = set(df2["hash"].unique())

    unique_rows = df1[~df1["hash"].isin(hashes_in_df2)]

    return unique_rows


if __name__ == "__main__":
    raw_statements_folder = "raw_statements"
    output_folder = "processed_statements"
    process_files(raw_statements_folder, output_folder)
