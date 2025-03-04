#! /usr/bin/env python
"""
    Created on 2016-4-28
    
    @author: lingjie
    @name:   sshdir_permissions_config
    @Usage: python sshdir_permissions_config.py
    @description:
        Set the permissions of the ssh key file to 600 and change the group to Users.
        If the platform is Windows, the script will print an error message and exit.
"""

import os
import sys

# debug mode
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import _func

def main():
    # Print the banner
    # Check if the platform is Windows
    if sys.platform == "win32":
            _func.print_banner("Error: This script is not supported on Windows.")
            exit(1)
    else:
        _func.print_banner("Starting sshdir_permissions_config .....")
            
    # Check if the ssh key file exists    
    ssh_key_path = os.path.expanduser('~/.ssh/id_rsa')
    if not os.path.exists(ssh_key_path):
        print(f"Error: ssh key file '{ssh_key_path}' does not exist.")
    else:        
        # Run the commands
        cmds = [
            f"setfacl -b {ssh_key_path}",
            f"chgrp Users {ssh_key_path}",
            f"chmod 600 {ssh_key_path}"
        ]

        for cmd in cmds:
            print(f"Running command: {cmd}")
            _func.run_command(cmd)
            
        # Print the banner
        _func.print_banner("sshdir_permissions_config has been executed successfully.")

if __name__ == "__main__":
    main()
