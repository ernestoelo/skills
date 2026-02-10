# CI/CD Best Practices for Dev-Workflow

## Monitoring Workflows
- After commits, check GitHub Actions status via `gh run list`.
- Use `fetch_ci_logs.py` for detailed error logs.
- Common workflows: "Skill Validation CI" (validates skills), "Validate Skills" (tests).

## Auto-Correction Guidelines
- Run `auto_correct_ci.py` for known issues (e.g., large files, YAML errors).
- Avoid over-automation: Manual review for complex failures.
- Integrate with pre-commit hooks for early detection.

## Troubleshooting
- "File too large": Remove assets >10MB.
- "YAML failed": Check frontmatter in SKILL.md.
- "Test failure": Run `uv run pytest` locally.