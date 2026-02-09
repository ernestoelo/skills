---
name: web-scraper
description: Fetches web pages (documentation, articles) and converts them into clean, noise-free Markdown for context building. Use when the user wants to scrape, fetch, or download a page, read a URL, extract content from a website, or convert HTML to Markdown.
---
# Web Scraper & Context Builder

You are an expert at gathering external information. Your goal is to convert messy HTML from the web into clean, semantic Markdown that is easy for LLMs to read.

## ⚡ Capabilities

### 1. Fetch & Clean URL

Use this when the user sends a link and says "read this", "save this as context", or "summarize this page".

* **Script:** `python3 scripts/extract.py <url>`
* **Behavior:**
  1. Downloads the HTML.
  2. Removes UI noise (navbars, ads, buttons).
  3. Converts semantic content to Markdown.
  4. Outputs to STDOUT.

### 2. Save Context (Common Workflow)

If the user asks to "save" a URL as documentation:

1. Run the script and redirect output to a file in the user's project.
   ```bash
   python3 scripts/extract.py "https://example.com/docs" > ./docs/topic.md
   ```

## 🧠 Best Practices

* **Documentation:** When fetching docs, prefer naming the file with a specific suffix (e.g., `libs/pandas-guide.md`).
* **Append Mode:** If building a large context file from multiple pages, use `>>` to append.
