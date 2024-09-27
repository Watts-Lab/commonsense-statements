// Import necessary modules
import fs from "fs/promises"; // For reading files asynchronously
import { csvParse, csvFormat } from "d3-dsv"; // For parsing and formatting CSV

async function main() {
  try {
    // Read the statements CSV file
    const statementsText = await fs.readFile(
      "../statements_db_translated.csv",
      "utf8"
    );

    const statements = csvParse(statementsText);

    const propertiesText = await fs.readFile(
      "../features/statementproperties.csv",
      "utf8"
    );

    const propertiesData = csvParse(propertiesText);

    const parentIdSet = new Set();
    statements.forEach((row) => {
      if (row.parentId && row.parentId.trim() !== "") {
        parentIdSet.add(row.parentId.trim());
      }
    });

    const filteredData = statements.filter(
      (row) => !parentIdSet.has(row.id.trim())
    );

    // Map statementId to its properties
    const propertiesByStatementId = new Map();

    propertiesData.forEach((prop) => {
      const statementId = prop.statementId.trim();
      if (!propertiesByStatementId.has(statementId)) {
        propertiesByStatementId.set(statementId, []);
      }
      propertiesByStatementId.get(statementId).push(prop);
    });

    // For each statement, add its properties
    const outputData = filteredData.map((statement) => {
      const statementId = statement.id.trim();
      const properties = propertiesByStatementId.get(statementId) || [];

      // Create an object to hold property values
      const propertiesObj = {};
      properties.forEach((prop) => {
        propertiesObj[prop.name] = prop.available;
      });

      // For properties not in this statement, set to null or default value
      // Assuming you want to include all possible properties
      const allPropertyNames = [...new Set(propertiesData.map((p) => p.name))];
      allPropertyNames.forEach((propName) => {
        if (!(propName in propertiesObj)) {
          propertiesObj[propName] = null; // Or default value
        }
      });

      return {
        ...statement,
        ...propertiesObj,
      };
    });

    // Define the order of columns (optional)
    const columns = [
      ...Object.keys(filteredData[0]),
      ...[...new Set(propertiesData.map((p) => p.name))],
    ];

    // Output the data as CSV
    process.stdout.write(csvFormat(outputData, columns));
  } catch (error) {
    console.error("Error processing statements:", error);
    process.exit(1); // Exit with an error code
  }
}

main();
