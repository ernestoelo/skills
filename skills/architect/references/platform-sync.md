# Platform Sync & Distribution

This guide explains how to distribute skills across different AI platforms when working with a git repository.

## Overview

When skills are stored in a git repository (recommended for version control and collaboration), different platforms require different approaches to access them.

## Platform Requirements

### GitHub Copilot (VSCode/Visual Studio)

**Location:** `~/.copilot/workflows/`

**Setup:**
- Clone repository directly to this location, OR
- Create symlink from repository to this location

**Sync:** Not needed (reads files directly)

### OpenCode

**Location:** `~/.config/opencode/skills/`

**Setup:** Requires symbolic links from repository

**Sync:** Use `scripts/sync-skills.sh` script

**Auto-Activation:** Skills are automatically validated and activated after sync via `architect/scripts/activate_all.py`, ensuring all skills are ready for conversation starts. (see below)

### Claude Desktop

**Location:** 
- Linux: `~/.config/claude/skills/`
- macOS: `~/Library/Application Support/Claude/skills/`

**Setup:** Requires symbolic links from repository

**Sync:** Use `scripts/sync-skills.sh` script (see below)

### Cursor

**Location:**
- Linux: `~/.config/cursor/skills/`
- macOS: `~/Library/Application Support/Cursor/skills/`

**Setup:** Requires symbolic links from repository

**Sync:** Use `scripts/sync-skills.sh` script (see below)

## Recommended Setup: Central Repository

The best practice is to maintain skills in a **single git repository** and use the multi-platform sync script:

```
~/skills-repo/              # Your git repository (e.g., ~/.copilot/workflows)
├── .git/
├── scripts/
│   └── sync-skills.sh      # Multi-platform sync script
├── architect/
├── skill-1/
└── skill-2/

# GitHub Copilot (uses repository directly):
~/.copilot/workflows/  → This IS the repository

# Other platforms (symlinks to individual skills):
~/.config/opencode/skills/
├── skill-1 → ~/.copilot/workflows/skill-1
├── skill-2 → ~/.copilot/workflows/skill-2

~/.config/claude/skills/  (or ~/Library/Application Support/Claude/skills/ on macOS)
├── skill-1 → ~/.copilot/workflows/skill-1
├── skill-2 → ~/.copilot/workflows/skill-2

~/.config/cursor/skills/  (or ~/Library/Application Support/Cursor/skills/ on macOS)
├── skill-1 → ~/.copilot/workflows/skill-1
├── skill-2 → ~/.copilot/workflows/skill-2
```

**Benefits:**
- Single source of truth
- Version control with git
- Easy collaboration
- Changes automatically available across platforms
- One script for all platforms

## Multi-Platform Sync Script

The `sync-skills.sh` script automates synchronization across all AI platforms:

**Location:** `scripts/sync-skills.sh`

**Features:**
- Auto-detects installed AI platforms (OpenCode, Claude Desktop, Cursor)
- Creates individual skill symlinks for each platform
- Cross-platform support (Linux + macOS)
- Verifies existing symlinks
- Detailed reporting
- Dry-run mode for preview

**Usage:**

```bash
# Auto-sync to all installed platforms
./scripts/sync-skills.sh

# Sync to specific platform only
./scripts/sync-skills.sh --platform opencode
./scripts/sync-skills.sh --platform claude
./scripts/sync-skills.sh --platform cursor

# Preview changes without applying
./scripts/sync-skills.sh --dry-run

# Show help
./scripts/sync-skills.sh --help
```

**Example Output:**

```
╔══════════════════════════════════════════════════════════════╗
║           SKILL SYNCHRONIZATION: Multi-Platform              ║
╚══════════════════════════════════════════════════════════════╝

🔍 Searching for skills in: ~/.copilot/workflows/

📍 Platform Detection:
  ✅ OpenCode       → ~/.config/opencode/skills/
  ✅ Claude Desktop → ~/.config/claude/skills/
  ⊘  Cursor         → Not installed

Syncing to OpenCode...
  ✅ architect → already synced
  🆕 my-skill → creating symlink...

Syncing to Claude Desktop...
  ✅ architect → already synced
  🆕 my-skill → creating symlink...

╔══════════════════════════════════════════════════════════════╗
║                          SUMMARY                             ║
╚══════════════════════════════════════════════════════════════╝
  Platforms synced:        2 (opencode, claude)
  Total skills found:      5
  Already synced:          4
  Newly synced:            1

✨ Synchronization complete! 1 skill(s) synced across 2 platform(s).
```

## Git Hook for Auto-Sync

Automate multi-platform sync after every `git pull`:

**The repository includes `.git/hooks/post-merge`:**

```bash
#!/bin/bash
#
# post-merge hook
# Executes automatically after 'git pull' or 'git merge'
# Syncs skills to installed AI platforms
#

echo ""
echo "🔄 Syncing skills to installed platforms..."
echo ""

# Execute the sync script
"$(dirname "$0")/../../scripts/sync-skills.sh"

exit 0
```

**Make executable (if not already):**

```bash
chmod +x .git/hooks/post-merge
```

Now every `git pull` automatically syncs to **all installed platforms**!

## Workflow Integration

### Creating a New Skill

When scaffolding a new skill, include sync step:

1. **Create skill structure**
   ```bash
   mkdir my-skill
   # Create SKILL.md and resources
   ```

2. **Test locally**
   ```bash
   # Use skill with your AI assistant
   ```

3. **Commit to git**
   ```bash
   git add my-skill/
   git commit -m "feat: add my-skill"
   git push
   ```

4. **Sync to platforms**
   ```bash
   # Auto-sync to all installed platforms
   ./scripts/sync-skills.sh
   
   # Or if git hook configured:
   git pull  # Auto-syncs to all platforms
   ```

### Pulling Updates

When collaborators add skills:

```bash
git pull  # Downloads new skills + auto-syncs to all platforms (if git hook configured)

# Manual sync (if needed):
./scripts/sync-skills.sh  # Syncs to all installed platforms
```

## Multi-Machine Setup

When working across multiple machines:

**Machine 1:**
```bash
cd ~/skills-repo
git push  # Push your changes
```

**Machine 2:**
```bash
cd ~/skills-repo
git pull  # Get latest changes + auto-syncs to all platforms (if git hook configured)

# Manual sync (if needed):
# ./scripts/sync-skills.sh
```

## Troubleshooting

### Skill not appearing in any platform

1. Verify symlink exists:
   ```bash
   # OpenCode
   ls -la ~/.config/opencode/skills/
   
   # Claude Desktop (Linux)
   ls -la ~/.config/claude/skills/
   
   # Cursor (Linux)
   ls -la ~/.config/cursor/skills/
   ```

2. Re-sync to all platforms:
   ```bash
   ./scripts/sync-skills.sh
   ```

3. Sync to specific platform:
   ```bash
   ./scripts/sync-skills.sh --platform opencode
   ./scripts/sync-skills.sh --platform claude
   ./scripts/sync-skills.sh --platform cursor
   ```

4. Restart your AI assistant

### Skill not appearing in GitHub Copilot

1. Verify repository location:
   ```bash
   ls -la ~/.copilot/workflows/
   ```

2. GitHub Copilot reads directly from the repository (no sync needed)

### Git hook not running

1. Check file exists and is executable:
   ```bash
   ls -la .git/hooks/post-merge
   chmod +x .git/hooks/post-merge
   ```

2. Test manually:
   ```bash
   .git/hooks/post-merge
   ```

## Platform-Specific Considerations

### OpenCode

- Requires individual skill-level symlinks (not repo-level)
- Use `scripts/sync-skills.sh` script
- Git hook provides auto-sync to all platforms
- Skills listed in skill tool description

### GitHub Copilot

- Uses repository directly at `~/.copilot/workflows/`
- No sync needed (source directory)
- Works in VSCode and Visual Studio

### Claude Desktop

- Requires individual skill-level symlinks
- Platform-specific paths (Linux vs macOS)
- Use `scripts/sync-skills.sh --platform claude`
- Follows Anthropic's skill specification

### Cursor

- Requires individual skill-level symlinks  
- Platform-specific paths (Linux vs macOS)
- Use `scripts/sync-skills.sh --platform cursor`
- Similar to GitHub Copilot

## Best Practices

1. **Use git for version control**
   - Commit frequently
   - Write clear commit messages
   - Tag releases

2. **Maintain single repository**
   - Don't duplicate across platforms
   - Use symlinks for access

3. **Automate multi-platform sync**
   - Use git hook for auto-sync to all installed platforms
   - Include sync script in repository (`scripts/sync-skills.sh`)

4. **Document your setup**
   - README with setup instructions
   - Platform-specific notes

5. **Test across platforms**
   - Verify skill works everywhere
   - Check triggering and loading

## Example: Complete Setup

Starting from scratch:

```bash
# 1. Clone repository to standard GitHub Copilot location
git clone https://github.com/user/skills.git ~/.copilot/workflows
cd ~/.copilot/workflows

# 2. GitHub Copilot is already set up (uses this directory directly)

# 3. Sync to other platforms (OpenCode, Claude, Cursor)
./scripts/sync-skills.sh

# 4. Git hook is already configured - test it
git pull  # Should auto-sync to all platforms

# Done! All platforms now access the same skills
```

## Summary

| Platform | Location (Linux) | Location (macOS) | Sync Method | Auto-Sync |
|----------|-----------------|------------------|-------------|-----------|
| GitHub Copilot | `~/.copilot/workflows/` | `~/.copilot/workflows/` | Direct (repository) | N/A |
| OpenCode | `~/.config/opencode/skills/` | `~/.config/opencode/skills/` | Script + skill symlinks | Git hook |
| Claude Desktop | `~/.config/claude/skills/` | `~/Library/Application Support/Claude/skills/` | Script + skill symlinks | Git hook |
| Cursor | `~/.config/cursor/skills/` | `~/Library/Application Support/Cursor/skills/` | Script + skill symlinks | Git hook |

**Recommendation:** Use the central repository approach at `~/.copilot/workflows/` with `scripts/sync-skills.sh` and git hooks for the best multi-platform developer experience.
