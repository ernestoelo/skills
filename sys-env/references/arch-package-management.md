# Arch Package Management Guide

This guide covers safe package operations on Arch Linux to avoid system crashes. Use pacman or yay (AUR helper).

## Basic Commands
- **Check installed**: `pacman -Q <package>`
- **Info**: `pacman -Si <package>`
- **Search**: `pacman -Ss <query>`
- **Install/Update**: `sudo pacman -S <package>` (updates if exists)
- **Remove**: `sudo pacman -R <package>`
- **Remove with deps**: `sudo pacman -Rs <package>`
- **Clean cache**: `sudo pacman -Sc`

## Dev Environment Packages
Based on common workspaces (C/C++, Python, PlatformIO, LaTeX, R, OpenCV):
- **C/C++**: gcc, clang, make. Install: `sudo pacman -S gcc clang make`
- **Python**: python, pip, conda (miniforge3). Install: `sudo pacman -S python python-pip`
- **PlatformIO**: platformio, avrdude, esptool. Install: `yay -S platformio avrdude esptool`
- **LaTeX**: texlive, biber. Install: `sudo pacman -S texlive-core biber`
- **R**: r, rstudio. Install: `sudo pacman -S r rstudio-desktop-bin`
- **OpenCV**: opencv, python-opencv. Install: `sudo pacman -S opencv python-opencv`

## Safety Checks
- **Conflicts**: `pacman -Qi <package>` for dependencies.
- **Orphans**: `pacman -Qdt` to find unused.
- **Update all**: `sudo pacman -Syu` (careful with breaking changes).
- **Downgrade if crash**: `sudo pacman -U /var/cache/pacman/pkg/<package>-version.pkg.tar.zst`

## Best Practices
- Backup with `timeshift` before major changes.
- Test in live USB if risky.
- Use `--needed` to avoid reinstalls.
- For AUR: `yay -S <package>` with caution.