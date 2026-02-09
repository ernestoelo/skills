#!/bin/bash

# post-clone-setup.sh - Initialization script for developers cloning the repository.
# This script sets up the environment, including git hooks, required dependencies, etc.
# Run this script after cloning to ensure proper configuration.

# Exit on error
set -e

# Ensure git hooks path is properly set
GIT_HOOKS_DIR="$(git rev-parse --show-toplevel)/.git/hooks"
HOOK_SCRIPT_SRC="$(git rev-parse --show-toplevel)/scripts/validate_skill_on_change.sh"
HOOK_SCRIPT_DEST="$GIT_HOOKS_DIR/pre-commit"

# Check if pre-commit hook exists
if [ ! -e "$HOOK_SCRIPT_DEST" ]; then
  echo "Setting up pre-commit hook for skill validation..."
  ln -sf "$HOOK_SCRIPT_SRC" "$HOOK_SCRIPT_DEST"
  chmod +x "$HOOK_SCRIPT_DEST"
  echo "Pre-commit hook installed successfully."
else
  echo "Pre-commit hook is already set up. Skipping installation."
fi

# Additional environment setup can be added here

# Confirmation message
echo "Repository setup complete. You are ready to work on this project."