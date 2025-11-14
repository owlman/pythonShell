#!/usr/bin/env python3
"""
Install oh-my-zsh and set zsh as default shell for current user
"""

import os, sys, shutil
import _func

def main():
    if sys.platform == "win32":
        _func.print_banner("Error: This script is not supported on Windows.")
        exit(1)

    _func.print_banner("Starting install_oh_myzsh .....")

    home = os.path.expanduser("~")
    oh_my_zsh_dir = os.path.join(home, ".oh-my-zsh")
    zshrc_template = os.path.join(oh_my_zsh_dir, "templates", "zshrc.zsh-template")
    zshrc_file = os.path.join(home, ".zshrc")

    cwd = os.getcwd()
    try:
        os.chdir(home)

        if os.path.exists(oh_my_zsh_dir):
            print("oh-my-zsh is already installed.")
        else:
            print("Installing oh-my-zsh...")
            _func.run_command(["git", "clone", "git://github.com/robbyrussell/oh-my-zsh.git", oh_my_zsh_dir])
            shutil.copy(zshrc_template, zshrc_file)
            print(f"Copied {zshrc_template} to {zshrc_file}")

        # Set zsh as default shell
        if shutil.which("zsh"):
            _func.run_command(["chsh", "-s", shutil.which("zsh")])
            print("Set zsh as default shell. You may need to restart your terminal.")
        else:
            print("Warning: zsh not found. Please install zsh first.")

    finally:
        os.chdir(cwd)

    _func.print_banner("install_oh_myzsh has been executed successfully.")

if __name__ == "__main__":
    main()
