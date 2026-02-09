# Skills & Agents Repository

Personal collection of reusable skills and agents for AI coding assistants across multiple platforms.

## Overview

This repository contains modular skills and agents that extend AI assistants with specialized knowledge, workflows, and tools. Skills are designed to be **platform-agnostic** and work across:

- **GitHub Copilot** (VSCode/Visual Studio)
- **OpenCode** (Terminal/Desktop/IDE)
- **Anthropic Claude** (Desktop/Web)
- **Cursor** (IDE)
- Any AI assistant supporting the standard skills format

## Available Skills

| Skill | Description | Platforms |
|-------|-------------|-----------|
| **architect** | Scaffolds skills & agents following official standards | All |
| **dev-workflow** | Development standards and Git workflows | All |
| **mcp-builder** | Guide for creating Model Context Protocol servers | All |
| **pdf** | Complete PDF processing (read, create, modify, OCR) | All |
| **sys-env** | System environment manager for Arch Linux + Hyprland | All |
| **web-scraper** | Web content extraction and conversion to Markdown | All |

## Quick Start

### Prerequisites

- Git installed
- AI assistant (GitHub Copilot, OpenCode, Cursor, etc.)
- Python 3.10+ (for tooling scripts)

### Clone and Setup

```bash
# Clone to standard location
git clone https://github.com/ernestoelo/skills.git ~/.copilot/skills

# Set up git hooks and environment
cd ~/.copilot/skills
bash scripts/post-clone-setup.sh
```

### Development Environment (optional, for running tests)

```bash
cd ~/.copilot/skills
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Platform Setup

<details>
<summary><b>GitHub Copilot (VSCode/Visual Studio)</b></summary>

Skills should be located at `~/.copilot/skills/`

```bash
# If you cloned to the standard location, you're done!
# Otherwise, create a symlink:
ln -s ~/path/to/your/skills ~/.copilot/skills
```

</details>

<details>
<summary><b>OpenCode</b></summary>

OpenCode reads skills from `~/.config/opencode/skills/`. Use the sync script:

```bash
cd ~/.copilot/skills
./scripts/sync-skills.sh
```

**Automatic Sync (Recommended):**

This repository includes a git hook that automatically syncs after `git pull`:

```bash
cd ~/.copilot/skills
git pull  # Skills automatically sync to installed platforms
```

</details>

<details>
<summary><b>Anthropic Claude Desktop</b></summary>

Claude Desktop reads skills from platform-specific locations:
- Linux: `~/.config/claude/skills/`
- macOS: `~/Library/Application Support/Claude/skills/`

Use the sync script:

```bash
cd ~/.copilot/skills
./scripts/sync-skills.sh
# or sync only to Claude:
./scripts/sync-skills.sh --platform claude
```

</details>

<details>
<summary><b>Cursor</b></summary>

Cursor reads skills from platform-specific locations:
- Linux: `~/.config/cursor/skills/`
- macOS: `~/Library/Application Support/Cursor/skills/`

Use the sync script:

```bash
cd ~/.copilot/skills
./scripts/sync-skills.sh
# or sync only to Cursor:
./scripts/sync-skills.sh --platform cursor
```

</details>

## Usage

### Using Skills

Skills are automatically available to your AI assistant. Simply mention what you need:

```
"I need help processing a PDF"        -> Loads pdf skill
"Help me create an MCP server"        -> Loads mcp-builder skill
"How should I structure my project?"   -> Loads dev-workflow skill
```

### Creating New Skills

Use the **architect** skill to scaffold new skills:

```
"Create a new skill for database migrations"
"I need a skill to work with Docker containers"
```

See `architect/SKILL.md` for the complete skill creation process.

### Adding a New Skill Manually

```bash
cd ~/.copilot/skills
mkdir my-new-skill && cd my-new-skill

# Create SKILL.md with frontmatter
cat > SKILL.md << 'EOF'
---
name: my-new-skill
description: Brief description of what the skill does and when to use it
---

# Skill Content

Instructions for the AI...
EOF

# Create resource directories as needed
mkdir -p scripts references assets

# Validate, commit and push
python3 scripts/quick_validate.py my-new-skill/
git add my-new-skill/
git commit -m "feat: add my-new-skill"
git push
```

**Sync to AI platforms:**

```bash
./scripts/sync-skills.sh                      # Auto-detect and sync to all
./scripts/sync-skills.sh --platform opencode  # Sync to specific platform
git pull                                       # Auto-syncs via hook
```

## Skill Requirements

For a skill to work across all platforms:

### Frontmatter (Required)

```yaml
---
name: skill-name         # Must match directory name
description: Clear description of what the skill does and when to use it (1-1024 chars)
license: Optional        # e.g., MIT, Proprietary
---
```

### Naming Conventions

**Skill names** must follow the pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`

Valid: `pdf`, `web-scraper`, `mcp-builder`, `dev-workflow`
Invalid: `PDF`, `web_scraper`, `mcp--builder`, `-myskill`

### Skill Directory Structure

```
skill-name/
├── SKILL.md              # Required: AI instructions
├── scripts/              # Optional: Executable code
├── references/           # Optional: Documentation
└── assets/               # Optional: Templates, files
```

**Do NOT create** README.md, INSTALL.md, CHANGELOG.md, or other auxiliary docs inside skills.

## Tools & Scripts

All repository tooling is centralized in the `scripts/` directory at the root:

| Script | Purpose |
|--------|---------|
| `scripts/quick_validate.py` | Validates skill structure, frontmatter, and conventions |
| `scripts/init_skill.py` | Scaffolds a new skill from template |
| `scripts/package_skill.py` | Packages a skill into a distributable `.skill` file |
| `scripts/sync-skills.sh` | Syncs skills to AI platform directories (OpenCode, Claude, Cursor) |
| `scripts/validate_skill_on_change.sh` | Git pre-commit hook for automatic validation |
| `scripts/post-clone-setup.sh` | Post-clone setup (installs git hooks) |

### Validation

```bash
# Validate a single skill
python3 scripts/quick_validate.py <skill-directory>

# Run full test suite
pytest tests/ -v
```

### CI/CD

GitHub Actions automatically validates all skills and runs tests on push/PR to `main` and `develop`.

## Repository Structure

```
~/.copilot/skills/
├── README.md                         # This file
├── requirements-dev.txt              # Dev dependencies (pytest, pyyaml, ruff)
├── .github/workflows/
│   └── validate-skills.yml           # CI: validate + test on push/PR
│
├── scripts/                          # Centralized repository tooling
│   ├── quick_validate.py
│   ├── init_skill.py
│   ├── package_skill.py
│   ├── sync-skills.sh
│   ├── validate_skill_on_change.sh
│   └── post-clone-setup.sh
│
├── tests/                            # Test suite
│   └── validator/
│       ├── test_validator.py
│       ├── passing-skills/
│       └── failing-skills/
│
├── architect/                        # Skill: scaffolding tool
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
│       └── update_docs.sh
│
├── dev-workflow/                      # Skill: development standards
│   ├── SKILL.md
│   ├── checklists/
│   ├── diagrams/
│   ├── guides/
│   ├── references/
│   └── templates/
│
├── mcp-builder/                      # Skill: MCP server creation
│   ├── SKILL.md
│   ├── reference/
│   └── scripts/
│
├── pdf/                              # Skill: PDF processing
│   ├── SKILL.md
│   └── scripts/
│
├── sys-env/                          # Skill: system environment
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
│
└── web-scraper/                      # Skill: web content extraction
    ├── SKILL.md
    └── scripts/
```

## Platform-Specific Notes

### OpenCode

- Skills loaded from `~/.config/opencode/skills/` (symlinks to this repo)
- Use `scripts/sync-skills.sh` to sync new skills
- Git hook provides automatic sync after `git pull`

### GitHub Copilot

- Skills loaded directly from `~/.copilot/skills/`
- No sync needed (this is the source directory)

### Anthropic Claude

- Skills loaded from platform-specific directory
- Use `scripts/sync-skills.sh --platform claude` to sync

### Cursor

- Skills loaded from platform-specific directory
- Use `scripts/sync-skills.sh --platform cursor` to sync

## Contributing

When adding or updating skills:

1. Follow the skill requirements above
2. Run `python3 scripts/quick_validate.py <skill-dir>` before committing
3. Test the skill with your AI assistant
4. Use conventional commits (`feat:`, `fix:`, `docs:`)
5. Push to GitHub for others to use

## License

Individual skills may have different licenses (see LICENSE.txt in each skill directory). Default is for personal use.
