#!/bin/bash
#
# sync-skills.sh
# Multi-platform skill synchronization script
# Creates symlinks from repository skills to AI platform directories
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
DRY_RUN=false
VERBOSE=false
SPECIFIC_PLATFORM=""

# Function to print usage
usage() {
    cat << EOF
╔══════════════════════════════════════════════════════════════╗
║           SKILL SYNCHRONIZATION: Multi-Platform              ║
╚══════════════════════════════════════════════════════════════╝

Syncs skills from repository to AI platform directories using symlinks.

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --platform PLATFORM    Sync to specific platform only (opencode, claude, cursor)
    --dry-run             Preview changes without applying them
    --verbose             Show detailed output
    --help               Show this help message

PLATFORMS:
    opencode    OpenCode AI assistant
    claude      Claude Desktop
    cursor      Cursor IDE

EXAMPLES:
    $0                    # Sync to all detected platforms
    $0 --platform opencode # Sync to OpenCode only
    $0 --dry-run          # Preview what would be synced
    $0 --verbose          # Show detailed output

EOF
}

# Function to detect platforms
detect_platforms() {
    echo -e "${BLUE}📍 Platform Detection:${NC}"

    # OpenCode
    if [ -d "$HOME/.config/opencode/skills" ]; then
        echo -e "  ✅ OpenCode       → $HOME/.config/opencode/skills/"
        PLATFORMS["opencode"]="$HOME/.config/opencode/skills"
    else
        echo -e "  ❌ OpenCode       → Not installed ($HOME/.config/opencode/skills/)"
    fi

    # Claude Desktop (Linux)
    if [ -d "$HOME/.config/claude/skills" ]; then
        echo -e "  ✅ Claude Desktop → $HOME/.config/claude/skills/"
        PLATFORMS["claude"]="$HOME/.config/claude/skills"
    elif [ -d "$HOME/Library/Application Support/Claude/skills" ]; then
        echo -e "  ✅ Claude Desktop → $HOME/Library/Application Support/Claude/skills/"
        PLATFORMS["claude"]="$HOME/Library/Application Support/Claude/skills"
    else
        echo -e "  ❌ Claude Desktop → Not installed"
    fi

    # Cursor (Linux)
    if [ -d "$HOME/.config/cursor/skills" ]; then
        echo -e "  ✅ Cursor         → $HOME/.config/cursor/skills/"
        PLATFORMS["cursor"]="$HOME/.config/cursor/skills"
    elif [ -d "$HOME/Library/Application Support/Cursor/skills" ]; then
        echo -e "  ✅ Cursor         → $HOME/Library/Application Support/Cursor/skills/"
        PLATFORMS["cursor"]="$HOME/Library/Application Support/Cursor/skills"
    else
        echo -e "  ❌ Cursor         → Not installed"
    fi
}

# Function to find skills in current directory
find_skills() {
    echo -e "\n${BLUE}🔍 Searching for skills in: $(pwd)/skills${NC}"

    # Look for directories containing SKILL.md in the skills subdirectory
    SKILLS=()
    if [ -d "skills" ]; then
        for dir in skills/*/; do
            dir=${dir%/}  # Remove trailing slash
            if [ -f "$dir/SKILL.md" ]; then
                skill_name=$(basename "$dir")
                SKILLS+=("$skill_name")
                if [ "$VERBOSE" = true ]; then
                    echo -e "  📁 Found skill: $skill_name"
                fi
            fi
        done
    fi

    echo -e "  Found ${#SKILLS[@]} skill(s)"
}

# Function to create symlink
create_symlink() {
    local skill="$1"
    local target_dir="$2"
    local platform="$3"

    local source_path="$(pwd)/skills/$skill"
    local link_path="$target_dir/$skill"

    if [ -L "$link_path" ]; then
        # Symlink exists, check if it's correct
        local current_target=$(readlink "$link_path")
        if [ "$current_target" = "$source_path" ]; then
            echo -e "  ✅ $skill → already synced"
            return 0
        else
            if [ "$DRY_RUN" = false ]; then
                rm "$link_path"
                ln -s "$source_path" "$link_path"
                echo -e "  🔄 $skill → updated symlink"
                return 1
            else
                echo -e "  🔄 $skill → would update symlink"
                return 1
            fi
        fi
    elif [ -e "$link_path" ]; then
        # Something else exists (file/directory)
        echo -e "  ${RED}⚠️  $skill → conflict (file/directory exists, skipping)${NC}"
        return 0
    else
        # Create new symlink
        if [ "$DRY_RUN" = false ]; then
            ln -s "$source_path" "$link_path"
            echo -e "  🆕 $skill → creating symlink"
            return 1
        else
            echo -e "  🆕 $skill → would create symlink"
            return 1
        fi
    fi
}

# Function to sync to platform
sync_to_platform() {
    local platform="$1"
    local target_dir="$2"

    echo -e "\n${CYAN}Syncing to $platform...${NC}"

    local synced_count=0
    local total_count=0

    for skill in "${SKILLS[@]}"; do
        total_count=$((total_count + 1))
        if create_symlink "$skill" "$target_dir" "$platform"; then
            synced_count=$((synced_count + 1))
        fi
    done

    echo -e "${GREEN}  Synced $synced_count/$total_count skills to $platform${NC}"
    return $synced_count
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --platform)
            SPECIFIC_PLATFORM="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            exit 1
            ;;
    esac
done

# Main execution
echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║           SKILL SYNCHRONIZATION: Multi-Platform              ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}🔍 DRY RUN MODE - No changes will be made${NC}\n"
fi

# Detect platforms
declare -A PLATFORMS
detect_platforms

# Find skills
find_skills

# Validate specific platform if requested
if [ -n "$SPECIFIC_PLATFORM" ]; then
    if [ -z "${PLATFORMS[$SPECIFIC_PLATFORM]}" ]; then
        echo -e "\n${RED}❌ Platform '$SPECIFIC_PLATFORM' not detected or not installed${NC}"
        exit 1
    fi
fi

# Sync to platforms
total_synced=0
platforms_synced=0

for platform in "${!PLATFORMS[@]}"; do
    if [ -n "$SPECIFIC_PLATFORM" ] && [ "$platform" != "$SPECIFIC_PLATFORM" ]; then
        continue
    fi

    target_dir="${PLATFORMS[$platform]}"
    if sync_to_platform "$platform" "$target_dir"; then
        platforms_synced=$((platforms_synced + 1))
        total_synced=$((total_synced + $?))
    fi
done

# Summary
echo -e "\n${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                          SUMMARY                             ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo -e "  Platforms synced:        $platforms_synced"
echo -e "  Total skills found:      ${#SKILLS[@]}"
echo -e "  Newly synced:            $total_synced"

if [ "$DRY_RUN" = false ]; then
    echo -e "\n${GREEN}✨ Synchronization complete! $total_synced skill(s) synced across $platforms_synced platform(s).${NC}"
else
    echo -e "\n${YELLOW}🔍 Dry run complete. Use without --dry-run to apply changes.${NC}"
fi

exit 0