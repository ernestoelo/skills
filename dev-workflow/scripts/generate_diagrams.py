#!/usr/bin/env python3
"""
Diagram generation script for dev-workflow.

Generates PNG diagrams from PlantUML files. If PlantUML is not installed,
provides instructions using sys-env for installation on Arch Linux.
"""

import getpass
import sys
import subprocess
from pathlib import Path


def check_plantuml():
    """Check if PlantUML is installed."""
    try:
        result = subprocess.run(
            ["plantuml", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print("PlantUML is installed.")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    print("PlantUML is not installed.")
    return False


def install_plantuml_via_sys_env():
    """Provide interactive prompt for password and install via @sys-env."""
    print("Activating @sys-env/SKILL.md for installation:")
    print(
        "Enter your sudo password to install PlantUML (interactive prompt for security):"
    )
    password = getpass.getpass("Password: ")
    try:
        # Use echo to pipe password to sudo -S
        proc = subprocess.run(
            ["sudo", "-S", "pacman", "-S", "--noconfirm", "plantuml"],
            input=password + "\n",
            text=True,
            capture_output=True,
            check=True,
        )
        print("PlantUML installed successfully via @sys-env.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e.stderr}")
        print("Check @sys-env/SKILL.md for manual installation or NOPASSWD config.")
        return False


def generate_diagram(diagram_name):
    """Generate PNG from .puml file."""
    puml_file = (
        Path(__file__).parent.parent / "assets" / "diagrams" / f"{diagram_name}.puml"
    )
    if not puml_file.exists():
        print(f"Error: {puml_file} not found.")
        sys.exit(1)

    try:
        subprocess.run(["plantuml", str(puml_file)], check=True)
        png_file = puml_file.with_suffix(".png")
        print(f"Diagram generated: {png_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating diagram: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--diagram":
        print("Usage: python3 generate_diagrams.py --diagram <diagram_name>")
        print("Example: python3 generate_diagrams.py --diagram skills-architecture")
        sys.exit(1)

    diagram_name = sys.argv[2]

    if not check_plantuml():
        if not install_plantuml_via_sys_env():
            sys.exit(1)

    generate_diagram(diagram_name)


if __name__ == "__main__":
    main()
