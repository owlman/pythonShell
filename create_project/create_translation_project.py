#! /usr/bin/env python
'''
    Created on 2018-10-31
    
    @author: lingjie
    @name:   create_translation_project
'''

import os
import sys

if not len(sys.argv) in range(2, 4):
    print("Usage: create_translation_project.py <project_dir> [project_name]") 
    exit(1)

title = "=    Starting " + sys.argv[0] + "......    ="
n = len(title)
print(n*'=')
print(title)
print(n*'=')

project_dir = sys.argv[1]
if len(sys.argv) == 3 and sys.argv[2] != "":
    project_name = sys.argv[2]
else : 
    project_name = "translation_proj"

if not os.path.exists(project_dir):
    print("Your <project_dir> is error !")
else :
    if not os.path.exists("translation_proj"):
        print("Creating the project template...")
        unzip_cmd = "unzip " + sys.path[0] + "/template/translation_proj.zip" 
        os.system(unzip_cmd)

    print("Creating your project to <project_dir>....")
    move_cmd = "mv ./translation_proj " + project_dir + "/" + project_name
    os.system(move_cmd) 

print(n*'=')    
print("=     Done!" + (n-len("=     Done!")-1)*' ' + "=")
print(n*'=')
