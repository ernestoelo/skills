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
python3 shared/scripts/init_skill.py <skill-name> --path <output-dir>
```
- Genera una carpeta de skill con `SKILL.md` y recursos.
- Nombres en kebab-case (ej: `pdf-processor`).
- **Post-Scaffold:** Ejecuta `python3 shared/scripts/sync-skills.sh` para sincronizar la skill. Reinicia el asistente si es necesario.
- **Desarrollo:** Siempre ejecuta @dev-workflow tras crear una skill:
   ```bash
   python3 shared/scripts/quick_validate.py <skill-name>
   python3 dev-workflow/scripts/auto_correct_portable.py --workflow "Skill Validation CI"
   git add . && git commit -m "feat: add <skill-name> skill"
   git push
   ```

#### Validate and Package
```bash
python3 shared/scripts/quick_validate.py <skill-path>
python3 shared/scripts/package_skill.py <skill-path> [output-dir]
```
- Genera y valida la skill.

#### Validate and Package
```bash
python3 shared/scripts/quick_validate.py <skill-path>
python3 shared/scripts/package_skill.py <skill-path> [output-dir]
```
- Valida y empaqueta la skill.

### Global Skill Activation
Para plataformas como OpenCode, activa todas las skills al inicio de la conversación:

```bash
python3 shared/architect/scripts/activate_all.py
```
- Descubre y valida skills usando `shared/scripts/quick_validate.py`.

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

#### Autonomous Skill Loading
For fully autonomous skill activation without @ mentions, use the `auto_skill_loader` MCP server:

1. **Run the MCP Server:**
   ```bash
   cd ~/.copilot/skills
   ./start_auto_skill_loader.sh
   # Or manually: ~/.local/bin/fastmcp run auto_skill_loader.py
   ```

2. **Integration with OpenCode:**
   - The MCP server provides tools for automatic skill loading based on conversation context
   - Tools analyze messages and load relevant skills autonomously
   - Supports pattern matching for keywords like "pdf", "git", "web-scraper", etc.

3. **Available Tools:**
   - `analyze_message_for_skills`: Analyzes messages for relevant skills
   - `load_skill`: Loads specific skill content
   - `load_relevant_skills`: Automatically loads all relevant skills for a message
   - `list_available_skills`: Lists all available skills

**Note:** While OpenCode doesn't currently support direct MCP integration, the server can run independently and be used programmatically for skill management.
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
| 1.5.0   | 2026-02-11 | Added autonomous skill loading via MCP server for automatic activation without @ mentions|
| 1.4.0   | 2026-02-11 | Added post-scaffold @dev-workflow application for consistent skill creation|
| 1.3.0   | 2026-02-11 | Added automatic skill activation for OpenCode via sync script|
| 1.2.0   | 2026-02-10 | Added global skill activation script for OpenCode support|
| 1.1.0   | 2026-02-09 | Applied standardized SKILL.md template for consistency|
| 1.0.0   | 2025-05-16 | Initial documentation for skills and agents scaffolding|

## Resources
- **Design Patterns:** `shared/references/workflows.md`, `shared/references/output-patterns.md`
- **Platform Sync:** `shared/references/platform-sync.md`
- **Auto Skill Loading:** `shared/core/auto_skill_loader.py` (MCP server), `shared/core/start_auto_skill_loader.sh` (startup script)
- **Tooling Scripts:** `shared/scripts/init_skill.py`, `shared/scripts/package_skill.py`, `shared/scripts/quick_validate.py`