#! /usr/bin/env python
"""
    Created on 2016-4-10
    
    @author: lingjie
    @name:   git_create_repository
"""

import os
import sys

# debug mode
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import _func

def main():
    # Check the number of arguments
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: git_create_repository.py <git_reps_dir> [init_commit_message]")
        exit(1)

    # Print the banner
    scriptname = os.path.basename(sys.argv[0])
    _func.print_banner(f"Starting {scriptname} .....")
    
    # Create the git repository if it does not exist
    projectdir = sys.argv[1]
    if not os.path.exists(projectdir):
        os.makedirs(projectdir)

    # Change to the git directory
    cwd = os.getcwd()
    os.chdir(projectdir)
    print(f"Changed to directory: {os.getcwd()}\n")

    # Initialize the git repository
    if not os.path.exists(".git"):
        _func.run_command("git init .")
    if not os.path.exists(".gitignore"):
        open(".gitignore", "w")
    if not os.path.exists("README.md"):
        open("README.md", "w")
    _func.run_command("git status")
    _func.run_command("git add .")
    if len(sys.argv) == 3 and sys.argv[2] != "":
        _func.run_command(f"git commit -m '{sys.argv[2]}'")
    else:
        _func.run_command("git commit -m 'Initial_commit'")
        
    # Restore the original working directory
    os.chdir(cwd)
    # Print the banner
    _func.print_banner(f"{scriptname} has been executed successfully.")
    
if __name__ == "__main__":
    main()
