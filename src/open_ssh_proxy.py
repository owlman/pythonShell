#! /usr/bin/env python  
# -*- coding: utf-8 -*-  
"""
    Created on 2018-06-11 
        
    @author: lingjie 
    @name:   open_ssh_proxy
    @Usage: python open_ssh_proxy.py
    @description:
        open a ssh proxy to the host
"""

import pexpect
import os

def main():
    # get the environment variables
    user = os.getenv("SSH_USER")
    host = os.getenv("SSH_HOST")
    pword = os.getenv("SSH_PASSWORD")

    # chrck if the environment variables are set
    if not user or not host or not pword:
        print("Please set SSH_USER, SSH_HOST, and SSH_PASSWORD environment variables.")
        exit(1)

    print(f"Connecting to {user}@{host}...")

    try:
        # spawn a new ssh process and connect to the host
        child = pexpect.spawn("ssh -D 7070 %s@%s" % (user, host))
        
        # expect the password prompt
        child.expect("password:")
        child.sendline(pword)
        
        # interact with the child process and pass the input/output to the user
        child.interact()
    except pexpect.ExceptionPexpect as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
