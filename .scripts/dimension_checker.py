import hashlib
import pandas as pd
import os

# Define dimensions
DIMENSIONS = [
    "behavior",
    "everyday",
    "figure_of_speech",
    "judgment",
    "opinion",
    "reasoning",
]


def calculate_hash(statement):
    hash_object = hashlib.sha256(statement.encode())
    return hash_object.hexdigest()[:10]


def process_files(input_folder, output_folder):

    all_dataframes = []

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
                output_df.to_csv(output_file_path, index=False)

                all_dataframes.append(output_df)

                print(f"Processed {filename} and saved to {output_filename}")
            else:
                print(f"No 'statement' column in {filename}")

    # Combine all dataframes into one
    combined_df = pd.concat(all_dataframes)
    return combined_df


if __name__ == "__main__":
    raw_statements_folder = "raw_statements"
    output_folder = "processed_statements"
    process_files(raw_statements_folder, output_folder)
