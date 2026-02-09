"""
Tests for the skill validator (scripts/quick_validate.py).

Fixture layout::

    tests/validator/
    ├── failing-skills/        # Each subdirectory must FAIL validation
    │   ├── angle-brackets-in-desc/
    │   ├── consecutive-hyphens/
    │   ├── duplicate-skill/
    │   ├── duplicate-skill-copy/
    │   ├── empty-description/
    │   ├── empty-name/
    │   ├── empty-skill-md/
    │   ├── invalid-name-uppercase/
    │   ├── name-mismatch/
    │   ├── name-too-long/
    │   ├── truly-missing-skill-md/
    │   └── unexpected-key/
    └── passing-skills/        # Each subdirectory must PASS validation
        ├── crlf-frontmatter/
        └── valid-skill/
"""

import os
import subprocess
import sys

import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
FAILING_SKILLS_DIR = os.path.join(BASE_DIR, "failing-skills")
PASSING_SKILLS_DIR = os.path.join(BASE_DIR, "passing-skills")
QUICK_VALIDATE = os.path.join(REPO_ROOT, "scripts", "quick_validate.py")


def _collect_fixtures(base_dir: str) -> list[str]:
    """Return sorted list of subdirectory names inside *base_dir*."""
    return sorted(
        name
        for name in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, name))
    )


# Collect at import time so parametrize has the ids
FAILING_SKILLS = _collect_fixtures(FAILING_SKILLS_DIR)
PASSING_SKILLS = _collect_fixtures(PASSING_SKILLS_DIR)


def run_validation(skill_dir: str):
    """Run the validator script on a skill directory."""
    result = subprocess.run(
        [sys.executable, QUICK_VALIDATE, skill_dir],
        capture_output=True,
        text=True,
        check=False,
        cwd=REPO_ROOT,
    )
    return result.returncode, result.stdout, result.stderr


# ---------------------------------------------------------------------------
# Parametrized tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("skill", FAILING_SKILLS)
def test_failing_skill(skill: str):
    """Skill fixture in failing-skills/ must fail validation."""
    skill_path = os.path.join(FAILING_SKILLS_DIR, skill)
    returncode, stdout, stderr = run_validation(skill_path)
    assert returncode != 0, (
        f"Skill '{skill}' should fail validation, but it passed.\n"
        f"STDOUT: {stdout}\nSTDERR: {stderr}"
    )


@pytest.mark.parametrize("skill", PASSING_SKILLS)
def test_passing_skill(skill: str):
    """Skill fixture in passing-skills/ must pass validation."""
    skill_path = os.path.join(PASSING_SKILLS_DIR, skill)
    returncode, stdout, stderr = run_validation(skill_path)
    assert returncode == 0, (
        f"Skill '{skill}' should pass validation, but it failed.\n"
        f"STDOUT: {stdout}\nSTDERR: {stderr}"
    )
