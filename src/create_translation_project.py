#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on 2018-10-31

    Author: lingjie
    Name: create_translation_project
    Usage:
        create-translation-project <project_directory> [project_name]

    Description:
        project_directory: Path to the project directory.
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
        print("Usage: create-translation-project <project_directory> [project_name]")
        sys.exit(1)

    script_name = os.path.basename(sys.argv[0])
    common.print_banner(f"Starting {script_name} .....")

    project_directory = sys.argv[1]
    project_name = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] else "translation_proj"
    target_directory = os.path.join(project_directory, project_name)

    # Create the project directory if it doesn't exist
    if not os.path.exists(project_directory):
        os.makedirs(project_directory)

    # Remove target directory if exists
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)

    print(f"Creating your project at {target_directory} ...")

    # Extract template zip
    template_zip = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template", "translation_proj.zip")
    try:
        with zipfile.ZipFile(template_zip, 'r') as zip_ref:
            zip_ref.extractall(target_directory)
    except Exception as e:
        print(f"Failed to extract template: {e}")
        sys.exit(1)

    common.print_banner(f"{script_name} has been executed successfully.")

if __name__ == "__main__":
    main()
