#! /usr/bin/env python
"""
    Created on 2016-5-31

    Author: lingjie
    Name:   install
    Usage:  install.py <install_directory>
    Description: Install all the necessary files to the specified directory.
        - <install_directory>: The directory where the files will be installed.
"""

import os
import sys
import shutil
import glob

# Add common module path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
import common

def main():
    # Check the number of arguments
    if len(sys.argv) != 2:
        print("Usage: install.py <install_directory>")
        sys.exit(1)

    # Print the banner
    script_name = os.path.basename(sys.argv[0])
    common.print_banner(f"Starting {script_name} .....")    

   # Get all the python files in the current directory
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    files = glob.glob(os.path.join(current_directory, "**", "*.py"), recursive=True)
    template_files = glob.glob(os.path.join(current_directory, "**", "*.zip"),
                               recursive=True)

    # Save the current working directory
    cwd = os.getcwd() 
    print("PWD: " + cwd)
    # Change to the installation directory
    install_directory = sys.argv[1]
    os.chdir(install_directory)

    # Create 'tmp' and 'template' directories if they do not exist
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    if not os.path.exists("template"):
        os.mkdir("template")
        for file in template_files:
            filename = os.path.basename(file)
            print("copying..." + filename)
            shutil.copy(file, os.path.join("template", filename))

    # Copy all the python files to the installation directory
    for file in files:
        filepath = os.path.dirname(file)
        dirname = os.path.basename(filepath)
        filename = os.path.basename(file)
        if filename in ("install.py", "uninstall.py"):
            continue
        if dirname in ("tmp", "test", "__pycache__"):
            continue
        print("copying..." + filename)
        shutil.copy(file, filename)
        os.chmod(filename, os.stat(filename).st_mode | 0o111)

    # Restore the original working directory
    os.chdir(cwd)
    # Print the banner
    common.print_banner(f"{script_name} has been executed successfully.")

if __name__ == "__main__":
    main()
