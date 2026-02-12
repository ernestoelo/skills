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
python3 shared/scripts/extract.py <url>
```
This script performs the following tasks:
1. Downloads the HTML from the given URL.
2. Removes noise (ads, buttons, UI elements).
3. Outputs clean HTML in semantic Markdown format.

### Save Web Documentation as Markdown
```bash
python3 shared/scripts/extract.py "<url>" > shared/docs/article.md
```
- Redirects extracted content to a `.md` file.
- Use `>>` to append to an existing Markdown file.

### Batch Processing
For processing lists of URLs:
```bash
while read url; do
  python3 shared/scripts/extract.py "$url" >> shared/docs/knowledge-base.md
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
