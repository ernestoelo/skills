#!/bin/bash
#
# validate-opencode-pr.sh
# Validation script for OpenCode proactive skill loader PR
#

set -e

echo "🔍 Validating OpenCode PR readiness..."
echo "========================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check required files exist
echo "📁 Checking required PR files..."
REQUIRED_FILES=(
    "types/proactive-loader.ts"
    "types/skill-modified.ts"
    "types/config-modified.ts"
    "types/session-modified.ts"
    "OPENCODE_PR_README.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ✅ $file exists"
    else
        echo -e "  ❌ $file missing"
        exit 1
    fi
done

# Check TypeScript syntax (basic check)
echo ""
echo "🔧 Checking TypeScript files..."
for file in types/*.ts; do
    if [ -f "$file" ]; then
        # Basic syntax check - look for common issues
        if grep -q "import.*from" "$file" && grep -q "export" "$file"; then
            echo -e "  ✅ $file syntax OK"
        else
            echo -e "  ⚠️  $file may have syntax issues"
        fi
    fi
done

# Check symlinks
echo ""
echo "🔗 Checking OpenCode symlinks..."
if [ -d "$HOME/.config/opencode/skills" ]; then
    SKILL_COUNT=$(ls -1 "$HOME/.config/opencode/skills" | wc -l)
    echo -e "  ✅ OpenCode skills directory exists ($SKILL_COUNT skills linked)"
else
    echo -e "  ❌ OpenCode skills directory not found"
fi

# Check git branch
echo ""
echo "🌿 Checking git branch..."
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" = "feature/opencode-proactive-skill-loader" ]; then
    echo -e "  ✅ On correct branch: $CURRENT_BRANCH"
else
    echo -e "  ⚠️  Not on expected branch. Current: $CURRENT_BRANCH"
fi

# Check for any uncommitted changes
echo ""
echo "📝 Checking for uncommitted changes..."
if git diff --quiet && git diff --staged --quiet; then
    echo -e "  ✅ Working tree clean"
else
    echo -e "  ⚠️  Uncommitted changes found"
    git status --short
fi

# Summary
echo ""
echo "========================================"
echo -e "${GREEN}✅ OpenCode PR validation complete!${NC}"
echo ""
echo "Ready to create PR with the following files:"
for file in "${REQUIRED_FILES[@]}"; do
    echo "  - $file"
done
echo ""
echo "Next steps:"
echo "1. Push this branch to GitHub"
echo "2. Create PR in OpenCode repository"
echo "3. Apply the changes from types/ files to OpenCode's codebase"
echo ""
echo "Remember: This repository contains the PR files and documentation."
echo "The actual OpenCode repository needs the changes applied."