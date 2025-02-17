#! /usr/bin/env python
"""
    Created on 2016-5-31
    
    @author: lingjie
    @name:   uninstall
"""

import os
import sys
import shutil
import platform
import subprocess

if len(sys.argv) != 2:
    print("Usage: uninstall.py <install_dir>")
    exit(0)

title = "= Starting " + sys.argv[0] + "... ="
n = len(title)
print(n*'=')
print(title)
print(n*'=')

my_dir = sys.path[0]
files = subprocess.check_output(["find", my_dir, "-name", "*.py"]).decode().splitlines()

os.chdir(sys.argv[1])
print("PWD: " + os.getcwd())
if os.path.exists("tmp"):
    shutil.rmtree("tmp")

if os.path.exists("template"):
    shutil.rmtree("template")

for file in files:
    filepath = os.path.split(os.path.realpath(file))[0]
    dirname = os.path.basename(filepath)
    filename = os.path.split(os.path.realpath(file))[1]
    if filename == "install.py" or filename == "uninstall.py":
        continue

    print("removing..." + filename)
    os.remove(file)

print(n*'=')    
print("= uninstalled!" + (n-len("= uninstalled!")-1)*' ' + "=")
print(n*'=')
