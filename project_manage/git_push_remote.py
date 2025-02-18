#! /usr/bin/env python
"""
    Created on 2015-12-20
    
    @author: lingjie
    @name:   git_push_remote
"""

import os
import sys

# debug mode
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import _func

def main(): 
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: git_push_remote.py <git_dir> [commit_message]")
        exit()

    # Print the banner
    scriptname = os.path.basename(sys.argv[0])
    _func.print_banner(f"Starting {scriptname} .....")

    # Change to the git directory
    try:
        cwd = os.getcwd()
        os.chdir(sys.argv[1])
        print(f"Changed to directory: {os.getcwd()}\n")
    except FileNotFoundError:
        print(f"Error: Directory '{sys.argv[1]}' not found.")
        exit()
    except PermissionError:
        print(f"Error: No permission to access directory '{sys.argv[1]}'.")
        exit()

    # Add and commit changes if a commit message is provided
    if len(sys.argv) == 3 and sys.argv[2] != "":
        print("Adding and committing changes...")
        _func.run_command("git add .")
        _func.run_command(f"git commit -m '{sys.argv[2]}'")

    # Push to all remotes
    for remote in os.popen("git remote show").readlines():
        remote = remote.strip()
        print(f"\nPushing to remote: {remote}...")
        _func.run_command(f"git push -u {remote}")
        print("Push is complete!")

    # Restore the original working directory
    os.chdir(cwd)

    # Print the banner
    _func.print_banner(f"{scriptname} has been executed successfully.")

if __name__ == "__main__":
    main()
