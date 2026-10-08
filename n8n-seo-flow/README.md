# AI SEO Article Generator (n8n workflow)

**What it does:** turns a keyword list into clean, publish-ready article drafts. Builds a structured prompt per keyword (audience, tone, structure), calls an OpenAI-compatible LLM — or runs offline in mock mode with no API key — converts the Markdown output to tidy HTML, and quality-checks every article (title present, at least 3 sections, minimum length, no leftover Markdown).

**How to run:**

1. In n8n: Workflows → Import from File → `ai-seo-article-generator.workflow.json`
2. Click **Execute workflow** (default `mode = mock`, no API key needed)
3. For live mode: in **Config** set `mode = live`, then add a *Header Auth* credential on the LLM node; change the URL and model for other providers

**Result:** tested in n8n 2.8.4 — a full mock run turns 3 sample keywords into 3 articles marked READY, plus a summary table (keyword, title, word count, status, slug). No credentials or customer data included. All sample data is fictional.
