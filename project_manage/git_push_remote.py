#! /usr/bin/env python
"""
    Created on 2015-12-20
    
    @author: lingjie
    @name:   git_push_remote
"""

import os
import sys

sys.path.append("..")
import _func

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: git_push_remote.py <git_dir> [commit_message]")
    exit()

script_name = os.path.basename(sys.argv[0])
title = f"=    Starting {script_name}......    "
_func.print_banner(title)

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
    _func.run_command("git add .")
    _func.run_command(f"git commit -m '{sys.argv[2]}'")

for remote in os.popen("git remote show").readlines():
    remote = remote.strip()
    print("")
    print("Pushing to " + remote + "...")
    _func.run_command(f"git push -u {remote}")
    print("Push is complete!")

_func.print_banner("=     Done!")
