#! /usr/bin/env python
'''
    Created on 2016-4-27
    
    @author: lingjie
    @name:   git_show_status
'''

import os
import sys

if len(sys.argv) < 2:
	print("Usage: git_show_status.py <git_dir> [option]") 
	exit(1)

os.chdir(sys.argv[1])
print("work_dir: " + sys.argv[1])

cmd = "git status "
if len(sys.argv) >= 3:
	cmd += " ".join(sys.argv[2:])

print("CMD: " + cmd)
os.system(cmd) 
