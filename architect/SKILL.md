---
name: architect
description: Scaffolds skills and agents following official standards for multiple AI platforms (OpenCode, GitHub Copilot, Claude, Cursor). Creates proper folder structures, SKILL.md with valid frontmatter, and sets up bundled resources. Use when creating new skills or agents, or when structuring AI extension projects.
---

# Skill Architect

Expert scaffolding tool for creating skills and agents across AI platforms.

## Overview

This skill helps you create well-structured, platform-compatible skills and agents. It follows official standards from Anthropic and adapts them for use across multiple platforms: OpenCode, GitHub Copilot, Claude Desktop, and Cursor.

## Sources of Truth

The scaffolding process is based on:

1. **Anthropic's Official Template:** `./knowledge/templates/skill-creator/SKILL.md`
   - The gold standard for skill creation
   - Comprehensive guide on structure, content, and best practices
   
2. **Platform Specifications:** `./knowledge/specs/`
   - `vscode-agent-skills.md` - VSCode/Copilot specs
   - `vscode-custom-agents.md` - Custom agents for VSCode
   - `agentskills-spec.md` - General agent skills specification

3. **Repository Documentation:** `../../docs/creating-skills.md`
   - Practical guide for this specific repository
   - Platform-specific setup instructions

## Capabilities

### 1. Classify the Need

When asked to create something, first classify:

**Type A: Skill (Reusable Tool/Knowledge)**
- User wants a specific capability or domain knowledge
- Examples: "PDF processor", "Database schema reference", "Docker helper"
- **Output:** Full skill directory with `SKILL.md` + bundled resources

**Type B: Agent (Persona/Role)**
- User wants a role or specialized persona
- Examples: "Code reviewer", "Documentation writer", "Test engineer"
- **Output:** Single `.agent.md` file (if supported by platform)

### 2. Scaffold Skills

For **Type A (Skills)**, create a complete directory structure:

```
skill-name/
├── SKILL.md              # Required: Instructions for AI
├── scripts/              # Optional: Executable code (Python, Bash, etc.)
├── references/           # Optional: Documentation to load as needed
└── assets/               # Optional: Templates, images, files for output
```

**Naming Convention:**
- Use kebab-case: `my-skill-name`
- Lowercase only: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Name must match directory name

**SKILL.md Template:**

```markdown
---
name: skill-name
description: Comprehensive description of what the skill does and when to use it (include triggers, use cases, file types, etc.)
---

# Skill Name

Brief overview...

## Key Features

- Feature 1
- Feature 2

## Usage

Instructions for the AI...

## Examples

[Examples here]

## Resources

- See `references/file.md` for detailed documentation
- Run `scripts/tool.py` for automated processing
```

**Bundled Resources Guidelines:**

- **scripts/**: Executable code for deterministic or repeatedly-written operations
  - Test all scripts before committing
  - Include only essential scripts
  
- **references/**: Documentation loaded as needed
  - API docs, schemas, detailed guides
  - Keep SKILL.md lean by moving details here
  - Include table of contents for files >100 lines
  
- **assets/**: Files used in output (not loaded into context)
  - Templates, boilerplate code
  - Images, fonts, media
  - Files to be copied or modified in output

### 3. Scaffold Agents

For **Type B (Agents)**, create a persona file:

```markdown
---
name: agent-name
role: Brief role description
---

# Agent Name

You are a [role] who specializes in [domain].

## Responsibilities

- Responsibility 1
- Responsibility 2

## Approach

Your approach to tasks should...

## Guidelines

- Guideline 1
- Guideline 2
```

**Note:** Not all platforms support `.agent.md` files. Check platform compatibility.

### 4. Cross-Platform Compatibility

Ensure skills work across multiple platforms:

**Universal Frontmatter (All Platforms):**
```yaml
---
name: skill-name          # Required everywhere
description: ...          # Required everywhere
---
```

**Extended Frontmatter (Platform-Specific):**
```yaml
---
name: skill-name
description: ...
license: MIT              # OpenCode, Claude
compatibility: opencode   # OpenCode only
metadata:                 # OpenCode only
  author: Your Name
  version: 1.0.0
---
```

**Platform Locations:**
- **GitHub Copilot:** `~/.copilot/skills/`
- **OpenCode:** `~/.config/opencode/skills/` (via symlinks)
- **Claude Desktop:** `~/.claude/skills/`
- **Cursor:** `~/.cursor/skills/`

### 5. Repository Integration

For skills in this repository (`~/.copilot/skills/`):

**After Creating a Skill:**

1. **Test the skill** with your AI assistant
2. **Commit to git:**
   ```bash
   git add skill-name/
   git commit -m "feat: add skill-name"
   git push
   ```

3. **Sync to platforms:**
   - **GitHub Copilot**: No action needed (source directory)
   - **OpenCode/Claude/Cursor**: Run `./scripts/sync-skills.sh` or `git pull` (auto-syncs)
   - **Specific platform**: Run `./scripts/sync-skills.sh --platform <name>`

## Workflow Examples

### Example 1: Creating a Database Helper Skill

**User:** "Create a skill to help me work with PostgreSQL databases"

**Architect Analysis:**
- **Type:** A (Skill - Tool)
- **Needs:** SQL query helpers, schema documentation
- **Structure:**
  ```
  postgres-helper/
  ├── SKILL.md              # Quick reference + common queries
  ├── references/
  │   ├── schema.md         # Database schema
  │   └── best-practices.md # SQL best practices
  └── scripts/
      ├── backup.sh         # Backup script
      └── migrate.py        # Migration helper
  ```

**Actions:**
1. Create directory structure
2. Write SKILL.md with frontmatter
3. Add schema documentation to references/
4. Create utility scripts
5. Test with sample queries
6. Commit and sync

### Example 2: Creating a Code Reviewer Agent

**User:** "Create an agent that reviews code for security issues"

**Architect Analysis:**
- **Type:** B (Agent - Persona)
- **Needs:** Security-focused review guidelines
- **Structure:** Single `security-reviewer.agent.md`

**Actions:**
1. Create `.agent.md` with persona definition
2. Include security checklist
3. Define review approach
4. Test with sample code
5. Commit

### Example 3: Multi-Framework Skill

**User:** "Create a skill for deploying to different cloud providers"

**Architect Analysis:**
- **Type:** A (Skill - Multi-variant)
- **Structure:**
  ```
  cloud-deploy/
  ├── SKILL.md              # Overview + provider selection
  └── references/
      ├── aws.md            # AWS deployment patterns
      ├── gcp.md            # GCP deployment patterns
      └── azure.md          # Azure deployment patterns
  ```

**Progressive Disclosure:**
- SKILL.md: High-level workflow + "which provider?"
- AI loads only the relevant reference file based on user's choice

## Best Practices

### Description Writing

The `description` field is **critical** - it determines when the skill triggers.

✅ **Good:**
```yaml
description: Complete PostgreSQL database management including schema documentation, query helpers, backup scripts, and migration tools. Use when working with PostgreSQL databases, writing SQL queries, designing schemas, or managing database operations.
```

❌ **Bad:**
```yaml
description: Database tool
```

### Content Organization

**Keep SKILL.md under 500 lines:**
- Core workflow and instructions
- Quick reference
- Pointers to bundled resources

**Move to references/ when:**
- Content is long or detailed
- Content is domain-specific docs
- Content is only needed occasionally

**Move to scripts/ when:**
- Code is rewritten frequently
- Deterministic execution is critical
- Token efficiency matters

### Progressive Disclosure

Structure for efficient context usage:

1. **Metadata** (name + description) - Always loaded
2. **SKILL.md** - Loaded when skill triggers
3. **Bundled resources** - Loaded as needed

### Validation

Before committing a skill:

**Checklist:**
- [ ] Valid YAML frontmatter
- [ ] `name` matches directory name
- [ ] `description` is comprehensive (includes what, when, triggers)
- [ ] Name follows pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`
- [ ] No README.md or auxiliary docs
- [ ] Scripts are tested
- [ ] References are organized
- [ ] Compatible across target platforms

## Platform-Specific Notes

### OpenCode

After creating a skill, sync to AI platforms:
```bash
cd ~/.copilot/skills
./architect/scripts/sync-skills.sh  # Auto-syncs to all installed platforms
```

Or if git hook is configured:
```bash
git pull  # Auto-syncs to all installed platforms
```

### GitHub Copilot

Skills in `~/.copilot/skills/` are immediately available. No sync needed.

### Claude Desktop

If using symlinks from this repository:
```bash
ln -s ~/.copilot/skills ~/.claude/skills
```

### Cursor

If using symlinks from this repository:
```bash
ln -s ~/.copilot/skills ~/.cursor/skills
```

## Error Prevention

**Common mistakes to avoid:**

❌ Creating README.md (use SKILL.md instead)
❌ Inconsistent name in frontmatter vs directory
❌ Vague description ("A tool for...")
❌ Uppercase or underscore in skill names
❌ Deeply nested references (keep 1 level deep)
❌ Untested scripts
❌ Duplicating content between SKILL.md and references

## Resources

- **Anthropic's Official Guide:** `./knowledge/templates/skill-creator/SKILL.md`
- **Creation Guide:** `../../docs/creating-skills.md`
- **Platform Specs:** `./knowledge/specs/`
- **Example Skills:** `../../{pdf,mcp-builder,web-scraper}/`

---

**When in doubt, consult the official Anthropic template at `./knowledge/templates/skill-creator/SKILL.md` for comprehensive guidance.**
