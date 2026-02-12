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
2. **Install/Update**: Use `sudo pacman -S <package>` or `yay -S <package>` (see references/arch-package-management.md).
3. **Modify/Reconfigure**: Edit configs with care; backup first. Restart services as needed.
4. **Remove/Replace**: Use `sudo pacman -R <package>` and check dependencies.
5. **Remote Setup**: Use SSH for Jetson/ZedBox; see references/remote-setup.md.

## Bundled Resources

- **scripts/env_check.sh**: Checks for required packages, drivers, and session type.
- **assets/arch-logo.png, hyprland-logo.png**: Visual guides for environment.
- **references/**: Detailed guides for package management, compatibilities, safety, and remote setup.

## Best Practices

- Always check for conflicts before making changes.
- Backup configs and services before modification.
- Use NOPASSWD in /etc/sudoers for automation (with caution).
- Test on non-critical setups first.

## References

- [references/arch-package-management.md](references/arch-package-management.md): Package management
- [references/hyprland-compatibilities.md](references/hyprland-compatibilities.md): Hyprland compatibility
- [references/system-safety-checklist.md](references/system-safety-checklist.md): Safety checklist
- [references/remote-setup.md](references/remote-setup.md): Remote setup for Jetson/ZedBox

## Validation and CI/CD

- Integrate with @architect for environment scaffolding and validation.
- Use pre-commit hooks and CI for environment scripts.
- Validate system state before running critical operations.