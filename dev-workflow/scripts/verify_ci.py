#!/usr/bin/env python3
"""
Portable CI verification script for dev-workflow.

Verifies the status of the latest CI run for a given workflow after git operations.
Generic for any repository with GitHub Actions.

Usage: python3 verify_ci.py --workflow <workflow_name>
Example: python3 verify_ci.py --workflow "Validate Skills"
"""

import subprocess
import sys
import json
import os
import time


def check_dependencies():
    """Check for gh CLI and GITHUB_TOKEN."""
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("GitHub CLI (gh) not found. Install manually or run in CI environment.")
        sys.exit(1)

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set. Set in environment or GitHub secrets.")
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


def verify_ci(workflow_name, timeout=300):
    """Verify CI status, wait up to timeout seconds."""
    print(f"Verifying CI for '{workflow_name}'...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        status, conclusion = get_last_run_status(workflow_name)
        if status == "completed":
            if conclusion == "success":
                print("✅ CI verification: SUCCESS")
                return True
            else:
                print(f"❌ CI verification: FAILED (conclusion: {conclusion})")
                print("Run `gh run view <id> --log` for details.")
                return False
        elif status in ["in_progress", "queued"]:
            print("CI in progress, waiting...")
            time.sleep(10)
        else:
            print(f"CI status unknown: {status}, waiting...")
            time.sleep(10)
    print("⏰ CI verification timeout.")
    return False


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--workflow":
        print("Usage: python3 verify_ci.py --workflow <workflow_name>")
        sys.exit(1)

    workflow_name = sys.argv[2]

    check_dependencies()
    success = verify_ci(workflow_name)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
