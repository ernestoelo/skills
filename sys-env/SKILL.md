---
name: sys-env
description: System environment manager for Arch Linux with Hyprland + Wayland. This skill ensures safe and optimal configuration for package management, drivers, services, and hardware compatibility.
---

# System Environment Manager Skill Guide

## Description
The `sys-env` skill is designed for managing a Wayland-based Arch Linux workstation with Hyprland as the compositor. It ensures compatibility with hardware (AMD Radeon), services (PipeWire, systemd), and package managers (pacman, yay). Always consult this skill for best practices and safety checks when modifying system configurations.

## When to Use the Skill
- **Installing or upgrading packages:** Safety checks for conflicts using pre-install scripts.
- **Modifying environment variables:** Guidance on scope and compatibility.
- **Managing dotfiles:** Best practices for GNU Stow and version control.
- **Editing system services:** Safely restarting critical services.
- **Working remotely:** Special considerations for Jetson/ZedBox with SSH or local setups.

## Usage Guide
### Package Safety Verification
#### Check Package Compatibility
```bash
bash shared/scripts/pre-install-check.sh mesa pipewire hyprland
```
- Validates the presence of tools and evaluates risk levels (e.g., GPU or audio stack).

#### Example Output
```
=== Pre-Install Safety Check ===
System: Arch Linux + Hyprland (Wayland)

Processing item: mesa
  Tool already installed.
  Matches critical: mesa.
  Conflicts detected: libva-mesa-driver.
```

### Automatic Package Installation
For seamless automation in plans/builds, configure sudo NOPASSWD for safe package installation. This activates @sys-env when scripts detect missing packages.

#### Configure NOPASSWD for Pacman
Edit /etc/sudoers (use visudo):
```
your_username ALL=(ALL) NOPASSWD: /usr/bin/pacman
```
- Allows passwordless pacman commands for your user.
- Run `sudo visudo` to edit safely.

#### Automatic Installation Command
```bash
python3 shared/sys-env/scripts/install_package.py <package>
```
- Installs any Arch Linux package with NOPASSWD priority; provides manual steps if not configured.
- Use for any missing dependency across skills (e.g., @dev-workflow, @architect).

#### Interactive Prompts for Security
For secure installations, scripts prompt for sudo password:
```bash
# Example in script
Enter your sudo password: [hidden input]
```
- Uses getpass for hidden input; no password stored.
- Fallback if NOPASSWD not configured.

#### Integration with Other Skills
When a skill/script requires a package (e.g., @dev-workflow for diagrams), call `python3 sys-env/scripts/install_package.py <package>` for universal, automated installation.

## Best Practices and Version History
### Best Practices
- Always run pre-install checks before package changes.
- Use NOPASSWD judiciously for automation; limit to trusted commands.
- Backup configurations before modifying environment variables or services.

### Version History
| Version | Date       | Updates |
|---------|------------|---------|
| 1.3.0   | 2026-02-11 | Added generic install_package.py script for any Arch package with NOPASSWD automation.|
| 1.2.0   | 2026-02-11 | Added interactive prompts for secure package installation.|
| 1.1.0   | 2026-02-11 | Added automatic package installation with NOPASSWD config.|
| 1.0.0   | 2026-02-09 | Initial skill for Arch Linux + Hyprland management.|