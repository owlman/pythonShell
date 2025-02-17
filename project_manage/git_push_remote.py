#! /usr/bin/env python
"""
    Created on 2015-12-20
    
    @author: lingjie
    @name:   git_push_remote
"""

import os
import sys
import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}")
        print(result.stderr)
        exit()

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: git_push_remote.py <git_dir> [commit_message]")
    exit()

script_name = os.path.basename(sys.argv[0])
title = f"=    Starting {script_name}......    ="
n = len(title)
print(n * '=')
print(title)
print(n * '=')

try:
    os.chdir(sys.argv[1])
except FileNotFoundError:
    print(f"Error: Directory '{sys.argv[1]}' not found.")
    exit()
except PermissionError:
    print(f"Error: No permission to access directory '{sys.argv[1]}'.")
    exit()

print("work_dir: " + sys.argv[1])

if len(sys.argv) == 3 and sys.argv[2] != "":
    run_command("git add .")
    run_command(f"git commit -m '{sys.argv[2]}'")

for remote in os.popen("git remote show").readlines():
    remote = remote.strip()
    print("")
    print("Pushing to " + remote + "...")
    run_command(f"git push -u {remote}")
    print("Push is complete!")

print(n * '=')    
print("=     Done!" + (n - len("=     Done!") - 1) * ' ' + "=")
print(n * '=')
