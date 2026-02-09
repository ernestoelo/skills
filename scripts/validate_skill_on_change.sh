#!/bin/bash

# validate_skill_on_change.sh - Git hook to validate skills on commit
# This script validates modified skills using scripts/quick_validate.py.
# If any skill validation fails, the commit is aborted.

# Exit immediately if any command fails (enforces safer scripting)
set -e

# Path to the quick_validate.py script
VALIDATOR="$(git rev-parse --show-toplevel)/scripts/quick_validate.py"

# Check if validator exists
if [ ! -f "$VALIDATOR" ]; then
  echo "Error: Validation script not found at $VALIDATOR. Make sure it exists."
  exit 1
fi

# Get a list of staged skill directories from git diff
echo "Detecting staged skill changes..."
CHANGED_SKILLS=$(git diff --cached --name-only | grep '^.*/SKILL.md$' | xargs -I {} dirname {})

# Exit quietly if no skills were modified
if [ -z "$CHANGED_SKILLS" ]; then
  echo "No skill changes detected. Skipping validation."
  exit 0
fi

# Validate each detected skill directory
VALIDATION_FAILED=false
for SKILL in $CHANGED_SKILLS; do
  echo "Validating skill: $SKILL"
  python3 "$VALIDATOR" "$SKILL" || VALIDATION_FAILED=true
  
  if [ "$VALIDATION_FAILED" = true ]; then
    echo "Validation failed for $SKILL. Please fix the issues and try again."
    exit 1
  fi

done

# If all validations passed
echo "All skill validations passed. Proceeding with commit."
exit 0