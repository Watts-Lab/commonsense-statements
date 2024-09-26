// Import necessary modules
import fs from "fs/promises"; // For reading files asynchronously
import { csvParse, csvFormat } from "d3-dsv"; // For parsing and formatting CSV

async function main() {
  try {
    // Read the CSV file from the given path
    const dataText = await fs.readFile(
      "../statements_db_translated.csv",
      "utf8"
    );

    // Parse the CSV data
    const data = csvParse(dataText);

    // Step 1: Collect all parentIds
    const parentIdSet = new Set();
    data.forEach((row) => {
      if (row.parentId && row.parentId.trim() !== "") {
        parentIdSet.add(row.parentId.trim());
      }
    });

    // Step 2: Filter out rows that are parents (i.e., their id is in parentIdSet)
    const filteredData = data.filter((row) => !parentIdSet.has(row.id.trim()));

    // Output the filtered data as CSV
    process.stdout.write(csvFormat(filteredData));
  } catch (error) {
    console.error("Error processing statements:", error);
    process.exit(1); // Exit with an error code
  }
}

main();
