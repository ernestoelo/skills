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
                "10",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        runs = json.loads(result.stdout)
        if commit_sha:
            relevant_runs = [run for run in runs if run.get("headSha") == commit_sha]
            if relevant_runs:
                run = relevant_runs[0]
                return run["status"], run["conclusion"]
            else:
                return None, None
        else:
            if runs:
                return runs[0]["status"], runs[0]["conclusion"]
        return None, None
    except subprocess.CalledProcessError:
        return None, None


def verify_ci(workflow_name, commit_sha=None, timeout=300):
    """Verify CI status, wait up to timeout seconds. Filters by commit_sha if provided."""
    print(f"Verifying CI for '{workflow_name}'...")
    print("Waiting for CI to process...")
    time.sleep(30)  # Initial wait

    start_time = time.time()
    while time.time() - start_time < timeout:
        status, conclusion = get_last_run_status(workflow_name, commit_sha)
        if status is None:
            print("No CI run found for this commit yet, waiting...")
            time.sleep(10)
            continue
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
    import argparse

    parser = argparse.ArgumentParser(description="Verify CI status for a workflow.")
    parser.add_argument("--workflow", required=True, help="Workflow name")
    parser.add_argument("--commit-sha", help="Commit SHA to filter runs")
    args = parser.parse_args()

    workflow_name = args.workflow
    commit_sha = args.commit_sha

    check_dependencies()
    success = verify_ci(workflow_name, commit_sha)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
