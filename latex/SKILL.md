---
name: latex
description: Skill for compiling LaTeX documents in VS Code with specific formatting, integrable with document processing skills.
---

# LaTeX Compilation Skill

This skill provides tools and workflows for compiling LaTeX documents in VS Code with specific formatting standards. It focuses on academic and technical document compilation, supporting integration with document processing skills for output conversion.

## When to Use
- Compiling LaTeX documents to PDF in VS Code
- Applying predefined formats (academic reports, technical informes)
- Generating documents integrable with PDF/docx/xlsx processing

## Usage Guide
1. Open LaTeX file in VS Code with LaTeX Workshop extension
2. Use `scripts/compile_latex.sh <file.tex>` for compilation
3. Optional: Use pandoc via `scripts/integrate_docs.sh` for conversion to docx

## Integrations
- Generates PDFs usable by @pdf skill for text extraction/OCR
- Can convert to docx with pandoc for @docx processing
- Supports basic export for @xlsx if tables are included

## Best Practices
- Use provided templates in assets/
- Follow VS Code integration guidelines in references/
- Validate LaTeX syntax before compilation

### Important Warnings
- **Never use straight double quotes (`"`) in LaTeX or Beamer documents.** They can break the text rendering. Use `` (two backticks) for opening quotes and '' (two single quotes) for closing quotes, or use the appropriate LaTeX quote commands.
- **Always check the size of created tables.** Tables that are too wide may overflow the page in both standard LaTeX and Beamer presentations. Adjust table width or use packages like `tabularx` or `resizebox` to ensure tables fit within the page or slide boundaries.

## References
- [references/latex-formats.md](references/latex-formats.md): Formatting guidelines
- [references/vscode-integration.md](references/vscode-integration.md): VS Code setup