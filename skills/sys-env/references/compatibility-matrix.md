# Compatibility Matrix

Critical dependency and conflict information. **Read this before any HIGH RISK operation.**

## GPU Stack (AMD Radeon / amdgpu / Mesa)

### Safe Configuration (current)
```
mesa + vulkan-radeon + libva-mesa-driver + mesa-vdpau
```
These MUST be from the same mesa release. `pacman -Syu` handles this automatically.

### NEVER Install
| Package             | Reason                                                    |
|---------------------|-----------------------------------------------------------|
| `nvidia`            | No NVIDIA GPU locally — will conflict with amdgpu         |
| `nvidia-dkms`       | Same as above, plus breaks LTS kernel modules             |
| `xf86-video-amdgpu` | X11 DDX driver — unnecessary on Wayland, can cause issues |
| `vulkan-amdgpu-pro` | Proprietary Vulkan — conflicts with RADV (vulkan-radeon)  |
| `amdgpu-pro`        | Proprietary driver stack — conflicts with mesa            |
| `lib32-nvidia-utils` | 32-bit NVIDIA libs — completely wrong GPU                |

### Caution Zone
| Package                | Risk                                                         |
|------------------------|--------------------------------------------------------------|
| `mesa-git` (AUR)       | Bleeding edge, may break Hyprland. Only if testing           |
| `lib32-mesa`           | Needed for 32-bit apps (Steam). Safe IF matching mesa version |
| `vulkan-tools`         | Safe to install (diagnostic only)                            |
| `libva-utils`          | Safe to install (diagnostic only)                            |
| `rocm-*` packages      | ROCm not supported on Vega 7 APU — waste of space           |

### Diagnostic Commands
```bash
vulkaninfo --summary          # Verify Vulkan is working
vainfo                        # Verify VA-API hardware decode
glxinfo | grep "OpenGL"       # OpenGL version
lsmod | grep amdgpu           # Kernel module loaded
```

## Audio Stack (PipeWire)

### Safe Configuration (current)
```
pipewire + wireplumber + pipewire-pulse + pipewire-jack + pipewire-alsa
```

### NEVER Install
| Package              | Reason                                              |
|----------------------|-----------------------------------------------------|
| `pulseaudio`         | Conflicts with pipewire-pulse — will break audio    |
| `pulseaudio-alsa`    | Same conflict                                       |
| `pulseaudio-jack`    | Same conflict                                       |
| `pulseaudio-bluetooth` | Use pipewire-pulse for bluetooth audio instead    |
| `jack2`              | Conflicts with pipewire-jack                        |

### Caution Zone
| Package              | Risk                                                      |
|----------------------|-----------------------------------------------------------|
| `alsa-utils`         | Safe — ALSA is the kernel layer, PipeWire sits on top     |
| `pavucontrol`        | Safe — works with pipewire-pulse compatibility layer      |
| `easyeffects`        | Safe — uses PipeWire API directly                         |
| `helvum`             | Safe — PipeWire patchbay for routing                      |

### Diagnostic Commands
```bash
wpctl status                 # WirePlumber device/stream list
pw-cli info all              # PipeWire detailed info
pactl info                   # PulseAudio compat layer status
systemctl --user status pipewire wireplumber pipewire-pulse
```

## Wayland Compatibility

### Tools That MUST Be Wayland-Native
| Need              | Correct (Wayland)            | Wrong (X11-only)           |
|-------------------|------------------------------|----------------------------|
| Screenshot        | `grim` + `slurp`            | `scrot`, `maim`            |
| Clipboard         | `wl-clipboard` (`wl-copy`)  | `xclip`, `xsel`            |
| Screen record     | `wf-recorder`, `obs` (pipewire) | `ffmpeg` X11 capture   |
| Screen share      | `xdg-desktop-portal-hyprland` | `xdg-desktop-portal-gtk` alone |
| Color picker      | `hyprpicker`                 | `xcolor`, `gpick`          |
| App launcher      | `fuzzel`, `wofi`, `tofi`     | `rofi` (X11 version)       |
| Idle/lock         | `hypridle` + `hyprlock`      | `xautolock`, `i3lock`      |
| Display config    | `wlr-randr`, `hyprctl`      | `xrandr`                   |
| Keymap viewer     | `wev`                        | `xev`                      |

### XDG Desktop Portal Stack
```
xdg-desktop-portal + xdg-desktop-portal-hyprland + xdg-desktop-portal-gtk
```
- `xdg-desktop-portal-hyprland` handles: screen sharing, screenshots, window selection
- `xdg-desktop-portal-gtk` handles: file picker, app chooser, settings
- Both are needed. Do NOT remove `xdg-desktop-portal-gtk`.

### Wayland Environment Variables
These are typically set by Hyprland automatically. Do NOT override unless broken:
```bash
WAYLAND_DISPLAY=wayland-1          # Set by compositor
XDG_SESSION_TYPE=wayland            # Set by login
GDK_BACKEND=wayland                 # GTK apps
QT_QPA_PLATFORM=wayland             # Qt apps
MOZ_ENABLE_WAYLAND=1                # Firefox
SDL_VIDEODRIVER=wayland              # SDL2 games/apps
ELECTRON_OZONE_PLATFORM_HINT=auto   # Electron apps (VS Code, etc.)
```

## Kernel Considerations

### Current: linux-lts
- Stable, well-tested, fewer regressions
- Kernel modules (amdgpu, wifi, bluetooth) are version-matched

### Do NOT Switch To
| Kernel         | Risk                                                          |
|----------------|---------------------------------------------------------------|
| `linux`        | Mainline — more frequent updates, higher regression risk      |
| `linux-zen`    | Performance-tuned — may have different module compatibility    |
| `linux-hardened` | Security-focused — may break some software                  |

If kernel switch is ever needed: install both kernels, configure bootloader to dual-boot, test thoroughly before removing `linux-lts`.

## Common Conflict Patterns

### Pattern: "GUI app doesn't launch"
1. Check if it's X11-only: `pacman -Qi <pkg>` — look for `xorg` dependencies
2. Look for Wayland-native alternative (see table above)
3. If no alternative: run via `XWayland` (Hyprland enables this by default)

### Pattern: "Audio stopped working"
1. `systemctl --user status pipewire wireplumber pipewire-pulse`
2. `wpctl status` — check for missing sinks
3. `systemctl --user restart pipewire wireplumber`
4. If still broken: check if conflicting package was installed (`pacman -Qs pulseaudio`)

### Pattern: "Screen sharing doesn't work"
1. Verify portal stack: `pacman -Qs xdg-desktop-portal`
2. Must have: `xdg-desktop-portal`, `xdg-desktop-portal-hyprland`, `xdg-desktop-portal-gtk`
3. Restart portal: `systemctl --user restart xdg-desktop-portal-hyprland`
4. For browser: ensure PipeWire is running, use WebRTC with PipeWire backend

### Pattern: "Package upgrade broke display"
1. Boot with `linux-lts` fallback in bootloader
2. Check: `pacman -Qo /usr/lib/dri/radeonsi_dri.so` — should be `mesa`
3. Verify: `pacman -Syu` to ensure no partial upgrade
4. Downgrade if needed: `pacman -U /var/cache/pacman/pkg/mesa-<old-version>.pkg.tar.zst`
