#! /usr/bin/env python
"""
    Created on 2015-12-20
    
    @author: lingjie
    @name:   git_pull_remote
    @Usage: python git_pull_remote.py <git_dir> [branch]
    @description:
        git_dir: git directory
        branch: branch to pull, default is master
        if branch is not provided, default is master
"""

#! /usr/bin/env python3
import os, sys, subprocess
import _func

def main():
    if not len(sys.argv) in range(2, 4):
        print("Usage: git_pull_remote.py <git_dir> [branch]") 
        exit(1)

    gitrepo = sys.argv[1]
    if not os.path.isdir(gitrepo):
        print(f"Error: {gitrepo} is not a valid directory.")
        exit(1)

    _func.print_banner(f"Starting {os.path.basename(sys.argv[0])} .....")

    branch = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] else "master"
    cwd = os.getcwd()
    os.chdir(gitrepo)
    print(f"Changed to directory: {os.getcwd()}")
    print(f"Pulling branch: {branch}\n")

    remotes = subprocess.check_output(["git", "remote"]).decode().splitlines()
    for remote in remotes:
        print(f"\nPulling from remote: {remote} ...")
        _func.run_command(f"git pull {remote} {branch}")
        print("Pull is complete!")

    os.chdir(cwd)
    _func.print_banner(f"{os.path.basename(sys.argv[0])} executed successfully.")

if __name__ == "__main__":
    main()
