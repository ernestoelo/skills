---
name: docx
description: Skill for creating, editing, and analyzing Word documents (.docx). Based on best practices from anthropic-examples/docx and following architect, dev-workflow, and sys-env standards.
---

# DOCX Skill

Provides tools and workflows for:
- Creating and editing Word documents
- Extracting and analyzing content
- Automating document formatting and validation

## When to Use
- Any task involving .docx files (reports, memos, templates)
- Content extraction, tracked changes, or format conversion

## Usage Example
```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

## Advanced Example (docx-js)
```javascript
const { Document, Packer, Paragraph } = require('docx');
const doc = new Document({ sections: [{ children: [new Paragraph('Hello World')] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync('doc.docx', buffer));
```

## Validation
Use the provided validate.py script (see anthropic-examples/docx) to ensure document compliance.

## Best Practices
- Always set page size explicitly
- Use built-in heading styles for TOC
- Validate with validate.py and fix errors

## Referencias
- Incluye como bundle los ejemplos y scripts de anthropic-examples/docx
- Sigue las guías de architect, dev-workflow y sys-env
