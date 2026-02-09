# Remote Targets

Remote machines accessed via SSH. These have **completely different** package managers, OSes, and hardware constraints from the local Arch workstation.

## Network Topology

```
Local laptop (Arch) → OpenVPN → Lab Network (10.8.0.x)
                                  ├── Lab PC (10.8.0.21)
                                  └── ZedBox/Jetson (10.31.214.170 via SSH jump)
```

VPN must be active to reach any remote target.

## Lab PC

| Property        | Value                          |
|-----------------|--------------------------------|
| IP              | `10.8.0.21`                    |
| OS              | Ubuntu (likely 22.04 or 24.04) |
| Package manager | `apt`                          |
| GPU             | NVIDIA (CUDA capable)          |
| Access          | Direct SSH over VPN            |

**Key differences from local:**
- Uses `apt`, NOT `pacman`
- Has NVIDIA GPU with CUDA — can run GPU workloads
- Ubuntu packages often lag behind Arch versions

## ZedBox / Jetson

| Property        | Value                                    |
|-----------------|------------------------------------------|
| IP              | `10.31.214.170`                          |
| Access          | SSH jump through Lab PC                  |
| OS              | JetPack (Ubuntu-based, NVIDIA L4T)       |
| Package manager | `apt`                                    |
| GPU             | NVIDIA Jetson (CUDA, TensorRT)           |
| SDK             | ZED SDK v4 (stereo camera)               |

**Key differences from local:**
- ARM64 architecture (not x86_64)
- JetPack-specific packages — do NOT install generic Ubuntu CUDA packages
- ZED SDK has its own installer — do NOT use apt for ZED packages
- Limited storage — be conservative with package installations

## SSH Workflow

```bash
# Connect to Lab PC (VPN must be active)
ssh user@10.8.0.21

# Connect to ZedBox (via jump host)
ssh -J user@10.8.0.21 user@10.31.214.170
```

VS Code Remote SSH is configured for these targets in `~/.ssh/config`.

## Rules for Remote Package Management

1. **Always verify which machine you're on** before running package commands
   - `hostname` or check prompt
   - `cat /etc/os-release` for OS info

2. **Never run `pacman` on remote targets** — they use `apt`

3. **Never run `apt` locally** — Arch uses `pacman`/`yay`

4. **Jetson-specific:**
   - Use `sudo apt install` for system packages
   - Use NVIDIA's JetPack package repos (already configured)
   - ZED SDK: use the official installer script, not apt
   - CUDA version is tied to JetPack — do NOT upgrade CUDA independently

5. **Lab PC-specific:**
   - Standard Ubuntu apt workflow
   - NVIDIA drivers managed via `ubuntu-drivers` or manual `.run` installer
   - Python environments: use `uv` or `venv`, same as local

## VPN Connection

```bash
# Connect
sudo openvpn --config /path/to/client_ernesto.ovpn

# Verify
ip addr show tun0    # Should show 10.8.0.x address
ping 10.8.0.21       # Should reach Lab PC
```
