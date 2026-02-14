
# Diagram Generation Scripts

Includes utilities to automate diagram generation from .puml and .dot files using PlantUML and Graphviz.

- `generate_diagrams.sh`: Finds and converts all .puml files to PNG/SVG using PlantUML, and all .dot files to PNG/SVG using Graphviz.

## Quick Usage

```bash
cd scripts
chmod +x generate_diagrams.sh
./generate_diagrams.sh ../assets
```

Make sure PlantUML and Graphviz are installed (see instructions in SKILL.md and @sys-env).
