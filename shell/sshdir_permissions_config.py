#! /usr/bin/env python
'''
    Created on 2016-4-28
    
    @author: lingjie
    @name:   sshdir_permissions_config
'''

import os
import sys

title = "= Starting " + sys.argv[0] + "... ="
n = len(title)
print(n*'=')
print(title)
print(n*'=')

cmds = [
	"setfacl -b ~/.ssh/id_rsa",
	"chgrp Users ~/.ssh/id_rsa",
	"chmod 600 ~/.ssh/id_rsa"
]

for cmd in cmds:
	print(cmd)
	os.system(cmd)

print(n*'=')
print("= Done!" + (n-len("= Done!")-1)*' ' + "=")
print(n*'=')
