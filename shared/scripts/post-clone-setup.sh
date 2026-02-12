#!/usr/bin/env bash
#
# post-clone-setup.sh - Initialization script for developers cloning the repository
#
# Sets up git hooks and required dependencies.
# Run this script once after cloning to ensure proper configuration.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
GIT_HOOKS_DIR="$REPO_ROOT/.git/hooks"

# --- Pre-commit hook: validates skills on commit ---
PRE_COMMIT_SRC="$REPO_ROOT/scripts/validate-skill-on-change.sh"
PRE_COMMIT_DEST="$GIT_HOOKS_DIR/pre-commit"

if [ ! -e "$PRE_COMMIT_DEST" ]; then
    echo "Setting up pre-commit hook for skill validation..."
    ln -sf "$PRE_COMMIT_SRC" "$PRE_COMMIT_DEST"
    chmod +x "$PRE_COMMIT_DEST"
    echo "Pre-commit hook installed successfully."
else
    echo "Pre-commit hook is already set up. Skipping."
fi

# --- Post-merge hook: auto-syncs skills after git pull ---
SYNC_SCRIPT="$REPO_ROOT/scripts/sync-skills.sh"
POST_MERGE_DEST="$GIT_HOOKS_DIR/post-merge"

if [ ! -e "$POST_MERGE_DEST" ]; then
    echo "Setting up post-merge hook for skill auto-sync..."
    # Create a thin wrapper that calls sync-skills.sh
    cat > "$POST_MERGE_DEST" << 'HOOK'
#!/usr/bin/env bash
# Auto-sync skills to AI platforms after git pull / git merge
REPO_ROOT="$(git rev-parse --show-toplevel)"
SYNC_SCRIPT="$REPO_ROOT/scripts/sync-skills.sh"
if [ -x "$SYNC_SCRIPT" ]; then
    echo "Running post-merge skill sync..."
    "$SYNC_SCRIPT"
fi
HOOK
    chmod +x "$POST_MERGE_DEST"
    echo "Post-merge hook installed successfully."
else
    echo "Post-merge hook is already set up. Skipping."
fi

# Additional environment setup
# Install dependencies automatically
if command -v uv &>/dev/null; then
    echo "Installing dependencies with uv..."
    uv sync --group dev
else
    echo "uv is not installed. Skipping dependency installation."
fi

echo ""
echo "Repository setup complete. You are ready to work on this project."
