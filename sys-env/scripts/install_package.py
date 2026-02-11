#!/usr/bin/env python3
"""
Generic package installer for sys-env.

Installs any Arch Linux package via pacman. Prioritizes NOPASSWD automation;
falls back to manual instructions if not configured.

Usage: python3 install_package.py <package_name>
Example: python3 install_package.py plantuml
"""

import subprocess
import sys


def is_package_installed(package):
    """Check if package is installed."""
    try:
        subprocess.run(
            ["pacman", "-Q", package], capture_output=True, text=True, check=True
        )
        print(f"Package '{package}' is already installed.")
        return True
    except subprocess.CalledProcessError:
        return False


def install_via_nopasswd(package):
    """Attempt installation using NOPASSWD sudo."""
    try:
        subprocess.run(
            ["sudo", "-n", "pacman", "-S", "--noconfirm", package],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"Package '{package}' installed successfully via NOPASSWD.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"NOPASSWD installation failed: {e.stderr}")
        return False


def provide_manual_instructions(package):
    """Provide manual installation instructions."""
    print(f"Package '{package}' not installed.")
    print("Configure NOPASSWD for automation or install manually:")
    print(f"  sudo pacman -S --noconfirm {package}")
    print("Or configure NOPASSWD by editing /etc/sudoers with visudo:")
    print("  your_username ALL=(ALL) NOPASSWD: /usr/bin/pacman")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 install_package.py <package_name>")
        sys.exit(1)

    package = sys.argv[1]

    if is_package_installed(package):
        return

    if install_via_nopasswd(package):
        return

    provide_manual_instructions(package)


if __name__ == "__main__":
    main()
