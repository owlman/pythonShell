#! /usr/bin/env python
'''
    Created on 2016-6-5
    
    @author: lingjie
    @name:   hello_c
'''
import os
import sys
import shutil
import platform

if not len(sys.argv) in range(2, 3):
    print("Usage: hello_c.py <compiler>") 
    exit(1)

codepath = sys.path[0] + "/tmp/test_c.c"
if not os.path.exists("example"):
	os.mkdir("example")

if not os.path.exists(codepath):
	code = "#include <stdio.h>\nint main(){printf(\"hello world!\\n\");return 0;} "
	file = open(codepath,'w')
	file.writelines(code)
	file.close()

shutil.copy(codepath,"example/hello.c")
cmd = sys.argv[1] + r" example/hello.c -o example/test.exe"
os.system(cmd)

sysstr = platform.system()
if sysstr =="Windows":
	os.system(r"example\test.exe")
else:
	os.system(r"example/test.exe")

if os.path.exists("example"):
	shutil.rmtree("example")
