#!/usr/bin/env python3
"""
Local Development Auto-Commit Script for dev-workflow.

Runs linting, stages changes, and commits if no issues found.
Experimental feature for CI-like local automation.

Usage: python3 auto_commit_local.py --message "commit message" [--force]
"""

import subprocess
import sys
import argparse


def run_command(cmd, cwd=None):
    """Run a command and return success."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=cwd, check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        print(e.stderr)
        return False, e.stderr


def main():
    parser = argparse.ArgumentParser(
        description="Auto-commit local changes after linting."
    )
    parser.add_argument("--message", required=True, help="Commit message")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force commit even if linting fails (not recommended)",
    )
    args = parser.parse_args()

    print("🔍 Running local linting...")
    success, output = run_command("uv run ruff check .")
    if not success and not args.force:
        print("❌ Linting failed. Fix issues or use --force to commit anyway.")
        sys.exit(1)
    elif not success:
        print("⚠️  Linting failed but proceeding with --force.")
    else:
        print("✅ Linting passed.")

    print("📦 Staging changes...")
    success, output = run_command("git add .")
    if not success:
        print("❌ Failed to stage changes.")
        sys.exit(1)

    print("💾 Committing...")
    success, output = run_command(f'git commit -m "{args.message}"')
    if not success:
        print("❌ Commit failed (possibly no changes to commit).")
        sys.exit(1)

    print("✅ Local commit successful.")


if __name__ == "__main__":
    main()
