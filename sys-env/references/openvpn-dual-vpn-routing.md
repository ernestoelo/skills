# OpenVPN Dual Profile Routing and DNS Stability

This guide documents stable operation when running both:
- EnvironBio profile
- WildSense profile

on the same Arch Linux host with systemd-resolved.

## Root Cause Pattern

Intermittent DNS failures often come from route recursion between tunnels, not from resolved itself.

Typical evidence:
- repeated tunnel up/down events (tun0/tun1/tun2)
- frequent `systemd-resolved` DNS/default-route updates on tunnel links
- `ip route get <vpn-server-ip>` resolving through `tunX`
- kernel logs with repeated tunnel peer deletion events

## Why It Happens

If profile A pushes a route covering profile B's server subnet (or vice versa), traffic to VPN server B may be sent into tunnel A.
That creates recursive routing and repeated reconnect attempts.

## Stable Strategy

1. Pin each VPN server IP as host route (`/32`) through `net_gateway`.
2. Prevent duplicate instances of the same profile.
3. Ensure stop path removes process + pinned route + resolver cache state.
4. Prefer managed wrappers over raw `sudo openvpn ...` in ad-hoc terminals.

## Operational Commands

Use managed controller commands:

```bash
vpnctl up environbio
vpnctl up wildsense
vpnctl status
vpnctl down environbio
vpnctl down wildsense
vpnctl down all
vpnctl heal-dns
```

## Terminal Close Behavior (Super+D / killactive)

If VPN is launched with managed wrapper in attached mode, terminal closure sends HUP/TERM to the wrapper.
The wrapper trap performs cleanup:
- terminate matching OpenVPN process chain
- remove pinned server route
- reset resolver caches/features

If VPN is launched with raw detached commands, terminal closure may leave orphaned OpenVPN processes.

## Verification Checklist

```bash
/home/p3g4sus/.copilot/skills/sys-env/scripts/openvpn-dual-check.sh
```

Expected:
- VPN server remotes resolve via physical gateway (not tunX)
- no duplicate profile instances
- resolver timeout counters do not keep increasing during steady state
