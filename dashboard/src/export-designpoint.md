---
theme: dashboard
title: Export design points
toc: false
---

<h1 class="text-4xl font-bold mb-4">Export design points</h1>
This page allows you to export the design points from the experiment buckets.

```js
// Load your statements
const statements = await FileAttachment("data/statements.csv").csv({
  typed: true,
});
```

```jsx
import fuzzysort from "fuzzysort";
import { useState, useEffect } from "npm:react";

function Table({ searchQuery, data }) {
  if (!data) {
    return <div>Loading...</div>;
  }

  const [selectedIds, setSelectedIds] = useState(new Set());
  const [filteredData, setFilteredData] = useState([]);
  const [binaryFilter, setBinaryFilter] = useState({
    behavior: "",
    everyday: "",
    figure_of_speech: "",
    judgment: "",
    opinion: "",
    reasoning: "",
  });

  // Using useEffect to update filteredData based on searchQuery
  useEffect(() => {
    let filtered = data;

    if (searchQuery) {
      const results = fuzzysort.go(searchQuery, data, {
        keys: ["statement", "id", "statementCategory"],
      });
      filtered = results.map((r) => r.obj);
    }

    filtered = filtered.filter((item) => {
      return (
        (binaryFilter.behavior === "" ||
          binaryFilter.behavior == item.behavior) &&
        (binaryFilter.everyday === "" ||
          binaryFilter.everyday == item.everyday) &&
        (binaryFilter.figure_of_speech === "" ||
          binaryFilter.figure_of_speech == item.figure_of_speech) &&
        (binaryFilter.judgment === "" ||
          binaryFilter.judgment == item.judgment) &&
        (binaryFilter.opinion === "" || binaryFilter.opinion == item.opinion) &&
        (binaryFilter.reasoning === "" ||
          binaryFilter.reasoning == item.reasoning)
      );
    });

    setFilteredData(filtered);
  }, [searchQuery, data, binaryFilter]);

  const handleCheckboxChange = (id) => {
    setSelectedIds((prevSelectedIds) => {
      const newSelectedIds = new Set(prevSelectedIds);
      if (newSelectedIds.has(id)) {
        newSelectedIds.delete(id);
      } else {
        newSelectedIds.add(id);
      }
      return newSelectedIds;
    });
  };

  const exportSelectedIds = () => {
    const idsArray = Array.from(selectedIds);
    console.log("Selected IDs:", idsArray);
    setSelectedIds(new Set());
  };

  const handleFilterChange = (key, value) => {
    setBinaryFilter((prevFilters) => ({
      ...prevFilters,
      [key]: value,
    }));
  };

  return (
    <>
      <div className="overflow-x-auto">
        <div className="flex items-center space-x-2">
          <button
            onClick={exportSelectedIds}
            className="btn btn-xs p-2 bg-blue-500 text-white rounded"
          >
            Export Selected IDs
          </button>
          <p>
            [
            {Array.from(selectedIds).map((i, index) => (
              <span key={i}>
                {i}
                {index < selectedIds.size - 1 ? ", " : ""}
              </span>
            ))}
            ]
          </p>
          {[
            "behavior",
            "everyday",
            "figure_of_speech",
            "judgment",
            "opinion",
            "reasoning",
          ].map((key) => (
            <select
              key={key}
              value={binaryFilter[key]}
              onChange={(e) => handleFilterChange(key, e.target.value)}
              className="border p-1 rounded"
            >
              <option value="">{key}</option>
              <option value="0">0</option>
              <option value="1">1</option>
            </select>
          ))}
        </div>
        <table className="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th className="px-2 !py-1"></th>
              <th className="px-2 !py-1 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Id
              </th>
              <th className="px-6 !py-1 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Statement
              </th>
              <th className="px-2 !py-1 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Category
              </th>
              <th className="px-2 !py-1 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Behavior
              </th>
              <th className="px-2 !py-1 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Everyday
              </th>
              <th className="px-2 !py-1 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Figure of Speech
              </th>
              <th className="px-2 !py-1 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Judgment
              </th>
              <th className="px-2 !py-1 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Opinion
              </th>
              <th className="px-2 !py-1 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Reasoning
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredData.map((d, index) => {
              return (
                <tr key={`${index}-${d.id}`}>
                  <td className="px-2 py-4">
                    <input
                      type="checkbox"
                      checked={selectedIds.has(d.id)}
                      onChange={() => handleCheckboxChange(d.id)}
                    />
                  </td>
                  <td className="px-2 py-4 text-sm text-gray-900">{d.id}</td>
                  <td className="px-6 py-4 text-sm text-gray-900 break-words">
                    {d.statement}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 break-words">
                    {d.statementCategory}
                  </td>
                  <td className="px-2 py-4 text-sm text-gray-900 text-center">
                    {d.behavior}
                  </td>
                  <td className="px-2 py-4 text-sm text-gray-900 text-center">
                    {d.everyday}
                  </td>
                  <td className="px-2 py-4 text-sm text-gray-900 text-center">
                    {d.figure_of_speech}
                  </td>
                  <td className="px-2 py-4 text-sm text-gray-900 text-center">
                    {d.judgment}
                  </td>
                  <td className="px-2 py-4 text-sm text-gray-900 text-center">
                    {d.opinion}
                  </td>
                  <td className="px-2 py-4 text-sm text-gray-900 text-center">
                    {d.reasoning}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}
```

```js
const subjectInput = html`<input
  type="text"
  placeholder="Search for a statement..."
  class="min-w-[900px] p-2 rounded mt-2 border"
/>`;
const search = Generators.input(subjectInput);
```

${subjectInput}

```jsx
display(<Table searchQuery={search || ""} data={statements} />);
```

---

<script src="https://cdn.tailwindcss.com"></script>
