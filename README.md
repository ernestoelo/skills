# Skills & Agents Repository

Personal collection of reusable skills and agents for AI coding assistants across multiple platforms.

## 🎯 Overview

This repository contains modular skills and agents that extend AI assistants with specialized knowledge, workflows, and tools. Skills are designed to be **platform-agnostic** and work across:

- **GitHub Copilot** (VSCode/Visual Studio)
- **OpenCode** (Terminal/Desktop/IDE)
- **Anthropic Claude** (Desktop/Web)
- **Cursor** (IDE)
- Any AI assistant supporting the standard skills format

## 📚 Available Skills

| Skill | Description | Platforms |
|-------|-------------|-----------|
| **architect** | Scaffolds skills & agents following official standards | All |
| **dev-workflow** | Development standards and Git workflows | All |
| **mcp-builder** | Guide for creating Model Context Protocol servers | All |
| **pdf** | Complete PDF processing (read, create, modify, OCR) | All |
| **web-scraper** | Web content extraction and conversion to Markdown | All |

## 🚀 Quick Start

### Prerequisites

- Git installed
- AI assistant (GitHub Copilot, OpenCode, Cursor, etc.)
- Platform-specific configuration (see Platform Setup below)

### Clone Repository

```bash
# Clone to standard location
git clone https://github.com/ernestoelo/skills.git ~/.copilot/skills

# Or clone to custom location
git clone https://github.com/ernestoelo/skills.git ~/my-skills
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
cd ~/.copilot/skills  # or your skills directory
./architect/scripts/sync-skills.sh
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
./architect/scripts/sync-skills.sh
# or sync only to Claude:
./architect/scripts/sync-skills.sh --platform claude
```

**Alternative - Manual Symlink:**

```bash
# Linux
ln -s ~/.copilot/skills ~/.config/claude/skills

# macOS
ln -s ~/.copilot/skills ~/Library/Application\ Support/Claude/skills
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
./architect/scripts/sync-skills.sh
# or sync only to Cursor:
./architect/scripts/sync-skills.sh --platform cursor
```

**Alternative - Manual Symlink:**

```bash
# Linux
ln -s ~/.copilot/skills ~/.config/cursor/skills

# macOS
ln -s ~/.copilot/skills ~/Library/Application\ Support/Cursor/skills
```

</details>

## 📖 Usage

### Using Skills

Skills are automatically available to your AI assistant. Simply mention what you need:

```
"I need help processing a PDF"  → Loads pdf skill
"Help me create an MCP server"  → Loads mcp-builder skill
"How should I structure my project?" → Loads dev-workflow skill
```

### Creating New Skills

Use the **architect** skill to scaffold new skills:

```
"Create a new skill for database migrations"
"I need a skill to work with Docker containers"
```

The architect skill will:
1. Analyze your requirements
2. Generate proper folder structure
3. Create SKILL.md with valid frontmatter
4. Set up scripts/, references/, and assets/ directories
5. Guide you through implementation

**Manual Creation:**

See [architect/knowledge/creating-skills.md](architect/knowledge/creating-skills.md) for detailed guidance.

## 🔄 Workflow

### Adding a New Skill

**Option 1: Use the architect skill (Recommended)**

```
Ask your AI assistant: "Create a new skill called my-new-skill for [purpose]"
```

**Option 2: Manual creation**

```bash
cd ~/.copilot/skills
mkdir my-new-skill
cd my-new-skill

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

# Commit and push
git add my-new-skill/
git commit -m "feat: add my-new-skill"
git push
```

**Sync to AI platforms:**

```bash
# Auto-sync to all installed platforms (OpenCode, Claude, Cursor)
./architect/scripts/sync-skills.sh

# Or sync to specific platform
./architect/scripts/sync-skills.sh --platform opencode

# Or if you have the git hook configured, just:
git pull  # Auto-syncs to all installed platforms
```

### Updating Existing Skills

```bash
cd ~/.copilot/skills/skill-name
# Edit files
git add .
git commit -m "fix: description of changes"
git push
```

Changes are immediately available in GitHub Copilot (reads files directly). For OpenCode, Claude, and Cursor, changes are visible after `git pull` (with auto-sync).

### Syncing from GitHub

When someone else adds skills, or you work from another machine:

```bash
cd ~/.copilot/skills
git pull  # Auto-syncs to all installed platforms

# If auto-sync not configured:
./architect/scripts/sync-skills.sh
```

## 📋 Skill Requirements

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

✅ Valid: `pdf`, `web-scraper`, `mcp-builder`, `dev-workflow`
❌ Invalid: `PDF`, `web_scraper`, `mcp--builder`, `-myskill`

### Directory Structure

```
skill-name/
├── SKILL.md              # Required: AI instructions
├── scripts/              # Optional: Executable code
├── references/           # Optional: Documentation
└── assets/               # Optional: Templates, files
```

**Do NOT create:**
- README.md (redundant with SKILL.md)
- INSTALL.md
- CHANGELOG.md
- Other auxiliary documentation

## 🛠️ Tools & Scripts

### sync-skills.sh

Multi-platform synchronization script that automatically syncs skills to installed AI platforms:

```bash
./architect/scripts/sync-skills.sh                 # Auto-detect and sync to all
./architect/scripts/sync-skills.sh --platform opencode  # Sync only to OpenCode
./architect/scripts/sync-skills.sh --platform claude    # Sync only to Claude
./architect/scripts/sync-skills.sh --platform cursor    # Sync only to Cursor
./architect/scripts/sync-skills.sh --dry-run            # Preview changes
./architect/scripts/sync-skills.sh --help               # Show help
```

**Supported Platforms:**
- **OpenCode** - Terminal/Desktop/IDE AI assistant
- **Claude Desktop** - Anthropic's desktop application
- **Cursor** - AI-powered IDE
- **GitHub Copilot** - No sync needed (uses repository directly)

**Features:**
- Auto-detects installed platforms
- Creates symlinks for new skills
- Verifies existing symlinks
- Cross-platform (Linux + macOS)
- Detailed reporting

**Auto-sync with git hook:**

The repository includes `.git/hooks/post-merge` that runs this script automatically after `git pull`.

## 📁 Repository Structure

```
~/.copilot/skills/          # Repository root
├── README.md               # This file
├── .git/
│   └── hooks/
│       └── post-merge      # Auto-sync git hook
│
├── architect/              # Skill scaffolding tool
│   ├── SKILL.md
│   ├── knowledge/
│   │   ├── creating-skills.md    # Practical guide for creating skills
│   │   ├── specs/                # Platform specifications
│   │   └── templates/
│   │       └── skill-creator/    # Anthropic's reference template
│   └── scripts/
│       ├── sync-skills.sh        # Multi-platform sync script
│       └── update_docs.sh        # Documentation updater
│
├── dev-workflow/           # Development standards
│   ├── SKILL.md
│   └── guides/
│
├── mcp-builder/            # MCP server creation guide
│   ├── SKILL.md
│   ├── reference/
│   └── scripts/
│
├── pdf/                    # PDF processing
│   ├── SKILL.md
│   └── scripts/
│
└── web-scraper/            # Web content extraction
    ├── SKILL.md
    └── scripts/
```

## 🎯 Benefits

✅ **Single source of truth** - One repository for all platforms
✅ **Version controlled** - Full git history and collaboration
✅ **Cross-platform** - Works with multiple AI assistants
✅ **Modular** - Each skill is self-contained
✅ **Extensible** - Easy to add new skills
✅ **Well-documented** - Clear structure and guidelines

## 🔗 Resources

- **Repository:** https://github.com/ernestoelo/skills
- **Anthropic Skills Guide:** See `architect/knowledge/templates/skill-creator/SKILL.md`
- **OpenCode Docs:** https://opencode.ai/docs/skills
- **GitHub Copilot Docs:** https://docs.github.com/copilot

## 🤖 Platform-Specific Notes

### OpenCode

- Skills loaded from `~/.config/opencode/skills/` (symlinks to this repo)
- Use `architect/scripts/sync-skills.sh` to sync new skills
- Git hook provides automatic sync after `git pull`
- Skills listed in skill tool description

### GitHub Copilot

- Skills loaded directly from `~/.copilot/skills/`
- No sync needed (this is the source directory)
- Works in VSCode and Visual Studio

### Anthropic Claude

- Skills loaded from platform-specific directory
- Use `architect/scripts/sync-skills.sh --platform claude` to sync
- Or create manual symlink to this repository
- Follow Anthropic's skill specification

### Cursor

- Skills loaded from platform-specific directory
- Use `architect/scripts/sync-skills.sh --platform cursor` to sync
- Or create manual symlink to this repository

## 📝 Contributing

When adding or updating skills:

1. Follow the skill requirements above
2. Test the skill with your AI assistant
3. Update this README if adding a new skill
4. Use conventional commits (`feat:`, `fix:`, `docs:`)
5. Push to GitHub for others to use

## 📄 License

Individual skills may have different licenses (see LICENSE.txt in each skill directory). Default is for personal use.
