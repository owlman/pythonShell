#! /usr/bin/env python
"""
Uninstall script to remove all files from a specified installation directory.

Usage: python script.py <install_dir>
"""

import os
import sys
import shutil
import glob

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <install_dir>")
        sys.exit(1)

    install_dir = sys.argv[1]
    if not os.path.isdir(install_dir):
        print(f"Error: {install_dir} is not a valid directory.")
        sys.exit(1)

    # Save the current working directory
    cwd = os.getcwd()

    # Change to the installation directory
    os.chdir(install_dir)
    print(f"Current working directory: {os.getcwd()}")

    # Remove 'tmp' and 'template' directories if they exist
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")
    if os.path.exists("template"):
        shutil.rmtree("template")

    # Remove all files except 'install.py' and 'uninstall.py'
    for file in glob.glob(os.path.join(install_dir, "*")):
        if file.startswith(os.path.join(os.getcwd(), 'tmp')) or file.startswith(os.path.join(os.getcwd(), 'template')):
            continue

        dirname, filename = os.path.split(file)
        if filename in ["install.py", "uninstall.py"]:
            continue

        try:
            print(f"Removing... {filename}")
            os.remove(file)
            print(f"Removed {filename}")
        except OSError as e:
            print(f"Error removing {filename}: {e}")

    # Restore the original working directory
    os.chdir(cwd)

    # Print uninstallation success message
    message = "Uninstalled!"
    print("=" * (len(message) + 10))
    print("=" * (len(message) + 8) + message + "=" * (len(message) + 8))
    print("=" * (len(message) + 10))

if __name__ == "__main__":
    main()
