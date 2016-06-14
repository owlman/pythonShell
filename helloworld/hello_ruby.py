#! /usr/bin/env python
'''
    Created on 2016-6-12
    
    @author: lingjie
    @name:   hello_ruby
'''
import os
import sys
import platform 

code = "puts \"hello world!\""
sysstr = platform.system()
if(sysstr =="Windows"):
	codepath = sys.path[0] + "\\tmp\\test_ruby.rb"
else:
	codepath = sys.path[0] + "/tmp/test_ruby.rb"

if(not os.path.exists(codepath)):
	file = open(codepath,'w')
	file.writelines(code)
	file.close()

os.system("ruby " + codepath)