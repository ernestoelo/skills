# Systemd Ordering Cycles & Boot Delays - Arch Linux

## Problem Summary

When Arch Linux boots slowly or freezes with `[SKIP]` messages, the culprit is usually a **systemd Ordering Cycle** - a circular dependency where Service A must start before Service B, but Service B is configured to start before Service A.

When systemd detects this impossible loop, it **breaks the cycle** by skipping critical services, which cascades into missing D-Bus, broken Wi-Fi, DNS resolution failures, or multi-minute boot delays.

## Common Causes (in order of prevalence)

### 1. Custom Driver Load Services (MOST COMMON)
**Problem**: A custom `.service` file (like `rtw88-load.service`) trying to load Wi-Fi/GPU drivers at boot.

**Why it breaks**: systemd is **not designed** to load kernel modules during early boot. It creates impossible dependency chains with `sysinit.target` and `basic.target`.

**Symptoms**:
- `[SKIP] Network Name Resolution` messages
- D-Bus fails to start
- `iwctl` doesn't work (no Wi-Fi)
- 1+ minute boot delay

**Solution**: 
```bash
# Find and disable the offending service
sudo systemctl disable rtw88-load.service  # or whatever .service file it is
sudo systemctl mask rtw88-load.service

# Use the CORRECT way: kernel module loading configuration
# For Realtek drivers specifically:
sudo nano /etc/modules-load.d/rtw88.conf
# Add: rtw88
```

### 2. Multiple Network Managers Fighting
**Problem**: Having both `dhcpcd`, `systemd-networkd`, `NetworkManager`, and `iwd` enabled simultaneously.

**Symptoms**:
- IP assignment race conditions
- DNS resolution fails (can connect to router, can't access websites)
- Networking services keep restarting
- Boot hangs at network.target

**Solution**:
```bash
# Pick ONE network manager stack. For minimal/fast setups:

# Option A: iwd + systemd-networkd (recommended for Arch + Hyprland)
sudo systemctl enable iwd
sudo systemctl enable systemd-networkd
sudo systemctl enable systemd-resolved
# Then DISABLE all others:
sudo systemctl disable dhcpcd
sudo systemctl disable wpa_supplicant
sudo systemctl disable NetworkManager

# Option B: If you really need NetworkManager
sudo systemctl enable NetworkManager
# Disable everything else
sudo systemctl disable iwd
sudo systemctl disable dhcpcd
sudo systemctl disable systemd-networkd
```

### 3. Residual Override Configurations
**Problem**: Old `override.conf` files from failed troubleshooting attempts still exist and create bad dependencies.

**Symptoms**:
- `[SKIP]` messages even after fixing the underlying cause
- Services appear enabled but fail silently
- Boot times don't improve even after removing the culprit service

**Solution**:
```bash
# Purge all override configurations and return to defaults
sudo systemctl revert systemd-networkd.service
sudo systemctl revert systemd-resolved.service
sudo systemctl revert docker.service
# For any custom service:
sudo systemctl revert my-custom.service

# Clean up orphaned override files
sudo rm -rf /etc/systemd/system/*.service.d/override.conf
sudo systemctl daemon-reload
```

## Diagnosis Tools

### Check for Ordering Cycles
```bash
# See which services are skipped
journalctl -b | grep SKIP

# See dependency chain
systemd-analyze critical-chain

# See slowest services/units
systemd-analyze blame | head -20

# Full dependency tree (helps identify cycles)
systemctl list-dependencies --all
```

### Verify Network Manager Setup
```bash
# Check which network manager is active
systemctl status iwd
systemctl status systemd-networkd
systemctl status dhcpcd
systemctl status NetworkManager
systemctl status wpa_supplicant

# List all enabled network-related services
systemctl list-units --type=service | grep -i network

# Check actual network interfaces
ip a
nmcli device status  # if using NetworkManager
```

### Find Custom Services Causing Problems
```bash
# List all custom services in system
sudo ls -la /etc/systemd/system/*.service

# Check for driver-loading services
sudo grep -r "modprobe\|insmod" /etc/systemd/system/

# Check for circular dependencies explicitly
systemd-analyze verify
```

## The Correct Way to Load Kernel Modules

**❌ WRONG** (what causes ordering cycles):
```ini
# /etc/systemd/system/rtw88-load.service
[Unit]
Description=Load RTW88 Driver
After=sysinit.target

[Service]
Type=oneshot
ExecStart=/sbin/modprobe rtw88

[Install]
WantedBy=multi-user.target
```

**✅ CORRECT** (native Linux approach):
```bash
# /etc/modules-load.d/rtw88.conf
rtw88

# For module options:
# /etc/modprobe.d/rtw88.conf
options rtw88 param1=value1 param2=value2
```

Then systemd loads these automatically during proper early boot, **without creating cycles**.

## Golden Rules for Arch Stability

1. **Never use `.service` files to load kernel modules**
   - Use `/etc/modules-load.d/` and `/etc/modprobe.d/` instead
   - These are processed by systemd-modules-load.service at the right time

2. **Pick ONE network manager and DISABLE all others**
   - iwd + systemd-networkd (minimal, fast)
   - OR NetworkManager (full-featured)
   - NEVER mix them

3. **Use `systemctl revert` to clean up failed attempts**
   - Much faster than reinstalling
   - Restores original "factory" service configs

4. **Monitor boot every time you troubleshoot**
   ```bash
   systemd-analyze blame
   journalctl -b -p err
   systemctl status <service>
   ```

5. **When in doubt, check dependencies**
   ```bash
   systemctl show <service> | grep -E "After|Before|Wants|Requires"
   ```

## Reference: RTW88 (Realtek Wi-Fi) Specific

If you have a Realtek RTW88 Wi-Fi card:

```bash
# Install the driver package (not a custom service!)
sudo pacman -S rtw88-dkms  # Or rtl8188fu, rtl8192du depending on chip

# Configure it properly (NOT with a custom service):
cat > /etc/modprobe.d/rtw88.conf <<EOF
# Realtek RTW88 options
options rtw88 power_save=N
EOF

cat > /etc/modules-load.d/rtw88.conf <<EOF
rtw88
EOF

# Then reboot - systemd handles the rest
sudo reboot
```

## Quick Troubleshooting Flowchart

```
Boot slow or hangs?
├── See [SKIP] messages?
│   ├── Check for custom .service driver loaders
│   │   └── Fix: Use /etc/modules-load.d/ instead
│   └── Check for ordering cycles
│       └── Fix: systemctl revert + daemon-reload
│
├── Can't connect to Wi-Fi?
│   ├── Check if D-Bus running: systemctl status dbus
│   │   └── If not: check for cycles (above)
│   └── Check which network manager: ip a && systemctl status iwd
│
├── Connected to router but no internet?
│   ├── Check DNS: cat /etc/resolv.conf
│   └── Fix: Enable systemd-resolved, disable dhcpcd
│
└── Everything works but boot slow?
    └── Check: systemd-analyze blame
        └── Might be unrelated (disk I/O, TPM, NVMe init)
```

## See Also
- [Arch Linux systemd Documentation](https://man.archlinux.org/man/systemd.unit.5)
- [How systemd resolves ordering cycles](https://www.freedesktop.org/wiki/Software/systemd/BootCycle/)
- [RTW88 Device Driver Wiki](https://github.com/morrissimo/rtw88)
