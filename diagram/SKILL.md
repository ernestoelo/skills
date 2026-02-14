---
name: diagram
description: Generates diagrams using PlantUML, providing templates and examples for architecture, documentation, and visualization.
---

# Diagram Generator Skill

Generates diagrams using PlantUML and Graphviz (dot) for architecture, workflows, and documentation. Mermaid is fully discarded. Provides bundled templates and examples for quick setup and reproducibility.

## When to Use
- Creating system architecture diagrams.
- Documenting workflows like Gitflow.
- Generating visual overviews for projects.
- Ensuring consistency in team diagrams.

## Usage
Follow this unified workflow for diagram generation and automation:

1. **Install PlantUML and Graphviz**: On Arch Linux, run `sudo pacman -S plantuml graphviz` (see compatibility and best practices in @sys-env).
2. **Choose template**: Use assets/ (examples/, imgs/, templates/) as reference.
3. **Edit .puml or .dot files**: Create or edit files using PlantUML syntax (`@startuml ... @enduml`) or Graphviz (`digraph {...}`).
4. **Generate diagrams automatically**: Run the script `scripts/generate_diagrams.sh [directory]` to convert all .puml and .dot files to PNG/SVG using PlantUML and Graphviz (see scripts/README.md). This enables integration and reproducibility, aligned with @architect and @dev-workflow.
5. **Integrate and version**: Add generated PNG/SVG files to documentation/repositories and version .puml/.dot files in Git.

## Anatomy
Skill structure:
- SKILL.md (metadata and instructions)
- scripts/ (automation and utilities)
- references/ (additional documentation)
- assets/ (resources: examples/, imgs/, templates/)
- README.md

## Best Practices
- Use assets to maintain visual consistency.
- Version .puml and .dot files in Git (as source code).
- Automate diagram generation with scripts/ for reproducibility.
- Integrate with @dev-workflow for robust workflows.
- Consult @sys-env before installing dependencies or modifying the environment.

## Resources
- Included assets: see assets/ for templates and examples.
- scripts/: automation utilities.
- PlantUML and Graphviz documentation.
- Inspiration: @anthropic-examples (theme-showcase.pdf for diagram styles).
- Cross-references: @architect for structure and automation, @dev-workflow for integration, @sys-env for safe environment.
## Example
- PlantUML: assets/examples/skill_structure_example.puml (compliant syntax, only top-level folders)
- Graphviz: add .dot examples in assets/examples/

## Company Standards
- Templates and reference diagrams are located in assets/templates/ and assets/examples/.
- Standard workflow diagrams (Gitflow, branches) are in assets/imgs/.
- All PlantUML examples must use only top-level folders, no nested folders or files, to avoid syntax errors and ensure compatibility.
- See assets/templates/system-architecture.png, system-overview.png, system-prod-env.png for company architecture standards.
- See assets/examples/biomass-web-architecture.png, biomass-web-overview.png, biomass-web-prod-env.png for real project examples.
- See assets/imgs/gitflow.png, gitflow-feature-branch.png, gitflow-release-branch.png for workflow standards.

## Syntax and Visualization Corrections
- The skill was updated to ensure PlantUML diagrams use only top-level folders or rectangles, avoiding errors from nested folders/files.
- Explicit arrows (-->), rectangles, and hidden links are used to guarantee valid and clear visualization.
- Example skills_project_structure.puml in Downloads shows the correct use of rectangles and arrows for project structure.
- All diagrams must be based on the templates and examples found in assets/templates/, assets/examples/, and assets/imgs/ to comply with company standards.
- Visual corrections and standards are documented for reproducibility and team alignment.
## Migration Notes
- Mermaid is fully discarded. All diagrams use PlantUML or Graphviz.
- Scripts updated to support .puml and .dot.