# Skills & Agents Repository

[![Validate Skills](https://github.com/<your-username>/<your-repo>/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/<your-username>/<your-repo>/actions/workflows/validate-skills.yml)
[![Skill Validation CI](https://github.com/<your-username>/<your-repo>/actions/workflows/skill-validation.yml/badge.svg)](https://github.com/<your-username>/<your-repo>/actions/workflows/skill-validation.yml)

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
- Python 3.12+ and [uv](https://docs.astral.sh/uv/) (for tooling scripts)

### Clone and Setup

```bash
# Clone to standard location
git clone https://github.com/<your-username>/<your-repo>.git ~/.copilot/skills

# Set up git hooks and environment
cd ~/.copilot/skills
bash scripts/post-clone-setup.sh
```

### Development Environment (optional, for running tests)

```bash
cd ~/.copilot/skills
uv sync --group dev
uv run pytest tests/ -v
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
uv run python3 scripts/quick_validate.py my-new-skill/
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
| `scripts/validate-skill-on-change.sh` | Git pre-commit hook for automatic validation |
| `scripts/post-clone-setup.sh` | Post-clone setup (installs git hooks) |

### Validation

```bash
# Validate a single skill
uv run python3 scripts/quick_validate.py <skill-directory>

# Run full test suite
uv run pytest tests/ -v
```

### CI/CD

GitHub Actions automatically validates all skills and runs tests on push/PR to `main` and `develop`.

- **Validate Skills** workflow: Runs full validation, Ruff checks, and tests using `uv sync --group dev`.
- **Skill Validation CI** workflow: Validates only changed SKILL.md files on PR/push, using `uv sync` and git diff for efficiency.

✅ CI is fully operational and validated (Feb 2026) - all workflows pass consistently.

## Repository Structure

```
~/.copilot/skills/
├── README.md                         # This file
├── pyproject.toml                    # Project metadata, dev dependencies, tool config
├── uv.lock                           # Deterministic lockfile for dependencies
├── .github/workflows/
│   └── validate-skills.yml           # CI: validate + test on push/PR
│
├── scripts/                          # Centralized repository tooling
│   ├── __init__.py
│   ├── init_skill.py
│   ├── package_skill.py
│   ├── quick_validate.py
│   ├── sync-skills.sh
│   ├── validate-skill-on-change.sh
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
│       └── update-docs.sh
│
├── dev-workflow/                     # Skill: development standards
│   ├── SKILL.md
│   ├── references/
│   └── assets/
│       └── diagrams/
│
├── mcp-builder/                     # Skill: MCP server creation
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
│
├── pdf/                             # Skill: PDF processing
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
│
├── sys-env/                         # Skill: system environment
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
│
└── web-scraper/                     # Skill: web content extraction
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

## SKILL.md Format

To ensure all skills in the repository are consistent, structured, and easy to maintain, each skill includes a `SKILL.md` file. This file acts as the central documentation for the skill, detailing its purpose, usage, and additional resources. The following outlines the structure and expectations for `SKILL.md` files:

### Frontmatter (Required)
Every `SKILL.md` begins with YAML frontmatter that defines basic metadata:

```yaml
---
name: skill-name         # Must match the directory name (kebab-case)
description: Brief description of what the skill does and when to use it
author: Author name (optional)
version: 1.0.0           # Versioning for the skill
license: Optional        # e.g., MIT, Proprietary
---
```

- **`name`**: The name of the skill (matches its directory name).
- **`description`**: A clear and concise explanation of the skill's functionality and use cases.
- **`version`**: Semantic versioning to track updates and improvements.
- **`license`** *(optional)*: License applicable to the skill.

### Body Structure
The main body follows a standard structure to ensure clarity:

1. **Description:** Overview of the skill’s purpose and capabilities.
2. **When to Use:** Scenarios where the skill is applicable, with examples.
3. **Usage Guide:** Step-by-step instructions for using the skill, including CLI commands and examples.
4. **Inputs and Outputs:** Details on input parameters, arguments, and expected outputs.
5. **Best Practices & Limitations:** Suggestions for effective use and common pitfalls.
6. **Example Workflows:** Practical examples demonstrating real-world use cases.
7. **Version History:** A table tracking changes over time.
8. **Resources:** Links to additional documentation, scripts, or references.

### Example SKILL.md for Reference
An example of a minimal SKILL.md is as follows:

```markdown
---
name: pdf
description: Automates PDF processing: reading, modifying, OCR, and creation.
author: OpenCode Project Team
version: 1.0.0
---

# PDF Skill

## Description
This skill enables advanced PDF processing, including text extraction, merging/splitting, and OCR.

## When to Use
- Extracting data from PDF files.
- Adding encryption, watermarks, or metadata.
- Creating brand-new PDF files dynamically.

## Usage Guide
### Extracting Text
```python
from pypdf import PdfReader
reader = PdfReader("document.pdf")
for page in reader.pages:
    print(page.extract_text())
```
```

### Creating a Watermarked PDF
```python
from pypdf import PdfReader, PdfWriter
watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("input.pdf")
writer = PdfWriter()
for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)
writer.write("output.pdf")
```
```

## Inputs and Outputs
- **Inputs:** PDF file paths, watermark PDFs.
- **Outputs:** Modified or transformed PDFs.
```

### Maintaining SKILL.md Files
Contributors are expected to format all `SKILL.md` files according to this template when creating or updating skills. This ensures clarity, consistency, and ease of collaboration across all platforms.

## Adapting for Your Repository

If you fork this repository or create your own skills collection:

1. **Replace placeholders in README.md**:
   - `<your-username>` → your GitHub username
   - `<your-repo>` → your repository name

2. **Update pyproject.toml**:
   - Change author and repository fields to match your project

3. **Customize skills**: Modify SKILL.md files as needed for your use cases

4. **Test portability**: Ensure scripts work when repo is cloned to `~/.copilot/skills/` or synced to platform directories
