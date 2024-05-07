import pandas as pd
import os
import sys


def exit_error(message):
    print("Exiting:", message)
    sys.exit(1)


def check_csv_files(directory):
    required_columns = {"statement", "elicitation", "committer"}
    all_statements = []

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            try:
                df = pd.read_csv(filepath)

                # Check for required columns
                if set(df.columns) != required_columns:
                    exit_error(
                        f"Error: {filename} does not have the required columns. Expected: {required_columns}, Found: {set(df.columns)}"
                    )

                # Check for non-null, non-empty cells in the required columns
                if (
                    df[required_columns].isnull().values.any()
                    or (df[required_columns] == "").any().any()
                ):
                    exit_error(
                        f"Error: {filename} contains empty entries in required columns."
                    )

                # Remove empty rows
                if df.dropna(how="all").shape[0] != df.shape[0]:
                    exit_error(f"Error: {filename} contains completely empty rows.")

                # Check for duplicates in 'statement' column
                duplicates = df[df.duplicated("statement", keep=False)]
                if not duplicates.empty:
                    print(f"Duplicates found in {filename}:")
                    print(duplicates["statement"])
                    exit_error(f"Error processing {filename} due to duplicates.")

                all_statements.extend(df["statement"].tolist())

            except Exception as e:
                exit_error(f"Error processing {filename}: {e}")

    # Check for overall duplicates across all files
    if len(all_statements) != len(set(all_statements)):
        exit_error("Global duplicates found across multiple files.")

    return "OK"


if __name__ == "__main__":
    result = check_csv_files("raw_statements")
    print(result)
