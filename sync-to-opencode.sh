#!/bin/bash
#
# sync-to-opencode.sh
# 
# Purpose: Synchronizes all skills from this repository to OpenCode
# 
# This script creates symbolic links from ~/.copilot/skills/ (this repository)
# to ~/.config/opencode/skills/ so that OpenCode can discover and use the skills.
#
# Usage:
#   ./sync-to-opencode.sh              # Sync all skills
#   ./sync-to-opencode.sh --help       # Show this help message
#
# Features:
#   - Automatically detects all skills (directories with SKILL.md)
#   - Creates symlinks for new skills
#   - Verifies existing symlinks point to correct locations
#   - Provides detailed report of actions taken
#
# Git Hook Integration:
#   This script is automatically called by .git/hooks/post-merge
#   after every 'git pull' or 'git merge' command.
#
# Cross-Platform:
#   This script is OpenCode-specific. For other platforms:
#   - GitHub Copilot: Uses this directory directly (no sync needed)
#   - Claude Desktop: Create symlink: ln -s ~/.copilot/skills ~/.claude/skills
#   - Cursor: Create symlink: ln -s ~/.copilot/skills ~/.cursor/skills
#

set -e  # Exit on error

# Configuration
COPILOT_SKILLS="$HOME/.copilot/skills"
OPENCODE_SKILLS="$HOME/.config/opencode/skills"

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'  # No Color

# Help message
show_help() {
    echo "sync-to-opencode.sh - Sync skills from repository to OpenCode"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --help, -h     Show this help message"
    echo ""
    echo "Description:"
    echo "  Synchronizes all skills from ~/.copilot/skills/ to ~/.config/opencode/skills/"
    echo "  using symbolic links. This allows OpenCode to discover and use the skills"
    echo "  while maintaining a single source of truth in the git repository."
    echo ""
    echo "Examples:"
    echo "  $0              # Sync all skills"
    echo "  git pull        # Auto-syncs if git hook is configured"
    echo ""
    echo "See README.md for more information."
    exit 0
}

# Parse command-line arguments
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    show_help
fi

# Header
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         SKILL SYNCHRONIZATION: Repository → OpenCode         ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Create OpenCode skills directory if it doesn't exist
if [ ! -d "$OPENCODE_SKILLS" ]; then
    echo -e "${YELLOW}📁 Creating directory: $OPENCODE_SKILLS${NC}"
    mkdir -p "$OPENCODE_SKILLS"
    echo ""
fi

echo -e "${BLUE}🔍 Searching for skills in: $COPILOT_SKILLS${NC}"
echo ""

# Validate source directory exists
if [ ! -d "$COPILOT_SKILLS" ]; then
    echo -e "${RED}❌ Error: Source directory not found: $COPILOT_SKILLS${NC}"
    echo -e "${YELLOW}   Make sure this script is run from the skills repository.${NC}"
    exit 1
fi

# Counters for summary
new_count=0
existing_count=0
updated_count=0
error_count=0
total_count=0

# Iterate over all directories containing SKILL.md
for skill_path in "$COPILOT_SKILLS"/*/SKILL.md; do
    # Check if file exists (avoids error if no matches found)
    [ -e "$skill_path" ] || continue
    
    # Extract directory and skill name
    skill_dir=$(dirname "$skill_path")
    skill_name=$(basename "$skill_dir")
    
    # Skip hidden directories (like .git)
    if [[ "$skill_name" == .* ]]; then
        continue
    fi
    
    # Skip non-skill directories (docs, scripts, etc.)
    if [[ "$skill_name" == "docs" ]] || [[ "$skill_name" == "scripts" ]]; then
        continue
    fi
    
    total_count=$((total_count + 1))
    symlink_path="$OPENCODE_SKILLS/$skill_name"
    
    # Check if symlink already exists
    if [ -L "$symlink_path" ]; then
        # Verify it points to the correct location
        current_target=$(readlink "$symlink_path")
        if [ "$current_target" = "$skill_dir" ]; then
            echo -e "  ✅ ${GREEN}$skill_name${NC} → already synced"
            existing_count=$((existing_count + 1))
        else
            echo -e "  🔄 ${YELLOW}$skill_name${NC} → updating symlink (was: $current_target)"
            rm "$symlink_path"
            ln -s "$skill_dir" "$symlink_path"
            updated_count=$((updated_count + 1))
        fi
    elif [ -e "$symlink_path" ]; then
        # Exists but is not a symlink (regular file or directory)
        echo -e "  ❌ ${RED}$skill_name${NC} → exists as regular file/directory (not a symlink)"
        echo -e "     ${YELLOW}Please remove manually: $symlink_path${NC}"
        error_count=$((error_count + 1))
    else
        # Doesn't exist, create symlink
        echo -e "  🆕 ${GREEN}$skill_name${NC} → creating symlink..."
        ln -s "$skill_dir" "$symlink_path"
        new_count=$((new_count + 1))
    fi
done

# Summary
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                          SUMMARY                             ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo -e "  Total skills found:      ${GREEN}$total_count${NC}"
echo -e "  Already synced:          ${GREEN}$existing_count${NC}"
echo -e "  Newly synced:            ${GREEN}$new_count${NC}"

if [ $updated_count -gt 0 ]; then
    echo -e "  Updated:                 ${YELLOW}$updated_count${NC}"
fi

if [ $error_count -gt 0 ]; then
    echo -e "  Errors:                  ${RED}$error_count${NC}"
fi

echo ""

# Final message
if [ $error_count -gt 0 ]; then
    echo -e "${RED}⚠️  Synchronization completed with errors.${NC}"
    echo -e "${YELLOW}   Please resolve the errors shown above.${NC}"
    exit 1
elif [ $new_count -gt 0 ] || [ $updated_count -gt 0 ]; then
    changes=$((new_count + updated_count))
    echo -e "${GREEN}✨ Synchronization complete! $changes skill(s) synced.${NC}"
else
    echo -e "${GREEN}✅ All skills already synchronized.${NC}"
fi

echo ""
echo -e "${BLUE}📍 OpenCode skills location: $OPENCODE_SKILLS${NC}"
echo -e "${BLUE}📍 Repository location:      $COPILOT_SKILLS${NC}"
echo ""

# Helpful tips
if [ $new_count -gt 0 ]; then
    echo -e "${YELLOW}💡 Tip: Restart OpenCode to ensure new skills are detected.${NC}"
    echo ""
fi
