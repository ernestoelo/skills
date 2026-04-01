# sys-env

System environment management skill for Arch Linux + Hyprland.

## Purpose

This skill provides reproducible checks and operational guidance for:
- package safety (pacman/yay + Python env boundaries)
- system services and boot diagnostics
- network and DNS stability checks
- environment integration with @architect workflows

## Canonical Structure

This skill follows the architect skill structure:

- SKILL.md: entrypoint, usage, references
- scripts/: executable checks and helpers
- references/: deep-dive documentation
- assets/: optional visual resources
- README.md: quick overview and navigation

## Quick Start

Run baseline checks:

```bash
/home/p3g4sus/.copilot/skills/sys-env/scripts/env_check.sh
/home/p3g4sus/.copilot/skills/sys-env/scripts/check-python-env.sh
```

Run OpenVPN dual-profile safety check:

```bash
/home/p3g4sus/.copilot/skills/sys-env/scripts/openvpn-dual-check.sh
```

## Related References

- references/systemd-ordering-cycles.md
- references/openvpn-dual-vpn-routing.md
- references/ARCHITECTURE-INTEGRATION.md
