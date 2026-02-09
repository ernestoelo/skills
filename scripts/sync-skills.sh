#!/bin/bash
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
#   - Cross-platform support (Linux + macOS)
#   - Provides detailed report of actions taken
#
# Git Hook Integration:
#   This script is automatically called by .git/hooks/post-merge
#   after every 'git pull' or 'git merge' command.
#

set -e  # Exit on error

# Configuration
COPILOT_SKILLS="$HOME/.copilot/skills"

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

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
GRAY='\033[0;90m'
NC='\033[0m'  # No Color

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

# Detect installed platforms
echo -e "${BLUE}📍 Platform Detection:${NC}"

declare -A PLATFORMS
declare -A PLATFORM_PATHS

# Check OpenCode
if [[ -z "$PLATFORM_FILTER" || "$PLATFORM_FILTER" == "opencode" ]]; then
    if [ -d "$(dirname "$OPENCODE_SKILLS")" ] || [[ "$PLATFORM_FILTER" == "opencode" ]]; then
        PLATFORMS[opencode]=true
        PLATFORM_PATHS[opencode]="$OPENCODE_SKILLS"
        if [ -d "$OPENCODE_SKILLS" ]; then
            echo -e "  ✅ ${GREEN}OpenCode${NC}       → $OPENCODE_SKILLS"
        else
            echo -e "  📦 ${YELLOW}OpenCode${NC}       → $OPENCODE_SKILLS ${GRAY}(will be created)${NC}"
        fi
    else
        PLATFORMS[opencode]=false
        echo -e "  ⊘  ${GRAY}OpenCode${NC}       → Not installed"
    fi
fi

# Check Claude Desktop
if [[ -z "$PLATFORM_FILTER" || "$PLATFORM_FILTER" == "claude" ]]; then
    if [ -d "$(dirname "$CLAUDE_SKILLS")" ] || [[ "$PLATFORM_FILTER" == "claude" ]]; then
        PLATFORMS[claude]=true
        PLATFORM_PATHS[claude]="$CLAUDE_SKILLS"
        if [ -d "$CLAUDE_SKILLS" ]; then
            echo -e "  ✅ ${GREEN}Claude Desktop${NC} → $CLAUDE_SKILLS"
        else
            echo -e "  📦 ${YELLOW}Claude Desktop${NC} → $CLAUDE_SKILLS ${GRAY}(will be created)${NC}"
        fi
    else
        PLATFORMS[claude]=false
        echo -e "  ⊘  ${GRAY}Claude Desktop${NC} → Not installed"
    fi
fi

# Check Cursor
if [[ -z "$PLATFORM_FILTER" || "$PLATFORM_FILTER" == "cursor" ]]; then
    if [ -d "$(dirname "$CURSOR_SKILLS")" ] || [[ "$PLATFORM_FILTER" == "cursor" ]]; then
        PLATFORMS[cursor]=true
        PLATFORM_PATHS[cursor]="$CURSOR_SKILLS"
        if [ -d "$CURSOR_SKILLS" ]; then
            echo -e "  ✅ ${GREEN}Cursor${NC}         → $CURSOR_SKILLS"
        else
            echo -e "  📦 ${YELLOW}Cursor${NC}         → $CURSOR_SKILLS ${GRAY}(will be created)${NC}"
        fi
    else
        PLATFORMS[cursor]=false
        echo -e "  ⊘  ${GRAY}Cursor${NC}         → Not installed"
    fi
fi

echo ""

# Count installed platforms
installed_count=0
for platform in "${!PLATFORMS[@]}"; do
    if [[ "${PLATFORMS[$platform]}" == true ]]; then
        installed_count=$((installed_count + 1))
    fi
done

if [[ $installed_count -eq 0 ]]; then
    echo -e "${YELLOW}⚠️  No AI platforms detected for synchronization.${NC}"
    echo ""
    echo "To sync skills to a platform:"
    echo "  • Install the platform first, or"
    echo "  • Use --platform NAME to force sync to a specific platform"
    echo ""
    exit 0
fi

# Sync function for a single platform
sync_to_platform() {
    local platform_key=$1     # e.g., "opencode", "claude", "cursor"
    local platform_name=$2     # e.g., "OpenCode", "Claude Desktop", "Cursor"
    local target_dir=$3
    
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
    
    # Counters for this platform
    local new_count=0
    local existing_count=0
    local updated_count=0
    local error_count=0
    local total_count=0
    
    # Iterate over all directories containing SKILL.md
    for skill_path in "$COPILOT_SKILLS"/*/SKILL.md; do
        # Check if file exists (avoids error if no matches found)
        [ -e "$skill_path" ] || continue
        
        # Extract directory and skill name
        local skill_dir=$(dirname "$skill_path")
        local skill_name=$(basename "$skill_dir")
        
        # Skip hidden directories (like .git)
        if [[ "$skill_name" == .* ]]; then
            continue
        fi
        
        # Skip non-skill directories
        if [[ "$skill_name" == "docs" ]] || [[ "$skill_name" == "scripts" ]]; then
            continue
        fi
        
        total_count=$((total_count + 1))
        local symlink_path="$target_dir/$skill_name"
        
        # Check if symlink already exists
        if [ -L "$symlink_path" ]; then
            # Verify it points to the correct location
            local current_target=$(readlink "$symlink_path")
            if [ "$current_target" = "$skill_dir" ]; then
                echo -e "  ✅ ${GREEN}$skill_name${NC} → already synced"
                existing_count=$((existing_count + 1))
            else
                if [[ "$DRY_RUN" == true ]]; then
                    echo -e "  ${GRAY}[DRY RUN]${NC} 🔄 ${YELLOW}$skill_name${NC} → would update symlink (currently: $current_target)"
                else
                    echo -e "  🔄 ${YELLOW}$skill_name${NC} → updating symlink (was: $current_target)"
                    rm "$symlink_path"
                    ln -s "$skill_dir" "$symlink_path"
                fi
                updated_count=$((updated_count + 1))
            fi
        elif [ -e "$symlink_path" ]; then
            # Exists but is not a symlink (regular file or directory)
            echo -e "  ❌ ${RED}$skill_name${NC} → exists as regular file/directory (not a symlink)"
            echo -e "     ${YELLOW}Please remove manually: $symlink_path${NC}"
            error_count=$((error_count + 1))
        else
            # Doesn't exist, create symlink
            if [[ "$DRY_RUN" == true ]]; then
                echo -e "  ${GRAY}[DRY RUN]${NC} 🆕 ${GREEN}$skill_name${NC} → would create symlink"
            else
                echo -e "  🆕 ${GREEN}$skill_name${NC} → creating symlink..."
                ln -s "$skill_dir" "$symlink_path"
            fi
            new_count=$((new_count + 1))
        fi
    done
    
    # Store results in global arrays using platform key
    PLATFORM_TOTALS[$platform_key]=$total_count
    PLATFORM_EXISTING[$platform_key]=$existing_count
    PLATFORM_NEW[$platform_key]=$new_count
    PLATFORM_UPDATED[$platform_key]=$updated_count
    PLATFORM_ERRORS[$platform_key]=$error_count
    
    echo ""
}

# Global result arrays
declare -A PLATFORM_TOTALS
declare -A PLATFORM_EXISTING
declare -A PLATFORM_NEW
declare -A PLATFORM_UPDATED
declare -A PLATFORM_ERRORS

# Sync to each detected platform
for platform in "${!PLATFORMS[@]}"; do
    if [[ "${PLATFORMS[$platform]}" == true ]]; then
        platform_display=""
        case $platform in
            opencode) platform_display="OpenCode" ;;
            claude) platform_display="Claude Desktop" ;;
            cursor) platform_display="Cursor" ;;
        esac
        
        sync_to_platform "$platform" "$platform_display" "${PLATFORM_PATHS[$platform]}"
    fi
done

# Summary
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                          SUMMARY                             ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"

# Platforms synced
synced_platforms=""
for platform in "${!PLATFORMS[@]}"; do
    if [[ "${PLATFORMS[$platform]}" == true ]]; then
        if [[ -z "$synced_platforms" ]]; then
            synced_platforms="$platform"
        else
            synced_platforms="$synced_platforms, $platform"
        fi
    fi
done

echo -e "  Platforms synced:        ${GREEN}$installed_count${NC} ($synced_platforms)"

# Aggregate totals across all platforms
total_skills=0
total_existing=0
total_new=0
total_updated=0
total_errors=0

for platform in "${!PLATFORMS[@]}"; do
    if [[ "${PLATFORMS[$platform]}" == true ]]; then
        # Get the max skills count (should be same across all platforms)
        platform_skills=${PLATFORM_TOTALS[$platform]:-0}
        if [ $platform_skills -gt $total_skills ]; then
            total_skills=$platform_skills
        fi
        
        total_existing=$((total_existing + ${PLATFORM_EXISTING[$platform]:-0}))
        total_new=$((total_new + ${PLATFORM_NEW[$platform]:-0}))
        total_updated=$((total_updated + ${PLATFORM_UPDATED[$platform]:-0}))
        total_errors=$((total_errors + ${PLATFORM_ERRORS[$platform]:-0}))
    fi
done

echo -e "  Total skills found:      ${GREEN}$total_skills${NC}"
echo -e "  Already synced:          ${GREEN}$total_existing${NC}"

if [ $total_new -gt 0 ]; then
    echo -e "  Newly synced:            ${GREEN}$total_new${NC}"
fi

if [ $total_updated -gt 0 ]; then
    echo -e "  Updated:                 ${YELLOW}$total_updated${NC}"
fi

if [ $total_errors -gt 0 ]; then
    echo -e "  Errors:                  ${RED}$total_errors${NC}"
fi

echo ""

# Final message
if [[ "$DRY_RUN" == true ]]; then
    echo -e "${BLUE}🔍 Dry run complete - no changes were made.${NC}"
elif [ $total_errors -gt 0 ]; then
    echo -e "${RED}⚠️  Synchronization completed with errors.${NC}"
    echo -e "${YELLOW}   Please resolve the errors shown above.${NC}"
    exit 1
elif [ $total_new -gt 0 ] || [ $total_updated -gt 0 ]; then
    changes=$((total_new + total_updated))
    echo -e "${GREEN}✨ Synchronization complete! $changes skill(s) synced across $installed_count platform(s).${NC}"
else
    echo -e "${GREEN}✅ All skills already synchronized across $installed_count platform(s).${NC}"
fi

echo ""
echo -e "${BLUE}📍 Repository location:  $COPILOT_SKILLS${NC}"
echo -e "${BLUE}📍 Synced platforms:     $synced_platforms${NC}"
echo ""

# Helpful tips
if [ $total_new -gt 0 ] && [[ "$DRY_RUN" == false ]]; then
    echo -e "${YELLOW}💡 Tip: Restart your AI assistant to ensure new skills are detected.${NC}"
    echo ""
fi
