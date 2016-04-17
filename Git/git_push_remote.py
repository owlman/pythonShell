#! /usr/bin/env python
'''
    Created on 2015-12-20
    
    @author: lingjie
    @name:   git_push_remote
'''

import os
import sys

if len(sys.argv) < 2:
    print "Usage: git_push_remote.py <git_dir> [commit_message]" 
    exit()

title = "= Starting " + sys.argv[0] + "... ="
n = len(title)
print n*'='
print title
print n*'='

os.chdir(sys.argv[1])
print "PWD: "+ os.popen("pwd").readline()
if len(sys.argv) == 3 and sys.argv[2] != "":
    os.system("git add .")
    os.system("git commit -m '"+sys.argv[2]+"'")

for remote in os.popen("git remote show").readlines():
    print ""
    print "Being pushed to " + remote[0:-1] + "..."
    os.system("git push -u " + remote[0:-1])
    print "Push is complete!"

print n*'='    
print "= Done!" + (n-len("= Done!")-1)*' ' + "="
print n*'='
