#! /usr/bin/env python
'''
    Created on 2016-4-29
    
    @author: lingjie
    @name:   install_apt_cyg
'''

import os
import sys

title = "= Starting " + sys.argv[0] + "... ="
n = len(title)
print(n*'=')
print(title)
print(n*'=')


if os.path.exists("/usr/bin/gdb"):
	print("the gnu tool has installed.")
else :
	cmds = [
		"brew install coreutils",
		"brew tap homebrew/dupes",
		"brew install binutils",
		"brew install diffutils",
		"brew install ed --default-names",
		"brew install findutils --default-names",
		"brew install gawk",
		"brew install gnu-indent --default-names",
		"brew install gnu-sed --default-names",
		"brew install gnu-tar --default-names",
		"brew install gnu-which --default-names",
		"brew install gnutls --default-names",
		"brew install grep --default-names",
		"brew install gzip",
		"brew install screen",
		"brew install watch",
		"brew install wdiff --with-gettext",
		"brew install wget",
		"brew install emacs",
		"brew install gdb",  .
		"brew install gpatch",
		"brew install m4",
		"brew install make",
		"brew install nano"
	]
	
	for cmd in cmds:
		print(cmd)
		os.system(cmd)

print(n*'=')
print("= Done!" + (n-len("= Done!")-1)*' ' + "=")
print(n*'=')
