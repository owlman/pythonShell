#!/usr/bin/env python3
"""
Created on 2016-4-29

Author: lingjie
Name: mac_install_gnu_tool
Usage:
    python mac_install_gnu_tool.py

Description:
    Install GNU tools on macOS using Homebrew.
    Only installs tools that are not already installed.
"""

import os
import shutil
import subprocess
import _func

def is_installed(pkg_name):
    """
    Check if a Homebrew package is already installed.
    """
    try:
        subprocess.run(
            ["brew", "list", pkg_name],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    _func.print_banner("Starting mac_install_gnu_tool .....")

    # Check if running on macOS
    if os.uname().sysname != "Darwin":
        print("Error: This script is only supported on macOS.")
        return

    # Check if Homebrew is installed
    if not shutil.which("brew"):
        print("Error: Homebrew is not installed. Please install it first:")
        print("      /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        return

    # List of GNU tools to install
    brew_packages = [
        "coreutils", "binutils", "diffutils", "ed", "findutils", "gawk",
        "gnu-indent", "gnu-sed", "gnu-tar", "gnu-which", "gnutls", "grep",
        "gzip", "screen", "watch", "wdiff", "wget", "emacs",
        "gdb", "gpatch", "m4", "make", "nano"
    ]

    # Options for specific packages
    package_options = {
        "wdiff": "--with-gettext"
    }

    # Install missing packages
    for pkg in brew_packages:
        option = package_options.get(pkg, "")
        if not is_installed(pkg):
            cmd = ["brew", "install", pkg]
            if option:
                cmd.append(option)
            print(f"\nInstalling {pkg} ...")
            _func.run_command(cmd)
        else:
            print(f"{pkg} is already installed, skipping.")

    _func.print_banner("mac_install_gnu_tool has been executed successfully.")

if __name__ == "__main__":
    main()
