#!/usr/bin/env bash
#
# sync-skills.sh
# 
# Purpose: Synchronizes all skills from this repository to AI platforms
# 
# This script creates symbolic links from ~/.copilot/skills/ (this repository)
# to various AI platform directories, enabling them to discover and use the skills.
#
# Supported Platforms:
#   - OpenCode:       Linux: ~/.config/opencode/skills/
#   - Claude Desktop: Linux: ~/.config/claude/skills/  | macOS: ~/Library/Application Support/Claude/skills/
#   - Cursor:         Linux: ~/.config/cursor/skills/  | macOS: ~/Library/Application Support/Cursor/skills/
#   - GitHub Copilot: Uses this directory directly (no sync needed)
#
# Usage:
#   ./sync-skills.sh                       # Auto-detect and sync to all installed platforms
#   ./sync-skills.sh --platform opencode   # Sync only to OpenCode
#   ./sync-skills.sh --platform claude     # Sync only to Claude Desktop
#   ./sync-skills.sh --platform cursor     # Sync only to Cursor
#   ./sync-skills.sh --dry-run             # Show what would be done without making changes
#   ./sync-skills.sh --help                # Show this help message
#
# Features:
#   - Automatically detects installed AI platforms
#   - Creates symlinks for new skills
#   - Verifies existing symlinks point to correct locations
#   - Cleans up stale symlinks for removed/renamed skills
#   - Cross-platform support (Linux + macOS)
#   - Provides detailed report of actions taken
#
# Git Hook Integration:
#   This script is automatically called by .git/hooks/post-merge
#   after every 'git pull' or 'git merge' command.
#

set -euo pipefail

# Configuration — derive source from script location, not hardcoded $HOME
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COPILOT_SKILLS="$(cd "$SCRIPT_DIR/.." && pwd)"

# Detect OS
OS_TYPE="$(uname -s)"

# Platform directories (OS-specific)
if [[ "$OS_TYPE" == "Darwin" ]]; then
    # macOS
    OPENCODE_SKILLS="$HOME/.config/opencode/skills"
    CLAUDE_SKILLS="$HOME/Library/Application Support/Claude/skills"
    CURSOR_SKILLS="$HOME/Library/Application Support/Cursor/skills"
else
    # Linux
    OPENCODE_SKILLS="$HOME/.config/opencode/skills"
    CLAUDE_SKILLS="$HOME/.config/claude/skills"
    CURSOR_SKILLS="$HOME/.config/cursor/skills"
fi

# Colors for terminal output (suppress when not a terminal)
if [[ -t 1 ]]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    RED='\033[0;31m'
    GRAY='\033[0;90m'
    NC='\033[0m'
else
    GREEN='' YELLOW='' BLUE='' RED='' GRAY='' NC=''
fi

# Flags
DRY_RUN=false
PLATFORM_FILTER=""

# Help message
show_help() {
    cat << EOF
sync-skills.sh - Multi-Platform AI Skills Synchronization

Usage: $0 [OPTIONS]

Options:
  --platform NAME    Sync only to specified platform (opencode, claude, cursor)
  --dry-run          Show what would be done without making changes
  --help, -h         Show this help message

Description:
  Synchronizes all skills from ~/.copilot/skills/ to installed AI platforms
  using symbolic links. By default, auto-detects installed platforms and
  syncs to all of them.

Supported Platforms:
  • OpenCode       - ~/.config/opencode/skills/
  • Claude Desktop - ~/.config/claude/skills/ (Linux) or ~/Library/.../Claude/skills/ (macOS)
  • Cursor         - ~/.config/cursor/skills/ (Linux) or ~/Library/.../Cursor/skills/ (macOS)
  • GitHub Copilot - Uses repository directly (no sync needed)

Examples:
  $0                          # Auto-detect and sync to all installed platforms
  $0 --platform opencode      # Sync only to OpenCode
  $0 --dry-run                # Preview changes without applying them
  git pull                    # Auto-syncs if git hook is configured

See README.md for more information.
EOF
    exit 0
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            show_help
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --platform)
            if [[ $# -lt 2 ]]; then
                echo -e "${RED}Error: --platform requires a value${NC}"
                exit 1
            fi
            PLATFORM_FILTER="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}Error: Unknown option: $1${NC}"
            echo "Use --help for usage information."
            exit 1
            ;;
    esac
done

# Validate platform filter if provided
if [[ -n "$PLATFORM_FILTER" ]]; then
    case "$PLATFORM_FILTER" in
        opencode|claude|cursor)
            # Valid platform
            ;;
        *)
            echo -e "${RED}Error: Invalid platform '$PLATFORM_FILTER'${NC}"
            echo "Supported platforms: opencode, claude, cursor"
            exit 1
            ;;
    esac
fi

# Header
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           SKILL SYNCHRONIZATION: Multi-Platform              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [[ "$DRY_RUN" == true ]]; then
    echo -e "${YELLOW}🔍 DRY RUN MODE - No changes will be made${NC}"
    echo ""
fi

# Validate source directory exists
if [ ! -d "$COPILOT_SKILLS" ]; then
    echo -e "${RED}❌ Error: Source directory not found: $COPILOT_SKILLS${NC}"
    echo -e "${YELLOW}   Make sure this script is run from the skills repository.${NC}"
    exit 1
fi

echo -e "${BLUE}🔍 Searching for skills in: $COPILOT_SKILLS${NC}"
echo ""

# Detect installed platforms — use plain arrays for Bash 3 compatibility (macOS)
PLATFORM_NAMES=()
PLATFORM_PATHS_ARR=()

add_platform() {
    PLATFORM_NAMES+=("$1")
    PLATFORM_PATHS_ARR+=("$2")
}

# Check OpenCode
if [[ -z "$PLATFORM_FILTER" || "$PLATFORM_FILTER" == "opencode" ]]; then
    if [ -d "$(dirname "$OPENCODE_SKILLS")" ] || [[ "$PLATFORM_FILTER" == "opencode" ]]; then
        add_platform "opencode" "$OPENCODE_SKILLS"
        if [ -d "$OPENCODE_SKILLS" ]; then
            echo -e "  ✅ ${GREEN}OpenCode${NC}       → $OPENCODE_SKILLS"
        else
            echo -e "  📦 ${YELLOW}OpenCode${NC}       → $OPENCODE_SKILLS ${GRAY}(will be created)${NC}"
        fi
    else
        echo -e "  ⊘  ${GRAY}OpenCode${NC}       → Not installed"
    fi
fi

# Check Claude Desktop
if [[ -z "$PLATFORM_FILTER" || "$PLATFORM_FILTER" == "claude" ]]; then
    if [ -d "$(dirname "$CLAUDE_SKILLS")" ] || [[ "$PLATFORM_FILTER" == "claude" ]]; then
        add_platform "claude" "$CLAUDE_SKILLS"
        if [ -d "$CLAUDE_SKILLS" ]; then
            echo -e "  ✅ ${GREEN}Claude Desktop${NC} → $CLAUDE_SKILLS"
        else
            echo -e "  📦 ${YELLOW}Claude Desktop${NC} → $CLAUDE_SKILLS ${GRAY}(will be created)${NC}"
        fi
    else
        echo -e "  ⊘  ${GRAY}Claude Desktop${NC} → Not installed"
    fi
fi

# Check Cursor
if [[ -z "$PLATFORM_FILTER" || "$PLATFORM_FILTER" == "cursor" ]]; then
    if [ -d "$(dirname "$CURSOR_SKILLS")" ] || [[ "$PLATFORM_FILTER" == "cursor" ]]; then
        add_platform "cursor" "$CURSOR_SKILLS"
        if [ -d "$CURSOR_SKILLS" ]; then
            echo -e "  ✅ ${GREEN}Cursor${NC}         → $CURSOR_SKILLS"
        else
            echo -e "  📦 ${YELLOW}Cursor${NC}         → $CURSOR_SKILLS ${GRAY}(will be created)${NC}"
        fi
    else
        echo -e "  ⊘  ${GRAY}Cursor${NC}         → Not installed"
    fi
fi

echo ""

installed_count=${#PLATFORM_NAMES[@]}

if [[ $installed_count -eq 0 ]]; then
    echo -e "${YELLOW}⚠️  No AI platforms detected for synchronization.${NC}"
    echo ""
    echo "To sync skills to a platform:"
    echo "  • Install the platform first, or"
    echo "  • Use --platform NAME to force sync to a specific platform"
    echo ""
    exit 0
fi

# Known non-skill directories to skip
SKIP_DIRS="docs scripts tests .github"

is_skip_dir() {
    local name="$1"
    for skip in $SKIP_DIRS; do
        [[ "$name" == "$skip" ]] && return 0
    done
    return 1
}
# Sync a single platform: sync_to_platform <platform_name> <target_dir>
# Sets global LAST_* variables with results (Bash 3 compatible).
LAST_TOTAL=0
LAST_EXISTING=0
LAST_NEW=0
LAST_UPDATED=0
LAST_ERRORS=0

sync_to_platform() {
    local platform_name="$1"
    local target_dir="$2"

    # Reset per-platform counters
    LAST_TOTAL=0
    LAST_EXISTING=0
    LAST_NEW=0
    LAST_UPDATED=0
    LAST_ERRORS=0

    echo -e "${BLUE}Syncing to ${platform_name}...${NC}"

    # Create target directory if it doesn't exist
    if [ ! -d "$target_dir" ]; then
        if [[ "$DRY_RUN" == true ]]; then
            echo -e "  ${GRAY}[DRY RUN]${NC} Would create directory: $target_dir"
        else
            echo -e "  📁 ${YELLOW}Creating directory: $target_dir${NC}"
            mkdir -p "$target_dir"
        fi
    fi

    # Iterate over all directories containing SKILL.md
    for skill_path in "$COPILOT_SKILLS"/*/SKILL.md; do
        [ -e "$skill_path" ] || continue

        local skill_dir
        skill_dir="$(dirname "$skill_path")"
        local skill_name
        skill_name="$(basename "$skill_dir")"

        # Skip hidden directories
        [[ "$skill_name" == .* ]] && continue

        # Skip non-skill directories
        is_skip_dir "$skill_name" && continue

        LAST_TOTAL=$((LAST_TOTAL + 1))
        local symlink_path="$target_dir/$skill_name"

        if [ -L "$symlink_path" ]; then
            # Verify it points to the correct location
            local current_target
            current_target="$(readlink "$symlink_path")"
            if [ "$current_target" = "$skill_dir" ]; then
                echo -e "  ✅ ${GREEN}$skill_name${NC} → already synced"
                LAST_EXISTING=$((LAST_EXISTING + 1))
            else
                if [[ "$DRY_RUN" == true ]]; then
                    echo -e "  ${GRAY}[DRY RUN]${NC} 🔄 ${YELLOW}$skill_name${NC} → would update symlink (currently: $current_target)"
                else
                    echo -e "  🔄 ${YELLOW}$skill_name${NC} → updating symlink (was: $current_target)"
                    rm "$symlink_path"
                    ln -s "$skill_dir" "$symlink_path"
                fi
                LAST_UPDATED=$((LAST_UPDATED + 1))
            fi
        elif [ -e "$symlink_path" ]; then
            echo -e "  ❌ ${RED}$skill_name${NC} → exists as regular file/directory (not a symlink)"
            echo -e "     ${YELLOW}Please remove manually: $symlink_path${NC}"
            LAST_ERRORS=$((LAST_ERRORS + 1))
        else
            if [[ "$DRY_RUN" == true ]]; then
                echo -e "  ${GRAY}[DRY RUN]${NC} 🆕 ${GREEN}$skill_name${NC} → would create symlink"
            else
                echo -e "  🆕 ${GREEN}$skill_name${NC} → creating symlink..."
                ln -s "$skill_dir" "$symlink_path"
            fi
            LAST_NEW=$((LAST_NEW + 1))
        fi
    done

    # Clean up stale symlinks (point to skills that no longer exist)
    if [ -d "$target_dir" ]; then
        for entry in "$target_dir"/*; do
            [ -L "$entry" ] || continue
            local link_target
            link_target="$(readlink "$entry")"
            if [ ! -e "$link_target" ]; then
                local stale_name
                stale_name="$(basename "$entry")"
                if [[ "$DRY_RUN" == true ]]; then
                    echo -e "  ${GRAY}[DRY RUN]${NC} 🗑  ${YELLOW}$stale_name${NC} → would remove stale symlink"
                else
                    echo -e "  🗑  ${YELLOW}$stale_name${NC} → removing stale symlink (target missing: $link_target)"
                    rm "$entry"
                fi
            fi
        done
    fi

    echo ""
}

# Aggregate counters across all platforms
grand_total_skills=0
grand_total_existing=0
grand_total_new=0
grand_total_updated=0
grand_total_errors=0
synced_platforms=""

# Sync to each detected platform
idx=0
while [ $idx -lt $installed_count ]; do
    platform_name="${PLATFORM_NAMES[$idx]}"
    platform_path="${PLATFORM_PATHS_ARR[$idx]}"

    # Build display name
    platform_display=""
    case "$platform_name" in
        opencode) platform_display="OpenCode" ;;
        claude)   platform_display="Claude Desktop" ;;
        cursor)   platform_display="Cursor" ;;
        *)        platform_display="$platform_name" ;;
    esac

    sync_to_platform "$platform_display" "$platform_path"

    # Accumulate results
    if [ $LAST_TOTAL -gt $grand_total_skills ]; then
        grand_total_skills=$LAST_TOTAL
    fi
    grand_total_existing=$((grand_total_existing + LAST_EXISTING))
    grand_total_new=$((grand_total_new + LAST_NEW))
    grand_total_updated=$((grand_total_updated + LAST_UPDATED))
    grand_total_errors=$((grand_total_errors + LAST_ERRORS))

    # Build synced platforms list
    if [ -z "$synced_platforms" ]; then
        synced_platforms="$platform_name"
    else
        synced_platforms="$synced_platforms, $platform_name"
    fi

    idx=$((idx + 1))
done

# Summary
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                          SUMMARY                             ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"

echo -e "  Platforms synced:        ${GREEN}$installed_count${NC} ($synced_platforms)"
echo -e "  Total skills found:      ${GREEN}$grand_total_skills${NC}"
echo -e "  Already synced:          ${GREEN}$grand_total_existing${NC}"

if [ $grand_total_new -gt 0 ]; then
    echo -e "  Newly synced:            ${GREEN}$grand_total_new${NC}"
fi

if [ $grand_total_updated -gt 0 ]; then
    echo -e "  Updated:                 ${YELLOW}$grand_total_updated${NC}"
fi

if [ $grand_total_errors -gt 0 ]; then
    echo -e "  Errors:                  ${RED}$grand_total_errors${NC}"
fi

echo ""

# Final message
if [[ "$DRY_RUN" == true ]]; then
    echo -e "${BLUE}🔍 Dry run complete - no changes were made.${NC}"
elif [ $grand_total_errors -gt 0 ]; then
    echo -e "${RED}⚠️  Synchronization completed with errors.${NC}"
    echo -e "${YELLOW}   Please resolve the errors shown above.${NC}"
    exit 1
elif [ $grand_total_new -gt 0 ] || [ $grand_total_updated -gt 0 ]; then
    changes=$((grand_total_new + grand_total_updated))
    echo -e "${GREEN}✨ Synchronization complete! $changes skill(s) synced across $installed_count platform(s).${NC}"
else
    echo -e "${GREEN}✅ All skills already synchronized across $installed_count platform(s).${NC}"
fi

echo ""
echo -e "${BLUE}📍 Repository location:  $COPILOT_SKILLS${NC}"
echo -e "${BLUE}📍 Synced platforms:     $synced_platforms${NC}"
echo ""

# Helpful tips
if [ $grand_total_new -gt 0 ] && [[ "$DRY_RUN" == false ]]; then
    echo -e "${YELLOW}💡 Tip: Restart your AI assistant to ensure new skills are detected.${NC}"
    echo ""
fi
