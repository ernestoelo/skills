# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-10

### Added
- CI status badges in README.md for workflow visibility.
- Comprehensive CI pipeline with GitHub Actions for skill validation.
- Release tagging and merge workflow from develop to main.

### Changed
- Updated Skill Validation CI workflow to use `uv sync` for dependency management.
- Improved git diff handling in CI for shallow clones by fetching base SHAs.
- Restructured CI to validate only changed SKILL.md files for efficiency.
- Enhanced README.md with detailed CI/CD section and success notes.

### Fixed
- Resolved PyYAML ModuleNotFoundError in CI by switching to uv environment.
- Fixed undefined `skill_dir` in workflows with dynamic detection of changed files.
- Corrected YAML syntax and formatting issues in workflow files.
- Applied Ruff formatting across all Python files for consistency.

### Removed
- PyYAML from requirements.txt (now handled via pyproject.toml and uv).

## [1.0.0] - 2025-05-16

### Added
- Initial release of skills repository with core skills: architect, dev-workflow, mcp-builder, pdf, sys-env, web-scraper.
- Basic validation scripts and repository structure.
- Git hooks for post-clone setup and skill syncing.</content>
<parameter name="filePath">CHANGELOG.md