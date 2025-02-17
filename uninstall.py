#! /usr/bin/env python
"""
    Created on 2018-10-31
    
    @author: lingjie
    @name:   uninstall
"""

import os
import sys
import shutil
import glob
import _func

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
    print(f"Changed to directory: {os.getcwd()}")

    # Remove 'tmp' and 'template' directories if they exist
    for dir_name in ["tmp", "template"]:
        dir_path = os.path.join(install_dir, dir_name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"Removed directory: {dir_name}")

    # Remove all files except 'install.py' and 'uninstall.py'
    for file_path in glob.glob(os.path.join(install_dir, "*")):
        if file_path.startswith(os.path.join(install_dir, 'tmp')) \
            or file_path.startswith(os.path.join(install_dir, 'template')):
            continue

        dirname, filename = os.path.split(file_path)
        if filename in ["install.py", "uninstall.py"]:
            continue

        try:
            print(f"Removing... {filename}")
            os.remove(file_path)
            print(f"Removed {filename}")
        except OSError as e:
            print(f"Error removing {filename}: {e}")

    # Restore the original working directory
    os.chdir(cwd)

    # Print uninstallation success message
    message = "=       Uninstalled!"
    _func.print_banner(message)

if __name__ == "__main__":
    main()
