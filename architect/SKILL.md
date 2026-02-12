---
name: architect
description: Scaffolds skills and agents for AI platforms, ensuring proper structures, workflows, and resources. Use to create or refine skills and maintain compatibility across tooling.
---

# Architect Skill Guide

## Description
The `architect` skill provides tools and workflows to scaffold, organize, and maintain skills and agents for AI platforms. It enforces the canonical structure and best practices from anthropic-examples, the skill-creator example, and the official https://github.com/anthropics/skills.git repository.

## When to Use
- To create new skills or agents: generates the recommended folder and file structure.
- To reorganize resources: enforces SKILL.md, scripts/, references/, and assets/ according to the skill's domain.
- To ensure cross-platform compatibility and maintainability.
- To package skills for distribution or deployment.

## Usage Guide
When a new skill is requested, architect automatically runs the `scripts/skill_scaffold.py` script with the skill name and description. This generates the standard structure (SKILL.md, scripts/, references/, assets/, README.md) following the skill-creator and anthropic-examples pattern.

### Example
To create a new skill called "my-skill":

```bash
python scripts/skill_scaffold.py my-skill "Description of the new skill."
```

This will create the structure:
```
my-skill/
├── SKILL.md
├── scripts/
├── references/
├── assets/
├── README.md
```

You can customize SKILL.md and add resources as needed for your domain.

## Integration with dev-workflow and sys-env
- **Validation:** Use pre-commit hooks and validation flows from @dev-workflow to ensure quality and reproducibility.
- **Compatibility:** Before running scripts, check dependencies and environment using @sys-env guidelines.
- **CI/CD:** Skills can be integrated into pipelines following dev-workflow standards (semantic commits, branch management, hooks, etc.).

## Anatomy of the Skill
- SKILL.md (guide and metadata)
- scripts/ (automation and utilities)
- references/ (additional documentation, examples)
- assets/ (visual resources, templates)
- README.md

## Best Practices
- Follow the canonical structure for all new skills.
- Use scripts/ for automation and reproducibility.
- Document usage and integration in SKILL.md and README.md.
- Reference @dev-workflow and @sys-env for validation and environment management.

## References
- [references/skill-creator.md](references/skill-creator.md): Canonical skill template and best practices from anthropic
- Follow the conventions of https://github.com/anthropics/skills.git for maximum compatibility.