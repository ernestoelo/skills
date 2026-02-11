#!/usr/bin/env python3
"""
Setup Validation Script
Valida que el entorno esté correctamente configurado para la integración con OpenCode.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


# Colors for output
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"


def print_status(message: str, status: bool):
    """Print status message with color."""
    color = Colors.GREEN if status else Colors.RED
    symbol = "✅" if status else "❌"
    print(f"{color}{symbol} {message}{Colors.NC}")


def check_command(command: str, description: str) -> bool:
    """Check if a command is available."""
    try:
        subprocess.run([command, "--version"], capture_output=True, check=True)
        print_status(f"{description} available", True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_status(f"{description} not found", False)
        return False


def check_file(file_path: str, description: str) -> bool:
    """Check if a file exists."""
    if os.path.isfile(file_path):
        print_status(f"{description} exists", True)
        return True
    else:
        print_status(f"{description} missing", False)
        return False


def check_directory(dir_path: str, description: str) -> bool:
    """Check if a directory exists."""
    if os.path.isdir(dir_path):
        print_status(f"{description} exists", True)
        return True
    else:
        print_status(f"{description} missing", False)
        return False


def validate_github_auth() -> bool:
    """Validate GitHub authentication."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"], capture_output=True, text=True
        )
        if result.returncode == 0 and "Logged in" in result.stderr:
            print_status("GitHub CLI authenticated", True)
            return True
        else:
            print_status("GitHub CLI not authenticated", False)
            return False
    except Exception:
        print_status("GitHub CLI authentication check failed", False)
        return False


def validate_config_file() -> bool:
    """Validate configuration file."""
    config_path = Path(__file__).parent.parent / "config" / "opencode_config.json"

    if not config_path.exists():
        print_status("Configuration file missing", False)
        return False

    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        # Validate required fields
        required_fields = ["repository", "branch", "commit", "pr"]
        for field in required_fields:
            if field not in config:
                print_status(f"Config missing required field: {field}", False)
                return False

        print_status("Configuration file is valid", True)
        return True

    except json.JSONDecodeError:
        print_status("Configuration file is not valid JSON", False)
        return False


def validate_integration_files() -> bool:
    """Validate that all integration files exist."""
    script_dir = Path(__file__).parent.parent
    project_root = script_dir.parent

    required_files = [
        # Integration files
        "scripts/run_integration.py",
        "core/repository_manager.py",
        "core/change_applier.py",
        "automation/ci_runner.py",
        "automation/pr_creator.py",
        # Project files
        "../types/proactive-loader.ts",
        "../types/skill-modified.ts",
        "../types/config-modified.ts",
        "../types/session-modified.ts",
        "../OPENCODE_PR_README.md",
    ]

    all_valid = True
    for file_path in required_files:
        full_path = script_dir / file_path
        if not full_path.exists():
            print_status(f"Required file missing: {file_path}", False)
            all_valid = False
        else:
            print_status(f"Required file exists: {file_path}", True)

    return all_valid


def check_github_actions_workflow() -> bool:
    """Check if GitHub Actions workflow is configured."""
    workflow_path = (
        Path(__file__).parent.parent.parent
        / ".github"
        / "workflows"
        / "opencode-integration.yml"
    )

    if workflow_path.exists():
        print_status("GitHub Actions workflow configured", True)
        return True
    else:
        print_status("GitHub Actions workflow missing", False)
        return False


def main():
    """Main validation function."""
    print(f"{Colors.BLUE}🔍 Validating OpenCode Integration Setup{Colors.NC}")
    print("=" * 50)

    all_checks_passed = True

    # Check system requirements
    print(f"\n{Colors.BLUE}🔧 System Requirements:{Colors.NC}")
    checks = [
        ("python3", "Python 3"),
        ("git", "Git"),
        ("gh", "GitHub CLI"),
    ]

    for command, description in checks:
        if not check_command(command, description):
            all_checks_passed = False

    # Check GitHub authentication
    print(f"\n{Colors.BLUE}🐙 GitHub Authentication:{Colors.NC}")
    if not validate_github_auth():
        all_checks_passed = False

    # Check file structure
    print(f"\n{Colors.BLUE}📁 File Structure:{Colors.NC}")
    if not validate_integration_files():
        all_checks_passed = False

    # Check configuration
    print(f"\n{Colors.BLUE}⚙️ Configuration:{Colors.NC}")
    if not validate_config_file():
        all_checks_passed = False

    # Check CI/CD
    print(f"\n{Colors.BLUE}🔄 CI/CD:{Colors.NC}")
    if not check_github_actions_workflow():
        all_checks_passed = False

    # Summary
    print(f"\n{Colors.BLUE}📋 Summary:{Colors.NC}")
    if all_checks_passed:
        print(f"{Colors.GREEN}✅ All validation checks passed!{Colors.NC}")
        print("\n🎯 Ready to run integration:")
        print(
            "  python scripts/run_integration.py --target-repo https://github.com/opencode-ai/opencode --changes-dir ../types"
        )
        return 0
    else:
        print(f"{Colors.RED}❌ Some validation checks failed.{Colors.NC}")
        print("\n🔧 Fix the issues above and run validation again:")
        print("  python scripts/validate_setup.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
