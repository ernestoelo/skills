#!/usr/bin/env python3
"""
Diagram generation script for dev-workflow.

Generates PNG diagrams from PlantUML files. If PlantUML is not installed,
provides instructions using sys-env for installation on Arch Linux.
"""

import subprocess
import sys
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
    """Provide sys-env style installation instructions."""
    print("Using @sys-env/SKILL.md for installation:")
    print("Run the following command to install PlantUML on Arch Linux:")
    print("  sudo pacman -S plantuml")
    print("(Refer to @sys-env/SKILL.md for package safety checks.)")
    # Optionally, try to install if running with privileges
    try:
        print("Attempting automatic installation...")
        subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "plantuml"], check=True)
        print("PlantUML installed successfully.")
        return True
    except subprocess.CalledProcessError:
        print("Installation failed. Please run manually or check @sys-env/SKILL.md.")
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
