#!/usr/bin/env python3
"""
Portable CI auto-correction script for dev-workflow.

Detects CI failures, applies safe fixes iteratively (linting, tests, builds),
and re-commits. Triggered by GitHub Actions webhooks or manual run.

Usage: python3 auto_correct_portable.py --workflow <workflow_name>
Example: python3 auto_correct_portable.py --workflow "Validate Skills"
"""

import subprocess
import sys
import json
import os
from pathlib import Path


def check_dependencies():
    """Check and install missing dependencies (gh, token)."""
    # Check gh
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("GitHub CLI (gh) not found. Installing...")
        subprocess.run(["pacman", "-S", "--noconfirm", "github-cli"], check=True)

    # Check token
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set. Please set it or configure gh auth.")
        sys.exit(1)


def get_last_run_status(workflow_name):
    """Get status of the last CI run."""
    try:
        result = subprocess.run(
            [
                "gh",
                "run",
                "list",
                "--workflow",
                workflow_name,
                "--json",
                "status,conclusion",
                "--limit",
                "1",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        runs = json.loads(result.stdout)
        if runs:
            return runs[0]["status"], runs[0]["conclusion"]
        return None, None
    except subprocess.CalledProcessError:
        return None, None


def detect_error_type():
    """Detect error type from CI logs (simplified: check for common keywords)."""
    # In real implementation, fetch logs with gh run view --log
    # For now, assume ruff/test errors; expand to builds
    # This is placeholder; integrate with actual log parsing
    return "linting"  # Example


def apply_safe_fix(error_type):
    """Apply safe fixes based on error type."""
    fixes = {
        "linting": ["uv", "run", "ruff", "check", "--fix", "."],
        "tests": ["uv", "run", "pytest"],  # Run tests to check
        "builds": ["uv", "run", "python", "-m", "build"],  # Build check
    }
    if error_type in fixes:
        subprocess.run(fixes[error_type], check=True)
        return True
    return False


def re_commit():
    """Stage, commit, and push changes."""
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "fix: auto-correct CI issues"], check=True)
    subprocess.run(["git", "push"], check=True)


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--workflow":
        print("Usage: python3 auto_correct_portable.py --workflow <workflow_name>")
        sys.exit(1)

    workflow_name = sys.argv[2]

    check_dependencies()

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        status, conclusion = get_last_run_status(workflow_name)
        if status == "completed" and conclusion == "success":
            print(f"CI passed on attempt {attempt}.")
            break
        elif conclusion == "failure":
            error_type = detect_error_type()
            print(f"CI failed (attempt {attempt}). Applying fix for {error_type}...")
            if apply_safe_fix(error_type):
                re_commit()
            else:
                print(f"No fix available for {error_type}.")
        else:
            print(f"CI in progress or unknown status (attempt {attempt}). Waiting...")
        if attempt == max_attempts:
            print("Max attempts reached. Manual intervention needed.")
            sys.exit(1)


if __name__ == "__main__":
    main()
