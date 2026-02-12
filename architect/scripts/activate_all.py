#!/usr/bin/env python3
"""
Global skill activation script for OpenCode.

Lists and validates all skills in the repository, ensuring they are ready
for declarative activation in OpenCode conversations. Outputs a summary
of available skills.
"""

import subprocess
import sys
from pathlib import Path


def find_skills(root_path: Path) -> list[Path]:
    """Find all skill directories containing SKILL.md."""
    skills = []
    for item in root_path.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skills.append(item)
    return sorted(skills)


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    """Validate a skill using quick_validate.py."""
    try:
        result = subprocess.run(
            [
                sys.executable,
                str(
                    Path(__file__).parent.parent.parent
                    / "scripts"
                    / "quick_validate.py"
                ),
                str(skill_path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        valid = result.returncode == 0
        message = result.stdout.strip() or result.stderr.strip()
        return valid, message
    except subprocess.TimeoutExpired:
        return False, "Validation timed out"
    except Exception as e:
        return False, f"Validation error: {e}"


def main():
    # Assume script is run from repository root
    repo_root = Path.cwd()
    if not (repo_root / "scripts" / "quick_validate.py").exists():
        print("Error: Not in repository root or quick_validate.py missing")
        sys.exit(1)

    print("🔍 Discovering skills...")
    skills = find_skills(repo_root)
    if not skills:
        print("No skills found.")
        sys.exit(1)

    print(f"Found {len(skills)} skill(s): {', '.join(s.name for s in skills)}")
    print("\n🔧 Validating skills...")

    valid_skills = []
    invalid_skills = []

    for skill in skills:
        valid, message = validate_skill(skill)
        status = "✅" if valid else "❌"
        print(f"{status} {skill.name}: {message}")
        if valid:
            valid_skills.append(skill.name)
        else:
            invalid_skills.append(skill.name)

    print("\n📋 Summary:")
    print(f"Total skills: {len(skills)}")
    print(f"Valid skills: {len(valid_skills)}")
    if valid_skills:
        print(f"Available for activation: {', '.join(valid_skills)}")
    if invalid_skills:
        print(f"Invalid skills (fix before activation): {', '.join(invalid_skills)}")
        sys.exit(1)

    print("\n✨ All skills validated! Ready for OpenCode activation.")


if __name__ == "__main__":
    main()
