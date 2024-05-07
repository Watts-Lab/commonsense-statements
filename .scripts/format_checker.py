import pandas as pd
import os
import sys


def exit_error(message):
    print("Exiting : ", message)
    sys.exit(1)


def check_csv_files(directory):
    required_columns = {"statement", "elicitation", "committer"}
    all_statements = []

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            try:
                df = pd.read_csv(filepath)
                if set(df.columns) != required_columns:
                    print(
                        f"Error: {filename} does not have the required columns. Expected: {required_columns}, Found: {set(df.columns)}"
                    )
                    exit_error(f"Error processing {filename}")

                duplicates = df[df.duplicated("statement", keep=False)]
                if not duplicates.empty:
                    print(f"Duplicates found in {filename}:")
                    print(duplicates["statement"])
                    exit_error(f"Error processing {filename}")

                all_statements.extend(df["statement"].tolist())

            except Exception as e:
                exit_error(f"Error processing {filename}: {e}")

    # Check for overall duplicates across all files
    if len(all_statements) != len(set(all_statements)):
        print("Global duplicates found across multiple files.")
        exit_error(f"Error processing {filename}: {e}")

    return "OK"


if __name__ == "__main__":
    result = check_csv_files("raw_statements")
    print(result)
