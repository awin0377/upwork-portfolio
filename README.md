# upwork-portfolio

Two small, self-contained demos of automation work: a Python script that cleans messy product CSVs, and an n8n workflow that turns a keyword list into article drafts.

## csv-cleanup — messy product CSV → import-ready data

**Problem.** Product exports arrive in mixed formats: prices like `$1,299.00 USD`, four different date styles, duplicate and missing SKUs, broken emails. Most store tools can't import that.

**How to run.** No dependencies, standard library only:

```bash
cd csv-cleanup
python3 clean_csv.py messy_products.csv
```

**Result.** 42 rows in → 33 clean rows + 9 rejected rows, each with a written reason. The script fixes what it can (prices, dates, categories, emails) and leaves cells it cannot fix safely blank and counted as "needs review" instead of guessing. Full numbers in [csv-cleanup/report.md](csv-cleanup/report.md).

## n8n-seo-flow — keyword list → clean article drafts

**Problem.** Writing SEO drafts one by one is repetitive: the same prompt structure, the same Markdown cleanup, the same quality checks every time.

**How to run.** In n8n: Workflows → Import from File → `ai-seo-article-generator.workflow.json`, then click **Execute workflow**. Default mode is offline mock — no API key needed. Live mode calls any OpenAI-compatible LLM through a Header Auth credential you add yourself.

**Result.** Tested in n8n 2.8.4: a full mock run turns 3 sample keywords into 3 articles marked READY, each with title, slug, word count and quality-check status, plus a one-row-per-article summary table.

---

Sample data is fictional. No credentials or customer data in this repository.
