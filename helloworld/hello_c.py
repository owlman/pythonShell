#! /usr/bin/env python
'''
    Created on 2016-6-5
    
    @author: lingjie
    @name:   hello_c
'''
import os
import sys
import shutil

if not len(sys.argv) in range(2, 3):
    print("Usage: hello_c.py <compiler>") 
    exit(1)

code = "#include <stdio.h>\n int main(void) { printf(\"hello world!\\n\"); return 0;} "

if(not os.path.exists("example")):
	os.mkdir("example")

file = open(r"example/hello.c",'w')
file.writelines(code)
file.close()
	
cmd = sys.argv[1] + r" example/hello.c -o example/test.exe"
os.system(cmd)
os.system(r"example/test.exe")

if(os.path.exists("example")):
	shutil.rmtree("example")
