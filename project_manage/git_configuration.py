#! /usr/bin/env python
"""
    Created on 2016-4-15
    
    @author: lingjie
    @name:   git_configuration
"""

import platform
import subprocess

title = "=    Starting Git Configuration...    ="
n = len(title)
print(n*'=')
print(title)
print(n*'=')

cmds = [
    "git config --global user.name 'owlman'",
    "git config --global user.email 'jie.owl2008@gmail.com'",
    "git config --global push.default simple",
    "git config --global color.ui true",
    "git config --global core.quotepath false",
    "git config --global core.editor nvim",
    "git config --global i18n.logOutputEncoding utf-8",
    "git config --global i18n.commitEncoding utf-8",
    "git config --global color.diff auto",
    "git config --global color.status auto",
    "git config --global color.branch auto",
    "git config --global color.interactive auto"
]

if platform.system() == "Windows":
    cmds.append("git config --global core.autocrlf true")
else:
    cmds.append("git config --global core.autocrlf input")

for cmd in cmds:
    print(cmd)
    subprocess.run(cmd, shell=True, check=True)

print(n*'=')    
print(f"=     Done!{' ' * (n - len('=     Done!') - 1)}=")
print(n*'=')
