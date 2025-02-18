#! /usr/bin/env python
"""
    Created on 2016-5-31

    @author: lingjie
    @name:   install
"""

import os
import sys
import shutil
import glob
import _func

def main():
    # Check the number of arguments
    if len(sys.argv) != 2:
        print("Usage: install.py <install_dir>")
        sys.exit(1)

    # Print the banner
    scriptname = os.path.basename(sys.argv[0])
    _func.print_banner(f"Starting {scriptname} .....")    

   # Get all the python files in the current directory
    my_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    files = glob.glob(os.path.join(my_dir, "**", "*.py"), recursive=True)
    template_files = glob.glob(os.path.join(my_dir, "**", "*.zip"), recursive=True)

    # Save the current working directory
    cwd = os.getcwd() 
    print("PWD: " + cwd)
   # Change to the installation directory
    install_dir = sys.argv[1]
    os.chdir(install_dir)

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
        if dirname in ("tmp", "template", "__pycache__"):
            continue
        print("copying..." + filename)
        shutil.copy(file, filename)
        os.chmod(filename, os.stat(filename).st_mode | 0o111)

    # Restore the original working directory
    os.chdir(cwd)
    # Print the banner
    _func.print_banner(f"{scriptname} has been executed successfully.")

if __name__ == "__main__":
    main()
