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

if(not os.path.exists("example")):
	os.mkdir("example")
	codepath = sys.path[0] + "/src/test_c.c"
	if(os.path.exists(codepath)):
		shutil.copy(codepath,"example/hello.c")
	else:
		code = "#include <stdio.h>\nint main(){printf(\"hello world!\\n\");return 0;} "
		file = open(r"example/hello.c",'w')
		file.writelines(code)
		file.close()

cmd = sys.argv[1] + r" example/hello.c -o example/test.exe"
os.system(cmd)

sysstr = platform.system()
if(sysstr =="Windows"):
	os.system(r"example\test.exe")
else:
	os.system(r"example/test.exe")

if(os.path.exists("example")):
	shutil.rmtree("example")
