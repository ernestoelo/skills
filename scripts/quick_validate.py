#!/usr/bin/env python3
"""
Quick validation script for skills.

Validates SKILL.md frontmatter, naming conventions, and detects
duplicate skill names across sibling directories.
"""

import argparse
import re
import sys
import yaml
from pathlib import Path

# Ensure sibling modules are importable regardless of CWD
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import (
    ALLOWED_PROPERTIES,
    DESCRIPTION_MAX_LENGTH,
    NAME_MAX_LENGTH,
    NAME_REGEX,
    REQUIRED_FIELDS,
)


# ---------------------------------------------------------------------------
# Pure validation helpers — each returns (ok: bool, error_message: str | None)
# ---------------------------------------------------------------------------


def parse_frontmatter(content: str) -> tuple[dict | None, str | None]:
    """Extract and parse YAML frontmatter from SKILL.md content.

    Tolerates both ``\\n`` and ``\\r\\n`` line endings.

    Returns:
        (frontmatter_dict, None) on success, or (None, error_message) on failure.
    """
    # Normalise to \n so the regex stays simple
    content = content.replace("\r\n", "\n")

    if not content.startswith("---"):
        return None, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, "Invalid frontmatter format"

    try:
        frontmatter = yaml.safe_load(match.group(1))
        if not isinstance(frontmatter, dict):
            return None, "Frontmatter must be a YAML dictionary"
        return frontmatter, None
    except yaml.YAMLError as exc:
        return None, f"Invalid YAML in frontmatter: {exc}"


def validate_frontmatter_schema(frontmatter: dict) -> tuple[bool, str | None]:
    """Check required keys and reject unexpected keys."""
    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            return False, f"Missing '{field}' in frontmatter"

    return True, None


def validate_name(name, dir_name: str | None = None) -> tuple[bool, str | None]:
    """Validate the ``name`` field value.

    If *dir_name* is supplied the name must also match the directory.
    """
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"

    name = name.strip()
    if not name:
        return False, "Name cannot be empty"

    if not NAME_REGEX.match(name):
        return False, (
            f"Name '{name}' should be hyphen-case "
            "(lowercase letters, digits, and hyphens only)"
        )

    if len(name) > NAME_MAX_LENGTH:
        return False, (
            f"Name is too long ({len(name)} characters). "
            f"Maximum is {NAME_MAX_LENGTH} characters."
        )

    if dir_name is not None and name != dir_name:
        return False, (
            f"Name '{name}' does not match directory name '{dir_name}'. "
            "The frontmatter 'name' must match the skill directory name exactly."
        )

    return True, None


def validate_description(description) -> tuple[bool, str | None]:
    """Validate the ``description`` field value."""
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"

    description = description.strip()
    if not description:
        return False, "Description cannot be empty"

    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets (< or >)"

    if len(description) > DESCRIPTION_MAX_LENGTH:
        return False, (
            f"Description is too long ({len(description)} characters). "
            f"Maximum is {DESCRIPTION_MAX_LENGTH} characters."
        )

    return True, None


def check_duplicates(skill_path: Path, name: str) -> tuple[bool, str | None]:
    """Detect duplicate ``name`` values across sibling skill directories."""
    skills_root = skill_path.parent
    for other_dir in skills_root.iterdir():
        if not other_dir.is_dir() or other_dir == skill_path:
            continue
        other_skill_md = other_dir / "SKILL.md"
        if not other_skill_md.exists():
            continue
        try:
            other_content = other_skill_md.read_text(encoding="utf-8")
        except OSError:
            continue
        other_fm, _ = parse_frontmatter(other_content)
        if other_fm is None:
            continue
        if isinstance(other_fm, dict) and other_fm.get("name") == name:
            return False, f"Duplicate skill name conflict with '{other_dir.name}'"

    return True, None


# ---------------------------------------------------------------------------
# High-level entry point
# ---------------------------------------------------------------------------


def validate_skill(skill_path) -> tuple[bool, str]:
    """Validate a skill's structure and metadata.

    Returns:
        (True, "Skill is valid!") or (False, error_message).
    """
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read content with error handling
    try:
        content = skill_md.read_text(encoding="utf-8")
    except OSError as exc:
        return False, f"Cannot read SKILL.md: {exc}"

    # Parse frontmatter
    frontmatter, err = parse_frontmatter(content)
    if frontmatter is None:
        return False, err  # type: ignore[return-value]

    # Schema check
    ok, err = validate_frontmatter_schema(frontmatter)
    if not ok:
        return False, err  # type: ignore[return-value]

    # Name
    dir_name = skill_path.resolve().name
    ok, err = validate_name(frontmatter.get("name", ""), dir_name=dir_name)
    if not ok:
        return False, err  # type: ignore[return-value]

    # Description
    ok, err = validate_description(frontmatter.get("description", ""))
    if not ok:
        return False, err  # type: ignore[return-value]

    # Duplicates
    name = frontmatter["name"].strip()
    ok, err = check_duplicates(skill_path, name)
    if not ok:
        return False, err  # type: ignore[return-value]

    return True, "Skill is valid!"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a skill directory's SKILL.md frontmatter and structure.",
    )
    parser.add_argument(
        "skill_directory",
        help="Path to the skill directory to validate",
    )
    args = parser.parse_args()

    valid, message = validate_skill(args.skill_directory)
    print(message)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
