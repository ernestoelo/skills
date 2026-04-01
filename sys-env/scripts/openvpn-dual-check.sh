#!/usr/bin/env bash
# openvpn-dual-check.sh
# Read-only diagnostic for dual OpenVPN profile stability on Arch + systemd-resolved.

set -euo pipefail

WILDSENSE_REMOTE="${WILDSENSE_REMOTE:-200.1.17.171}"
ENVIRONBIO_REMOTE="${ENVIRONBIO_REMOTE:-200.1.17.2}"
HAS_OPENVPN=0
HAS_TUN=0

ok() { printf '[OK] %s\n' "$*"; }
warn() { printf '[WARN] %s\n' "$*"; }
info() { printf '[INFO] %s\n' "$*"; }

echo "=== OpenVPN Process Check ==="
OPENVPN_LINES="$(ps -eo pid,ppid,user,cmd | grep -E 'openvpn( |$)' | grep -v grep || true)"
if [[ -z "$OPENVPN_LINES" ]]; then
    ok "No OpenVPN process found (expected when disconnected)."
else
    echo "$OPENVPN_LINES"
    COUNT="$(echo "$OPENVPN_LINES" | wc -l | tr -d ' ')"
    if (( COUNT > 2 )); then
        warn "Multiple OpenVPN processes detected ($COUNT). Verify no duplicate sessions are active."
    else
        ok "OpenVPN process count looks normal ($COUNT)."
    fi
    HAS_OPENVPN=1
fi

echo
echo "=== Tunnel Interface Check ==="
TUN_LINES="$(ip -br link show type tun | sed '/^$/d' || true)"
if [[ -z "$TUN_LINES" ]]; then
    ok "No active tun interfaces detected."
else
    echo "$TUN_LINES"
    HAS_TUN=1
fi

echo
info "Route check for VPN remotes (should point to physical gateway, not tunX)."
for remote in "$WILDSENSE_REMOTE" "$ENVIRONBIO_REMOTE"; do
    echo "--- ip route get $remote"
    ROUTE_LINE="$(ip route get "$remote" 2>/dev/null | head -n 1 || true)"
    echo "$ROUTE_LINE"
    if echo "$ROUTE_LINE" | grep -q ' dev tun'; then
        warn "Recursive routing risk: $remote currently resolves through tunnel interface."
    elif [[ -n "$ROUTE_LINE" ]]; then
        ok "$remote route does not use tunnel interface."
    else
        warn "Could not resolve route for $remote."
    fi
    echo
 done

echo "=== Resolver Health ==="
if command -v resolvectl >/dev/null 2>&1; then
    resolvectl statistics 2>/dev/null | sed -n '1,80p'
    TIMEOUTS="$(resolvectl statistics 2>/dev/null | awk '/Total Timeouts:/ {print $3; exit}' || echo 0)"
    if [[ -n "$TIMEOUTS" && "$TIMEOUTS" != "0" ]]; then
        if (( HAS_OPENVPN == 0 && HAS_TUN == 0 )); then
            info "Resolver timeouts are historical since boot ($TIMEOUTS); no active VPN/tun currently."
        else
            warn "Resolver has timeout history ($TIMEOUTS). Correlate with VPN flapping windows."
        fi
    else
        ok "No resolver timeouts reported."
    fi

    echo
    info "Current resolver summary:"
    resolvectl status 2>/dev/null | sed -n '1,70p'
else
    warn "resolvectl not available."
fi

echo
info "Recent log hints (last 120 relevant lines):"
if command -v rg >/dev/null 2>&1; then
    journalctl -b --no-pager 2>/dev/null \
        | rg -i 'openvpn|tun[0-9]|systemd-resolved|recursive routing|could not resolve|temporary failure|dns' \
        | tail -n 120
else
    journalctl -b --no-pager 2>/dev/null \
        | grep -Ei 'openvpn|tun[0-9]|systemd-resolved|recursive routing|could not resolve|temporary failure|dns' \
        | tail -n 120
fi

echo
info "Recommendation: if remotes route through tunX, pin /32 host routes for VPN servers via net_gateway before tunnel routes are applied."
