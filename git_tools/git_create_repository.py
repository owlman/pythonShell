#! /usr/bin/env python
"""
    Created on 2016-4-10
    
    @author: lingjie
    @name:   git_create_repository
"""

import os
import sys
import subprocess

def print_border(title):
    n = len(title)
    print(n * '=')
    print(title)
    print(n * '=')

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: git_create_repository.py <git_reps_dir> [init_commit_message]")
    exit(1)

print_border("=    Starting " + sys.argv[0] + "......    =")

if not os.path.isdir(sys.argv[1]):
    print(f"Error: Directory '{sys.argv[1]}' does not exist.")
    exit(1)

os.chdir(sys.argv[1])
print("work_dir: " + sys.argv[1])

subprocess.run(["git", "init"], check=True)
subprocess.run(["touch", ".gitignore"], check=True)
subprocess.run(["touch", "README.md"], check=True)
subprocess.run(["git", "add", "."], check=True)

commit_message = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] else "init commit."
subprocess.run(["git", "commit", "-m", commit_message], check=True)

print_border("=     Done!" + (len("=    Starting " + sys.argv[0] + "......    =") - len("=     Done!") - 1) * ' ' + "=")
