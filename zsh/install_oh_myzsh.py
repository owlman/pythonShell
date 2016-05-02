#! /usr/bin/env python
'''
    Created on 2016-4-28
    
    @author: lingjie
    @name:   install_oh_myzsh
'''

import os
import sys

title = "= Starting " + sys.argv[0] + "... ="
n = len(title)
print n*'='
print title
print n*'='

os.system("cd")
if os.path.exists("./.oh-my-zsh"):
	print "oh-my-zsh has installed."
else :
	cmds = [
		"git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh",
		"cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc"
	]

	for cmd in cmds:
		print cmd
		os.system(cmd)

print n*'='    
print "= Done!" + (n-len("= Done!")-1)*' ' + "="
print n*'='
