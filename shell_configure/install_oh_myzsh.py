#! /usr/bin/env python
"""
    Created on 2016-4-28
    
    @author: lingjie
    @name:   install_oh_myzsh
    @Usage: python install_oh_myzsh.py    
    @description:
        install oh-my-zsh and set zsh as default shell for current user
"""

import os
import sys
# debug mode
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import _func

def main():
    # Print the banner
    if sys.platform == "win32":
        _func.print_banner("Error: This script is not supported on Windows.")
        exit(1)
    else:
        _func.print_banner("Starting install_oh_myzsh .....")

    # switch to the home directory
    cwd = os.getcwd()
    os.chdir(os.path.expanduser("~"))

    # Check if oh-my-zsh has installed
    if os.path.exists("./.oh-my-zsh"):
        print("oh-my-zsh has installed.")
    else:
        cmds = [
            "git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh",
            "cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc"
        ]
        # Run the commands
        for cmd in cmds:
            print(f"Running command: {cmd}")
            _func.run_command(cmd)
            
    # Restore the original working directory
    os.chdir(cwd)
    # Print the banner
    _func.print_banner("install_oh_myzsh has been executed successfully.")
    
if __name__ == "__main__":
    main()