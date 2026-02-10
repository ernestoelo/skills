---
name: web-scraper
description: Fetches web pages (documentation, articles) and converts them into clean, noise-free Markdown for context building. Use when the user wants to scrape, fetch, or download a page, read a URL, extract content from a website, or convert HTML to Markdown.
---
# Web Scraper Skill Guide

## Description
The Web Scraper skill automates the retrieval and transformation of web page content. It excels at noise-free extraction to Markdown, enabling seamless integration for LLM consumption, documentation, or offline use.

## When to Use the Skill
- **Save a URL as Context or Documentation:** Extract and store site content in Markdown.
- **Summarize HTML pages:** Clean and process noisy or unstructured data.
- **Merge pages for context-building:** Combine multiple sources into a coherent Markdown file.

## Usage Guide

### Fetch and Clean a URL
```bash
python3 scripts/extract.py <url>
```
This script performs the following tasks:
1. Downloads the HTML from the given URL.
2. Removes noise (ads, buttons, UI elements).
3. Outputs clean HTML in semantic Markdown format.

### Save Web Documentation as Markdown
```bash
python3 scripts/extract.py "<url>" > docs/article.md
```
- Redirects extracted content to a `.md` file.
- Use `>>` to append to an existing Markdown file.

### Batch Processing
For processing lists of URLs:
```bash
while read url; do
  python3 scripts/extract.py "$url" >> knowledge-base.md
done < urls.txt
```

## Inputs and Outputs

### Inputs
- **URL:** Fully qualified link to the webpage (e.g., `https://example.com`).

### Outputs
- **Result Markdown:** Noise-free semantic Markdown.

## Best Practices
- Always save Markdown files clearly (e.g., `pandas-summary.md`).

## Version History
| Version | Date       | Notes                                          |
|---------|------------|-----------------------------------------------|
| 1.1.0   | 2026-02-09 | Major reorganization aligned to skill standards |

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
