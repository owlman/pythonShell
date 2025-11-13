#! /usr/bin/env python
"""
    Created on 2016-4-15
    
    @author: lingjie
    @name:   git_configuration
    @description:
        git_configuration.py
        set the git configuration for the current user
"""

import sys, os
# debug mode
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import _func

def main():
    # print the banner
    _func.print_banner("Starting git_configuration .....")

    # git configuration commands 
    cmds = [
        "git config --global user.name 'owlman'",
        "git config --global user.email 'jie.owl2008@gmail.com'",
        "git config --global push.default simple",
        "git config --global color.ui true",
        "git config --global core.quotepath false",
        "git config --global core.editor nvim",
        "git config --global i18n.logOutputEncoding utf-8",
        "git config --global i18n.commitEncoding utf-8",
        "git config --global color.diff auto",
        "git config --global color.status auto",
        "git config --global color.branch auto",
        "git config --global color.interactive auto"
    ]
    # set the autocrlf to true on Windows
    if sys.platform == "win32":
        cmds.append("git config --global core.autocrlf true")
    else:
        cmds.append("git config --global core.autocrlf input")

    # run the git configuration commands
    for cmd in cmds:
        print(f"Running command: {cmd}")
        _func.run_command(cmd)

    # print the banner
    _func.print_banner("git_configuration has been executed successfully.")
    
if __name__ == "__main__":
    main()