#! /usr/bin/env python
'''
    Created on 2016-4-26
    
    @author: lingjie
    @name:   git_show_log
'''

import os
import sys

if len(sys.argv) < 2:
	print("Usage: git_show_log.py <git_dir> [option]") 
	exit(1)

os.chdir(sys.argv[1])
print("work_dir: " + sys.argv[1])

cmd = "git log "
if len(sys.argv) >= 3:
	cmd += " ".join(sys.argv[2:])

print("CMD: " + cmd)
os.system(cmd) 
