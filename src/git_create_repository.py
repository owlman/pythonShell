#!/usr/bin/env python3
"""
    Created on 2015-12-20

    Author: lingjie
    Program: git-create-repository
    usage:
        git-create-repository <git_directory> [init_commit_message]
    Description: Create a git repository with optional initial commit
        git_directory : Path to create the Git repository.
        init_commit_message : Commit message for the initial commit (default: "Initial commit").
"""

import os
import subprocess
import sys
from . import common

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: git-create-repository <git_directory> [init_commit_message]")
        exit(1)

    scriptname = os.path.basename(sys.argv[0])
    common.print_banner(f"Starting {scriptname} .....")

    projectdir = sys.argv[1]
    os.makedirs(projectdir, exist_ok=True)

    cwd = os.getcwd()
    try:
        os.chdir(projectdir)
        print(f"Changed to directory: {os.getcwd()}\n")

        if not os.path.exists(".git"):
            common.run_command(["git", "init"])

        for fname in [".gitignore", "README.md"]:
            if not os.path.exists(fname):
                with open(fname, "w") as f:
                    pass

        common.run_command(["git", "status"])
        common.run_command(["git", "add", "."])

        # Commit only if there are changes
        gitstatus = subprocess.check_output(["git", "status", "--porcelain"], text=True)
        if gitstatus.strip():
            commit_msg = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] else "Initial commit"
            common.run_command(["git", "commit", "-m", commit_msg])
        else:
            print("No files to commit.")

    finally:
        os.chdir(cwd)

    common.print_banner(f"{scriptname} has been executed successfully.")

if __name__ == "__main__":
    main()
