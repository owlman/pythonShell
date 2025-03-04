#! /usr/bin/env python
"""
    Created on 2018-10-31
    
    @author: lingjie
    @name:   create_translation_project
    @Usage: python create_translation_project.py <project_dir> [project_name]
    @description:
        project_dir: project directory
        project_name: project name
        if project_name is not provided, the default name is "translation_proj"
        if project directory exists, it will be removed.
        if project directory does not exist, it will be created.
        if project directory is not empty, it will be removed.                
"""

import os
import sys
import shutil
# debug mode
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
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
        os.makedirs(projectdir)
    
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
        # remove the target directory if it exists
        if os.path.exists(targetdir):
            shutil.rmtree(targetdir)
        print(f"Moving {extractedpath} to {targetdir}....")
        shutil.move(extractedpath, targetdir)
    except Exception as e:
        print(f"Failed to move project: {e}")
        sys.exit(1)

    # Print the banner
    _func.print_banner(f"{scriptname} has been executed successfully.")

if __name__ == "__main__":
    main()
