#!/usr/bin/env python3
"""
Code Review Analysis Script

Analyzes code files for various issues including linting, security, and performance.
Supports multiple programming languages and integrates with CI/CD pipelines.

Usage:
    python3 analyze.py <file_or_dir> [options]

Options:
    --language LANG    Specify language (auto-detected if not provided)
    --check TYPE       Check type: lint, security, performance, all (default: all)
    --dir              Treat input as directory (recursive analysis)
    --ci               CI mode: exit with error code on issues, suppress verbose output
    --fix              Attempt auto-fixes where possible (experimental)
    --output FORMAT    Output format: text, json (default: text)
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
import re
import yaml
import fnmatch


class CodeAnalyzer:
    def __init__(
        self, language=None, check_types=None, ci_mode=False, output_format="text"
    ):
        self.language = language
        self.check_types = check_types or ["lint", "security", "performance"]
        self.ci_mode = ci_mode
        self.output_format = output_format
        self.issues = []
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from .code-review.yml"""
        config_paths = [
            Path(__file__).parent.parent / ".code-review.yml",  # skill dir
            Path.cwd() / ".code-review.yml",  # project root
        ]
        for path in config_paths:
            if path.exists():
                try:
                    with open(path, "r") as f:
                        return yaml.safe_load(f)
                except Exception:
                    pass
        return {}  # default empty config

    def detect_language(self, file_path):
        """Auto-detect programming language from file extension"""
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
        }
        return lang_map.get(ext, "unknown")

    def run_command(self, cmd, cwd=None):
        """Run a command and return output"""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, cwd=cwd
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)

    def analyze_file(self, file_path):
        """Analyze a single file"""
        if not os.path.exists(file_path):
            self.add_issue("error", f"File not found: {file_path}")
            return

        lang = self.language or self.detect_language(file_path)
        if lang == "unknown":
            self.add_issue("warning", f"Unknown language for file: {file_path}")
            return

        if "lint" in self.check_types:
            self.run_linting(file_path, lang)
        if "security" in self.check_types:
            self.run_security_check(file_path, lang)
        if "performance" in self.check_types:
            self.run_performance_check(file_path, lang)

    def run_linting(self, file_path, lang):
        """Run linting checks"""
        if lang == "python":
            self._check_python_lint(file_path)
        elif lang in ["javascript", "typescript"]:
            self._check_js_lint(file_path)
        # Add more languages as needed

    def _check_python_lint(self, file_path):
        """Python linting with pylint/flake8"""
        # Try pylint first
        code, out, err = self.run_command(
            f"pylint --output-format=parseable {file_path}"
        )
        if code == 0:
            pass  # No issues
        else:
            for line in (out + err).split("\n"):
                if ": " in line and file_path in line:
                    parts = line.split(":")
                    if len(parts) >= 4:
                        severity = "error" if "error" in line.lower() else "warning"
                        msg = ":".join(parts[3:]).strip()
                        self.add_issue(
                            severity,
                            f"Lint: {msg}",
                            file_path,
                            int(parts[1]) if parts[1].isdigit() else None,
                        )

        # Try flake8
        code, out, err = self.run_command(f"flake8 {file_path}")
        for line in (out + err).split("\n"):
            if ":" in line and len(line.split(":")) >= 4:
                parts = line.split(":")
                severity = "warning"  # flake8 typically warnings
                msg = ":".join(parts[3:]).strip()
                self.add_issue(
                    severity,
                    f"Flake8: {msg}",
                    file_path,
                    int(parts[1]) if parts[1].isdigit() else None,
                )

    def _check_js_lint(self, file_path):
        """JavaScript/TypeScript linting"""
        # Try eslint
        code, out, err = self.run_command(f"npx eslint {file_path} --format=compact")
        for line in (out + err).split("\n"):
            if "error" in line or "warning" in line:
                self.add_issue(
                    "warning" if "warning" in line else "error",
                    f"ESLint: {line}",
                    file_path,
                )

    def run_security_check(self, file_path, lang):
        """Run security vulnerability checks"""
        if lang == "python":
            self._check_python_security(file_path)

    def _check_python_security(self, file_path):
        """Python security with bandit"""
        code, out, err = self.run_command(f"bandit -f json {file_path}")
        if code != 0:
            try:
                results = json.loads(out)
                for issue in results.get("results", []):
                    severity = issue.get("issue_severity", "medium").lower()
                    msg = issue.get("issue_text", "")
                    self.add_issue(
                        severity,
                        f"Security: {msg}",
                        file_path,
                        issue.get("line_number"),
                    )
            except Exception:
                self.add_issue("warning", f"Security check failed for {file_path}")

    def run_performance_check(self, file_path, lang):
        """Run performance analysis"""
        if lang == "python":
            self._check_python_performance(file_path)

    def _check_python_performance(self, file_path):
        """Basic Python performance checks"""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Check for inefficient patterns
        if re.search(r"for.*in.*range\(len\(", content):
            self.add_issue(
                "warning",
                "Performance: Use enumerate() instead of range(len())",
                file_path,
            )

        # Check for nested loops
        if content.count("for ") > 3:  # Rough heuristic
            self.add_issue(
                "info", "Performance: Consider optimizing nested loops", file_path
            )

    def add_issue(self, severity, message, file_path=None, line=None):
        """Add an issue to the results"""
        issue = {
            "severity": severity,
            "message": message,
            "file": file_path,
            "line": line,
        }
        self.issues.append(issue)

    def analyze_directory(self, dir_path):
        """Analyze all files in directory recursively"""
        exclusions = self.config.get("exclusions", {}).get(
            "files", []
        ) + self.config.get("exclusions", {}).get("directories", [])

        for root, dirs, files in os.walk(dir_path):
            # Skip excluded directories
            dirs[:] = [
                d
                for d in dirs
                if not any(fnmatch.fnmatch(d, excl) or d == excl for excl in exclusions)
            ]

            for file in files:
                file_path = os.path.join(root, file)
                # Skip excluded files
                if any(fnmatch.fnmatch(file_path, excl) for excl in exclusions):
                    continue

                if file.endswith(
                    (".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".c", ".h")
                ):
                    self.analyze_file(file_path)

    def generate_output(self):
        """Generate formatted output"""
        if self.output_format == "json":
            return json.dumps({"issues": self.issues}, indent=2)

        if not self.issues:
            return "✅ No issues found"

        output = []
        for issue in self.issues:
            severity_icon = {
                "error": "❌",
                "warning": "⚠️",
                "info": "ℹ️",
                "medium": "🟡",
                "high": "🔴",
                "low": "🟢",
            }.get(issue["severity"], "❓")

            line_info = f":{issue['line']}" if issue["line"] else ""
            file_info = f" in {issue['file']}{line_info}" if issue["file"] else ""
            output.append(
                f"{severity_icon} {issue['severity'].title()}: {issue['message']}{file_info}"
            )

        return "\n".join(output)

    def get_exit_code(self):
        """Determine exit code for CI mode"""
        if not self.ci_mode:
            return 0
        errors = [i for i in self.issues if i["severity"] in ["error", "high"]]
        return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description="Code Review Analysis Tool")
    parser.add_argument("path", help="File or directory to analyze")
    parser.add_argument("--language", help="Programming language")
    parser.add_argument(
        "--check",
        choices=["lint", "security", "performance", "all"],
        default="all",
        help="Type of check to perform",
    )
    parser.add_argument("--dir", action="store_true", help="Treat path as directory")
    parser.add_argument("--ci", action="store_true", help="CI mode")
    parser.add_argument(
        "--fix", action="store_true", help="Attempt auto-fixes (experimental)"
    )
    parser.add_argument(
        "--output", choices=["text", "json"], default="text", help="Output format"
    )

    args = parser.parse_args()

    check_types = (
        ["lint", "security", "performance"] if args.check == "all" else [args.check]
    )

    analyzer = CodeAnalyzer(
        language=args.language,
        check_types=check_types,
        ci_mode=args.ci,
        output_format=args.output,
    )

    if args.dir or os.path.isdir(args.path):
        analyzer.analyze_directory(args.path)
    else:
        analyzer.analyze_file(args.path)

    print(analyzer.generate_output())
    sys.exit(analyzer.get_exit_code())


if __name__ == "__main__":
    main()
