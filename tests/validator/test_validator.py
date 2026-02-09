import os
import subprocess
import pytest

# Define paths based on __file__ for portability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
FAILING_SKILLS_DIR = os.path.join(BASE_DIR, "failing-skills")
PASSING_SKILLS_DIR = os.path.join(BASE_DIR, "passing-skills")
QUICK_VALIDATE = os.path.join(REPO_ROOT, "scripts", "quick_validate.py")


def run_validation(skill_dir):
    """Run the validator script on a skill directory."""
    result = subprocess.run(
        ["python3", QUICK_VALIDATE, skill_dir],
        capture_output=True,
        text=True,
        check=False,
        cwd=REPO_ROOT,
    )
    return result.returncode, result.stdout, result.stderr


def test_failing_skills():
    """Each skill in failing-skills/ must fail validation."""
    for skill in sorted(os.listdir(FAILING_SKILLS_DIR)):
        skill_path = os.path.join(FAILING_SKILLS_DIR, skill)
        if os.path.isdir(skill_path):
            returncode, stdout, stderr = run_validation(skill_path)
            assert returncode != 0, (
                f"Skill '{skill}' should fail validation, but it passed.\n"
                f"STDOUT: {stdout}\nSTDERR: {stderr}"
            )


def test_passing_skills():
    """Each skill in passing-skills/ must pass validation."""
    for skill in sorted(os.listdir(PASSING_SKILLS_DIR)):
        skill_path = os.path.join(PASSING_SKILLS_DIR, skill)
        if os.path.isdir(skill_path):
            returncode, stdout, stderr = run_validation(skill_path)
            assert returncode == 0, (
                f"Skill '{skill}' should pass validation, but it failed.\n"
                f"STDOUT: {stdout}\nSTDERR: {stderr}"
            )
