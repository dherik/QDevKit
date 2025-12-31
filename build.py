#!/usr/bin/env python3
"""
QDevKit Build Script
Cross-platform build script for creating distributables
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and print output"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
        sys.exit(1)
    return result


def build_pyinstaller():
    """Build using PyInstaller"""
    print("=" * 60)
    print("Building QDevKit with PyInstaller...")
    print("=" * 60)

    # Check if spec file exists
    spec_file = Path("QDevKit.spec")
    if not spec_file.exists():
        print(f"Error: {spec_file} not found!")
        sys.exit(1)

    # Run PyInstaller
    run_command(["pyinstaller", "--clean", str(spec_file)])

    print("\n✅ PyInstaller build completed!")
    print(f"Output directory: dist/QDevKit/")


def build_appimage():
    """Build AppImage for Linux"""
    if platform.system() != "Linux":
        print("AppImage builds are only supported on Linux")
        return

    print("\n" + "=" * 60)
    print("Building AppImage...")
    print("=" * 60)

    appimage_script = Path("build/linux/appimage/build-appimage.sh")
    if not appimage_script.exists():
        print(f"Error: {appimage_script} not found!")
        print("Please create the AppImage build script first.")
        sys.exit(1)

    # Make script executable
    os.chmod(appimage_script, 0o755)

    # Run AppImage build
    run_command([str(appimage_script)], cwd=Path.cwd())

    print("\n✅ AppImage build completed!")


def main():
    """Main build function"""
    import argparse

    parser = argparse.ArgumentParser(description="Build QDevKit")
    parser.add_argument(
        "--appimage",
        action="store_true",
        help="Build AppImage (Linux only)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean build directories before building"
    )

    args = parser.parse_args()

    # Clean build directories if requested
    if args.clean:
        print("Cleaning build directories...")
        for dir_name in ["build", "dist"]:
            if Path(dir_name).exists():
                shutil.rmtree(dir_name)
                print(f"Removed {dir_name}/")

    # Build with PyInstaller
    build_pyinstaller()

    # Build AppImage if requested
    if args.appimage:
        build_appimage()

    print("\n" + "=" * 60)
    print("Build completed successfully!")
    print("=" * 60)

    # Show platform-specific instructions
    system = platform.system()
    if system == "Linux":
        print("\nTo run the application:")
        print("  ./dist/QDevKit/QDevKit")
        if args.appimage:
            print("\nOr use the AppImage:")
            print("  ./dist/QDevKit-x86_64.AppImage")
    elif system == "Windows":
        print("\nTo run the application:")
        print("  dist\\QDevKit\\QDevKit.exe")
    elif system == "Darwin":  # macOS
        print("\nTo run the application:")
        print("  dist/QDevKit/QDevKit.app/Contents/MacOS/QDevKit")


if __name__ == "__main__":
    main()
