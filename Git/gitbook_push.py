#! /usr/bin/env python
"""
    Created on 2018-11-04
    
    @author: lingjie
    @name:   gitbook_push
"""

import os
import sys

if not len(sys.argv) in range(2, 4):
    print("Usage: gitbook_push.py <git_dir> [commit_message]")
    exit()

title = "=    Starting " + sys.argv[0] + "......    ="
n = len(title)
print(n*'=')
print(title)
print(n*'=')

os.chdir(sys.argv[1])
print("work_dir: " + sys.argv[1])

os.system("gitbook build")

if len(sys.argv) == 3 and sys.argv[2] != "":
    os.system("git add .")
    os.system("git commit -m '"+sys.argv[2]+"'")

if os.path.exists("../_book"):
    os.system("rm -rf ../_book")

os.system("cp -r _book ../")
os.system("git checkout gh-pages")
os.system("rm -rf ./*")
os.system("cp -r ../_book/* ./")

if len(sys.argv) == 3 and sys.argv[2] != "":
    os.system("git add .")
    os.system("git commit -m '"+sys.argv[2]+"'")


 for remote in os.popen("git remote show").readlines():
    print("")
    print("Pushing to " + remote[0:-1] + "...")
    os.system("git push -u " + remote[0:-1])
    print("Push is complete!")

os.system("git checkout master")

print(n*'=')    
print("=     Done!" + (n-len("=     Done!")-1)*' ' + "=")
print(n*'=')
