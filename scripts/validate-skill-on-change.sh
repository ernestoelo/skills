#!/usr/bin/env bash
#
# validate-skill-on-change.sh - Git pre-commit hook for skill validation
#
# Validates modified skills using scripts/quick_validate.py.
# If any skill validation fails, the commit is aborted.

set -euo pipefail

# Resolve paths relative to the repository root
REPO_ROOT="$(git rev-parse --show-toplevel)"
VALIDATOR="$REPO_ROOT/scripts/quick_validate.py"

# Check if validator exists
if [ ! -f "$VALIDATOR" ]; then
    echo "Error: Validation script not found at $VALIDATOR."
    exit 1
fi

# Get staged skill directories (one per line, safe for spaces)
echo "Detecting staged skill changes..."
CHANGED_SKILLS="$(git diff --cached --name-only | grep '^.*/SKILL.md$' | while IFS= read -r f; do dirname "$f"; done)"

# Exit quietly if no skills were modified
if [ -z "$CHANGED_SKILLS" ]; then
    echo "No skill changes detected. Skipping validation."
    exit 0
fi

# Validate each detected skill directory
while IFS= read -r SKILL; do
    [ -n "$SKILL" ] || continue
    echo "Validating skill: $SKILL"
    if ! python3 "$VALIDATOR" "$SKILL"; then
        echo "Validation failed for $SKILL. Please fix the issues and try again."
        exit 1
    fi
done <<< "$CHANGED_SKILLS"

echo "All skill validations passed. Proceeding with commit."
exit 0
