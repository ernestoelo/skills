---
name: xlsx
description: Skill for creating, editing, analyzing, and validating Excel and spreadsheet files (.xlsx, .xlsm, .csv, .tsv). Based on best practices from anthropic-examples/xlsx and following architect, dev-workflow, and sys-env standards.
---

# XLSX Skill

Provides tools and workflows for:
- Reading, editing, and creating Excel files
- Validating formulas and formatting
- Automating spreadsheet workflows

## When to Use
- Any task involving spreadsheet files as input or output
- Data cleaning, formula validation, or template creation

## Usage Example
```python
import pandas as pd
df = pd.read_excel('file.xlsx')
df.to_excel('output.xlsx', index=False)
```

## Advanced Example (openpyxl)
```python
from openpyxl import Workbook
wb = Workbook()
sheet = wb.active
sheet['A1'] = '=SUM(B2:B10)'
wb.save('output.xlsx')
```

## Formula Recalculation
Use the provided recalc.py script (see anthropic-examples/xlsx) to ensure all formulas are up to date.

## Best Practices
- Always use formulas, not hardcoded values
- Validate with recalc.py and fix errors
- Follow color and formatting standards

## Referencias
- Incluye como bundle los ejemplos y scripts de anthropic-examples/xlsx
- Sigue las guías de architect, dev-workflow y sys-env
