# Python Shell Utilities

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A collection of powerful command-line utilities designed to automate common developer tasks, such as Git operations, SSH configuration, and project scaffolding. This project provides a suite of standalone scripts that are packaged for easy installation and use directly from your shell.

## Key Features

- **Git Automation**: Configure Git, create repositories, and streamline push/pull operations.
- **SSH Management**: Easily configure SSH keys and manage SSH proxies.
- **Project Scaffolding**: Quickly create new project structures from predefined templates.
- **Robust and Secure**: Scripts are designed with security in mind, preventing common issues like shell injection.
- **Well-Tested**: A comprehensive unit test suite ensures reliability and stability.

## Architecture

The project follows a simple and robust architectural pattern. A central utility module, `src/common.py`, provides shared, secure functions for executing shell commands with real-time output. Each piece of functionality is implemented as a separate script within the `src/` directory. These scripts act as standalone command-line entry points, parsing their own arguments and utilizing the common module for heavy lifting.

This design promotes modularity, making it easy to test, maintain, and extend each tool independently.

A typical script is structured with a `main` function to serve as the entry point defined in `pyproject.toml`:

```python
# Example structure for a script in src/
import sys
from .common import run_command, print_banner

def execute_logic(arg1, arg2):
    """Contains the core logic for the script."""
    print(f"Executing with {arg1} and {arg2}")
    # Utilizes the robust command runner
    run_command(f"echo Hello {arg1}")

def main():
    """
    Entry point for the command-line tool.
    Parses arguments and calls the core logic.
    """
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <arg1> <arg2>")
        sys.exit(1)
    
    print_banner(f"Running {sys.argv[0]}")
    execute_logic(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
```

## Installation

This project is designed to be installed using `pip`. The `install.py` script is deprecated and should not be used.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/owlman/pythonShell.git
    cd python-shell
    ```

2.  **Install the package using pip:**
    This command will install the package and automatically make all the command-line tools available in your system's path.
    ```bash
    pip install .
    ```

## Available Commands

After installation, the following commands will be available in your shell.

| Command              | Source Script                     | Description                                                                 |
| -------------------- | --------------------------------- | --------------------------------------------------------------------------- |
| `git-config`         | `src/git_configuration.py`        | Configures local Git user name and email.                                   |
| `git-create-repo`    | `src/git_create_repository.py`    | Initializes a new Git repository in the current directory.                  |
| `git-pull`           | `src/git_pull_remote.py`          | Pulls changes from a specified remote branch.                               |
| `git-push`           | `src/git_push_remote.py`          | Pushes the current branch to a specified remote.                            |
| `ssh-proxy`          | `src/open_ssh_proxy.py`           | Opens an SSH proxy connection.                                              |
| `ssh-key-config`     | `src/sshkey_configure.py`         | Configures SSH keys for Git authentication.                                 |
| `create-book`        | `src/create_book_project.py`      | Creates a new book project structure from a template.                       |
| `create-translation` | `src/create_translation_project.py` | Creates a new translation project structure from a template.              |

## Outputs

The execution of these scripts produces the following artifacts or system-state changes.

| Name                        | Description                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
| `Configured .gitconfig`     | The user's local `.gitconfig` file is updated with their name and email.    |
| `Initialized Git Repository`| A `.git` directory is created, turning the current folder into a repository.  |
| `New Project Directory`     | A new directory is created based on the specified project template (`.zip`).  |
| `Updated SSH Config`        | The user's SSH configuration may be updated with new key or proxy settings. |

## Development

To contribute to the project, set up your environment as follows.

1.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install in editable mode with development dependencies:**
    ```bash
    pip install -e .[dev]
    ```

3.  **Run tests:**
    ```bash
    pytest
    ```

4.  **Run linter:**
    ```bash
    ruff check .
    ```

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.