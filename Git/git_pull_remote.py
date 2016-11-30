#! /usr/bin/env python
'''
    Created on 2015-5-9
    
    @author: lingjie
    @name:   git_pull_remote
'''

import os
import sys

if not len(sys.argv) in range(2, 4):
    print("Usage: git_pull_remote.py <git_dir> [branch]") 
    exit(1)

title = "= Starting " + sys.argv[0] + "... ="
n = len(title)
print(n*'=')
print(title)
print(n*'=')

if len(sys.argv) == 3 and sys.argv[2] != "":
	branch = sys.argv[2]
else :
	branch = "master"

os.chdir(sys.argv[1])
print("work_dir: " + sys.argv[1])

for remote in os.popen("git remote show").readlines():
    print("")
    print("Pulling from " + remote[0:-1] + "...")
    os.system("git pull " + remote[0:-1] + " " + branch)
    print("Pull is complete!")

print(n*'=')    
print("= Done!" + (n-len("= Done!")-1)*' ' + "=")
print(n*'=')
