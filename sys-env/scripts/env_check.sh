#!/bin/bash
# Quick environment check for Arch Linux + Hyprland
# Usage: ./env_check.sh

set -e

echo "Checking for required packages..."
for pkg in pacman yay systemctl; do
  if ! command -v $pkg &> /dev/null; then
    echo "Missing: $pkg"
  else
    echo "Found: $pkg"
  fi
done

echo "Checking for AMD GPU..."
lspci | grep -i amd || echo "AMD GPU not detected."

echo "Checking for Wayland/Hyprland..."
loginctl show-session $(loginctl | awk '/tty/ {print $1; exit}') -p Type | grep -i wayland || echo "Wayland not detected."

# Add more checks as needed

echo "Environment check complete."
