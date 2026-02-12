# Remote Setup for Jetson/ZedBox

Setup for remote access to NVIDIA Jetson or ZedBox devices.

## SSH Setup
- Install OpenSSH: `sudo pacman -S openssh`
- Enable: `sudo systemctl enable sshd`
- Start: `sudo systemctl start sshd`
- Connect: `ssh user@jetson-ip`

## Dev Environment Compatibilities
- **VS Code Remote**: Use remote-ssh extension for editing workspaces remotely.
- **Builds**: Run `make` for C++, `uv run` for Python, `pio run` for PlatformIO via SSH.
- **OpenCV/AI**: Sync models/data; ensure GPU libs (mesa on Jetson if NVIDIA).
- **LaTeX/R**: Process docs remotely with `pdflatex` or R scripts.

## Local Commands
- From workstation: SSH into device for package ops.
- Avoid direct installs; use SSH for safety.

## Considerations
- Power: Jetson needs stable power; monitor temps.
- GPU: NVIDIA drivers via pacman.
- Network: Static IP for reliable access.
- Backup: Use rsync for configs.

## Safety
- Don't modify critical services remotely without local access.
- Test commands locally first.