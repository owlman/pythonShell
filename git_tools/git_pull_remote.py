#! /usr/bin/env python
"""
    Created on 2015-12-20
    
    @author: lingjie
    @name:   git_pull_remote
"""

import os
import sys
import subprocess

if not len(sys.argv) in range(2, 4):
    print("Usage: git_pull_remote.py <git_dir> [branch]") 
    exit(1)

git_dir = sys.argv[1]
if not os.path.isdir(git_dir):
    print(f"Error: {git_dir} is not a valid directory.")
    exit(1)

title = "=    Starting " + sys.argv[0] + "......    ="
n = len(title)
print(n*'=')
print(title)
print(n*'=')

branch = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] != "" else "master"

os.chdir(git_dir)
print("work_dir: " + git_dir)

try:
    remotes = subprocess.check_output(["git", "remote", "show"]).decode().splitlines()
    for remote in remotes:
        print("")
        print("Pulling from " + remote + "...")
        subprocess.run(["git", "pull", remote, branch], check=True)
        print("Pull is complete!")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    exit(1)

print(n*'=')    
print("=     Done!" + (n-len("=     Done!")-1)*' ' + "=")
print(n*'=')
