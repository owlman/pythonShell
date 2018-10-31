#! /usr/bin/env python
'''
    Created on 2016-4-10
    
    @author: lingjie
    @name:   git_create_repository
'''

import os
import sys

if not len(sys.argv) in range(2,4):
	print("Usage: git_create_repository.py <git_reps_dir> [init_commit_message]")
	exit(1)

title = "=    Starting " + sys.argv[0] + "......    ="
n = len(title)
print(n*'=')
print(title)
print(n*'=')

os.chdir(sys.argv[1])
print("work_dir: " + sys.argv[1])

os.system("git init")
os.system("touch .gitignore")
os.system("touch README.md")
os.system("git add .")

if len(sys.argv) == 3 and sys.argv[2] != "":
	os.system("git commit -m '" + sys.argv[2] + "' ")
else:
	os.system("git commit -m 'init commit.'")

print(n*'=')    
print("=     Done!" + (n-len("=     Done!")-1)*' ' + "=")
print(n*'=')
