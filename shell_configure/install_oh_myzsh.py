#! /usr/bin/env python
"""
    Created on 2016-4-28
    
    @author: lingjie
    @name:   install_oh_myzsh
"""

import os
import sys

title = "=    Starting " + sys.argv[0] + "......    ="
n = len(title)
print(n * '=')
print(title)
print(n * '=')

# 切换到用户主目录
os.chdir(os.path.expanduser("~"))

# 检查是否已经安装了 oh-my-zsh
if os.path.exists("./.oh-my-zsh"):
    print("oh-my-zsh has installed.")
else:
    cmds = [
        "git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh",
        "cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc"
    ]

    for cmd in cmds:
        print(cmd)
        ret = os.system(cmd)
        if ret != 0:
            print(f"Command failed with return code {ret}")
            sys.exit(1)

print(n * '=')
# 使用 str.ljust 来对齐字符串
done_msg = "=     Done!".ljust(n - 1) + "="
print(done_msg)
print(n * '=')
