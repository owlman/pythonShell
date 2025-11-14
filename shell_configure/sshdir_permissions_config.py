#!/usr/bin/env python3
"""
Set proper permissions for SSH key and directory.
"""

import os
import sys
import stat
import _func

def main():
    if sys.platform == "win32":
        _func.print_banner("Error: This script is not supported on Windows.")
        sys.exit(1)

    _func.print_banner("Starting sshdir_permissions_config .....")

    ssh_key_path = os.path.expanduser("~/.ssh/id_rsa")
    ssh_dir = os.path.dirname(ssh_key_path)

    if not os.path.exists(ssh_key_path):
        print(f"Error: SSH key file '{ssh_key_path}' does not exist.")
        sys.exit(1)

    # Set permissions: 600 for private key, 700 for .ssh directory
    os.chmod(ssh_key_path, stat.S_IRUSR | stat.S_IWUSR)
    os.chmod(ssh_dir, stat.S_IRWXU)

    print(f"Permissions set: {ssh_key_path} -> 600, {ssh_dir} -> 700")

    _func.print_banner("sshdir_permissions_config has been executed successfully.")

if __name__ == "__main__":
    main()
