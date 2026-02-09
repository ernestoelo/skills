# Platform Sync & Distribution

This guide explains how to distribute skills across different AI platforms when working with a git repository.

## Overview

When skills are stored in a git repository (recommended for version control and collaboration), different platforms require different approaches to access them.

## Platform Requirements

### GitHub Copilot (VSCode/Visual Studio)

**Location:** `~/.copilot/skills/`

**Setup:**
- Clone repository directly to this location, OR
- Create symlink from repository to this location

**Sync:** Not needed (reads files directly)

### OpenCode

**Location:** `~/.config/opencode/skills/`

**Setup:** Requires symbolic links from repository

**Sync:** Use `sync-to-opencode.sh` script (see below)

### Claude Desktop

**Location:** `~/.claude/skills/`

**Setup:**
- Clone repository directly to this location, OR
- Create symlink from repository to this location

**Sync:** Not needed (reads files directly)

### Cursor

**Location:** `~/.cursor/skills/` (verify in settings)

**Setup:**
- Clone repository directly to this location, OR
- Create symlink from repository to this location

**Sync:** Not needed (reads files directly)

## Recommended Setup: Central Repository

The best practice is to maintain skills in a **single git repository** and create platform-specific access:

```
~/skills-repo/              # Your git repository
├── .git/
├── skill-1/
├── skill-2/
└── sync-to-opencode.sh

# Platform access via symlinks:
~/.copilot/skills/    → ~/skills-repo/
~/.claude/skills/     → ~/skills-repo/
~/.cursor/skills/     → ~/skills-repo/

# OpenCode (requires individual skill symlinks):
~/.config/opencode/skills/
├── skill-1 → ~/skills-repo/skill-1
├── skill-2 → ~/skills-repo/skill-2
```

**Benefits:**
- Single source of truth
- Version control with git
- Easy collaboration
- Changes automatically available across platforms

## OpenCode Sync Script

OpenCode requires individual skill-level symlinks. Use this script to automate:

```bash
#!/bin/bash
#
# sync-to-opencode.sh
# Syncs skills from repository to OpenCode
#

REPO_DIR="$HOME/.copilot/skills"  # Your repository location
OPENCODE_DIR="$HOME/.config/opencode/skills"

# Create OpenCode directory
mkdir -p "$OPENCODE_DIR"

# Sync all skills
for skill_path in "$REPO_DIR"/*/SKILL.md; do
    [ -e "$skill_path" ] || continue
    
    skill_dir=$(dirname "$skill_path")
    skill_name=$(basename "$skill_dir")
    
    # Skip hidden directories
    [[ "$skill_name" == .* ]] && continue
    
    symlink_path="$OPENCODE_DIR/$skill_name"
    
    # Create or update symlink
    if [ ! -L "$symlink_path" ]; then
        ln -s "$skill_dir" "$symlink_path"
        echo "✅ Synced: $skill_name"
    fi
done

echo "✨ OpenCode sync complete!"
```

**Usage:**
```bash
chmod +x sync-to-opencode.sh
./sync-to-opencode.sh
```

## Git Hook for Auto-Sync

Automate OpenCode sync after every `git pull`:

**Create `.git/hooks/post-merge`:**
```bash
#!/bin/bash
#
# post-merge hook
# Auto-syncs skills to OpenCode after git pull/merge
#

echo "🔄 Syncing skills to OpenCode..."
"$(dirname "$0")/../../sync-to-opencode.sh"
```

**Make executable:**
```bash
chmod +x .git/hooks/post-merge
```

Now every `git pull` automatically syncs to OpenCode!

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
   # OpenCode only (others auto-update via symlinks)
   ./sync-to-opencode.sh
   
   # Or if git hook configured:
   git pull  # Auto-syncs
   ```

### Pulling Updates

When collaborators add skills:

```bash
git pull  # Downloads new skills

# OpenCode users:
./sync-to-opencode.sh  # Or auto-syncs with git hook

# Other platforms: already updated via symlinks
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
git pull  # Get latest changes

# OpenCode auto-syncs if git hook configured
# Otherwise run: ./sync-to-opencode.sh
```

## Troubleshooting

### Skill not appearing in OpenCode

1. Verify symlink exists:
   ```bash
   ls -la ~/.config/opencode/skills/
   ```

2. Re-sync:
   ```bash
   ./sync-to-opencode.sh
   ```

3. Restart OpenCode

### Skill not appearing in other platforms

1. Verify platform-specific directory exists and has symlink:
   ```bash
   ls -la ~/.copilot/skills/
   ls -la ~/.claude/skills/
   ```

2. Create symlink if missing:
   ```bash
   ln -s ~/skills-repo ~/.copilot/skills
   ```

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
- Use `sync-to-opencode.sh` script
- Git hook provides auto-sync
- Skills listed in skill tool description

### GitHub Copilot

- Can use repo-level or individual symlinks
- Prefers direct directory access
- No sync needed

### Claude Desktop

- Can use repo-level or individual symlinks
- Follows Anthropic's standard closely
- No sync needed

### Cursor

- Similar to GitHub Copilot
- Verify location in Cursor settings
- No sync needed

## Best Practices

1. **Use git for version control**
   - Commit frequently
   - Write clear commit messages
   - Tag releases

2. **Maintain single repository**
   - Don't duplicate across platforms
   - Use symlinks for access

3. **Automate sync for OpenCode**
   - Use git hook for auto-sync
   - Include sync script in repository

4. **Document your setup**
   - README with setup instructions
   - Platform-specific notes

5. **Test across platforms**
   - Verify skill works everywhere
   - Check triggering and loading

## Example: Complete Setup

Starting from scratch:

```bash
# 1. Clone repository
git clone https://github.com/user/skills.git ~/my-skills

# 2. Set up GitHub Copilot
ln -s ~/my-skills ~/.copilot/skills

# 3. Set up Claude Desktop
ln -s ~/my-skills ~/.claude/skills

# 4. Set up Cursor
ln -s ~/my-skills ~/.cursor/skills

# 5. Set up OpenCode
cd ~/my-skills
./sync-to-opencode.sh

# 6. Configure git hook for auto-sync
chmod +x .git/hooks/post-merge

# Done! All platforms now access the same skills
```

## Summary

| Platform | Location | Sync Method | Auto-Sync |
|----------|----------|-------------|-----------|
| GitHub Copilot | `~/.copilot/skills/` | Repo symlink | N/A |
| OpenCode | `~/.config/opencode/skills/` | Script + skill symlinks | Git hook |
| Claude Desktop | `~/.claude/skills/` | Repo symlink | N/A |
| Cursor | `~/.cursor/skills/` | Repo symlink | N/A |

**Recommendation:** Use the central repository approach with `sync-to-opencode.sh` and git hooks for the best developer experience.
