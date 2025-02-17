#! /usr/bin/env python
"""
    Created on 2019-06-17

    @author: lingjie
    @name:   create_book_project
"""

import os
import sys
import shutil
import subprocess

if not len(sys.argv) in range(2, 4):
    print("Usage: create_book_project.py <project_dir> [project_name]")
    exit(1)

title = "=    Starting " + sys.argv[0] + "......    ="
n = len(title)
print(n * '=')
print(title)
print(n * '=')

project_dir = sys.argv[1]

if len(sys.argv) == 3 and sys.argv[2] != "":
    project_name = sys.argv[2]
else:
    project_name = "book_proj"

if not os.path.exists(project_dir):
    print("Your <project_dir> is error !")
    exit(1)

script_dir = os.path.dirname(os.path.abspath(__file__))
template_zip = os.path.join(script_dir, "template", "book_proj.zip")
extracted_dir = os.path.join(script_dir, "book_proj")

if not os.path.exists(extracted_dir):
    print("Creating the project template...")
    try:
        subprocess.run(["unzip", template_zip], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to unzip template: {e}")
        exit(1)

print("Creating your project to " + project_dir + "....")
target_dir = os.path.join(project_dir, project_name)
try:
    shutil.move(extracted_dir, target_dir)
except Exception as e:
    print(f"Failed to move project: {e}")
    exit(1)

print(n * '=')
print("=     Done!" + (n - len("=     Done!") - 1) * ' ' + "=")
print(n * '=')
