#! /usr/bin/env python
"""
    Created on 2016-4-29
    
    @author: lingjie
    @name:   mac_install_gnu_tool
"""

import os
import sys
import subprocess

title = "= Starting " + os.path.basename(sys.argv[0]) + "... ="
n = len(title)
print(n*'=')
print(title)
print(n*'=')

def install_gnu_tools():
    cmds = [
        "brew install coreutils",
        "brew install binutils",
        "brew install diffutils",
        "brew install ed",
        "brew install findutils",
        "brew install gawk",
        "brew install gnu-indent",
        "brew install gnu-sed",
        "brew install gnu-tar",
        "brew install gnu-which",
        "brew install gnutls",
        "brew install grep",
        "brew install gzip",
        "brew install screen",
        "brew install watch",
        "brew install wdiff --with-gettext",
        "brew install wget",
        "brew install emacs",
        "brew install gdb",
        "brew install gpatch",
        "brew install m4",
        "brew install make",
        "brew install nano"
    ]
    for cmd in cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=True)

if not os.path.exists("/usr/local/bin/brew"):
    print("Homebrew is not installed. Please install Homebrew first.")
    sys.exit(1)

if os.system("which gdb") == 0:
    print("the gnu tool has installed.")
else:
    install_gnu_tools()

print(n*'=')
print("= Done!" + max(0, n - len("= Done!") - 1) * ' ' + "=")
print(n*'=')
