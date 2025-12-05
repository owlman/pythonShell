#!/usr/bin/env python3
"""
Created on 2018-10-31

Author: lingjie
Name: create_translation_project
Usage:
    python create_translation_project.py <project_dir> [project_name]

Description:
    project_dir: Path to the project directory.
    project_name: Name of the new project (default: "translation_proj").

This script will:
    - Create or overwrite the target project directory.
    - Extract the project template into the target directory.
"""

import os
import sys
import shutil
import zipfile
import common

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: create_translation_project.py <project_dir> [project_name]")
        sys.exit(1)

    scriptname = os.path.basename(sys.argv[0])
    common.print_banner(f"Starting {scriptname} .....")

    projectdir = sys.argv[1]
    projectname = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] else "translation_proj"
    targetdir = os.path.join(projectdir, projectname)

    # Create the project directory if it doesn't exist
    if not os.path.exists(projectdir):
        os.makedirs(projectdir)

    # Remove target directory if exists
    if os.path.exists(targetdir):
        shutil.rmtree(targetdir)

    print(f"Creating your project at {targetdir} ...")

    # Extract template zip
    template_zip = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template", "translation_proj.zip")
    try:
        with zipfile.ZipFile(template_zip, 'r') as zip_ref:
            zip_ref.extractall(targetdir)
    except Exception as e:
        print(f"Failed to extract template: {e}")
        sys.exit(1)

    common.print_banner(f"{scriptname} has been executed successfully.")

if __name__ == "__main__":
    main()
