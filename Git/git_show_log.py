#! /usr/bin/env python
'''
    Created on 2016-4-26
    
    @author: lingjie
    @name:   git_show_log
'''

import os
import sys

if len(sys.argv) < 2:
	print "Usage: git_show_log.py <git_dir> [number_log]" 
	exit()

os.chdir(sys.argv[1])
cmd = "git log --oneline"
if len(sys.argv) == 3:
	cmd += " " + sys.argv[2]

os.system(cmd) 
