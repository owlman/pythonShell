#! /usr/bin/env python
"""
    Created on 2016-4-29
    
    @author: lingjie
    @name:   mac_install_gnu_tool
"""

import os
# debug mode
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import _func

def main():
    # Print the banner
    _func.print_banner("Starting mac_install_gnu_tool .....")
    # Check if the gnu tool has installed
    if os.path.exists("/usr/local/bin/gawk"):
        print("GNU tool has installed.")
    else:
        # Run the commands
        cmds = [
            "brew install coreutils",
            "brew install binutils",
            "brew install diffutils",
            "brew install ed",
            "brew install findutils",
            "brew install gawk",
            "brew install gnu-indent",
            "brew install gnu-sed",
            "brew install gnu-tar",
            "brew install gnu-which",
            "brew install gnutls",
            "brew install grep",
            "brew install gzip",
            "brew install screen",
            "brew install watch",
            "brew install wdiff --with-gettext",
            "brew install wget",
            "brew install emacs",
            "brew install gdb",
            "brew install gpatch",
            "brew install m4",
            "brew install make",
            "brew install nano"
        ]
        for cmd in cmds:
            print(f"Running command: {cmd}")
            _func.run_command(cmd)

    # Print the banner
    _func.print_banner("mac_install_gnu_tool has been executed successfully.")
    
if __name__ == "__main__":
    main()
