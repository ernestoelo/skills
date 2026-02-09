---
name: dev-workflow
description: Provides official development standards and workflows for structuring projects, handling version control, and ensuring best practices for development processes.
author: OpenCode Project Team
version: 1.1.0
---

# Development Workflow Skill Guide

## Description
The `dev-workflow` skill ensures consistent project setup, version control, and adherence to organizational standards. Covering everything from Git branching to AI project scaffolding, these workflows are mandatory for all new projects and collaboration tasks.

## When to Use the Skill
- **Setting up a repository or project:** Ensure correct structures, environments, and configurations.
- **Version control workflows:** Commit, branch management, and Gitflow adherence.
- **AI/ML-specific needs:** Proper Python package management, environments, and coding standards.
- **Synchronizing or updating project artifacts:** Ensure clean execution of project syncs.

## Usage Guide
### Setting Up AI/ML Projects
#### Scaffold a New Project
```bash
uv init --lib <project_name>
uv python pin 3.12
```
- Creates the project structure and pins the Python version.
- Populate `pyproject.toml` and configure `uv.lock` for dependencies.

#### Example Gitignore
```plaintext
# Python artifacts
__pycache__/
.venv
*.pyc

# Data directories
data/
```

### Git Workflow
#### Branch Creation
Keep branch names descriptive of the feature or fix:
```bash
git checkout -b feat/user-auth
git checkout -b fix/login-timeout
```
- Feature/fix branches merge to `develop`.
- Ensure all commits follow the Conventional Commits format.

#### Commit Workflow
1. Use `git status` and `git diff` to identify changes.
2. Avoid staging sensitive files (e.g., `.env`, credentials).
3. Write a semantic commit message (example):
   ```bash
   git commit -m "fix(login): handle timeout edge cases"
   ```

## Inputs and Outputs
### Inputs
- **Repository context:** Current Git state (branches, changes).
- **Project environment:** Python version, package manager configurations, or AI frameworks required.

### Outputs
- **Git changes:** Staged/stable commits reflecting best practices.
- **Project files:** Well-organized structure based on `uv` or repo templates.

## Best Practices and Version History
### Best Practices
- **Git:** Always work on feature branches; avoid direct `main` commits.
- **AI Projects:** Use `uv` for reproducible environments; pin Python versions.

### Version History
| Version | Date       | Updates                                                  |
|---------|------------|---------------------------------------------------------|
| 1.1.0   | 2026-02-09 | Reorganized content into SKILL.md standard template.    |
| 1.0.0   | 2024-11-03 | Initial workflow for AI/ML projects and Git workflows.  |