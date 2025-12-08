#!/usr/bin/env python3
"""
    Created on 2018-10-31

    Author: lingjie
    Name: git_configuration
    Usage:
        git-configuration <user_name> <user_email>       

    Description: 
        user_name: Git user name 
        user_email: Git user email
"""

import os
import platform
import sys

from . import common

def main():
    # if user_name or user_email is not provided, exit
    if len(sys.argv) != 3:
        print("Usage: git-configuration [user_name] [user_email]")
        sys.exit(1)
    common.print_banner("Starting git_configuration .....")

    user_name, user_email = sys.argv[1], sys.argv[2]
    cmds = [
        ["git", "config", "--global", "user.name", user_name],
        ["git", "config", "--global", "user.email", user_email],
        ["git", "config", "--global", "push.default", "simple"],
        ["git", "config", "--global", "color.ui", "true"],
        ["git", "config", "--global", "core.quotepath", "false"],
        ["git", "config", "--global", "core.editor", "vim"],
        ["git", "config", "--global", "i18n.logOutputEncoding", "utf-8"],
        ["git", "config", "--global", "i18n.commitEncoding", "utf-8"],
        ["git", "config", "--global", "color.diff", "auto"],
        ["git", "config", "--global", "color.status", "auto"],
        ["git", "config", "--global", "color.branch", "auto"],
        ["git", "config", "--global", "color.interactive", "auto"]
    ]

    # autocrlf setting
    if platform.system() == "Windows":
        cmds.append(["git", "config", "--global", "core.autocrlf", "true"])
    else:
        cmds.append(["git", "config", "--global", "core.autocrlf", "input"])

    for cmd in cmds:
        print(f"Running command: {' '.join(cmd)}")
        common.run_command(cmd)

    common.print_banner("git_configuration has been executed successfully.")

if __name__ == "__main__":
    main()
