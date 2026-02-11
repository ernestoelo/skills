#!/bin/bash
# Post-commit hook for generic CI verification in dev-workflow.
# Copies to <target-repo>/.git/hooks/post-commit and makes executable.
# Assumes scripts/verify_ci.py is in repo root/scripts/.

# Get repo root
REPO_ROOT=$(git rev-parse --show-toplevel)

# Check if verify_ci.py exists
if [ -f "$REPO_ROOT/scripts/verify_ci.py" ]; then
    # Infer workflow name from recent commit or default
    # For simplicity, default to "Validate Skills" or parse from commit
    WORKFLOW_NAME="Validate Skills"  # Customize per repo

    echo "Waiting for CI processing after commit..."
    sleep 30
    COMMIT_SHA=$(git rev-parse HEAD)
    echo "Running post-commit CI verification for commit $COMMIT_SHA..."
    python3 "$REPO_ROOT/scripts/verify_ci.py" --workflow "$WORKFLOW_NAME" --commit-sha "$COMMIT_SHA"
else
    echo "verify_ci.py not found. Skipping CI verification."
fi