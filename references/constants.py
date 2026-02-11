"""
Shared constants for skill validation and scaffolding.

These values are the single source of truth for naming rules,
field limits, and schema definitions used across the tooling.
"""

import re

# --- Naming ---
NAME_REGEX = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX_LENGTH = 64

# --- Description ---
DESCRIPTION_MAX_LENGTH = 1024

# --- Frontmatter schema ---
REQUIRED_FIELDS = {"name", "description"}
ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}

# --- Packaging exclusions ---
EXCLUDE_PATTERNS = {".git", "__pycache__", "*.pyc", ".DS_Store", ".env", "*.swp"}
