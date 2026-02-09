# Software Stack

## Desktop Environment

### Compositor & Window Management
- **Hyprland** 0.53.x — Wayland compositor, dwindle layout
- **Config:** `~/.config/hypr/hyprland.conf` (Stow-managed)
- **Plugins:** None currently

### Bar & UI
- **Waybar** — Status bar (systemd user service)
- **nwg-drawer** — Application launcher (SUPER+A)
- **nwg-dock** — Dock panel (SUPER+D)
- **fuzzel** — Lightweight launcher (dmenu-like, Wayland-native)

### Notifications
- **dunst** — Lightweight notification daemon
- **swaync** — SwayNotificationCenter (alternative, also installed)
- Note: Only one should be active at a time

### Wallpaper
- **swww** — Animated wallpaper daemon (Wayland)
- **hyprpaper** — Static wallpaper (backup/alternative)

### Screenshots & Screen
- **grim** — Screenshot utility (Wayland)
- **slurp** — Region selection tool
- **wl-clipboard** — Clipboard manager (Wayland, replaces xclip)

### Theme
- **Catppuccin Mocha** applied to:
  - GTK apps (via `gsettings` or `~/.config/gtk-3.0/`)
  - Hyprland borders and colors
  - Waybar CSS
  - Kitty terminal colors
  - Starship prompt

## Terminal & Shell
- **Kitty** — GPU-accelerated terminal (Wayland-native)
- **zsh** — Shell with plugins (oh-my-zsh or manual)
- **starship** — Cross-shell prompt

## Audio
- **PipeWire** — Audio/video server (replaces PulseAudio)
- **WirePlumber** — Session manager for PipeWire
- **pipewire-pulse** — PulseAudio compatibility layer
- **pipewire-jack** — JACK compatibility layer
- All managed as systemd user services

## Editors & IDEs
- **VS Code** — Primary IDE (3 workspaces configured)
- **Neovim** — Terminal editor
- **QtCreator** — Qt/C++ development

## AI & Coding Tools
- **opencode** (`opencode-bin` from AUR) — AI coding assistant
- **gemini-cli** — Google Gemini CLI tool

## Development Toolchain

### Build Systems
- **cmake** — C/C++ build system
- **meson** + **ninja** — Alternative build system
- **make** — GNU Make

### Languages & Runtimes
- **gcc/g++** — C/C++ compiler
- **python** (3.12+) — via `uv` for project management
- **uv** — Python package/project manager (replaces pip/poetry)
- **rust** (if installed) — via rustup

### Embedded & Hardware
- **PlatformIO** — Embedded development (ESP32, Arduino, etc.)
- Accessed via VS Code extension or CLI

### Documents & Writing
- **texlive** — LaTeX distribution
- **tectonic** — Rust-based LaTeX compiler (faster builds)
- **R** — Statistical computing (if installed)

### Containers
- **Docker** — Container runtime (systemd system service)
- **Docker Compose** — Multi-container orchestration

### Version Control
- **git** — Version control
- **gh** — GitHub CLI
- Gitflow workflow (see dev-workflow skill)

## Key System Services

### User Services (systemctl --user)
| Service        | Purpose                    |
|----------------|----------------------------|
| waybar         | Status bar                 |
| pipewire       | Audio server               |
| wireplumber    | PipeWire session manager   |
| pipewire-pulse | PulseAudio compatibility   |
| swaync         | Notification center        |

### System Services (systemctl)
| Service          | Purpose                  |
|------------------|--------------------------|
| docker           | Container runtime        |
| NetworkManager   | Network management       |
| bluetooth        | Bluetooth support        |
| sshd             | SSH server (if enabled)  |

## Keyboard & Input
- **Layout:** Latin American (`latam`)
- **Config:** Set in Hyprland via `input:kb_layout = latam`
- **Keyboard rules:** `input:kb_options` in hyprland.conf

## VPN
- **OpenVPN** — Used for lab access
- Config: `client_ernesto.ovpn` → connects to `200.1.17.171:21101`
- Provides access to lab network `10.8.0.x`

## Package Count
- ~1450 packages installed (pacman + AUR)
- Use `pacman -Qq | wc -l` to check current count
