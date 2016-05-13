#! /usr/bin/env python
'''
    Created on 2016-5-13
    
    @author: lingjie
    @name:   git_commit
'''

import os
import sys
import time

if not len(sys.argv) in range(1, 4):
    print "Usage: git_commit.py <git_dir> [commit_message]" 
    exit()

title = "= Starting " + sys.argv[0] + "... ="
n = len(title)
print n*'='
print title
print n*'='

os.chdir(sys.argv[1])
print "PWD: "+ os.popen("pwd").readline()
if len(sys.argv) == 3 and sys.argv[2] != "":
    commit_message = sys.argv[2]
else:
    commit_message = "committed at " + time.strftime("%Y-%m-%d",time.localtime(time.time()))

os.system("git add .")
os.system("git commit -m '"+ commit_message + "'")

print "Push is complete!"

print n*'='    
print "= Done!" + (n-len("= Done!")-1)*' ' + "="
print n*'=' 
