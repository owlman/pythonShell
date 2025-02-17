#! /usr/bin/env python
"""
    Created on 2018-10-31
    
    @author: lingjie
    @name:   create_translation_project
"""

import os
import sys
import shutil
import subprocess
import _lib.func as _func

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: create_translation_project.py <project_dir> [project_name]")
        sys.exit(1)

    title = "=    Starting " + sys.argv[0] + "......    ="
    _func.print_banner(title)

    project_dir = sys.argv[1]
    project_name = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] else "translation_proj"

    if not os.path.exists(project_dir):
        print("Your <project_dir> is error!")
        sys.exit(1)

    template_dir = os.path.join(sys.path[0], "template", "translation_proj.zip")
    if not os.path.exists(project_name):
        print("Creating the project template...")
        try:
            _func.run_command(["unzip", template_dir], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to unzip template: {e}")
            sys.exit(1)

    print(f"Creating your project to {project_dir}....")
    try:
        shutil.move(project_name, os.path.join(project_dir, project_name))
    except Exception as e:
        print(f"Failed to move project: {e}")
        sys.exit(1)

    _func.print_banner("=     Done!" + (len(title) - len("=     Done!") - 1) * ' ' + "=")

if __name__ == "__main__":
    main()
