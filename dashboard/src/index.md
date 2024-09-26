---
toc: false
---

```js
const statements = await FileAttachment("data/statements.csv").csv({
  typed: true,
});
```

```js
function statementsByCategory(data, { width } = {}) {
  return Plot.plot({
    title: "Statements by Category",
    width,
    height: 300,
    marginBottom: 100,
    y: { grid: true, label: "Number of Statements" },
    x: { label: "Category", tickRotate: 45 },
    marks: [
      Plot.barY(
        data,
        Plot.groupX(
          { y: "count" },
          { x: "statementCategory", fill: "statementCategory" }
        )
      ),
      Plot.ruleY([0]),
    ],
  });
}
```

<div class="hero">
  <h1 class="text-6xl font-bold mb-4">Welcome to the Commonsense Statements Project</h1>
  <p class="text-xl text-gray-600 max-w-2xl mx-auto">
    We extract commonsense statements for a wide range of categories from various sources.
    Our project aims to gather a comprehensive set of statements that reflect everyday knowledge.
    These statements can be used for research, education, and applications in artificial intelligence.
  </p>
  <p class="text-xl text-gray-600 mt-4">
    Currently, we have extracted <span class="font-semibold">${statements.length.toLocaleString()}</span> statements.
  </p>
  <div class="mt-8">
    <a href="/platform-report" class="text-blue-500 hover:underline mx-4">View Statements Report</a> |
    <a href="/statement-dashboard" class="text-blue-500 hover:underline mx-4">Go to Dashboard</a> |
    <a href="/export-designpoint" class="text-blue-500 hover:underline mx-4">Export Experiment Buckets</a>
  </div>
</div>

   <div class="grid grid-cols-1">
     <div class="card">
       ${resize((width) => statementsByCategory(statements, { width }))}
     </div>
   </div>

---

<script src="https://cdn.tailwindcss.com"></script>

<style>
.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 2rem;
  text-align: center;
}
</style>
