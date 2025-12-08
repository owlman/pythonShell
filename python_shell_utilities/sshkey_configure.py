#!/usr/bin/env python3
"""
Configure SSH key if not already configured.
"""

import os
import sys
from . import common

def check_default_ssh_key():
    ssh_dir = os.path.expanduser('~/.ssh')
    private_key = os.path.join(ssh_dir, 'id_rsa')
    public_key = os.path.join(ssh_dir, 'id_rsa.pub')
    return os.path.isfile(private_key) and os.path.isfile(public_key)

def main():
    common.print_banner("Starting sshkey_configure .....")

    if sys.platform == "win32":
        print("Warning: This script may not work on Windows without Git Bash or WSL.")

    ssh_dir = os.path.expanduser('~/.ssh')
    os.makedirs(ssh_dir, exist_ok=True)

    if check_default_ssh_key():
        print("SSH key has been configured.")
    else:
        email = input("Please enter your email for the SSH key: ")
        private_key_path = os.path.join(ssh_dir, "id_rsa")
        cmd = ["ssh-keygen", "-t", "rsa", "-C", email, "-f", private_key_path, "-N", ""]
        common.run_command(cmd)

    common.print_banner("sshkey_configure has been executed successfully.")

if __name__ == "__main__":
    main()
