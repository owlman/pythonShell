#! /usr/bin/env python
"""
    Created on 2016-5-15
    
    @author: lingjie
    @name:   sshky_configure
"""

import os
import sys
import subprocess

def main():
    title = "Starting " + sys.argv[0] + "..."
    n = len(title)
    print(n * '=')
    print(title)
    print(n * '=')

    ssh_key_path = os.path.join(os.environ.get("HOME", ""), ".ssh", "id_rsa")
    if os.path.exists(ssh_key_path):
        print("The SSH key has configuration completed.")
    else:
        email = input("Please enter your email for the SSH key: ")
        cmd = ["ssh-keygen", "-t", "rsa", "-C", email]
        try:
            subprocess.run(cmd, check=True)
            print("SSH key generated successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while generating the SSH key: {e}")

    print(n * '=')    
    print("= Done!" + (n - len("= Done!") - 1) * ' ' + "=")
    print(n * '=')

if __name__ == "__main__":
    main()
