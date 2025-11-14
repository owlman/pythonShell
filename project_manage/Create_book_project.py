#!/usr/bin/env python3
"""
Created on 2019-06-17

Author: lingjie
Name: create_book_project
Usage:
    python create_book_project.py <project_dir> [projectname]

Description:
    project_dir: Path where the project should be created.
    projectname: Name of the new project (default: "book_proj").
    The project template is stored in the "template/book_proj.zip" file.

This script will:
    - Create the project directory if it does not exist.
    - Extract the template zip file.
    - Move it into the target project directory.
"""

import os
import sys
import shutil
import zipfile
import _func

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: create_book_project.py <project_dir> [projectname]")
        exit(1)

    scriptname = os.path.basename(sys.argv[0])
    _func.print_banner(f"Starting {scriptname} .....")

    projectdir = sys.argv[1]
    projectname = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] else "book_proj"

    if not os.path.exists(projectdir):
        os.makedirs(projectdir)

    # Paths
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    template_zip = os.path.join(scriptdir, "template", "book_proj.zip")
    targetdir = os.path.join(projectdir, projectname)

    # Remove existing target dir if exists
    if os.path.exists(targetdir):
        shutil.rmtree(targetdir)

    print(f"Creating your project at {targetdir} ...")

    # Extract zip using Python built-in module
    try:
        with zipfile.ZipFile(template_zip, 'r') as zip_ref:
            zip_ref.extractall(targetdir)
    except Exception as e:
        print(f"Failed to extract template: {e}")
        exit(1)

    _func.print_banner(f"{scriptname} has been executed successfully.")


if __name__ == "__main__":
    main()
