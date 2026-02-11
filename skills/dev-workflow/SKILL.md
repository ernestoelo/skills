---
name: dev-workflow
description: Provides official development standards and workflows for structuring projects, handling version control, and ensuring best practices for development processes.
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

### CI/CD Workflow
#### Fetch CI Logs
Fetch specific logs from GitHub Actions workflows for debugging:
```bash
gh run list --workflow "Skill Validation CI" --json status,conclusion,headSha | jq '.[] | select(.conclusion == "failure") | .headSha' | xargs -I {} gh run view {} --log
```
- Requires GitHub CLI (`gh`); outputs logs for failed runs.

#### Auto-Correct Common CI Issues
Run auto-correction for known errors (e.g., file size, validation):
```bash
python3 scripts/auto_correct_ci.py --workflow "Skill Validation CI" --commit <commit-sha>
```
- Detects and fixes issues like oversized assets; re-commits if needed.

#### Automated CI/CD with GitHub Actions
The repository includes automated CI/CD monitoring via `.github/workflows/auto-correct-ci.yml`:
- Triggers on CI failures (e.g., "Skill Validation CI").
- Iterates auto-corrections up to 5 times for all common issues (linting, tests, builds, deps, YAML, file size).
- Notifies via GitHub issue if fails after 5 attempts.

#### Automated Workflow Monitoring and Iterative Correction
Monitor GitHub Actions workflows post-commit, verify success, and apply iterative corrections until CI/CD converges. This ensures robust automation across repositories, following @architect for modular structure, @mcp-builder for seamless integration, and @sys-env for dependency management.

- **Process Overview:**
  1. Post-push, poll for workflow runs matching the commit SHA.
  2. Verify conclusion (success/failure).
  3. On failure, fetch logs and detect error types (YAML syntax, linting, tests, builds).
  4. Apply safe fixes iteratively (up to 5 attempts).
  5. Re-commit, push, and monitor again.
  6. Converge on success or notify for manual intervention.

- **Generic Implementation:**
  - Works in any repository with GitHub Actions and gh CLI.
  - Portable scripts detect repo context automatically.
  - Integrates @sys-env for installing missing deps (gh, jq).

- **Usage:**
  ```bash
  # After commit and push, run monitoring script
  python3 scripts/monitor_ci_iterative.py --workflow "<workflow-name>" --max-attempts 5
  ```
  - Monitors until workflow for current commit SHA completes.
  - Auto-corrects common issues and re-commits.
  - Outputs status and logs for transparency.

- **Supported Corrections (Safe, Non-Destructive):**
  - **YAML Syntax:** Validate and fix indentation/structure using Python yaml library.
  - **Linting:** Run ruff --fix or equivalent.
  - **Tests:** Execute pytest with fixes.
  - **Builds:** Run python -m build.
  - **Dependencies:** Install missing packages via @sys-env.

- **Integration with Other Skills:**
  - @architect: Ensures modular script structure for portability.
  - @mcp-builder: Provides protocol for external API interactions (GitHub API).
  - @sys-env: Manages system deps for cross-platform compatibility.

- **Porting to Any Repository:**
  1. Copy `scripts/monitor_ci_iterative.py`, `scripts/auto_correct_portable.py`, `scripts/verify_ci.py` to `<target-repo>/scripts/`.
  2. Ensure gh CLI and GITHUB_TOKEN access.
  3. Run `python3 scripts/monitor_ci_iterative.py --workflow <name>` post-push.
  - Universal: Adapts to repo's CI setup without hardcoded values.

#### Local Development Automation (Experimental)
For local development workflows, automate linting, staging, and committing (optional, non-mandatory):
```bash
python3 scripts/auto_commit_local.py --message "feat: add new feature"
```
- Runs linting (ruff check), stages all changes, commits with provided message if no issues.
- Use for quick local commits; review changes manually for complex updates.
- Disabled by default; enable via `--force` for CI-like local automation.

### Skills Architecture Diagrams
Visual representation of the skills ecosystem and activation flow:
- Central repository connects to individual skills.
- Sync process links skills to platforms like OpenCode.
- Automatic validation and loading at conversation start enables autonomous AI behavior.

![Skills Architecture](assets/diagrams/skills-architecture.png)

*(Diagram generated from `assets/diagrams/skills-architecture.puml` using PlantUML. Run `python3 scripts/generate_diagrams.py --diagram skills-architecture` to regenerate PNG automatically. If PlantUML is missing, uses @sys-env for installation.)*

#### Diagram Generation
Automatically generate PNG diagrams from PlantUML sources:
```bash
python3 scripts/generate_diagrams.py --diagram <diagram_name>
```
- Checks for PlantUML installation; if missing, integrates with @sys-env for safe installation on Arch Linux.
- Generates PNG in the same directory as the .puml file.
- Verifies PNG (existence, size >0) and auto-corrects by retrying up to 5 times if fails.
- Example: `python3 scripts/generate_diagrams.py --diagram skills-architecture` creates `skills-architecture.png`.

#### Visual References for Diagram Styles
Always reference `imgs/` and `examples/` for consistent styles in any repository:
- **imgs/ (Simple Flows):** Gitflow diagrams (gitflow.png, gitflow-feature-branch.png, gitflow-release-branch.png) – Use for linear process flows, standard colors, minimal annotations.
- **examples/ (Complex Architectures):** Biomass diagrams (biomass-web-architecture.png, biomass-web-overview.png, biomass-web-prod-env.png) – Use for system architectures, production templates with blocks, colored arrows, and detailed notes.
- When creating .puml, mimic layouts/colors from these to ensure visual appeal and uniformity across repos.

#### Porting Diagram Generation to Other Repositories
To use this diagram generation kit in any repository:
1. Copy `scripts/generate_diagrams.py` to `<target-repo>/scripts/`.
2. Copy templates from `assets/diagrams/templates/` to `<target-repo>/assets/diagrams/`.
3. Copy `@sys-env/scripts/install_package.py` for dependency installation (or configure NOPASSWD manually).
4. **Copy `assets/diagrams/imgs/` and `assets/diagrams/examples/` as visual reference libraries.**
5. Create/edit `.puml` files in `<target-repo>/assets/diagrams/` following the style (colored blocks, arrows, notes).
6. Run `python3 scripts/generate_diagrams.py --diagram <name>`; auto-installs PlantUML/graphviz if needed.
- Ensures consistency: Visual appeal, colored arrows, brief notes, verification, and auto-correction. Always reference imgs/examples for styles.

## Inputs and Outputs
### Inputs
- **Repository context:** Current Git state (branches, changes).
- **Project environment:** Python version, package manager configurations, or AI frameworks required.

### Outputs
- **Git changes:** Staged/stable commits reflecting best practices.
- **Project files:** Well-organized structure based on `uv` or repo templates.

## Best Practices and Version History
### Best Practices
- **Git:** Always work on feature branches; avoid direct `main` commits. Use `auto_commit_local.py` for quick local commits, but review manually for complex changes.
- **AI Projects:** Use `uv` for reproducible environments; pin Python versions.
- **CI/CD:** Monitor workflows after commits; use auto-correct for common issues. Always verify CI status post-push with `verify_ci.py` or hooks for generic repos.

### Version History
| Version | Date       | Updates                                                  |
|---------|------------|---------------------------------------------------------|
| 2.1.0   | 2026-02-11 | Added automated workflow monitoring and iterative correction for generic CI/CD convergence across repositories.|
| 2.0.0   | 2026-02-11 | Added experimental local auto-commit script for development automation.|
| 1.9.2   | 2026-02-11 | Improved CI verification by filtering runs by commit SHA to avoid confusion with auto-correct workflows.|
| 1.7.0   | 2026-02-11 | Integrated imgs/ and examples/ as permanent visual references for diagrams in any repo.|
| 1.6.0   | 2026-02-11 | Added portable diagram generation kit for any repository.|
| 1.5.0   | 2026-02-11 | Added automatic diagram generation with sys-env integration.|
| 1.4.0   | 2026-02-11 | Added skills architecture diagrams in PlantUML style.   |
| 1.3.0   | 2026-02-10 | Added automated CI/CD with GitHub Actions integration, email notifications, and all corrections.|
| 1.2.0   | 2026-02-10 | Added CI/CD workflow for log sharing and auto-correction.|
| 1.1.0   | 2026-02-09 | Reorganized content into SKILL.md standard template.    |
| 1.0.0   | 2024-11-03 | Initial workflow for AI/ML projects and Git workflows.  |

## Resources
- `references/ci-cd-best-practices.md`: CI/CD monitoring and troubleshooting guides.
- `scripts/monitor_ci_iterative.py`: Automated monitoring and iterative correction script.
- `scripts/auto_correct_portable.py`: Portable auto-correction for CI issues.