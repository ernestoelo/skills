#!/usr/bin/env bash
# pre-install-check.sh — Assess risk level before installing packages on Arch Linux
#
# Usage: bash pre-install-check.sh <package-name> [package-name...]
#
# Outputs: SAFE / CAUTION / HIGH RISK for each package with explanation.
# Does NOT install anything — dry-run only.

set -euo pipefail

# High-risk package patterns (GPU, audio, display, kernel)
HIGH_RISK_PATTERNS=(
    "mesa" "vulkan" "libdrm" "libva" "vdpau" "egl" "gbm"
    "xorg" "xf86" "wayland" "wlroots" "hyprland"
    "pipewire" "pulseaudio" "jack2" "wireplumber" "alsa-lib"
    "linux" "linux-lts" "linux-headers" "linux-lts-headers"
    "nvidia" "amdgpu-pro" "rocm"
    "systemd" "dbus" "glib2" "glibc"
)

# Packages that should NEVER be installed on this system
BLACKLIST=(
    "nvidia" "nvidia-dkms" "nvidia-utils" "nvidia-settings"
    "lib32-nvidia-utils" "nvidia-lts"
    "vulkan-amdgpu-pro" "amdgpu-pro" "amdgpu-pro-libgl"
    "pulseaudio" "pulseaudio-alsa" "pulseaudio-jack" "pulseaudio-bluetooth"
    "jack2"
    "xf86-video-amdgpu" "xf86-video-vesa" "xf86-video-fbdev"
)

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BOLD='\033[1m'
NC='\033[0m'

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <package-name> [package-name...]"
    echo ""
    echo "Assesses installation risk for packages on this Arch Linux + Hyprland system."
    echo "Does NOT install anything."
    exit 1
fi

check_package() {
    local pkg="$1"
    local risk="SAFE"
    local reasons=()

    # Check blacklist
    for blocked in "${BLACKLIST[@]}"; do
        if [[ "$pkg" == "$blocked" ]]; then
            echo -e "${RED}${BOLD}[BLOCKED]${NC} ${BOLD}$pkg${NC}"
            echo "  This package is blacklisted for this system."
            case "$pkg" in
                nvidia*) echo "  Reason: No NVIDIA GPU locally — AMD Radeon integrated only." ;;
                pulseaudio*) echo "  Reason: Conflicts with PipeWire audio stack." ;;
                jack2) echo "  Reason: Conflicts with pipewire-jack." ;;
                xf86-video*) echo "  Reason: X11 DDX driver — unnecessary on Wayland/Hyprland." ;;
                *amdgpu-pro*) echo "  Reason: Proprietary AMD driver — conflicts with mesa/RADV." ;;
            esac
            echo ""
            return
        fi
    done

    # Check if already installed
    if pacman -Qi "$pkg" &>/dev/null; then
        reasons+=("Already installed (upgrade only)")
    fi

    # Check high-risk patterns
    for pattern in "${HIGH_RISK_PATTERNS[@]}"; do
        if [[ "$pkg" == *"$pattern"* ]]; then
            risk="HIGH RISK"
            reasons+=("Matches critical pattern: $pattern")
        fi
    done

    # Check if package exists in repos
    local pkg_info
    if pkg_info=$(pacman -Si "$pkg" 2>/dev/null); then
        # Check for conflicts with installed packages
        local conflicts
        conflicts=$(echo "$pkg_info" | grep -i "Conflicts With" | sed 's/.*: //')
        if [[ -n "$conflicts" && "$conflicts" != "None" ]]; then
            risk="HIGH RISK"
            reasons+=("Has conflicts: $conflicts")
        fi

        # Check for replaces
        local replaces
        replaces=$(echo "$pkg_info" | grep -i "Replaces" | sed 's/.*: //')
        if [[ -n "$replaces" && "$replaces" != "None" ]]; then
            if [[ "$risk" != "HIGH RISK" ]]; then risk="CAUTION"; fi
            reasons+=("Replaces: $replaces")
        fi

        # Check dependencies for risky packages
        local deps
        deps=$(echo "$pkg_info" | grep -i "Depends On" | sed 's/.*: //')
        for pattern in "${HIGH_RISK_PATTERNS[@]}"; do
            if echo "$deps" | grep -qi "$pattern"; then
                if [[ "$risk" != "HIGH RISK" ]]; then risk="CAUTION"; fi
                reasons+=("Depends on critical package matching: $pattern")
                break
            fi
        done
    elif yay -Si "$pkg" &>/dev/null; then
        if [[ "$risk" != "HIGH RISK" ]]; then risk="CAUTION"; fi
        reasons+=("AUR package — review PKGBUILD before installing")
    else
        risk="CAUTION"
        reasons+=("Package not found in repos or AUR")
    fi

    # Print result
    case "$risk" in
        "SAFE")
            echo -e "${GREEN}${BOLD}[SAFE]${NC} ${BOLD}$pkg${NC}"
            ;;
        "CAUTION")
            echo -e "${YELLOW}${BOLD}[CAUTION]${NC} ${BOLD}$pkg${NC}"
            ;;
        "HIGH RISK")
            echo -e "${RED}${BOLD}[HIGH RISK]${NC} ${BOLD}$pkg${NC}"
            ;;
    esac

    if [[ ${#reasons[@]} -eq 0 ]]; then
        echo "  No issues detected."
    else
        for reason in "${reasons[@]}"; do
            echo "  - $reason"
        done
    fi
    echo ""
}

echo "=== Pre-Install Safety Check ==="
echo "System: Arch Linux + Hyprland (Wayland) + AMD Radeon (amdgpu) + PipeWire"
echo ""

for pkg in "$@"; do
    check_package "$pkg"
done

echo "---"
echo "Legend: SAFE = proceed | CAUTION = review first | HIGH RISK = read compatibility-matrix.md | BLOCKED = never install"
