#! /usr/bin/env python
"""
    Created on 2018-06-11 
    
    Author: lingjie 
    Usage: 
        open-ssh-proxy <user_name> <host_address> <password>
    Description: open a ssh proxy to the host
        - <user_name>: the user name to login the host
        - <host_address>: the host address to login
        - <password>: the password to login the host
"""

import os
import pexpect

def main():
    if len(os.sys.argv) != 4:
        print("Usage: open-ssh-proxy <user_name> <host_address> <password>")
        exit(1)
    # get the environment variables
    user, host, pword = os.sys.argv[1], os.sys.argv[2], os.sys.argv[3]

    # chrck if the environment variables are set
    if not user or not host or not pword:
        print("Please set SSH_USER, SSH_HOST, and SSH_PASSWORD environment variables.")
        exit(1)

    print(f"Connecting to {user}@{host}...")

    try:
        # spawn a new ssh process and connect to the host
        child = pexpect.spawn(f"ssh -D 7070 {user}@{host}")

        # expect the password prompt
        child.expect("password:")
        child.sendline(pword)

        # interact with the child process and pass the input/output to the user
        child.interact()
        exit(0)
    except pexpect.ExceptionPexpect as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
