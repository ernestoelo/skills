#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable .skill file of a skill folder.

Usage:
    package_skill.py <path/to/skill-folder> [--output <directory>]

Example:
    package_skill.py my-skill
    package_skill.py my-skill --output ./dist
"""

import argparse
import fnmatch
import sys
import zipfile
from pathlib import Path

# Ensure sibling modules are importable regardless of CWD
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import EXCLUDE_PATTERNS
from quick_validate import validate_skill


def _is_excluded(rel_path: Path) -> bool:
    """Return True if *rel_path* matches any exclusion pattern."""
    for pattern in EXCLUDE_PATTERNS:
        # Match against every component of the path and the filename
        for part in rel_path.parts:
            if fnmatch.fnmatch(part, pattern):
                return True
    return False


def package_skill(skill_path, output_dir=None):
    """
    Package a skill folder into a .skill file.

    Args:
        skill_path: Path to the skill folder.
        output_dir: Optional output directory for the .skill file (defaults to cwd).

    Returns:
        Path to the created .skill file, or None on error.
    """
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        return None

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ Error: SKILL.md not found in {skill_path}")
        return None

    # Run validation before packaging
    print("🔍 Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        print("   Please fix the validation errors before packaging.")
        return None
    print(f"✅ {message}\n")

    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.skill"

    try:
        with zipfile.ZipFile(skill_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in skill_path.rglob("*"):
                if not file_path.is_file():
                    continue
                rel = file_path.relative_to(skill_path)
                if _is_excluded(rel):
                    print(f"  Skipped: {rel}")
                    continue
                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")

        print(f"\n✅ Successfully packaged skill to: {skill_filename}")
        return skill_filename

    except Exception as exc:
        print(f"❌ Error creating .skill file: {exc}")
        return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Package a skill folder into a distributable .skill file.",
    )
    parser.add_argument(
        "skill_path",
        help="Path to the skill folder to package",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output directory for the .skill file (defaults to current directory)",
    )
    args = parser.parse_args()

    print(f"📦 Packaging skill: {args.skill_path}")
    if args.output:
        print(f"   Output directory: {args.output}")
    print()

    result = package_skill(args.skill_path, args.output)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
