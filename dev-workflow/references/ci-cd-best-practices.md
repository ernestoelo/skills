# CI/CD Best Practices for Dev-Workflow

## Monitoring Workflows
- After commits, check GitHub Actions status via `gh run list`.
- Use `fetch_ci_logs.py` for detailed error logs.
- Common workflows: "Skill Validation CI" (validates skills), "Validate Skills" (tests).

## Auto-Correction Guidelines
- Run `auto_correct_ci.py` for known issues (e.g., large files, YAML errors).
- Avoid over-automation: Manual review for complex failures.
- Integrate with pre-commit hooks for early detection.

## Automated CI/CD
- GitHub Actions workflow `auto-correct-ci.yml` handles failures automatically.
- Iterates up to 3 times, applying all fixes (linting, tests, builds, etc.).
- Creates GitHub issue with notification if fails after 3 attempts.
- No manual intervention needed for common errors.