#!/usr/bin/env python3
"""
Diagram generation script for dev-workflow.

Generates PNG diagrams from PlantUML files. If PlantUML is not installed,
uses @sys-env generic installer for installation on Arch Linux.
"""

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
    """Install PlantUML via generic @sys-env installer."""
    try:
        subprocess.run(
            [
                "python3",
                "/home/p3g4sus/.copilot/skills/sys-env/scripts/install_package.py",
                "plantuml",
            ],
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def verify_diagram(png_file):
    """Verify the generated PNG diagram."""
    if not png_file.exists():
        print(f"PNG file not found: {png_file}")
        return False
    size = png_file.stat().st_size
    if size == 0:
        print(f"PNG file is empty: {png_file}")
        return False
    print(f"PNG verified: {png_file} ({size} bytes)")
    return True


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--diagram":
        print("Usage: python3 generate_diagrams.py --diagram <diagram_name>")
        print("Example: python3 generate_diagrams.py --diagram skills-architecture")
        sys.exit(1)

    diagram_name = sys.argv[2]
    puml_file = (
        Path(__file__).parent.parent / "assets" / "diagrams" / f"{diagram_name}.puml"
    )
    if not puml_file.exists():
        print(f"Error: {puml_file} not found.")
        sys.exit(1)
    png_file = puml_file.with_suffix(".png")

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        if not check_plantuml():
            if not install_plantuml_via_sys_env():
                print(f"Installation failed on attempt {attempt}.")
                continue
        try:
            subprocess.run(
                ["plantuml", str(puml_file)], check=True, capture_output=True
            )
            print(f"Diagram generated on attempt {attempt}: {png_file}")
            if verify_diagram(png_file):
                print(f"Diagram verified successfully on attempt {attempt}.")
                break
        except subprocess.CalledProcessError as e:
            print(f"Generation failed on attempt {attempt}: {e}")
        if attempt == max_attempts:
            print("Max attempts reached. Diagram generation failed.")
            sys.exit(1)


if __name__ == "__main__":
    main()
