import pandas as pd
import os


def check_csv_files(directory):
    required_columns = {"statement", "elicitation", "committer"}
    all_statements = []

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            try:
                df = pd.read_csv(filepath)
                if set(df.columns) != required_columns:
                    print(f"Error: {filename} does not have the required columns.")
                    return "Not OK"

                duplicates = df[df.duplicated("statement", keep=False)]
                if not duplicates.empty:
                    print(f"Duplicates found in {filename}:")
                    print(duplicates["statement"])
                    return "Not OK"

                all_statements.extend(df["statement"].tolist())

            except Exception as e:
                print(f"Error processing {filename}: {e}")
                return "Not OK"

    # Check for overall duplicates across all files
    if len(all_statements) != len(set(all_statements)):
        print("Global duplicates found across multiple files.")
        return "Not OK"

    return "OK"


if __name__ == "__main__":
    result = check_csv_files("raw_statements")
    print(result)
