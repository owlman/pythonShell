#! /usr/bin/env python
"""
    Created on 2019-06-17

    @author: lingjie
    @name:   create_book_project
    @Usage: python create_book_project.py <project_dir> [projectname]
    @description:
        project_dir: project directory
        projectname: project name
        if projectname is not provided, the default name is "book_proj".
        The project template is in the "template" directory.
"""

import os
import sys
import shutil
# debug mode
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import _func

def main():
    # Check the number of arguments
    if not len(sys.argv) in range(2, 4):
        print("Usage: create_book_project.py <project_dir> [projectname]")
        exit(1)

    # Print the banner
    scriptname = os.path.basename(sys.argv[0])
    _func.print_banner(f"Starting {scriptname} .....")

    # Get the project directory and project name
    projectdir = sys.argv[1]

    # Check if the project name is provided
    if len(sys.argv) == 3 and sys.argv[2] != "":
        projectname = sys.argv[2]
    else:
        projectname = "book_proj"

    # Check if the project directory exists
    if not os.path.exists(projectdir):
        os.makedirs(projectdir)
        
    # Create the project template
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    template = os.path.join(scriptdir, "template", "book_proj.zip")
    extractedpath = os.path.join(scriptdir, "book_proj")
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
        exit(1)

    # Print the banner
    _func.print_banner(f"{scriptname} has been executed successfully.")
    
if __name__ == "__main__":
    main()
