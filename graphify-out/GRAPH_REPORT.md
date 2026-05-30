# Graph Report - .  (2026-05-25)

## Corpus Check
- Corpus is ~6,498 words - fits in a single context window. You may not need a graph.

## Summary
- 199 nodes · 156 edges · 60 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `TestIntegration` - 11 edges
2. `TestRunCommand` - 8 edges
3. `TestSSHKeyConfigure` - 8 edges
4. `TestGitCreateRepository` - 5 edges
5. `TestGitPullRemote` - 5 edges
6. `TestGitPushRemote` - 5 edges
7. `TestCreateBookProject` - 5 edges
8. `TestCreateTranslationProject` - 5 edges
9. `TestPrintBanner` - 3 edges
10. `TestGitConfiguration` - 3 edges

## Surprising Connections (you probably didn't know these)
- `TestRunCommand` --inherits--> `TestCase`  [EXTRACTED]
  test\test_common.py →   _Bridges community 5 → community 7_
- `TestGitCreateRepository` --inherits--> `TestCase`  [EXTRACTED]
  test\test_git_operations.py →   _Bridges community 7 → community 2_
- `TestGitPullRemote` --inherits--> `TestCase`  [EXTRACTED]
  test\test_git_operations.py →   _Bridges community 7 → community 9_
- `TestGitPushRemote` --inherits--> `TestCase`  [EXTRACTED]
  test\test_git_operations.py →   _Bridges community 7 → community 10_
- `TestIntegration` --inherits--> `TestCase`  [EXTRACTED]
  test\test_integration.py →   _Bridges community 7 → community 0_

## Communities

### Community 0 - "Integration Tests"
Cohesion: 0.09
Nodes (11): Integration tests for python-shell-utilities., Test error handling across different modules., Test cross-platform compatibility., Test command line interface integration., Integration tests for the entire package., Set up test fixtures., Clean up test fixtures., Test that all package modules can be imported. (+3 more)

### Community 1 - "Project Scaffolding Tests"
Cohesion: 0.11
Nodes (9): Test module for project scaffolding functionality., Clean up test fixtures., Test cases for create_book_project functionality., Set up test fixtures., Clean up test fixtures., Test cases for create_translation_project functionality., Set up test fixtures., TestCreateBookProject (+1 more)

### Community 2 - "Git Operations Tests"
Cohesion: 0.12
Nodes (5): Test module for Git operations functionality., Test cases for git_create_repository functionality., Set up test fixtures., Clean up test fixtures., TestGitCreateRepository

### Community 3 - "SSH Operations Tests"
Cohesion: 0.14
Nodes (3): Test module for SSH operations functionality., Test cases for open_ssh_proxy functionality., TestOpenSSHProxy

### Community 4 - "Test Fixtures"
Cohesion: 0.17
Nodes (11): mock_project_template(), mock_ssh_dir(), mock_sys_argv(), mock_terminal_size(), Pytest configuration and fixtures for python-shell-utilities tests., Create a temporary directory for tests., Create a mock SSH directory for tests., Create a mock project template for tests. (+3 more)

### Community 5 - "Command Execution Tests"
Cohesion: 0.17
Nodes (7): Test cases for the run_command function., Test running a simple successful command as string., Test running a simple successful command as list., Test running a command that fails., Test command timeout functionality., Test running command with shell=True., TestRunCommand

### Community 6 - "SSH Key Configure Tests"
Cohesion: 0.17
Nodes (7): Test check_default_ssh_key when only one key file exists., Test cases for sshkey_configure functionality., Set up test fixtures., Clean up test fixtures., Test check_default_ssh_key when keys exist., Test check_default_ssh_key when keys don't exist., TestSSHKeyConfigure

### Community 7 - "Mixed Test Classes"
Cohesion: 0.2
Nodes (6): Test module for common utility functions., Test cases for the print_banner function., TestPrintBanner, Test cases for git_configuration functionality., TestGitConfiguration, TestCase

### Community 8 - "Common Utilities"
Cohesion: 0.29
Nodes (5): print_banner(), Print a centered banner around a message, dynamically sized     to fit the termi, Execute a system command safely with real-time stdout/stderr output.      Featur, run_command(), Test package for python-shell-utilities.

### Community 9 - "Git Pull Tests"
Cohesion: 0.33
Nodes (4): Test cases for git_pull_remote functionality., Set up test fixtures., Clean up test fixtures., TestGitPullRemote

### Community 10 - "Git Push Tests"
Cohesion: 0.33
Nodes (4): Test cases for git_push_remote functionality., Set up test fixtures., Clean up test fixtures., TestGitPushRemote

### Community 11 - "Main Entry Point"
Cohesion: 0.67
Nodes (0): 

### Community 12 - "Graphify Internals"
Cohesion: 1.0
Nodes (0): 

### Community 13 - "SSH Key Configuration"
Cohesion: 1.0
Nodes (2): check_default_ssh_key(), main()

### Community 14 - "Book Project Creation"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "Translation Project Creation"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "Git Configuration"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "Git Repository Creation"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Git Pull Remote"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Git Push Remote"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Open SSH Proxy"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (0): 

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (0): 

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Test print_banner with default terminal width.

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Test print_banner with custom terminal width.

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Test print_banner with a long message.

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Test git configuration commands on Linux.

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Test git configuration commands on Windows.

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Test main function with invalid arguments.

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): Test successful repository creation.

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Test repository creation with custom name.

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): Test main function with invalid arguments.

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Test successful git pull.

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Test main function with invalid arguments.

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): Test git pull with different remote and branch.

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): Test successful git push.

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): Test main function with invalid arguments.

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (1): Test git push with different remote and branch.

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (1): Test git configuration integration.

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (1): Test SSH operations integration.

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (1): Test SSH key configuration integration.

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (1): Test main function with custom project name.

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (1): Test main function with invalid arguments.

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (1): Test successful project creation.

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (1): Test main function with custom project name.

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (1): Test main function with invalid arguments.

### Community 48 - "Community 48"
Cohesion: 1.0
Nodes (1): Test successful project creation.

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (1): Test main function with default project name.

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (1): Test main function when SSH key already exists.

### Community 51 - "Community 51"
Cohesion: 1.0
Nodes (1): Test main function creating new SSH key.

### Community 52 - "Community 52"
Cohesion: 1.0
Nodes (1): Test main function shows warning on Windows.

### Community 53 - "Community 53"
Cohesion: 1.0
Nodes (1): Test successful SSH proxy connection.

### Community 54 - "Community 54"
Cohesion: 1.0
Nodes (1): Test handling of pexpect errors.

### Community 55 - "Community 55"
Cohesion: 1.0
Nodes (1): Test main function with invalid arguments.

### Community 56 - "Community 56"
Cohesion: 1.0
Nodes (1): Test main function with empty username.

### Community 57 - "Community 57"
Cohesion: 1.0
Nodes (1): Test main function with empty host.

### Community 58 - "Community 58"
Cohesion: 1.0
Nodes (1): Test main function with empty password.

### Community 59 - "Community 59"
Cohesion: 1.0
Nodes (1): Test main function with complex username and password.

## Knowledge Gaps
- **88 isolated node(s):** `Execute a system command safely with real-time stdout/stderr output.      Featur`, `Print a centered banner around a message, dynamically sized     to fit the termi`, `Test package for python-shell-utilities.`, `Pytest configuration and fixtures for python-shell-utilities tests.`, `Create a temporary directory for tests.` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Book Project Creation`** (2 nodes): `create_book_project.py`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Translation Project Creation`** (2 nodes): `create_translation_project.py`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Git Configuration`** (2 nodes): `git_configuration.py`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Git Repository Creation`** (2 nodes): `git_create_repository.py`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Git Pull Remote`** (2 nodes): `git_pull_remote.py`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Git Push Remote`** (2 nodes): `git_push_remote.py`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Open SSH Proxy`** (2 nodes): `open_ssh_proxy.py`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `_graphify_ast.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `_graphify_cache_check.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `_graphify_final.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `_graphify_merge.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Test print_banner with default terminal width.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Test print_banner with custom terminal width.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Test print_banner with a long message.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Test git configuration commands on Linux.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `Test git configuration commands on Windows.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Test main function with invalid arguments.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `Test successful repository creation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `Test repository creation with custom name.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `Test main function with invalid arguments.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Test successful git pull.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Test main function with invalid arguments.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `Test git pull with different remote and branch.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `Test successful git push.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `Test main function with invalid arguments.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `Test git push with different remote and branch.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `Test git configuration integration.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `Test SSH operations integration.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `Test SSH key configuration integration.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `Test main function with custom project name.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `Test main function with invalid arguments.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `Test successful project creation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `Test main function with custom project name.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `Test main function with invalid arguments.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (1 nodes): `Test successful project creation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `Test main function with default project name.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 50`** (1 nodes): `Test main function when SSH key already exists.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 51`** (1 nodes): `Test main function creating new SSH key.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (1 nodes): `Test main function shows warning on Windows.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (1 nodes): `Test successful SSH proxy connection.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 54`** (1 nodes): `Test handling of pexpect errors.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (1 nodes): `Test main function with invalid arguments.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (1 nodes): `Test main function with empty username.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 57`** (1 nodes): `Test main function with empty host.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (1 nodes): `Test main function with empty password.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 59`** (1 nodes): `Test main function with complex username and password.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TestIntegration` connect `Integration Tests` to `Mixed Test Classes`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Why does `TestSSHKeyConfigure` connect `SSH Key Configure Tests` to `SSH Operations Tests`, `Mixed Test Classes`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Why does `TestRunCommand` connect `Command Execution Tests` to `Mixed Test Classes`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **What connects `Execute a system command safely with real-time stdout/stderr output.      Featur`, `Print a centered banner around a message, dynamically sized     to fit the termi`, `Test package for python-shell-utilities.` to the rest of the system?**
  _88 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Integration Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._
- **Should `Project Scaffolding Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._
- **Should `Git Operations Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._