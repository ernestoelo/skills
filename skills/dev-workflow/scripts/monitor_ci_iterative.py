#!/usr/bin/env python3
"""
Automated CI/CD Monitoring and Iterative Correction Script for dev-workflow.

Monitors GitHub Actions workflows post-commit, verifies success, and applies
iterative corrections until CI/CD converges. Generic and portable across repositories.

Usage: python3 monitor_ci_iterative.py --workflow <workflow_name> --max-attempts <n>

Requirements: gh CLI, GITHUB_TOKEN, Python libraries (subprocess, json, os, time)
Integrates with @sys-env for dependencies, @architect for structure, @mcp-builder for API integration.
"""

import subprocess
import sys
import json
import os
import time


def check_dependencies():
    """Check and install missing dependencies (gh CLI, token) using @sys-env patterns."""
    # Check gh
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("GitHub CLI (gh) not found. Installing via @sys-env...")
        # Use sys-env install_package.py if available
        try:
            subprocess.run(
                ["python3", "sys-env/scripts/install_package.py", "github-cli"],
                check=True,
            )
        except FileNotFoundError:
            print(
                "sys-env not available. Please install gh manually: https://cli.github.com/"
            )
            sys.exit(1)

    # Check token
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        print(
            "GITHUB_TOKEN or GH_TOKEN not set. Please configure in environment or secrets."
        )
        sys.exit(1)


def get_commit_sha():
    """Get current commit SHA."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def wait_for_workflow_run(workflow_name, commit_sha, timeout=600):
    """Wait for workflow run matching commit SHA to appear and complete."""
    print(f"Monitoring workflow '{workflow_name}' for commit {commit_sha[:8]}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            result = subprocess.run(
                [
                    "gh",
                    "run",
                    "list",
                    "--workflow",
                    workflow_name,
                    "--json",
                    "status,conclusion,headSha,databaseId",
                    "--limit",
                    "10",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            runs = json.loads(result.stdout)
            for run in runs:
                if run.get("headSha") == commit_sha:
                    status = run["status"]
                    conclusion = run.get("conclusion")
                    run_id = run["databaseId"]
                    if status == "completed":
                        return conclusion, run_id
                    elif status in ["in_progress", "queued"]:
                        print(f"Workflow in progress... ({status})")
                        time.sleep(30)
                        break  # Continue polling
                    else:
                        print(f"Workflow status: {status}")
                        time.sleep(10)
            else:
                print("No matching workflow run found yet, waiting...")
                time.sleep(10)
        except subprocess.CalledProcessError as e:
            print(f"Error checking workflow: {e}")
            time.sleep(10)
    print("Timeout waiting for workflow run.")
    return None, None


def fetch_logs_on_failure(run_id):
    """Fetch logs if failure occurred."""
    try:
        subprocess.run(["gh", "run", "view", str(run_id), "--log"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to fetch logs.")


def detect_error_type():
    """Detect error type from logs (placeholder: expand with log parsing)."""
    # TODO: Parse logs for YAML, linting, test, build errors
    # For now, assume linting as example
    return "linting"


def apply_correction(error_type, attempt):
    """Apply correction using auto_correct_portable.py or direct fixes."""
    print(f"Applying correction for {error_type} (attempt {attempt})...")
    try:
        # Call auto_correct_portable.py or implement fixes here
        subprocess.run(
            [
                "python3",
                "scripts/auto_correct_portable.py",
                "--workflow",
                sys.argv[2],  # Reuse workflow name
            ],
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def re_commit_and_push():
    """Stage, commit, push changes."""
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "fix: auto-correct CI issues"], check=True)
    subprocess.run(["git", "push"], check=True)
    # Return new SHA
    return get_commit_sha()


def main():
    if (
        len(sys.argv) < 5
        or sys.argv[1] != "--workflow"
        or sys.argv[3] != "--max-attempts"
    ):
        print(
            "Usage: python3 monitor_ci_iterative.py --workflow <workflow_name> --max-attempts <n>"
        )
        sys.exit(1)

    workflow_name = sys.argv[2]
    max_attempts = int(sys.argv[4])

    check_dependencies()
    commit_sha = get_commit_sha()
    print(f"Starting monitoring for commit {commit_sha[:8]}")

    for attempt in range(1, max_attempts + 1):
        conclusion, run_id = wait_for_workflow_run(workflow_name, commit_sha)
        if conclusion == "success":
            print(f"✅ CI converged successfully on attempt {attempt}")
            break
        elif conclusion == "failure":
            print(f"❌ CI failed on attempt {attempt}. Fetching logs...")
            fetch_logs_on_failure(run_id)
            error_type = detect_error_type()
            if apply_correction(error_type, attempt):
                new_sha = re_commit_and_push()
                commit_sha = new_sha  # Monitor new commit
                print(f"Re-committed as {new_sha[:8]}. Continuing monitoring...")
            else:
                print(f"No correction available for {error_type}.")
        else:
            print(f"Unexpected conclusion: {conclusion}")

        if attempt == max_attempts:
            print("❌ Max attempts reached. Manual intervention required.")
            sys.exit(1)


if __name__ == "__main__":
    main()
