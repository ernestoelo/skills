---
name: code-review
description: Analyzes code for bugs, style issues, security vulnerabilities, and performance problems, providing AI-powered suggestions for improvements. Use for code quality assurance, PR reviews, and CI integration.
---

# Code Review

## Overview

The `code-review` skill automates code analysis across multiple programming languages, detecting common issues like linting errors, security vulnerabilities, and code smells. It integrates with CI/CD pipelines and provides actionable suggestions to improve code quality and maintainability.

## When to Use the Skill
- **Pull Request Reviews:** Automatically analyze code changes for potential issues before merging.
- **Code Quality Assurance:** Run periodic checks on entire codebases to maintain standards.
- **Security Audits:** Detect vulnerabilities and suggest fixes.
- **Performance Optimization:** Identify inefficient code patterns.
- **CI Integration:** Automate reviews on commits or builds.

## Quick Start
```bash
# Analizar un archivo Python
python3 shared/scripts/analyze.py path/to/file.py

# Analizar un directorio recursivamente
python3 shared/scripts/analyze.py --dir path/to/project --language python

# Solo chequeos de seguridad
python3 shared/scripts/analyze.py path/to/file.py --check security
```

## Code Analysis Tasks

### Linting and Style Checks
Detects code style violations, unused imports, and formatting issues.

**Supported Languages:**
- Python: Uses pylint, flake8, black
- JavaScript/TypeScript: Uses eslint, prettier
- Go: Uses golint, gofmt
- Rust: Uses clippy, rustfmt

**Example Output:**
```
🔍 Analyzing code-review/scripts/analyze.py...
✅ No linting errors found
⚠️  Suggestion: Consider adding type hints for better readability
```

### Security Vulnerability Scanning
Identifies potential security issues like SQL injection, XSS, or insecure dependencies.

**Tools Used:**
- Bandit (Python)
- ESLint security plugins (JS/TS)
- Gosec (Go)
- Cargo audit (Rust)

**Example:**
```
🔒 Security Scan Results:
❌ High: Potential SQL injection in line 45
💡 Suggestion: Use parameterized queries instead of string formatting
```

### Performance Analysis
Detects inefficient patterns like nested loops, memory leaks, or blocking operations.

**Checks:**
- Complexity analysis (cyclomatic complexity)
- Memory usage patterns
- Asynchronous code best practices

### Custom Rules and AI Suggestions
Uses AI to provide contextual suggestions beyond static analysis, such as refactoring recommendations or best practices.

## CI Integration

### GitHub Actions Workflow
Add this to `.github/workflows/code-review.yml`:
```yaml
name: Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Code Review
        run: python3 scripts/analyze.py --dir . --ci
```

### Integration with @dev-workflow
Code-review is automatically included in @dev-workflow's CI auto-correction for linting fixes.

### Git Hooks
Automatic triggers are set up via git hooks:
- **Post-commit:** Runs lint checks on committed code files
- **Pre-push:** Runs security checks on files being pushed (blocks push if issues found)

### IDE Integration
VSCode tasks are configured for manual analysis:
- Analyze current file
- Analyze entire project
- Run security checks

Run via Command Palette: `Tasks: Run Task` → select Code Review option.

## Examples

### Basic File Analysis
```
User: Analyze this Python function for issues.

Assistant: I'll use @code-review to analyze the provided code.

[Analysis output with issues and suggestions]
```

### PR Review Automation
```
User: Review the changes in this pull request.

Assistant: Running @code-review on the diff...

[Comprehensive review report]
```

### Security Audit
```
User: Check this codebase for security vulnerabilities.

Assistant: Scanning with @code-review security tools...

[Security findings and recommendations]
```

## Best Practices and Version History

### Best Practices
- Run reviews on changed files only in CI to improve performance.
- Combine with static analysis tools for comprehensive coverage.
- Use AI suggestions as guidance, not definitive fixes.
- Configure language-specific rules via environment variables.

### Version History
| Version | Date       | Updates                                                |
|---------|------------|-------------------------------------------------------|
| 1.0.0   | 2026-02-11 | Initial implementation with multi-language support    |

## Resources

### scripts/
- `analyze.py`: Main analysis script supporting multiple languages and check types
- `utils.py`: Helper functions for language detection and tool integration

### references/
- `supported-languages.md`: Detailed guide to supported languages and tools
- `security-checklist.md`: Comprehensive security audit guidelines

### assets/
- `templates/`: Example configuration files for linters and security tools

