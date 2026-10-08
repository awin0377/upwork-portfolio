# CSV cleanup (Python, standard library only)

**What it does:** normalises a messy product list into an import-ready CSV — product names, categories, prices (`$35.5 USD` → `35.50`), four date formats → `YYYY-MM-DD`, emails, duplicate and missing SKUs. Rows it cannot fix safely go to a separate file with a written reason, instead of being guessed.

**How to run:**

```bash
python3 clean_csv.py messy_products.csv
```

Writes `clean_products.csv`, `rejected_rows.csv` and `report.md`.

**Result:** 42 rows in → 33 clean rows + 9 rejected with reasons. 25 price cells, 19 dates, 17 categories, 16 names, 14 emails and 13 stock values corrected; cells it cannot fix are left blank and counted as "needs review". Sample data is fictional.
