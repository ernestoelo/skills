import subprocess
import json


def auto_correct_ci(workflow_name, commit_sha):
    """Auto-correct common CI/CD issues based on workflow name."""
    # Simulate fetching logs (in real implementation, integrate with fetch_ci_logs.py)
    # For demo, assume common errors from dev-workflow context

    common_fixes = {
        "Skill Validation CI": {
            "file too large": lambda: remove_large_files(),
            "YAML validation failed": lambda: fix_yaml_syntax(),
            "missing dependency": lambda: install_missing_deps(),
            "linting error": lambda: fix_linting(),
            "build failure": lambda: fix_build_errors(),
        },
        "Validate Skills": {
            "linting error": lambda: fix_linting(),
            "test failure": lambda: run_tests_locally(),
        },
    }

    if workflow_name not in common_fixes:
        print(f"No auto-corrections available for workflow '{workflow_name}'.")
        return

    # Fetch logs (placeholder - in real, parse output)
    print(f"Analyzing logs for {workflow_name} on commit {commit_sha}...")

    # Apply fixes (example logic)
    for error, fix_func in common_fixes[workflow_name].items():
        if check_error_in_logs(error, workflow_name, commit_sha):
            print(f"Detected error: {error}. Applying fix...")
            if fix_func():
                print("Fix applied. Re-committing...")
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(
                    ["git", "commit", "-m", f"fix: auto-correct {error} from CI"],
                    check=True,
                )
                subprocess.run(["git", "push"], check=True)
                break
            else:
                print("Fix function returned no changes.")
        else:
            print(f"Error '{error}' not detected.")

    # Notify user with GitHub validation link
    notify_validation(workflow_name, commit_sha)


def check_error_in_logs(error, workflow, commit):
    """Check if error is present by running relevant checks."""
    if error == "linting error":
        # Run ruff check to see if there are errors
        result = subprocess.run(
            ["uv", "run", "ruff", "check", "."], capture_output=True, text=True
        )
        if result.returncode != 0 and "F401" in result.stderr:  # Unused import
            return True
    # Add more checks as needed
    return False


def remove_large_files():
    """Remove files >10MB to fix size issues."""
    subprocess.run(["find", ".", "-type", "f", "-size", "+10M", "-delete"], check=True)


def fix_yaml_syntax():
    """Placeholder: Run YAML validator."""
    print("Running YAML fix (manual for now).")


def install_missing_deps():
    """Install missing Python deps."""
    subprocess.run(["uv", "sync"], check=True)


def run_tests_locally():
    """Run tests to fix failures."""
    subprocess.run(["uv", "run", "pytest"], check=True)


def fix_linting():
    """Fix common linting errors."""
    print("Running ruff check --fix...")
    subprocess.run(["uv", "run", "ruff", "check", ".", "--fix"], check=True)
    # Check if there are changes
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    if result.stdout.strip():
        print("Changes detected after linting fix.")
        return True
    else:
        print("No changes after linting fix.")
        return False


def fix_build_errors():
    """Placeholder: Fix build errors (e.g., install build tools)."""
    subprocess.run(["uv", "sync"], check=True)  # Assume deps fix builds


def notify_validation(workflow_name, commit_sha):
    """Notify user with GitHub Actions run link for validation review."""
    try:
        # Get the run URL for the commit
        cmd = [
            "gh",
            "run",
            "list",
            "--workflow",
            workflow_name,
            "--commit",
            commit_sha,
            "--json",
            "url",
            "--limit",
            "1",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        runs = json.loads(result.stdout)
        if runs:
            url = runs[0].get("url")
            print(f"CI/CD validation completed. Review results at: {url}")
        else:
            print("No GitHub run found for the specified commit.")
    except subprocess.CalledProcessError:
        print("Failed to fetch GitHub run URL. Ensure GitHub CLI is authenticated.")
    except json.JSONDecodeError:
        print("Error parsing GitHub CLI output.")
    import argparse

    parser = argparse.ArgumentParser(description="Auto-correct common CI/CD errors.")
    parser.add_argument("--workflow", required=True, help="Workflow name")
    parser.add_argument("--commit", required=True, help="Commit SHA")
    args = parser.parse_args()

    auto_correct_ci(args.workflow, args.commit)
