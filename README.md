# pythonShell

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)

一个 Python 自动化脚本集合，提供日常开发中常用的 Git 管理、SSH 配置、项目创建等命令行工具。

## 功能特性

- 🔧 **Git 自动化**：配置、创建仓库、推送/拉取远程分支
- 🔑 **SSH 管理**：SSH 密钥配置、SSH 代理连接
- 📚 **项目模板**：快速创建书籍项目和翻译项目
- 🛡️ **安全可靠**：命令执行超时控制、实时输出、跨平台支持
- ✅ **测试覆盖**：完整的单元测试保障代码质量

## 安装

### 使用 uv（推荐）

```bash
# 克隆仓库
git clone https://github.com/owlman/pythonShell.git
cd pythonShell

# 使用 uv 安装
uv pip install -e .
```

### 使用 pip

```bash
pip install -e .
```

### 手动安装

```bash
# 运行安装脚本
python install.py /path/to/install/directory
```

## 命令行工具

安装后，以下命令将在系统中可用：

### Git 工具

#### `git-configuration`
配置 Git 全局设置（用户名、邮箱、编辑器等）

```bash
git-configuration <user_name> <user_email>
```

**示例：**
```bash
git-configuration "John Doe" "john@example.com"
```

#### `git-create-repo`
创建新的 Git 仓库并初始化提交

```bash
git-create-repo <git_directory> [init_commit_message]
```

**示例：**
```bash
git-create-repo ./my-project "Initial commit"
```

#### `git-pull-remote`
从所有远程仓库拉取指定分支

```bash
git-pull-remote <git_directory> [branch]
```

**示例：**
```bash
git-pull-remote ./my-project main
```

#### `git-push-remote`
提交更改并推送到所有远程仓库

```bash
git-push-remote <git_directory> [commit_message]
```

**示例：**
```bash
git-push-remote ./my-project "Update documentation"
```

### SSH 工具

#### `ssh-key-configure`
配置 SSH 密钥（如果不存在则创建）

```bash
ssh-key-configure
```

**交互式提示：**
```
Please enter your email for the SSH key: your-email@example.com
```

#### `open-ssh-proxy`
通过 SSH 建立 SOCKS 代理（端口 7070）

```bash
# 设置环境变量
export SSH_USER="username"
export SSH_HOST="example.com"
export SSH_PASSWORD="your_password"

# 运行命令
open-ssh-proxy
```

### 项目创建工具

#### `create-book-project`
从模板创建书籍项目

```bash
create-book-project <project_directory> [project_name]
```

**示例：**
```bash
create-book-project ./projects my-book
```

#### `create-translation-project`
从模板创建翻译项目

```bash
create-translation-project <project_directory> [project_name]
```

**示例：**
```bash
create-translation-project ./projects my-translation
```

## 开发

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest test/test_common.py

# 显示详细输出
pytest -v
```

### 项目结构

```
pythonShell/
├── src/                    # 源代码
│   ├── common.py          # 公共工具函数
│   ├── git_*.py           # Git 相关工具
│   ├── ssh*.py            # SSH 相关工具
│   ├── create_*.py        # 项目创建工具
│   └── template/          # 项目模板
├── test/                   # 单元测试
├── pyproject.toml         # 项目配置
├── install.py             # 安装脚本
└── uninstall.py           # 卸载脚本
```

### 核心模块：`common.py`

提供两个核心工具函数：

- **`run_command(cmd, shell=False, timeout=300)`**  
  安全执行系统命令，支持实时输出、超时控制、跨平台兼容

- **`print_banner(message)`**  
  打印居中的横幅消息，自动适应终端宽度

## 依赖

- Python >= 3.12
- pexpect >= 4.8.0
- pytest >= 9.0.1（开发依赖）

## 许可证

本项目采用 [GNU General Public License v3.0](LICENSE) 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

**Jie Ling** - [jie.owl2008@gmail.com](mailto:jie.owl2008@gmail.com)

## 链接

- [GitHub 仓库](https://github.com/owlman/pythonShell)
- [问题反馈](https://github.com/owlman/pythonShell/issues)
