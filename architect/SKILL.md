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
- **Post-Scaffold Step:** Run `./scripts/sync-skills.sh` to sync the new skill to AI platforms (e.g., OpenCode). Restart your assistant if needed for detection.

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

### Global Skill Activation
For platforms like OpenCode that support declarative skill loading, activate all skills at conversation start to ensure availability without runtime code execution.

```bash
python3 architect/scripts/activate_all.py
```
- Discovers all skills in the repository.
- Validates each skill using `quick_validate.py`.
- Outputs a summary of valid skills ready for activation.
- Run from repository root; fails if invalid skills found.

**Example Output:**
```
🔍 Discovering skills...
Found 7 skill(s): architect, dev-workflow, mcp-builder, pdf, recursive-context, sys-env, web-scraper

🔧 Validating skills...
✅ architect: Skill is valid!
✅ dev-workflow: Skill is valid!
✅ mcp-builder: Skill is valid!
✅ pdf: Skill is valid!
✅ recursive-context: Skill is valid!
✅ sys-env: Skill is valid!
✅ web-scraper: Skill is valid!

📋 Summary:
Total skills: 7
Valid skills: 7
Available for activation: architect, dev-workflow, mcp-builder, pdf, recursive-context, sys-env, web-scraper

✨ All skills validated! Ready for OpenCode activation.
```

**Integration Notes:** Use in OpenCode conversations requiring multiple skills. No platform restart needed if declarative. Run after adding new skills or updates.

#### Automatic Activation via Sync
Skills are automatically activated for OpenCode after synchronization via `scripts/sync-skills.sh`. This ensures skills are validated and ready for conversation starts without manual intervention. The sync script runs `activate_all.py` post-sync to OpenCode, providing context for autonomous AI behavior.
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
| 1.3.0   | 2026-02-11 | Added automatic skill activation for OpenCode via sync script|
| 1.2.0   | 2026-02-10 | Added global skill activation script for OpenCode support|
| 1.1.0   | 2026-02-09 | Applied standardized SKILL.md template for consistency|
| 1.0.0   | 2025-05-16 | Initial documentation for skills and agents scaffolding|

## Resources
- **Design Patterns:** `references/workflows.md`, `references/output-patterns.md`
- **Platform Sync:** `references/platform-sync.md`
- **Tooling Scripts:** `../scripts/init_skill.py`, `../scripts/package_skill.py`, `../scripts/quick_validate.py`

<!-- Test change for CI validation -->