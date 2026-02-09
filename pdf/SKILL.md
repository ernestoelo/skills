---
name: pdf
description: The PDF skill enables advanced operations on PDF files, including merging, splitting, extracting, creating, and modifying PDFs. It also supports OCR for scanned PDFs and detailed table/text extraction.
author: OpenCode Project Team
version: 1.0.0
---

# PDF Processing Skill Guide

## Description
The PDF skill provides a rich set of tools and examples to handle any PDF-related processing. Whether you need to extract text, merge files, create watermarks, or add password protection, the skill integrates Python libraries and command-line utilities to ensure robust functionality.

## When to Use the Skill
- Extracting tables or text from a PDF for data analysis.
- Merging or splitting PDF documents for organization.
- Adding encryption, watermarks, or metadata to enhance security and professionalism.
- Handling scanned PDFs via OCR to make them searchable or extract readable content.
- Creating brand-new PDF documents with dynamic content.

## Usage Guide

### Code Examples
#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Extract Text from Scanned PDFs
```python
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Command-Line Usage
#### Extract Text with `pdftotext`
```bash
pdftotext input.pdf output.txt
```

#### Merge PDFs with `qpdf`
```bash
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
```

## Inputs and Outputs

### Inputs
- **File path:** Path to the input PDF file(s) (e.g., `input.pdf`).
- **Operation:** The specific processing task (e.g., merge, split, extract).
- **Additional arguments:** Optional arguments such as passwords, metadata, or specific pages.

### Outputs
- **Result file:** Path to the output PDF file (e.g., `output.pdf`).
- **Extracted data:** Text, tables, or other extracted formats depending on the task.

## Best Practices and Known Limitations
- Always ensure that Python libraries (`pypdf`, `pdfplumber`) and external tools (`pdftotext`, `qpdf`) are correctly installed in your environment.
- OCR processes (e.g., `pytesseract`) rely on high-resolution scanned documents for optimal accuracy.
- Avoid using Unicode subscripts/superscripts with ReportLab due to font limitations.

## Example Workflows
### Creating PDFs from Scratch
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello_world.pdf", pagesize=letter)
c.drawString(100, 750, "Hello, World!")
c.save()
```

### Adding Watermarks to Pages
```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

## Version History and Changelog
| Version | Date       | Description                                                                 |
|---------|------------|-----------------------------------------------------------------------------|
| 1.0.0   | 2022-02-09 | Initial release with examples, usage guides, and best practices             |

