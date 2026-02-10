import subprocess
import json
import sys
import os


def fetch_ci_logs(workflow_name, commit_sha=None):
    """Fetch logs from a specific GitHub Actions workflow."""
    try:
        # Check if gh CLI is installed
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("GitHub CLI (gh) not installed. Install from https://cli.github.com/")
        sys.exit(1)

    # Get failed runs
    cmd = [
        "gh",
        "run",
        "list",
        "--workflow",
        workflow_name,
        "--json",
        "status,conclusion,headSha",
    ]
    if commit_sha:
        cmd.extend(["--commit", commit_sha])
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    runs = json.loads(result.stdout)

    failed_runs = [run for run in runs if run.get("conclusion") == "failure"]
    if not failed_runs:
        print(f"No failed runs found for workflow '{workflow_name}'.")
        return

    for run in failed_runs[:1]:  # Limit to latest failed run
        sha = run["headSha"]
        print(f"Fetching logs for failed run on commit {sha}...")
        log_cmd = ["gh", "run", "view", sha, "--log"]
        subprocess.run(log_cmd)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch CI/CD logs from GitHub Actions."
    )
    parser.add_argument(
        "--workflow", required=True, help="Workflow name (e.g., 'Skill Validation CI')"
    )
    parser.add_argument("--commit", help="Specific commit SHA")
    args = parser.parse_args()

    fetch_ci_logs(args.workflow, args.commit)
