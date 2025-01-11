# Commonsense statements

## Adding Statement Data

If you are looking to contribute statement data to the project, please follow the instructions outlined below to ensure your data is added correctly and efficiently. This will help us maintain the quality and consistency of the data within the project.

## Guidelines for Preparing Your Data

Your contribution should be in the form of a CSV file, and it should adhere to the following structure:

### Required Columns

Each CSV file must include exactly three columns:
- **statement**: Contains the textual statement.
- **elicitation**: Descriptive field on how the statement was elicited or under what circumstances.
- **committer**: Identifier (name or ID) for the individual who contributed the statement or is responsible for the entry.

### Example format:

```plaintext
statement,elicitation,committer
"Lorem ipsum dolor sit amet...","Survey Response","John Doe"
"Consectetur adipiscing elit...","Interview","Jane Smith"
```

### CSV File Requirements
- Do not include headers that are different from the ones mentioned (`statement`, `elicitation`, `committer`).
- Ensure there are no empty rows or columns.
- Verify that there are no cells with empty strings or null values in the required columns.
- Duplicate statements should be avoided for consistency and data integrity.

### CSV File Naming Convention

All files MUST follow a specific naming convention:
- File names must be unique
- File names must be suffixed with the language code 'en', assuming the source language code is in English. 

### Example format:

/commonsense-statements
├── /raw_statements                   
      ├── original_statements_en.csv
      ├── jane_statements_en.csv
      └── bob_statements_en.csv

Note: It is very important that your files follow this convention to ensure consistent parsing and processing of your files during automated workflows.

## Steps to Add Your Statements

To add your data correctly, follow these step-by-step instructions:

1. **Create a New Branch**
   - Avoid making changes directly to the main branch.
   - Name the branch meaningfully, related to your changes, e.g., `add-statements-{yourname}`.

2. **Adding Data**
   - Place your correctly formatted CSV file into the `raw_statements` folder.
   - Ensure your file ends with a `_en.csv` extension and adheres to the naming conventions already found in the project (if any).

3. **Commit and Push Your Changes**
   - Commit your changes with a clear message describing the modification, e.g., `Add new statements from survey responses`.
   - Push the commit to your branch and create a pull request to the main repository.

4. **Pull Request**
   - When creating the pull request, provide a concise yet comprehensive description of the changes and why they were made.
   - Request review from the project maintainers and address any comments to gain approval for merging.

## Automated Checks
Upon submission, automated checks will verify the format and integrity of the CSV files. If errors are detected, the submission will be flagged for manual review, and you will be notified of the necessary corrections.

To translate your files, select Github Actions and select the 'Translate Statements and Remove Any Duplicates' workflow. This workflow is triggered on workflow_dispatch and takes in three input fields: 
   - a comma-separated list of files you want to translate (e.g., original_statements_en.csv, bob_statements_en.csv)
   - the elicitation method
   - the committer's name

The workflow will then contribute 9 new language files, one for each language, for each file provided in the comma-separated list. 

Thank you for contributing to the project and following these guidelines. We appreciate your effort in maintaining the quality and reliability of the data.
