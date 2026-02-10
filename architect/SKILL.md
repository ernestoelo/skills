---
name: architect
description: Scaffolds skills and agents for AI platforms, ensuring proper structures, workflows, and resources. Use to create or refine skills and maintain compatibility across tooling.
---

# Architect Skill Guide

## Description
The `architect` skill provides tools and workflows for creating scalable, reusable skills and agents across AI platforms. Whether creating new skills or refining existing ones, `architect` ensures structures adhere to best practices, enabling maintainability and compatibility.

## When to Use the Skill
- **Setting up new skills or agents:** Quickly scaffold project directories with essential components.
- **Reorganizing resources:** Structure SKILL.md, bundled assets, and references for clarity.
- **Ensuring cross-platform compatibility:** Validate that skills work across environments.
- **Packaging skills for distribution:** Prepare skills for deployment.

## Usage Guide
Note: The following commands should be run from the repository root directory to access the shared tooling scripts.

### Skill Scaffolding
```bash
python3 ../scripts/init_skill.py <skill-name> --path <output-dir>
```
- Generates a skill folder with `SKILL.md` and template resources.
- Naming follows kebab-case conventions (e.g., `pdf-processor`).

#### Validate and Package
```bash
python3 ../scripts/quick_validate.py <skill-path>
python3 ../scripts/package_skill.py <skill-path> [output-dir]
```
- Generates a skill folder with `SKILL.md` and template resources.
- Naming follows kebab-case conventions (e.g., `pdf-processor`).

#### Validate and Package
```bash
python3 scripts/quick_validate.py <skill-path>
python3 scripts/package_skill.py <skill-path> [output-dir]
```
- Ensures the skill meets structural requirements.
- Creates a distributable `.skill` package.

### Agent Configuration
#### Create a New Agent
For Type B workflows, create an `.agent.md` file:
```markdown
---
name: agent-name
role: Specialized role description
---

# [Agent Name]

Responsibilities, approaches, and task guidelines for the agent.
```

## Inputs and Outputs
### Inputs
- **Skill name and scope:** Name for the skill/agent and its intended functionality.
- **Resources:** Scripts, references, assets defining the skill’s output.

### Outputs
- **Skill directory:** Properly structured directories ready for deployment.
- **Packaged skill:** A distributable `.skill` file with all required resources.

## Best Practices and Version History
### Best Practices
- Follow kebab-case naming conventions for skills.
- Ensure SKILL.md does not exceed 500 lines (split long sections into references).
- Always validate skills before committing them.

### Version History
| Version | Date       | Updates                                                |
|---------|------------|-------------------------------------------------------|
| 1.1.0   | 2026-02-09 | Applied standardized SKILL.md template for consistency|
| 1.0.0   | 2025-05-16 | Initial documentation for skills and agents scaffolding|

## Resources
- **Design Patterns:** `references/workflows.md`, `references/output-patterns.md`
- **Platform Sync:** `references/platform-sync.md`
- **Tooling Scripts:** `../scripts/init_skill.py`, `../scripts/package_skill.py`, `../scripts/quick_validate.py`

<!-- Test change for CI validation -->