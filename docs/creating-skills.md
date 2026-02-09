# Creating Skills Guide

This guide explains how to create effective skills for AI assistants.

## Quick Start

The **easiest way** to create a new skill is to use the `architect` skill:

```
Ask your AI assistant: "Create a new skill for [your use case]"
```

The architect skill will guide you through the entire process.

## Manual Creation

If you prefer to create skills manually, follow these steps:

### 1. Initialize Structure

```bash
cd ~/.copilot/skills
mkdir my-skill-name
cd my-skill-name
```

### 2. Create SKILL.md

```markdown
---
name: my-skill-name
description: Clear description of what this skill does and when to use it
---

# My Skill Name

Brief overview of what this skill provides.

## Usage

Instructions for the AI on how to use this skill...

## Examples

Example workflows or code...
```

### 3. Add Resources (Optional)

```bash
# Create directories as needed
mkdir scripts      # For executable code (Python, Bash, etc.)
mkdir references   # For documentation to load as needed
mkdir assets       # For templates, images, etc.
```

### 4. Commit and Sync

```bash
git add my-skill-name/
git commit -m "feat: add my-skill-name"
git push

# If using OpenCode
cd ..
./sync-to-opencode.sh
```

## Best Practices

### Frontmatter

**Required fields:**
- `name`: Lowercase, hyphen-separated, matches directory name
- `description`: Clear, comprehensive description (1-1024 chars)

**Optional fields:**
- `license`: License type (e.g., MIT, Proprietary)

### Description Writing

The description is **critical** - it's how the AI decides when to use your skill.

✅ **Good description:**
```yaml
description: Complete PDF processing including reading, creating, modifying, merging, splitting, rotating, adding watermarks, filling forms, encrypting/decrypting, extracting images, and OCR on scanned PDFs. Use when working with .pdf files or when the user mentions PDF operations.
```

❌ **Bad description:**
```yaml
description: PDF tool
```

**Guidelines:**
- Include **what** the skill does
- Include **when** to use it
- Include specific trigger words/phrases
- Be comprehensive but concise

### Content Organization

**SKILL.md should contain:**
- Core instructions and workflows
- Quick reference information
- Pointers to bundled resources

**Move to `references/` if:**
- Content is long (>500 lines total in SKILL.md)
- Content is only needed occasionally
- Content is domain-specific documentation
- Content is API reference material

**Move to `scripts/` if:**
- Code is rewritten frequently
- Deterministic execution is critical
- Token efficiency is important

**Move to `assets/` if:**
- Files are templates for output
- Files are images, fonts, or media
- Files shouldn't be loaded into context

### Progressive Disclosure

Structure skills for efficient context usage:

```
1. Metadata (name + description) - Always loaded (~100 words)
2. SKILL.md body - Loaded when skill triggers (<5k words)
3. Bundled resources - Loaded as needed by AI
```

**Example structure:**

```markdown
# My Skill

## Quick Start
[Essential information here]

## Common Tasks
[Brief guides with code examples]

## Advanced Features
For detailed information, see:
- `references/advanced.md` - Advanced workflows
- `references/api.md` - API reference
- `references/examples.md` - Complete examples
```

## Platform Compatibility

### Directory Structure

All platforms support this standard structure:

```
skill-name/
├── SKILL.md              # Required
├── scripts/              # Optional
├── references/           # Optional
└── assets/               # Optional
```

### Frontmatter

**OpenCode specific fields:**
```yaml
name: skill-name         # Required
description: ...         # Required
license: MIT             # Optional
compatibility: opencode  # Optional
metadata:                # Optional
  key: value
```

Other platforms typically use only `name` and `description`.

### File References

When referencing bundled resources in SKILL.md:

```markdown
# Good - Relative paths
See `references/api.md` for details.
Run `scripts/process.py` to execute.

# Also good - Explicit
See the `api.md` file in the `references/` directory.
```

### Testing Across Platforms

After creating a skill, test it with multiple AI assistants if possible:

1. **GitHub Copilot** - Test in VSCode
2. **OpenCode** - Test in terminal
3. **Claude Desktop** - Test in desktop app

## Common Patterns

### Pattern 1: Simple Tool Skill

For straightforward tools (PDF processing, image editing):

```
skill-name/
├── SKILL.md              # Quick reference + common tasks
└── scripts/
    ├── tool1.py
    └── tool2.py
```

### Pattern 2: Knowledge Skill

For domain knowledge or company-specific information:

```
skill-name/
├── SKILL.md              # Overview + navigation
└── references/
    ├── domain1.md
    ├── domain2.md
    └── schemas.md
```

### Pattern 3: Template/Boilerplate Skill

For generating files or projects:

```
skill-name/
├── SKILL.md              # Instructions for customization
└── assets/
    ├── template1/
    └── template2/
```

### Pattern 4: Multi-Framework Skill

For skills supporting multiple variants:

```
skill-name/
├── SKILL.md              # Overview + selection guide
└── references/
    ├── framework1.md
    ├── framework2.md
    └── framework3.md
```

## Validation

Before publishing a skill:

### Manual Checks

- [ ] SKILL.md has valid YAML frontmatter
- [ ] `name` field matches directory name
- [ ] `description` is clear and comprehensive
- [ ] Name follows pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`
- [ ] No README.md or other auxiliary docs
- [ ] Scripts are tested and working
- [ ] References are organized logically

### Test with AI

- [ ] Ask AI to use the skill
- [ ] Verify it triggers correctly
- [ ] Check if AI can find needed information
- [ ] Ensure bundled resources load properly

## Examples

See existing skills in this repository:

- **pdf** - Tool skill with scripts
- **mcp-builder** - Knowledge skill with references
- **architect** - Meta skill (creates other skills)
- **dev-workflow** - Workflow/process skill

## Resources

- **Official Template:** `architect/knowledge/templates/skill-creator/SKILL.md`
- **Anthropic Guide:** Inside skill-creator template
- **Platform Docs:**
  - [OpenCode](https://opencode.ai/docs/skills)
  - [GitHub Copilot](https://docs.github.com/copilot)
