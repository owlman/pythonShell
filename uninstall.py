#! /usr/bin/env python
'''
    Created on 2016-5-31
    
    @author: lingjie
    @name:   uninstall
'''

import os
import sys

if not len(sys.argv) in range(2,3):
	print("Usage: uninstall.py <install_dir>")
	exit(0)

title = "= Starting " + sys.argv[0] + "... ="
n = len(title)
print(n*'=')
print(title)
print(n*'=')

my_dir = sys.path[0]
files = os.popen("find " + my_dir + " -name '*.py'").readlines()

os.chdir(sys.argv[1])
print("PWD: " + os.popen("pwd").readline())

for file in files:
	filename = os.path.split(os.path.realpath(file[0:-1]))[1]
	if(filename == "install.py" or filename == "uninstall.py"):
		continue
	cmd = "rm " + filename		
	print cmd
	os.system(cmd)

print(n*'=')    
print("= installed!" + (n-len("= installed!")-1)*' ' + "=")
print(n*'=')
