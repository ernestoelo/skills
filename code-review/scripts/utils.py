#!/usr/bin/env python3
"""
Utility functions for code-review skill

Helper functions for language detection, tool integration, and common operations.
"""

import os
import subprocess
from pathlib import Path


def detect_language(file_path):
    """Detect programming language from file extension"""
    ext = Path(file_path).suffix.lower()
    lang_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".go": "go",
        ".rs": "rust",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".h": "c",
    }
    return lang_map.get(ext, "unknown")


def is_tool_available(tool_name):
    """Check if a command-line tool is available"""
    try:
        subprocess.run([tool_name, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_file_size_mb(file_path):
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)


def count_lines_of_code(file_path):
    """Count lines of code in a file (excluding comments and blank lines)"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        code_lines = 0
        for line in lines:
            stripped = line.strip()
            if (
                stripped
                and not stripped.startswith("#")
                and not stripped.startswith("//")
            ):
                code_lines += 1
        return code_lines
    except Exception:
        return 0


def calculate_complexity(file_path, lang):
    """Calculate cyclomatic complexity (basic implementation)"""
    if lang != "python":
        return 0

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        # Very basic complexity calculation
        complexity = 1  # Base complexity
        complexity += content.count("if ")
        complexity += content.count("elif ")
        complexity += content.count("for ")
        complexity += content.count("while ")
        complexity += content.count("try:")
        complexity += content.count("except ")
        return complexity
    except Exception:
        return 0
