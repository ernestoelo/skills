# Software Stack

Core software that defines the system's identity and determines which commands, configs, and workflows the AI should use. For checking whether a specific package is installed, use `pacman -Q <package>` or `pacman -Qs <keyword>` at runtime.

## Desktop Environment

### Compositor & Window Management
- **Hyprland** — Wayland compositor, dwindle layout
- **Config:** `~/.config/hypr/hyprland.conf` (Stow-managed)
- Check version: `hyprctl version`
- Check plugins: `hyprctl plugin list`

### Bar & UI
- **Waybar** — Status bar (systemd user service)
- **nwg-drawer** — Application launcher
- **nwg-dock** — Dock panel
- **fuzzel** — Lightweight launcher (dmenu-like, Wayland-native)

### Notifications
- **dunst** and **swaync** are both installed — only one should be active at a time
- Check which is running: `systemctl --user status dunst swaync`

### Wallpaper
- **swww** — Animated wallpaper daemon (Wayland)
- **hyprpaper** — Static wallpaper (backup/alternative)

### Screenshots & Screen
- **grim** — Screenshot utility (Wayland)
- **slurp** — Region selection tool
- **wl-clipboard** — Clipboard manager (Wayland, replaces xclip)

### Theme
- **Catppuccin Mocha** applied to: GTK, Hyprland borders, Waybar CSS, Kitty colors, Starship prompt

## Terminal & Shell
- **Kitty** — GPU-accelerated terminal (Wayland-native)
- **zsh** — Default shell
- **starship** — Cross-shell prompt
- Verify: `echo $SHELL; pacman -Q kitty starship`

## Audio
- **PipeWire** — Audio/video server (replaces PulseAudio)
- **WirePlumber** — Session manager for PipeWire
- **pipewire-pulse** — PulseAudio compatibility layer
- **pipewire-jack** — JACK compatibility layer
- All managed as systemd user services
- Verify: `pactl info; wpctl status`

## Development Tools

Rather than a hardcoded inventory, query what's installed at runtime:

```bash
# Editors & IDEs
pacman -Q code neovim qtcreator 2>/dev/null

# Build systems
pacman -Q cmake meson ninja make 2>/dev/null

# Languages & runtimes
python --version; uv --version; gcc --version; rustc --version 2>/dev/null

# Containers
pacman -Q docker docker-compose 2>/dev/null

# Documents & writing
pacman -Qs texlive tectonic 2>/dev/null

# AI tools
pacman -Q opencode-bin 2>/dev/null; which gemini 2>/dev/null

# Embedded
# PlatformIO is a VS Code extension — check via `pio --version` if CLI installed

# General package search
pacman -Qs <keyword>
```

**Key conventions** (these don't change):
- Python projects use **`uv`** (never pip globally) — see dev-workflow skill
- Version control uses **git** + **gh** with Gitflow workflow — see dev-workflow skill
- Containers use **Docker** + **Docker Compose** (systemd system service)

## Key System Services

Discover active services at runtime rather than relying on a hardcoded list:

```bash
# User services (display, audio, notifications)
systemctl --user list-unit-files --state=enabled

# System services (docker, network, bluetooth, etc.)
systemctl list-unit-files --state=enabled | grep enabled
```

## Keyboard & Input
- **Layout:** Latin American (`latam`)
- **Config:** Set in Hyprland via `input:kb_layout = latam`
- Verify: `hyprctl getoption input:kb_layout`

## VPN
- **OpenVPN** — Used for lab access
- Config: `client_ernesto.ovpn` → connects to `200.1.17.171:21101`
- Provides access to lab network `10.8.0.x`

## Package Count
- Use `pacman -Qq | wc -l` to check current count
