#! /usr/bin/env python
'''
    Created on 2016-4-26
    
    @author: lingjie
    @name:   git_show_log
'''

import os
import sys

if len(sys.argv) in range(1, 4):
	print "Usage: git_show_log.py <git_dir> [option]" 
	exit()

os.chdir(sys.argv[1])
print "PWD: " + os.popen("pwd").readline()

cmd = "git log "
if len(sys.argv) >= 3:
	cmd += " ".join(sys.argv[2:])

print "CMD: " + cmd
os.system(cmd) 
