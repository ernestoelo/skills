#!/usr/bin/env python3
"""
Quick validation script for skills with dependency checks
"""

import sys
import os
import re
import yaml
from pathlib import Path


def validate_skill(skill_path):
    """Enhanced validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Define allowed properties
    ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (hyphen-case: lowercase with hyphens)
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
            )
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return (
                False,
                f"Name is too long ({len(name)} characters). Maximum is 64 characters.",
            )

    # Context conflict detection (e.g., duplicate names)
    skills_root = skill_path.parent
    all_skill_dirs = [d for d in skills_root.iterdir() if d.is_dir()]
    duplicate_skill_dirs = [
        d for d in all_skill_dirs if d != skill_path and (d / "SKILL.md").exists()
    ]

    for other_skill_dir in duplicate_skill_dirs:
        other_skill = yaml.safe_load(
            (other_skill_dir / "SKILL.md").read_text().split("---")[1]
        )
        if other_skill["name"] == name:
            return False, f"Duplicate skill name conflict with '{other_skill_dir}'"

    # Check for script dependencies
    # Validate external dependencies and local paths
    def validate_external_dependencies(script_path):
        """
        Inspects a script to detect external imports or file references.
        """
        detected_issues = []
        with script_path.open() as script:
            for line in script:
                # Check for Python imports as an example
                if line.startswith("import") or line.startswith("from"):
                    module_name = line.split()[1].split(".")[0]
                    if not module_name in sys.modules and not module_name in globals():
                        detected_issues.append(f"Missing module: {module_name}")

                # Check for file references (e.g., ../ or ./)
                if "../" in line or "./" in line:
                    match = re.search(r"(\.\.\/[\w\-\/\.]+|\.\/[\w\-\/\.]+)", line)
                    if match:
                        file_ref = (skill_path / match.group(1)).resolve()
                        if not file_ref.exists():
                            detected_issues.append(
                                f"Invalid file reference: {file_ref}"
                            )
        return detected_issues

    scripts_dir = skill_path / "scripts"
    issues = []
    if scripts_dir.exists():
        for script_file in scripts_dir.iterdir():
            if script_file.is_file():
                dependencies_issues = validate_external_dependencies(script_file)
                issues.extend(dependencies_issues)

    if issues:
        return False, f"Dependency verification failed: {', '.join(issues)}"
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        unused_scripts = []
        for f in scripts_dir.iterdir():
            if f.is_file():
                with f.open() as file:
                    if not any(line.strip() for line in file):
                        unused_scripts.append(f)
        if unused_scripts:
            return (
                False,
                f"Unused or empty scripts detected: {', '.join([str(s.name) for s in unused_scripts])}",
            )

    # Validate references
    references_dir = skill_path / "references"
    if references_dir.exists():
        ref_files = [f for f in references_dir.iterdir() if f.is_file()]
        for ref_file in ref_files:
            # Check for broken or missing references
            with ref_file.open() as rf:
                if "TODO" in rf.read():
                    return False, f"Unresolved 'TODO' in reference: {ref_file.name}"

    # Final step: validate description
    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return (
                False,
                f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
            )

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
