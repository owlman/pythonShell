#! /usr/bin/env python
"""
    Created on 2016-4-28
    
    @author: lingjie
    @name:   sshdir_permissions_config
"""

import os
import sys

def run_command(cmd):
    """
    运行系统命令并检查其返回值。
    """
    return os.system(cmd)

def main():
    title = "=    Starting " + sys.argv[0] + "......    ="
    n = len(title)
    print(n*'=')
    print(title)
    print(n*'=')
    
    ssh_key_path = os.path.expanduser('~/.ssh/id_rsa')  # 展开用户主目录路径

    if not os.path.exists(ssh_key_path):
        print("Error: SSH key file does not exist at {}".format(ssh_key_path))
        return

    cmds = [
        "setfacl -b {}".format(ssh_key_path),
        "chgrp Users {}".format(ssh_key_path),
        "chmod 600 {}".format(ssh_key_path)
    ]

    for cmd in cmds:
        result = run_command(cmd)
        if result != 0:
            print("Error executing command: {}".format(cmd))
            return

    print("=" * n)    
    print("=     Done!" + (n-len("=     Done!")-1)*' ' + "=")
    print("=" * n)

if __name__ == "__main__":
    main()
