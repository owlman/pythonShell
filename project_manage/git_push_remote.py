#!/usr/bin/env python3
"""
Created on 2015-12-20

Author: lingjie
Name: git_push_remote
Usage:
    python git_push_remote.py <git_dir> [commit_message]

Description:
    git_dir: Path to the Git repository.
    commit_message: Message used for committing changes.
                    If commit_message is not provided, no commit will be made.

    This script switches into the target Git directory, optionally commits,
    and then pushes the current branch to all configured remotes.
"""

import os
import sys
import subprocess
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

    # check if the directory is a git repository
    try:
        # if is a git repository, do nothing.
        subprocess.run(
            ["git", "status"], 
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print("Error: Not a git repository.")
        exit()

    # Add and commit changes if a commit message is provided
    if len(sys.argv) == 3 and sys.argv[2] != "":
        # Check if there are any changes to commit
        print("Adding and committing changes...")
        gitstatus = subprocess.check_output(
            ["git", "status", "--porcelain"],
            text=True
        )
        if gitstatus == "":
            print("Error: No changes to commit.")
        else:
            _func.run_command(["git", "add", "."])
            _func.run_command(["git", "commit", "-m", sys.argv[2]])

    # Push to all remotes
    remotes = subprocess.check_output(["git", "remote"], text=True)
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"], text=True
    ).strip()
    for remote in remotes.splitlines():
        remote = remote.strip()
        print(f"\nPushing to remote:{remote} ...")
        _func.run_command(["git", "pull", "--rebase", remote, branch])
        _func.run_command(["git", "push", remote, branch])
        print("Push is complete!")

    # Restore the original working directory
    os.chdir(cwd)

    # Print the banner
    _func.print_banner(f"{scriptname} has been executed successfully.")

if __name__ == "__main__":
    main()
