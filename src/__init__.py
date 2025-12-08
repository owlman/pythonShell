"""
Python Shell Utilities

A collection of powerful command-line utilities designed to automate common developer tasks,
such as Git operations, SSH configuration, and project scaffolding.
"""

__version__ = "0.1.0"
__author__ = "Ling Jie"
__email__ = "jie.owl2008@gmail.com"

# Import common utilities
from .common import run_command, print_banner

# Import Git utilities
from . import git_configuration
from . import git_create_repository
from . import git_pull_remote
from . import git_push_remote

# Import SSH utilities
from . import open_ssh_proxy
from . import sshkey_configure

# Import project scaffolding utilities
from . import create_book_project
from . import create_translation_project

__all__ = [
    # Common utilities
    "run_command",
    "print_banner",
    
    # Git utilities
    "git_configuration",
    "git_create_repository", 
    "git_pull_remote",
    "git_push_remote",
    
    # SSH utilities
    "open_ssh_proxy",
    "sshkey_configure",
    
    # Project scaffolding utilities
    "create_book_project",
    "create_translation_project",
]

