#!/usr/bin/env python3
"""
git_configuration.py
Set the git configuration for the current user
"""

import sys, os
import platform
import _func

def main():
    _func.print_banner("Starting git_configuration .....")

    cmds = [
        ["git", "config", "--global", "user.name", "owlman"],
        ["git", "config", "--global", "user.email", "jie.owl2008@gmail.com"],
        ["git", "config", "--global", "push.default", "simple"],
        ["git", "config", "--global", "color.ui", "true"],
        ["git", "config", "--global", "core.quotepath", "false"],
        ["git", "config", "--global", "core.editor", "nvim"],
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
        _func.run_command(cmd)

    _func.print_banner("git_configuration has been executed successfully.")

if __name__ == "__main__":
    main()
