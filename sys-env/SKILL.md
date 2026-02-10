---
name: sys-env
description: System environment manager for Arch Linux with Hyprland + Wayland. This skill ensures safe and optimal configuration for package management, drivers, services, and hardware compatibility.
author: OpenCode Project Team
version: 1.2.0
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
bash scripts/pre-install-check.sh mesa pipewire hyprland
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

### Environment Variable Setup
#### Display and Toolkit Variables
```bash
export WAYLAND_DISPLAY=wayland-0
export XDG_SESSION_TYPE=wayland
```
- For longevity, update within `~/dotfiles/zsh/.zshrc`.

#### GPU Optimizations
```bash
export AMD_VULKAN_ICD=‘RADV’ 
``` 
 Full Visualization primitives are GPU-level!