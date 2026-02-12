# Hyprland Compatibilities

Hyprland is a Wayland compositor for Arch Linux. Ensure compatibilities to avoid crashes.

## Key Components
- **Wayland**: Base protocol; ensure apps support it (not X11).
- **PipeWire**: Audio/video; replaces PulseAudio/Jack.
- **AMD Radeon**: GPU drivers via mesa.

## Packages from Config (hyprland.conf)
- **kitty**: Terminal emulator. Install: `sudo pacman -S kitty`
- **waybar**: Status bar. Install: `sudo pacman -S waybar`
- **swww**: Wallpaper daemon. Install: `sudo pacman -S swww`
- **hypridle**: Idle manager. Install: `sudo pacman -S hypridle`
- **swaync**: Notifications. Install: `sudo pacman -S swaync`
- **polkit-gnome**: Auth agent. Install: `sudo pacman -S polkit-gnome`
- **gnome-keyring**: Keyring. Install: `sudo pacman -S gnome-keyring`
- **uwsm**: Session manager. Install: `yay -S uwsm`
- **nwg-drawer**: Menu. Install: `yay -S nwg-drawer`

## Dev Environment Compatibilities
- **VS Code/Editors**: code, kitty compatible with Wayland.
- **OpenCV/Python**: Ensure mesa for GPU acceleration; avoid CUDA conflicts on AMD.
- **PlatformIO**: Embedded tools work via SSH/remote.
- **LaTeX/R**: Docs/stats tools run in terminal (kitty).

## Compatibility Checks
- **GPU**: `lspci | grep VGA` for AMD. Install mesa, xf86-video-amdgpu.
- **Audio**: PipeWire with wireplumber. Conflicts with PulseAudio.
- **Services**: systemd for restarts: `sudo systemctl restart pipewire`.
- **Apps**: Use Wayland-native (firefox-wayland, alacritty).

## Known Issues
- Avoid mixing X11/Wayland apps.
- Radeon: Black screen? Check kernel modules (amdgpu).
- Remote: Use wlroots for VNC.

## Alternatives
- If crashes, fallback to sway or i3 with X11.