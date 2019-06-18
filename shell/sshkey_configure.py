#! /usr/bin/env python
"""
    Created on 2016-5-15
    
    @author: lingjie
    @name:   sshky_configure
"""

import os
import sys

title = "Starting " + sys.argv[0] + "..."
n = len(title)
print(n*'=')
print(title)
print(n*'=')

if os.path.exists(os.environ["HOME"]+"/.ssh/id_rsa"):
    print("the ssh key has configureation completed .")
else:
    cmd = "ssh-keygen -t rsa -C 'jie.owl2008@gmail.com'"
    print(cmd)
    os.system(cmd)

print(n*'=')    
print("= Done!" + (n-len("= Done!")-1)*' ' + "=")
print(n*'=')
