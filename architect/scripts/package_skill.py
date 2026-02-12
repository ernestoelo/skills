#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable .skill file of a skill folder

Usage:
    python package_skill.py <path/to/skill-folder> [output-directory]

Example:
    python package_skill.py skills/public/my-skill
    python package_skill.py skills/public/my-skill ./dist
"""

import sys
import zipfile
from pathlib import Path
from quick_validate import validate_skill

# ...rest of the script as in skill-creator/scripts/package_skill.py
