#! /usr/bin/env python
'''
    Created on 2015-5-9
    
    @author: lingjie
    @name:   git_pull_remote
'''

import os
import sys

if len(sys.argv) < 2:
    print "Usage: git_push_remote.py <git_dir>" 
    exit()

title = "= Starting " + sys.argv[0] + "... ="
n = len(title)
print n*'='
print title
print n*'='

os.chdir(sys.argv[1])
print "PWD: "+ os.popen("pwd").readline()

for remote in os.popen("git remote show").readlines():
    print ""
    print "Pulling from " + remote[0:-1] + "..."
    os.system("git pull " + remote[0:-1] + " master")
    print "Pull is complete!"

print n*'='    
print "= Done!" + (n-len("= Done!")-1)*' ' + "="
print n*'='
