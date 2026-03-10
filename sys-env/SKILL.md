---
name: sys-env
description: System environment management for Arch Linux + Hyprland. Use to validate, configure, and troubleshoot packages, drivers, and services. Triggers for package operations, compatibility checks, and environment validation.
license: Apache-2.0
---

# System Environment Manager Skill

This skill provides scripts, references, and best practices for managing Arch Linux + Hyprland environments. It ensures safe package management, hardware compatibility, and reproducible setups, following the anthropic skill structure and progressive disclosure principles.

## Core Principles

- **Safety**: Always check compatibility and backup configs before changes.
- **Transparency**: Scripts and references document every step and decision.
- **Validation**: Automated scripts check for required packages, drivers, and services.
- **Progressive Disclosure**: Only essential context is loaded; detailed guides live in references/.

## Anatomy

Every environment should be managed with:

```
sys-env/
├── scripts/         # Automation and validation scripts
├── references/      # Detailed guides and compatibility docs
├── assets/          # Logos, diagrams, or templates
└── SKILL.md         # Main guide
```

## Usage Guide

1. **Check Compatibility**: Run `scripts/env_check.sh` to verify required packages, drivers, and session type.
2. **Check Python Environment**: Before `yay -S`, verify conda is deactivated (see references/python-environments.md).
3. **Install/Update**: Use `sudo pacman -S <package>` or `yay -S <package>` (see references/arch-package-management.md).
4. **Modify/Reconfigure**: Edit configs with care; backup first. Restart services as needed.
5. **Remove/Replace**: Use `sudo pacman -R <package>` and check dependencies.
6. **Python Project Setup**: For new development projects, use @architect with isolated environments (not miniforge base).
7. **Remote Setup**: Use SSH for Jetson/ZedBox; see references/remote-setup.md.

## Bundled Resources

- **scripts/env_check.sh**: Checks for required packages, drivers, and session type.
- **scripts/check-python-env.sh**: **NEW** - Validates Python environment before system operations (checks for conda, miniforge, venv conflicts). Usage: `./scripts/check-python-env.sh` or `./scripts/check-python-env.sh --auto-fix`
- **assets/arch-logo.png, hyprland-logo.png**: Visual guides for environment.
- **references/**: Detailed guides for package management, compatibilities, safety, remote setup, and Python environment management.

## Best Practices

- **Python Environments**: Always deactivate conda/miniforge BEFORE running `yay -S` or `pacman -S` to avoid mixed dependency sources.
- **Project Isolation**: Create project-specific venv or conda environments instead of using miniforge base for development (see @architect).
- **Check Before Operating**: Run `echo $CONDA_DEFAULT_ENV` before system package operations. Should be empty or (base).
- **Always check for conflicts** before making changes.
- **Backup configs and services** before modification.
- **Use NOPASSWD in /etc/sudoers** for automation (with caution).
- **Test on non-critical setups** first.
- **Documentation**: Include environment instructions in project README when integrating with @architect.

## References

- [references/arch-package-management.md](references/arch-package-management.md): Package management
- [references/python-environments.md](references/python-environments.md): **NEW** - Python/conda/miniforge environment management, conda↔pacman conflicts, best practices, troubleshooting
- [references/ARCHITECTURE-INTEGRATION.md](references/ARCHITECTURE-INTEGRATION.md): **NEW** - Integration with @architect skill for development projects, best practices, CI/CD setup
- [references/hyprland-compatibilities.md](references/hyprland-compatibilities.md): Hyprland compatibility
- [references/system-safety-checklist.md](references/system-safety-checklist.md): Safety checklist
- [references/remote-setup.md](references/remote-setup.md): Remote setup for Jetson/ZedBox

## Validation and CI/CD

- **Integrate with @architect**: When scaffolding new development projects, ensure conda is deactivated before system package operations. See references/python-environments.md for integration strategies.
- **Integrate with @dev-workflow**: Document environment requirements in project setup (system Python version, conda env names, required deactivation steps).
- **Use pre-commit hooks**: Add hooks that check for active conda before git operations (prevents incorrect dependencies in commits).
- **Validate system state** before running critical operations.
- **CI/CD**: Ensure pipeline deactivates conda before installing system packages with pacman/yay.