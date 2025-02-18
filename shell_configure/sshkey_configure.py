#! /usr/bin/env python
"""
    Created on 2016-5-15
    
    @author: lingjie
    @name:   sshky_configure
"""

import os

# debug mode
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import _func

def check_default_ssh_key():
    ssh_dir = os.path.expanduser('~/.ssh')
    if not os.path.exists(ssh_dir):
        return False
    
    # Check if the private and public key files exist
    private_key = os.path.join(ssh_dir, 'id_rsa')
    public_key = os.path.join(ssh_dir, 'id_rsa.pub')
    
    return os.path.isfile(private_key) and os.path.isfile(public_key)

def main():
    # Print the banner
    _func.print_banner("Starting sshkey_configure .....")
    
    # Check if the ssh key has configuration completed
    if check_default_ssh_key():
        print("SSH key has been configured.")
    else:
        email = input("Please enter your email for the SSH key: ")
        cmd = ["ssh-keygen", "-t", "rsa", "-C", email]
        _func.run_command(cmd)
        
    # Print the banner
    _func.print_banner("sshkey_configure has been executed successfully.")

if __name__ == "__main__":
    main()

