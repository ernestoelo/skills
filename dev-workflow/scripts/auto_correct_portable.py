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


def check_dependencies():
    """Check and install missing dependencies (gh, token)."""
    # Check OS
    try:
        with open("/etc/os-release") as f:
            os_release = f.read().lower()
            is_ubuntu = "ubuntu" in os_release
            is_arch = "arch" in os_release
    except Exception:
        is_ubuntu = is_arch = False

    # Check gh
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("GitHub CLI (gh) not found. Installing...")
        if is_ubuntu:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "gh"], check=True)
        elif is_arch:
            subprocess.run(
                ["sudo", "pacman", "-S", "--noconfirm", "github-cli"], check=True
            )
        else:
            print("Unsupported OS for auto-install. Please install gh manually.")
            sys.exit(1)

    # Check token
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set. Please set it in environment or GitHub secrets.")
        sys.exit(1)


def get_last_run_status(workflow_name, commit_sha=None):
    """Get status of the last CI run, optionally filtered by commit SHA."""
    try:
        result = subprocess.run(
            [
                "gh",
                "run",
                "list",
                "--workflow",
                workflow_name,
                "--json",
                "status,conclusion,headSha",
                "--limit",
                "10",  # Increased limit to find relevant run
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        runs = json.loads(result.stdout)
        if commit_sha:
            # Filter runs for the specific commit SHA
            relevant_runs = [run for run in runs if run.get("headSha") == commit_sha]
            if relevant_runs:
                run = relevant_runs[0]  # Take the latest matching
                return run["status"], run["conclusion"]
            else:
                return None, None  # No run for this commit yet
        else:
            # Fallback to latest if no SHA provided
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
        "linting": [
            "python3",
            "code-review/scripts/analyze.py",
            "--dir",
            ".",
            "--ci",
            "--check",
            "lint",
            "&&",
            "uv",
            "run",
            "ruff",
            "check",
            "--fix",
            ".",
        ],
        "tests": ["uv", "run", "pytest"],  # Run tests to check
        "builds": ["uv", "run", "python", "-m", "build"],  # Build check
    }
    if error_type in fixes:
        subprocess.run(fixes[error_type], check=True)
        return True
    return False


def re_commit():
    """Stage, commit, and push changes. Returns commit SHA."""
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "fix: auto-correct CI issues"], check=True)
    # Get SHA before push
    commit_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    subprocess.run(["git", "push"], check=True)
    return commit_sha


def verify_ci_after_push(workflow_name, commit_sha=None, timeout=300):
    """Verify CI status after push, wait up to timeout seconds. Filters by commit_sha if provided."""
    import time

    print(f"Verifying CI status for '{workflow_name}' after push...")
    print("Waiting for CI to process the push...")
    time.sleep(30)  # Initial wait for GitHub to detect push and start workflow

    start_time = time.time()
    while time.time() - start_time < timeout:
        status, conclusion = get_last_run_status(workflow_name, commit_sha)
        if status is None:
            print("No CI run found for this commit yet, waiting...")
            time.sleep(10)
            continue
        if status == "completed":
            if conclusion == "success":
                print("CI verification: SUCCESS")
                return True
            else:
                print(f"CI verification: FAILED (conclusion: {conclusion})")
                return False
        elif status in ["in_progress", "queued"]:
            print("CI in progress, waiting...")
            time.sleep(10)  # Poll every 10s
        else:
            print(f"CI status unknown: {status}")
            time.sleep(10)
    print("CI verification timeout.")
    return False


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
                commit_sha = re_commit()
                if not verify_ci_after_push(workflow_name, commit_sha=commit_sha):
                    print("Post-push CI verification failed. Manual check recommended.")
            else:
                print(f"No fix available for {error_type}.")
        else:
            print(f"CI in progress or unknown status (attempt {attempt}). Waiting...")
        if attempt == max_attempts:
            print("Max attempts reached. Manual intervention needed.")
            sys.exit(1)


if __name__ == "__main__":
    main()
