#! /usr/bin/env python
"""
    Created on 2016-4-26
    
    @author: lingjie
    @name:   git_show_log
"""

import os
import sys
import subprocess

if len(sys.argv) < 2:
    print("Usage: git_show_log.py <git_dir> [option]")
    exit(1)

title = "=    Starting " + sys.argv[0] + "......    ="
separator = "=" * 50
print(separator)
print(title)
print(separator)

git_dir = sys.argv[1]
if not os.path.isdir(git_dir):
    print(f"Error: {git_dir} is not a valid directory.")
    exit(1)

try:
    os.chdir(git_dir)
except Exception as e:
    print(f"Error: Failed to change directory to {git_dir}: {e}")
    exit(1)

print("work_dir: " + git_dir)

cmd = ["git", "log"]
if len(sys.argv) >= 3:
    cmd.extend(sys.argv[2:])

print("CMD: " + " ".join(cmd))
try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    exit(1)

print(separator)    
print("=     Done!" + (len(separator) - len("=     Done!") - 1) * ' ' + "=")
print(separator)
