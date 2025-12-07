#!/usr/bin/env python3
"""
    Created on 2019-06-17

    Author: lingjie
    Name: create_book_project
    Usage:
        create-book-project <project_directory> [project_name]

    Description:
        <project_directory>: Path where the project should be created.
        [project_name]: Name of the new project (default: "book_proj").
        The project template is stored in the "template/book_proj.zip" file.

    This script will:
        - Create the project directory if it does not exist.
        - Extract the template zip file.
        - Move it into the target project directory.
"""

import os
import shutil
import sys
import zipfile
import common

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: create-book-project <project_directory> [project_name]")
        exit(1)

    script_name = os.path.basename(sys.argv[0])
    common.print_banner(f"Starting {script_name} .....")

    project_directory = sys.argv[1]
    project_name = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] else "book_proj"

    if not os.path.exists(project_directory):
        os.makedirs(project_directory)

    # Paths
    script_directory = os.path.dirname(os.path.abspath(__file__))
    template_zip = os.path.join(script_directory, "template", "book_proj.zip")
    target_directory = os.path.join(project_directory, project_name)

    # Remove existing target dir if exists
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)

    print(f"Creating your project at {target_directory} ...")

    # Extract zip using Python built-in module
    try:
        with zipfile.ZipFile(template_zip, 'r') as zip_ref:
            zip_ref.extractall(target_directory)
    except Exception as e:
        print(f"Failed to extract template: {e}")
        exit(1)

    common.print_banner(f"{script_name} has been executed successfully.")

if __name__ == "__main__":
    main()
