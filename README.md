# Python Shell Utilities

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](test/)

一个强大的命令行工具集合，旨在自动化常见的开发者任务，包括 Git 操作、SSH 配置和项目脚手架。该项目提供了一套独立的脚本，经过打包后可以直接从 shell 中轻松安装和使用。

## 主要特性

- **Git 自动化**: 配置 Git、创建仓库和简化推送/拉取操作
- **SSH 管理**: 轻松配置 SSH 密钥和管理 SSH 代理
- **项目脚手架**: 从预定义模板快速创建新的项目结构
- **健壮安全**: 脚本设计时考虑了安全性，防止常见问题如 shell 注入
- **充分测试**: 全面的单元测试套件确保可靠性和稳定性

## 架构设计

项目遵循简单而健壮的架构模式。核心工具模块 `src/common.py` 提供了共享的安全函数，用于执行具有实时输出的 shell 命令。每个功能都在 `src/` 目录中作为独立脚本实现。这些脚本作为独立的命令行入口点，解析自己的参数并利用公共模块来完成繁重的工作。

这种设计促进了模块化，使得每个工具都能独立测试、维护和扩展。

典型脚本结构包含一个 `main` 函数，作为在 `pyproject.toml` 中定义的入口点：

```python
# src/ 中脚本的示例结构
import sys
import common

def execute_logic(arg1, arg2):
    """包含脚本的核心逻辑"""
    print(f"执行参数: {arg1} 和 {arg2}")
    # 使用健壮的命令运行器
    common.run_command(f"echo Hello {arg1}")

def main():
    """
    命令行工具的入口点
    解析参数并调用核心逻辑
    """
    if len(sys.argv) < 3:
        print(f"用法: {sys.argv[0]} <参数1> <参数2>")
        sys.exit(1)
    
    common.print_banner(f"运行 {sys.argv[0]}")
    execute_logic(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
```

## 安装

该项目设计为使用 `pip` 安装。

1. **克隆仓库:**
   ```bash
   git clone https://github.com/owlman/pythonShell.git
   cd pythonShell
   ```

2. **使用 pip 安装包:**
   此命令将安装包并自动使所有命令行工具在系统路径中可用。
   ```bash
   pip install .
   ```

## 可用命令

安装后，以下命令将在您的 shell 中可用。

| 命令                 | 源脚本                           | 描述                                       |
| -------------------- | -------------------------------- | ------------------------------------------ |
| `git-config`         | `src/git_configuration.py`       | 配置本地 Git 用户名和邮箱                  |
| `git-create-repo`     | `src/git_create_repository.py`   | 在当前目录初始化新的 Git 仓库              |
| `git-pull-remote`    | `src/git_pull_remote.py`         | 从指定的远程分支拉取更改                   |
| `git-push-remote`    | `src/git_push_remote.py`         | 将当前分支推送到指定的远程                 |
| `ssh-proxy`          | `src/open_ssh_proxy.py`          | 打开 SSH 代理连接                          |
| `ssh-key-config`     | `src/sshkey_configure.py`        | 为 Git 身份验证配置 SSH 密钥               |
| `create-book`        | `src/create_book_project.py`     | 从模板创建新的书籍项目结构                 |
| `create-translation` | `src/create_translation_project.py` | 从模板创建新的翻译项目结构               |

## 输出

这些脚本的执行会产生以下产物或系统状态变化。

| 名称                    | 描述                                           |
| ----------------------- | ---------------------------------------------- |
| `配置的 .gitconfig`     | 用户的本地 `.gitconfig` 文件用姓名和邮箱更新    |
| `初始化的 Git 仓库`     | 创建 `.git` 目录，将当前文件夹转换为仓库       |
| `新项目目录`           | 基于指定的项目模板（`.zip`）创建新目录         |
| `更新的 SSH 配置`       | 用户的 SSH 配置可能用新密钥或代理设置更新       |

## 开发

要为项目做贡献，请按以下步骤设置环境。

1. **创建并激活虚拟环境:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # 或
   .venv\Scripts\activate     # Windows
   ```

2. **以可编辑模式安装开发依赖:**
   ```bash
   pip install -e .[dev]
   ```

3. **运行测试:**
   ```bash
   python -m unittest discover -s test -p "test_*.py"
   ```

4. **运行代码检查:**
   ```bash
   ruff check .
   ```

5. **类型检查:**
   ```bash
   mypy src/
   ```

## 项目结构

```
pythonShell/
├── src/                    # 源代码目录
│   ├── common.py          # 公共工具函数
│   ├── git_configuration.py
│   ├── git_create_repository.py
│   ├── git_pull_remote.py
│   ├── git_push_remote.py
│   ├── open_ssh_proxy.py
│   ├── sshkey_configure.py
│   ├── create_book_project.py
│   ├── create_translation_project.py
│   └── template/          # 项目模板
│       ├── book_proj.zip
│       └── translation_proj.zip
├── test/                  # 测试目录
│   ├── test_common.py
│   ├── test_git_configuration.py
│   ├── test_git_create_repository.py
│   ├── test_git_pull_remote.py
│   ├── test_git_push_remote.py
│   ├── test_open_ssh_proxy.py
│   ├── test_sshkey_configure.py
│   ├── test_create_book_project.py
│   └── test_create_translation_project.py
├── pyproject.toml         # 项目配置
├── README.md             # 本文件
└── LICENSE               # 许可证
```

## 许可证

本项目在 GNU 通用公共许可证 v3.0 下授权。详情请参见 [LICENSE](LICENSE) 文件。