#! /usr/bin/env python
"""
    Created on 2016-4-27
    
    @author: lingjie
    @name:   git_show_status
"""

import os
import sys
import subprocess

def print_separator(length):
    print(length * '=')

if len(sys.argv) < 2:
    print("Usage: git_show_status.py <git_dir> [option]")
    sys.exit(1)

title = "=    Starting " + sys.argv[0] + "......    ="
n = len(title)
print_separator(n)
print(title)
print_separator(n)

git_dir = sys.argv[1]
if not os.path.isdir(git_dir):
    print(f"Error: {git_dir} is not a valid directory.")
    sys.exit(1)
os.chdir(git_dir)
print("work_dir: " + git_dir)

cmd = ["git", "status"]
if len(sys.argv) >= 3:
    cmd.extend(sys.argv[2:])

print("CMD: " + " ".join(cmd))
result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(f"Error: {result.stderr}")
    sys.exit(result.returncode)

print_separator(n)    
print("=     Done!" + (n-len("=     Done!")-1)*' ' + "=")
print_separator(n)
