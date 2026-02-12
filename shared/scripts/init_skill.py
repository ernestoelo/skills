#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template.

Usage:
    init_skill.py <skill-name> --path <path>

Examples:
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private
    init_skill.py custom-skill --path /custom/location
"""

import argparse
import shutil
import sys
from pathlib import Path
import subprocess

# Ensure sibling modules are importable regardless of CWD
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import NAME_MAX_LENGTH, NAME_REGEX
from quick_validate import validate_skill


SKILL_TEMPLATE = """---
name: {skill_name}
description: "TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it."
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Common patterns:

**1. Workflow-Based** (best for sequential processes)
- Works well when there are clear step-by-step procedures
- Example: DOCX skill with "Workflow Decision Tree" → "Reading" → "Creating" → "Editing"
- Structure: ## Overview → ## Workflow Decision Tree → ## Step 1 → ## Step 2...

**2. Task-Based** (best for tool collections)
- Works well when the skill offers different operations/capabilities
- Example: PDF skill with "Quick Start" → "Merge PDFs" → "Split PDFs" → "Extract Text"
- Structure: ## Overview → ## Quick Start → ## Task Category 1 → ## Task Category 2...

**3. Reference/Guidelines** (best for standards or specifications)
- Works well for brand guidelines, coding standards, or requirements
- Example: Brand styling with "Brand Guidelines" → "Colors" → "Typography" → "Features"
- Structure: ## Overview → ## Guidelines → ## Specifications → ## Usage...

**4. Capabilities-Based** (best for integrated systems)
- Works well when the skill provides multiple interrelated features
- Example: Product Management with "Core Capabilities" → numbered capability list
- Structure: ## Overview → ## Core Capabilities → ### 1. Feature → ### 2. Feature...

Patterns can be mixed and matched as needed. Most skills combine patterns (e.g., start with task-based, add workflow for complex operations).

Delete this entire "Structuring This Skill" section when done - it's just guidance.]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. See examples in existing skills:
- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic user requests
- References to scripts/templates/references as needed]

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

This is a placeholder script that can be executed directly.
Replace with actual implementation or delete if not needed.

Example real scripts from other skills:
- pdf/scripts/fill_fillable_fields.py - Fills PDF form fields
- pdf/scripts/convert_pdf_to_images.py - Converts PDF pages to images
"""

def main():
    print("This is an example script for {skill_name}")
    # TODO: Add actual script logic here
    # This could be data processing, file conversion, API calls, etc.

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Documentation for {skill_title}

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.

Example real reference docs from other skills:
- product-management/references/communication.md - Comprehensive guide for status updates
- product-management/references/context_building.md - Deep-dive on gathering context
- bigquery/references/ - API references and query examples

## When Reference Docs Are Useful

Reference docs are ideal for:
- Comprehensive API documentation
- Detailed workflow guides
- Complex multi-step processes
- Information too lengthy for main SKILL.md
- Content that's only needed for specific use cases

## Structure Suggestions

### API Reference Example
- Overview
- Authentication
- Endpoints with examples
- Error codes
- Rate limits

### Workflow Guide Example
- Prerequisites
- Step-by-step instructions
- Common patterns
- Troubleshooting
- Best practices
"""

EXAMPLE_ASSET = """# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files (templates, images, fonts, etc.) or delete if not needed.

Asset files are NOT intended to be loaded into context, but rather used within
the output Claude produces.

Example asset files from other skills:
- Brand guidelines: logo.png, slides_template.pptx
- Frontend builder: hello-world/ directory with HTML/React boilerplate
- Typography: custom-font.ttf, font-family.woff2
- Data: sample_data.csv, test_dataset.json

## Common Asset Types

- Templates: .pptx, .docx, boilerplate directories
- Images: .png, .jpg, .svg, .gif
- Fonts: .ttf, .otf, .woff, .woff2
- Boilerplate code: Project directories, starter files
- Icons: .ico, .svg
- Data files: .csv, .json, .xml, .yaml

Note: This is a text placeholder. Actual assets can be any file type.
"""


def title_case_skill_name(skill_name: str) -> str:
    """Convert hyphenated skill name to Title Case for display."""
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def _validate_name_early(skill_name: str) -> str | None:
    """Return an error string if *skill_name* is invalid, else None."""
    if not skill_name:
        return "Skill name cannot be empty."
    if not NAME_REGEX.match(skill_name):
        return (
            f"Invalid name '{skill_name}'. "
            "Must be hyphen-case (lowercase letters, digits, and hyphens only)."
        )
    if len(skill_name) > NAME_MAX_LENGTH:
        return (
            f"Name is too long ({len(skill_name)} chars). "
            f"Maximum is {NAME_MAX_LENGTH} characters."
        )
    return None


def init_skill(skill_name: str, path: str, apply_dev_workflow: bool = False):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill (kebab-case).
        path: Parent directory where the skill directory will be created.

    Returns:
        Path to created skill directory, or None on error.
    """
    # Pre-creation name validation
    err = _validate_name_early(skill_name)
    if err:
        print(f"❌ {err}")
        return None

    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    # Create the directory tree — on ANY failure we clean up
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created skill directory: {skill_dir}")

        # SKILL.md
        skill_title = title_case_skill_name(skill_name)
        skill_content = SKILL_TEMPLATE.format(
            skill_name=skill_name,
            skill_title=skill_title,
        )
        (skill_dir / "SKILL.md").write_text(skill_content)
        print("✅ Created SKILL.md")

        # scripts/
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir()
        example_script = scripts_dir / "example.py"
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("✅ Created scripts/example.py")

        # references/
        references_dir = skill_dir / "references"
        references_dir.mkdir()
        (references_dir / "api-reference.md").write_text(
            EXAMPLE_REFERENCE.format(skill_title=skill_title),
        )
        print("✅ Created references/api-reference.md")

        # assets/
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir()
        (assets_dir / "example-asset.txt").write_text(EXAMPLE_ASSET)
        print("✅ Created assets/example-asset.txt")

    except Exception as exc:
        print(f"❌ Error during initialization: {exc}")
        # Clean up partial directory on failure
        if skill_dir.exists():
            shutil.rmtree(skill_dir, ignore_errors=True)
            print(f"🗑  Cleaned up partial directory: {skill_dir}")
        return None

    # Post-creation validation
    print(f"\n✅ Skill '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete the TODO items and update the description")
    print(
        "2. Customize or delete the example files in scripts/, references/, and assets/"
    )
    print("3. Automatically running validation to check the skill structure...")

    print("\nRunning validation...")
    try:
        valid, message = validate_skill(skill_dir)
        print(message)
        if not valid:
            print(
                "\n❌ Validation failed. Review the issues above and fix them before proceeding."
            )
            print(f"   Revalidate: python3 scripts/quick_validate.py {skill_dir}")
            return None
        print("\n✅ Validation passed successfully. Skill is ready to use.")
    except Exception as exc:
        print(f"❌ Error while running validation: {exc}")
        return None

    if apply_dev_workflow:
        print("\n🔧 Applying dev-workflow...")
        try:
            # Run auto-correct
            subprocess.run(
                [
                    "python3",
                    "dev-workflow/scripts/auto_correct_portable.py",
                    "--workflow",
                    "Skill Validation CI",
                ],
                check=True,
                cwd=skill_dir.parent.parent,
            )

            # Git operations
            subprocess.run(["git", "add", "."], check=True, cwd=skill_dir.parent.parent)
            subprocess.run(
                ["git", "commit", "-m", f"feat: add {skill_name} skill"],
                check=True,
                cwd=skill_dir.parent.parent,
            )
            subprocess.run(["git", "push"], check=True, cwd=skill_dir.parent.parent)

            print(
                "✅ Dev-workflow applied successfully: validated, committed, and pushed."
            )
        except subprocess.CalledProcessError as exc:
            print(f"❌ Dev-workflow failed: {exc}")
            return None

    return skill_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Initialize a new skill directory from template.",
    )
    parser.add_argument(
        "skill_name",
        help="Kebab-case skill name (e.g. 'data-analyzer')",
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Parent directory where the skill folder will be created",
    )
    parser.add_argument(
        "--apply-dev-workflow",
        action="store_true",
        help="Apply dev-workflow: validate, commit, push after creation",
    )
    args = parser.parse_args()

    print(f"🚀 Initializing skill: {args.skill_name}")
    print(f"   Location: {args.path}")
    print()

    result = init_skill(args.skill_name, args.path, args.apply_dev_workflow)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
