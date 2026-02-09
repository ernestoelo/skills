---
name: architect
description: Scaffolds skills and agents following official standards for multiple AI platforms (OpenCode, GitHub Copilot, Claude, Cursor). Creates proper folder structures, SKILL.md with valid frontmatter, and sets up bundled resources. Use when creating new skills or agents, or when structuring AI extension projects. Also use when users want to create a new skill (or update an existing skill) that extends AI capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skill Architect

Expert scaffolding tool for creating skills and agents across AI platforms.

## Core Principles

### Concise is Key

The context window is a public good shared with system prompt, conversation history, other skills' metadata, and the user request. **Default assumption: the AI is already very smart.** Only add context it doesn't already have. Challenge each piece of information: "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match specificity to the task's fragility:

- **High freedom** (text instructions): Multiple valid approaches, context-dependent decisions
- **Medium freedom** (pseudocode/parameterized scripts): Preferred pattern exists, some variation acceptable
- **Low freedom** (specific scripts): Fragile operations, consistency critical, specific sequence required

## Skill Anatomy

```
skill-name/
├── SKILL.md              # Required: Instructions for AI
├── scripts/              # Optional: Executable code (Python, Bash, etc.)
├── references/           # Optional: Documentation loaded as needed
└── assets/               # Optional: Templates, images, files for output
```

**Naming:** kebab-case, lowercase only: `^[a-z0-9]+(-[a-z0-9]+)*$`

### Progressive Disclosure

Three-level loading system:

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words, <500 lines)
3. **Bundled resources** - As needed (unlimited; scripts can execute without loading)

When SKILL.md approaches 500 lines, split into references. Always reference split files from SKILL.md with clear "when to read" guidance.

## Skill Creation Process

### Step 1: Classify the Need

**Type A: Skill (Reusable Tool/Knowledge)**
- Specific capability or domain knowledge
- Examples: "PDF processor", "Database schema reference", "Docker helper"
- Output: Full skill directory with `SKILL.md` + bundled resources

**Type B: Agent (Persona/Role)**
- Role or specialized persona
- Examples: "Code reviewer", "Documentation writer", "Test engineer"
- Output: Single `.agent.md` file (if supported by platform)

### Step 2: Understand with Concrete Examples

Ask the user:
- "What functionality should it support?"
- "Can you give examples of how it would be used?"
- "What would a user say that should trigger this skill?"

Conclude when there's a clear sense of required functionality.

### Step 3: Plan Reusable Contents

Analyze each example to identify:
- **scripts/**: Code rewritten repeatedly or needing deterministic reliability
- **references/**: Documentation the AI should consult while working
- **assets/**: Templates, images, fonts used in output (not loaded into context)

### Step 4: Initialize the Skill

For new skills, run from the **repository root**:

```bash
python3 scripts/init_skill.py <skill-name> --path <output-directory>
```

This creates the directory structure with template SKILL.md and example resource files.

### Step 5: Implement the Skill

#### Start with Bundled Resources

Implement scripts, references, and assets first. Test all scripts by running them. Delete example files not needed.

#### Write SKILL.md

**Frontmatter** (only `name` and `description` allowed, plus optional `license`):

```yaml
---
name: skill-name
description: Comprehensive description including WHAT it does and WHEN to use it. Include trigger scenarios, file types, and tasks. All "when to use" info goes HERE, not in the body.
---
```

**Body:** Instructions for using the skill and its bundled resources. Use imperative/infinitive form.

#### Design Patterns

Consult these based on your skill's needs:
- **Multi-step processes**: See `references/workflows.md`
- **Output formats/quality standards**: See `references/output-patterns.md`
- **Platform distribution**: See `references/platform-sync.md`

### Step 6: Validate and Package

**Validate** (from repository root):
```bash
python3 scripts/quick_validate.py <path/to/skill-folder>
```

**Package for distribution** (from repository root):
```bash
python3 scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

Creates a `.skill` file (zip format) after automatic validation.

### Step 7: Iterate

After testing the skill, iterate based on real usage:

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Update SKILL.md or bundled resources
4. Re-validate and test again

## Scaffolding Agents

For **Type B (Agents)**, create a single `.agent.md` file:

```markdown
---
name: agent-name
role: Brief role description
---

# Agent Name

You are a [role] who specializes in [domain].

## Responsibilities
- Responsibility 1

## Approach
Your approach to tasks should...

## Guidelines
- Guideline 1
```

**Note:** Not all platforms support `.agent.md` files. For the full `.agent.md` schema (including `tools`, `handoffs`, `mcp-servers`, `model`, etc.), see `references/agents-spec.md`.

## Cross-Platform Compatibility

**Universal Frontmatter:**
```yaml
---
name: skill-name
description: ...
---
```

**Platform Locations:**
- **GitHub Copilot:** `~/.copilot/skills/` (reads directly)
- **OpenCode:** `~/.config/opencode/skills/` (symlinks)
- **Claude Desktop:** `~/.config/claude/skills/` (symlinks)
- **Cursor:** `~/.config/cursor/skills/` (symlinks)

See `references/platform-sync.md` for complete distribution guide.

## Description Writing

The `description` field is **critical** - it determines when the skill triggers.

Good:
```yaml
description: Complete PostgreSQL database management including schema documentation, query helpers, backup scripts, and migration tools. Use when working with PostgreSQL databases, writing SQL queries, designing schemas, or managing database operations.
```

Bad:
```yaml
description: Database tool
```

## Content Organization Rules

**Keep in SKILL.md:** Core workflow, quick reference, pointers to resources
**Move to references/:** Long/detailed content, domain-specific docs, occasionally-needed content
**Move to scripts/:** Frequently rewritten code, deterministic operations, token-heavy tasks
**Move to assets/:** Templates for output, images, fonts, boilerplate

**Do NOT create:** README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, or any auxiliary docs.

## Validation Checklist

Before committing:
- [ ] Valid YAML frontmatter with `name` and `description`
- [ ] `name` matches directory name (kebab-case)
- [ ] `description` is comprehensive (what + when + triggers)
- [ ] No README.md or auxiliary docs
- [ ] Scripts are tested
- [ ] References organized (1 level deep, TOC for >100 lines)
- [ ] SKILL.md under 500 lines

## Resources

- **Design Patterns:** `references/workflows.md`, `references/output-patterns.md`
- **Agents Schema:** `references/agents-spec.md`
- **Platform Sync:** `references/platform-sync.md`
- **Tooling (repo root):** `scripts/init_skill.py`, `scripts/package_skill.py`, `scripts/quick_validate.py`
