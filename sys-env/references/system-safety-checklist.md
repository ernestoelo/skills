# System Safety Checklist

Use before/after package changes to avoid crashes.

## Pre-Change
- [ ] Backup system: `sudo timeshift --create`
- [ ] Check free space: `df -h`
- [ ] List critical services: `systemctl list-units --type=service`
- [ ] Note running processes: `ps aux`
- [ ] Backup configs: `cp -r ~/.config/hypr ~/hypr-backup` and `cp -r ~/.config/opencode ~/opencode-backup`
- [ ] Backup dev projects: `cp -r ~/Documents/Projects ~/Projects-backup`

## During Change
- [ ] Use `--dry-run` if available: `pacman -S --dry-run <package>`
- [ ] Monitor logs: `journalctl -f`
- [ ] Test in subshell if possible

## Post-Change
- [ ] Restart services: `sudo systemctl daemon-reload`
- [ ] Check boot: Reboot and verify.
- [ ] Verify packages: `pacman -Q`
- [ ] Test Hyprland: Launch and check waybar/kitty.
- [ ] Test dev builds: Run `make` in C++ project, `python -c` in OpenCV, `pio run` in PlatformIO.
- [ ] If crash: Boot live USB, chroot, fix.

## Recovery
- Downgrade: `sudo pacman -U /var/cache/pacman/pkg/...`
- Remove conflicting: `sudo pacman -Rdd <package>`
- Restore backups: `cp -r ~/hypr-backup/* ~/.config/hypr/`
- For dev: Restore ~/Projects-backup