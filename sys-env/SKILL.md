---
name: sys-env
description: "System environment manager for Arch Linux + Hyprland + Wayland workstation. Consult this skill BEFORE installing packages, modifying drivers, changing environment variables, editing dotfiles, or configuring system services. Covers package safety checks, hardware compatibility (AMD Ryzen APU with Radeon integrated graphics), Wayland-specific requirements, PipeWire audio stack, dotfiles via GNU Stow, and remote target awareness (Jetson/ZedBox via SSH). Use when the user mentions pacman, yay, system packages, drivers, mesa, vulkan, environment variables, dotfiles, stow, hyprland config, waybar, pipewire, or system services."
---

# System Environment Manager

Safety-first guide for managing an Arch Linux + Hyprland workstation. **Consult this skill before any system modification.**

## Core Safety Rule

**ALWAYS** check this skill before:
- Installing or removing packages (pacman, yay, uv, docker)
- Modifying GPU/display drivers or libraries
- Changing environment variables
- Editing system configs or dotfiles
- Enabling/disabling system services
- Adding kernel parameters or modules

## Quick Reference

| Component       | Value                              | Constraint                              |
|-----------------|------------------------------------|-----------------------------------------|
| Distro          | Arch Linux (rolling, LTS kernel)   | `pacman` + `yay` for AUR               |
| WM              | Hyprland (Wayland compositor)      | Never install X11-only tools            |
| GPU             | AMD Radeon integrated (amdgpu)     | Never install nvidia drivers locally    |
| Audio           | PipeWire + WirePlumber             | Never install PulseAudio daemon         |
| Dotfiles        | GNU Stow from `~/dotfiles/`        | Never edit configs in `~/.config/` directly |
| Python          | `uv` (project-scoped venvs)        | Never `pip install` globally            |
| Keyboard        | Latin American (`latam`)            | Keep XKB layout consistent              |
| Theme           | Catppuccin Mocha (system-wide)     | GTK, Hyprland borders, Waybar, Kitty    |

## Decision Tree: Package Installation

Follow this sequence for **every** package installation:

```
1. Local or remote target?
   ├── Remote (Jetson/ZedBox/Lab PC) → Read references/remote-targets.md
   └── Local → continue

2. Does package touch GPU/display stack?
   (mesa, vulkan, xorg, wayland, libdrm, egl, libva, vdpau)
   ├── YES → HIGH RISK. Read references/compatibility-matrix.md before proceeding
   └── NO → continue

3. Does package touch audio stack?
   (pipewire, pulseaudio, alsa, jack, wireplumber)
   ├── YES → HIGH RISK. Read references/compatibility-matrix.md before proceeding
   └── NO → continue

4. Does package replace an existing component?
   ├── YES → Check: pacman -Qi <existing> | grep "Required By"
   │         If anything depends on it → STOP, warn user
   └── NO → continue

5. Is this an AUR package?
   ├── YES → Review PKGBUILD, check AUR comments, verify maintainer activity
   └── NO → continue

6. Run pre-install safety check:
   scripts/pre-install-check.sh <package-name>

7. Install:
   - Official repo → sudo pacman -S <package>
   - AUR → yay -S <package>
   - Python → uv add <package> (inside project)
   - Container → docker pull <image>
```

## Decision Tree: Environment Variables

```
1. What scope?
   ├── Shell session only → export VAR=value (temporary)
   ├── User shell permanent → edit ~/dotfiles/zsh/.zshrc via Stow
   ├── System-wide → /etc/environment (reboot required)
   └── Service-specific → systemd unit override (systemctl edit)

2. Is it Wayland/display related?
   (WAYLAND_DISPLAY, XDG_SESSION_TYPE, GDK_BACKEND, QT_QPA_PLATFORM,
    MOZ_ENABLE_WAYLAND, SDL_VIDEODRIVER, CLUTTER_BACKEND)
   ├── YES → Verify Hyprland sets it already (hyprctl env)
   │         Do NOT override unless specifically needed
   └── NO → continue

3. Is it GPU related?
   (AMD_VULKAN_ICD, LIBVA_DRIVER_NAME, VDPAU_DRIVER, MESA_*)
   ├── YES → Read references/compatibility-matrix.md
   └── NO → safe to set
```

## Package Managers

| Manager   | Scope                    | Usage                                      |
|-----------|--------------------------|--------------------------------------------|
| `pacman`  | Official Arch repos      | `sudo pacman -S pkg` / `-Syu` for upgrade  |
| `yay`     | AUR + official repos     | `yay -S pkg` / `yay -Syu` for full upgrade |
| `uv`      | Python (project-scoped)  | `uv add pkg` inside project dir            |
| `docker`  | Containerized services   | `docker pull` / `docker compose up`        |
| `flatpak` | Sandboxed desktop apps   | Verify Wayland support before installing    |

**Upgrade safety:**
- Before `yay -Syu`: check Arch Linux news (`archlinux.org/news/`) for breaking changes
- Never do partial upgrades (`pacman -Sy pkg` without `-u` is dangerous on Arch)
- LTS kernel (`linux-lts`) provides stability buffer — do not switch to `linux` without reason

## Dotfiles Management (GNU Stow)

**Structure:** `~/dotfiles/<app>/.config/<app>/`

Discover managed apps at runtime:
```bash
ls ~/dotfiles/          # list all Stow packages
stow -n -v <app> 2>&1  # dry-run to preview symlink targets
```

**Workflow:**
1. `cd ~/dotfiles`
2. Edit files in the Stow source directory (e.g., `~/dotfiles/hypr/.config/hypr/hyprland.conf`)
3. Run `stow <app>` to create/update symlinks
4. Verify: `ls -la ~/.config/<app>/` should show symlinks pointing to `~/dotfiles/`

**Rules:**
- NEVER edit files directly in `~/.config/` — this breaks Stow tracking
- To add a new app: `mkdir -p ~/dotfiles/<app>/.config/<app>/`, move configs in, then `stow <app>`
- To remove: `stow -D <app>` (deletes symlinks only, source files remain)
- Git-managed: `~/dotfiles/` should be a git repo for version control

## Hyprland Scripts

Location: `~/.config/hypr/scripts/` (Stow-managed via `~/dotfiles/hypr/`)

Discover scripts and keybinds at runtime:
```bash
ls ~/.config/hypr/scripts/                  # available scripts
grep '^bind' ~/.config/hypr/hyprland.conf   # keybind definitions
```

When modifying scripts:
- Test changes in isolation before committing
- Check script dependencies (e.g., `swww`, `grim`, `slurp` must be installed)
- Keybinds are defined in `hyprland.conf` — keep script names and binds in sync

## Service Management

**User services** (managed per-user, no sudo):
```bash
systemctl --user list-unit-files --state=enabled   # discover active user services
systemctl --user status <service>
systemctl --user restart <service>
journalctl --user -u <service>   # check logs
```

**System services** (require sudo):
```bash
systemctl list-unit-files --state=enabled          # discover active system services
sudo systemctl status <service>
sudo systemctl enable/start <service>
```

**Before restarting any service:**
1. Check current status: `systemctl [--user] status <service>`
2. Check logs: `journalctl [--user] -u <service> -n 50`
3. If it's a display service (waybar, hyprland): warn user that display may flicker/reset
4. If it's audio (pipewire, wireplumber): warn user that audio output will briefly cut

## Resources

### References (load into context as needed)

- **`references/hardware-profile.md`** — Read for driver questions, hardware capabilities, kernel module info
- **`references/software-stack.md`** — Stack-defining software + runtime query commands for discovering installed packages and services
- **`references/compatibility-matrix.md`** — Read before ANY high-risk operation (GPU, audio, Wayland components)
- **`references/remote-targets.md`** — Read when working with Lab PC, ZedBox, or Jetson targets

### Scripts

- **`scripts/pre-install-check.sh`** — Run before installing packages to assess risk level
  Usage: `bash sys-env/scripts/pre-install-check.sh <package-name> [package-name...]`
