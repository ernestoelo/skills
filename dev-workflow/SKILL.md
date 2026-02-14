---
name: dev-workflow
description: Development standards and validation for AI/ML projects. Use to scaffold, validate, and maintain reproducible, high-quality repositories with Gitflow, uv, and best practices. Triggers for new project setup, structure validation, or workflow enforcement.
license: Apache-2.0
---

# Development Workflow Skill

This skill provides canonical standards, validation scripts, and best practices for AI/ML project development. It ensures reproducibility, code quality, and team alignment, following the anthropic skill structure and progressive disclosure principles.

## Core Principles

- **Reproducibility**: All environments and dependencies are pinned and documented.
- **Modularity**: Projects follow a clear, modular structure for code, data, and models.
- **Validation**: Automated scripts check for required files, structure, and compliance.
- **Progressive Disclosure**: Only essential context is loaded; detailed guides live in references/.

## Anatomy

Every project should have:

```
project-root/
├── src/           # Core code
├── data/          # Data files (with .gitkeep)
├── models/        # Model files (with .gitkeep)
├── notebooks/     # Jupyter or other notebooks
├── pyproject.toml # Project metadata
├── uv.lock        # Dependency lockfile
├── README.md      # Project overview
├── Makefile, run.sh, .gitignore
```

## Usage Guide

1. **Project Setup**: Initialize with `uv init --lib <project-name>`, pin Python with `uv python pin 3.12`, and add dependencies using `uv add`.
2. **Structure**: Organize code, data, and models as above. Use `.gitignore` to exclude `.venv/`, `data/*`, `models/*`, and `conf.env`.
3. **Git Workflow**: Use Gitflow (see references/git-workflow.md):
   - Branch from `develop` for features: `git checkout -b feat/your-feature`
   - Use Conventional Commits for messages: `feat(scope): subject`
   - Merge to `develop` via PR, then to `main` for releases
4. **Validation**: Run `scripts/validate_project.sh` to check structure and required files.
5. **Self-Validation**: Complete the checklist in references/checklist.md before handover or deployment.

## Bundled Resources

- **scripts/validate_project.sh**: Checks for required files and structure.
- **assets/gitflow.png, structure.png**: Visual guides for workflow and structure.
- **references/**: Detailed guides for AI development, Gitflow, and validation.

## Best Practices

- Work on feature branches; never commit directly to `main`.
- Use `uv` for dependency management; always pin Python versions.
- Validate structure and checklist before every release.
- Prefer clarity and reproducibility over cleverness.

## Code Language and Comments

> - All variable names, function names, and code comments must be in English.
> - Avoid non-English words in code, except where required by external APIs or data.
> - Documentation and code comments should explain intent, logic, and usage.
All code in project files **must be written in English** and include clear, descriptive comments in English. Additionally, **all GitHub workflow actions**—including commit messages, branch names, pull request titles/descriptions, and merge messages—**must be in English**. This ensures:

- Consistency and accessibility for international teams
- Easier onboarding and code review
- Alignment with open-source and industry standards

> **Guideline:**
> - All variable names, function names, and code comments must be in English.
> - All commit messages, branch names, PR titles/descriptions, and merge messages must be in English.
> - Avoid non-English words in code or workflow, except where required by external APIs or data.
> - Documentation and code comments should explain intent, logic, and usage.

This rule applies to all scripts, notebooks, source files, and all GitHub workflow actions in the repository.

## References

- [references/overview.md](references/overview.md): Project overview and standards
- [references/git-workflow.md](references/git-workflow.md): Gitflow and commit conventions
- [references/ai-development.md](references/ai-development.md): AI/ML best practices
- [references/checklist.md](references/checklist.md): Self-validation checklist


## Validation

- Integrate with @architect for skill/project scaffolding.
- Use pre-commit hooks for structure and code validation.
- Check environment and dependencies with @sys-env before running scripts.