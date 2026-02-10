import sys
import subprocess
import importlib


def check_libs(libs: list) -> bool:
    """Check if required libraries are installed."""
    missing = []
    for lib in libs:
        try:
            importlib.import_module(lib)
            print(f"✅ {lib} installed")
        except ImportError:
            missing.append(lib)
            print(f"❌ {lib} missing")
    return len(missing) == 0


def check_jetson():
    """Basic check for Jetson/ZedBox compatibility."""
    try:
        result = subprocess.run(["uname", "-a"], capture_output=True, text=True)
        if "tegra" in result.stdout.lower():
            print("✅ Jetson detected")
            return True
        else:
            print("⚠️ Not on Jetson, but compatible")
            return True
    except:
        print("⚠️ Cannot detect hardware")
        return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Check environment compatibility for recursive-context."
    )
    parser.add_argument(
        "--libs",
        nargs="+",
        default=["pypdf", "spacy", "pytesseract"],
        help="Libraries to check",
    )
    args = parser.parse_args()

    print("=== Environment Check for Recursive-Context ===")
    libs_ok = check_libs(args.libs)
    hw_ok = check_jetson()
    if libs_ok and hw_ok:
        print("✅ Environment ready")
        sys.exit(0)
    else:
        print("❌ Environment issues detected")
        sys.exit(1)
