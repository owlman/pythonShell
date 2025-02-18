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
    # Check the number of arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py <install_dir>")
        sys.exit(1)

    # Get the installation directory
    install_dir = sys.argv[1]
    if not os.path.isdir(install_dir):
        print(f"Error: {install_dir} is not a valid directory.")
        sys.exit(1)
    else:
        _func.print_banner(f"Uninstalling {install_dir}...")

    # Save the current working directory
    cwd = os.getcwd()

    # Change to the installation directory
    os.chdir(install_dir)
    print(f"Changed to directory: {os.getcwd()}")

    # Remove 'tmp' and 'template' directories if they exist
    for dir in ["tmp", "template"]:
        dirpath = os.path.join(install_dir, dir)
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)
            print(f"Removed directory: {dir}")

    # Remove all files except 'install.py' and 'uninstall.py'
    for file_path in glob.glob(os.path.join(install_dir, "*")):
        # Skip '__pycache__', 'tmp' and 'template' directories
        if file_path.startswith(os.path.join(install_dir, 'tmp')) \
            or file_path.startswith(os.path.join(install_dir, 'template')) \
            or file_path.startswith(os.path.join(install_dir, '__pycache__')):
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
    _func.print_banner(f"Uninstallation of {install_dir} is complete.")

if __name__ == "__main__":
    main()
