#! /usr/bin/env python
'''
    Created on 2016-4-10
    
    @author: lingjie
    @name:   git_create_repository
'''

import os
import sys

if len(sys.argv) < 2:
    print "Usage: git_create_repository.py <git_reps_dir> [init_commit_message]"     
    exit()

titlemsg = "= Starting " + sys.argv[0] + "... ="
n = len(titlemsg)
print n*'='
print titlemsg
print n*'='

os.chdir(sys.argv[1])
print "PWD: "+ os.popen("pwd").readline()
os.system("git init")
os.system("touch .gitignore")
os.system("touch README.md")
os.system("git add .")
if len(sys.argv)==3 and sys.argv[2]!="":
    os.system("git commit -m '"+sys.argv[2]+"'")
else:
	os.system("git commit -m 'init repository...' ")

print n*'='    
print "= Done!" + (n-len("= Done!")-1)*' ' + "="
print n*'='
