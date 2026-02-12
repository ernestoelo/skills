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
    except KeyboardInterrupt:
        print(f"⏹️ Command interrupted: {cmd}")
        return False, "KeyboardInterrupt"
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

    max_attempts = 5
    attempt = 1
    while attempt <= max_attempts:
        print(f"🔍 Linting attempt {attempt}...")
        success, output = run_command("uv run ruff check .")
        if success:
            print("✅ Linting passed.")
            break
        elif output == "KeyboardInterrupt":
            print("⏹️ Linting interrupted. Retrying...")
            attempt += 1
            continue
        else:
            print("❌ Linting failed. Attempting auto-fix...")
            run_command("uv run ruff check . --fix")
            run_command("python3 /home/p3g4sus/.copilot/skills/code-review/scripts/analyze.py . --dir --ci --check lint --fix")
            attempt += 1
    if not success and not args.force:
        print(f"❌ Linting failed after {max_attempts} attempts. Fix issues or use --force to commit anyway.")
        sys.exit(1)
    elif not success:
        print("⚠️  Linting failed but proceeding with --force.")

    print("📦 Staging changes...")
    stage_attempt = 1
    max_stage_attempts = 5
    while stage_attempt <= max_stage_attempts:
        success, output = run_command("git add .")
        if success:
            break
        elif output == "KeyboardInterrupt":
            print("⏹️ Staging interrupted. Retrying...")
            stage_attempt += 1
            continue
        else:
            print("❌ Failed to stage changes. Attempting auto-fix...")
            run_command("uv run ruff check . --fix")
            run_command("python3 /home/p3g4sus/.copilot/skills/code-review/scripts/analyze.py . --dir --ci --check lint --fix")
            stage_attempt += 1
    if not success:
        print(f"❌ Staging failed after {max_stage_attempts} attempts.")
        sys.exit(1)

    commit_attempt = 1
    max_commit_attempts = 5
    while commit_attempt <= max_commit_attempts:
        print(f"💾 Commit attempt {commit_attempt}...")
        success, output = run_command(f'git commit -m "{args.message}"')
        if success:
            print("✅ Local commit successful.")
            break
        elif output == "KeyboardInterrupt":
            print("⏹️ Commit interrupted. Retrying...")
            commit_attempt += 1
            continue
        else:
            print("❌ Commit failed. Attempting auto-fix...")
            run_command("uv run ruff check . --fix")
            run_command("python3 /home/p3g4sus/.copilot/skills/code-review/scripts/analyze.py . --dir --ci --check lint --fix")
            run_command("git add .")
            commit_attempt += 1
    if not success:
        print(f"❌ Commit failed after {max_commit_attempts} attempts. No changes to commit or unresolved issues.")
        sys.exit(1)


if __name__ == "__main__":
    main()
