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


def verify_ci_after_push(workflow_name, timeout=300):
    """Verify CI status after push, wait up to timeout seconds."""
    import time

    print(f"Verifying CI status for '{workflow_name}' after push...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        status, conclusion = get_last_run_status(workflow_name)
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
                re_commit()
                if not verify_ci_after_push(workflow_name):
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
