#! /usr/bin/env python
"""
    Created on 2015-12-20
    
    @author: lingjie
    @name:   git_pull_remote
"""

import os
import sys
import subprocess
# debug mode
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import _func

def main():
    if not len(sys.argv) in range(2, 4):
        print("Usage: git_pull_remote.py <git_dir> [branch]") 
        exit(1)

    gitrepo = sys.argv[1]
    if not os.path.isdir(gitrepo):
        print(f"Error: {gitrepo} is not a valid directory.")
        exit(1)
    # Print the banner
    _func.print_banner(f"Starting {os.path.basename(sys.argv[0])} .....")
    
    branch = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] != "" else "master"
    cwd = os.getcwd()
    os.chdir(gitrepo)
    print(f"Changed to directory: {os.getcwd()}\n")

    for remote in subprocess.check_output(["git", "remote", "show"]).decode().splitlines():
        print(f"\nPulling from remote:{remote} ...")
        _func.run_command(f"git pull {remote} {branch}")
        print("Pull is complete!")

    # Restore the original working directory
    os.chdir(cwd)
    # Print the banner
    _func.print_banner(f"{os.path.basename(sys.argv[0])} has been executed successfully.")
    
if __name__ == "__main__":
    main()