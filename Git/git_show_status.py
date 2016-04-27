#! /usr/bin/env python
'''
    Created on 2016-4-27
    
    @author: lingjie
    @name:   git_show_status
'''

import os
import sys

if len(sys.argv) < 2:
	print "Usage: git_show_log.py <git_dir> [option]" 
	exit()

os.chdir(sys.argv[1])
cmd = "git status "
if len(sys.argv) >= 3:
	cmd += " ".join(sys.argv[2:])
print cmd
os.system(cmd) 
