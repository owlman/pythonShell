#! /usr/bin/env python
"""
    Created on 2018-10-31
    
    @author: lingjie
    @name:   create_translation_project
"""

import os
import sys
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import _func

def main():
    # Check the number of arguments
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: create_translation_project.py <project_dir> [project_name]")
        sys.exit(1)

    # Print the banner
    scriptname = os.path.basename(sys.argv[0])
    _func.print_banner(f"Starting {scriptname} .....")

    # Get the project directory and project name
    projectdir = sys.argv[1]
    
    # Check if the project name is provided
    if len(sys.argv) == 3 and sys.argv[2] != "":
        projectname = sys.argv[2]
    else:
        projectname = "translation_proj"
    
    # Check if the project directory exists
    if not os.path.exists(projectdir):
        print("Your <project_dir> is error!")
        sys.exit(1)

    # Create the project template
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    template = os.path.join(scriptdir, "template", "translation_proj.zip")
    extractedpath = os.path.join(scriptdir, "translation_proj")
    if not os.path.exists(extractedpath):
        print("Creating the project template...")
        _func.run_command(f"unzip {template} -d {scriptdir}")
    
    # Move the project to the project directory
    print(f"Creating your project to {projectdir}....")
    try:
        targetdir = os.path.join(projectdir, projectname)
        shutil.move(extractedpath, targetdir)
    except Exception as e:
        print(f"Failed to move project: {e}")
        sys.exit(1)

    # Print the banner
    _func.print_banner(f"{scriptname} has been executed successfully.")

if __name__ == "__main__":
    main()
