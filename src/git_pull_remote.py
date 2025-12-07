#!/usr/bin/env python3
"""
Created on 2015-12-20

Author: lingjie
Program: git-pull-remote
Usage:
    git-pull-remote.py <git_directory> [branch]

Description:
    git_dir : Path to a Git repository.
    branch  : Branch name to pull (default: master).

    The script changes into the target Git directory and pulls updates
    from all configured remotes for the specified branch.
"""

import os
import subprocess
import sys

import common


def main():
    # Ensure correct number of arguments
    if len(sys.argv) not in (2, 3):
        print("Usage: git-pull-remote <git_directory> [branch]")
        exit(1)

    gitrepo = sys.argv[1]

    # Validate directory
    if not os.path.isdir(gitrepo):
        print(f"Error: '{gitrepo}' is not a valid directory.")
        exit(1)

    common.print_banner(f"Starting {os.path.basename(sys.argv[0])} ...")

    # Determine branch (default: master)
    branch = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] else "master"

    cwd = os.getcwd()
    os.chdir(gitrepo)

    # check if the directory is a git repository
    try:
        # if is a git repository, do nothing.
        subprocess.run(
            ["git", "status"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print(f"Changed to directory: {os.getcwd()}")
        print(f"Pulling branch: {branch}\n")

        # Get list of remotes
        remotes = subprocess.check_output(["git", "remote"], text=True)

        # Pull from each remote
        for remote in remotes.splitlines():
            print(f"\nPulling from remote: {remote} ...")
            common.run_command(["git", "pull", remote, branch])
            print("Pull complete!")
    except subprocess.CalledProcessError:
        print("Error: Not a git repository.")
        exit()
    
    os.chdir(cwd)
    common.print_banner(f"{os.path.basename(sys.argv[0])} executed successfully.")

if __name__ == "__main__":
    main()
