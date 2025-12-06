# pythonShell

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)

一个 Python 自动化脚本集合，提供日常开发中常用的 Git 管理、SSH 配置、项目模板创建等命令行工具。

## 功能特性

- 🔧 **Git 自动化**：配置、创建仓库、推送/拉取远程分支
- 🔑 **SSH 管理**：SSH 密钥配置、SSH 代理连接
- 📚 **项目模板**：快速创建书籍项目和翻译项目
- 🛡️ **安全可靠**：命令执行超时控制、实时输出、跨平台支持
- ✅ **测试覆盖**：完整的单元测试保障代码质量

## 安装

### 方式一：手动安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/owlman/pythonShell.git
cd pythonShell

# 安装依赖
pip install pexpect

# 运行安装脚本（将命令安装到指定目录）
python install.py ~/.local/bin
```

### 方式二：使用 pip（需要路径不含中文）

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装项目
pip install -e .
```

### 方式三：使用 uv

```bash
uv pip install -e .
```

## 命令行工具

安装后，以下命令将在系统中可用：

### Git 工具

#### `git-configuration`
配置 Git 全局设置（用户名、邮箱、编辑器、颜色等）

```bash
git-configuration <user_name> <user_email>
```

**功能：**
- 设置用户名和邮箱
- 配置推送策略为 `simple`
- 启用彩色输出
- 设置 UTF-8 编码
- 配置 Vim 为默认编辑器
- 根据操作系统自动配置换行符处理（Windows: `true`, Linux/macOS: `input`）

**示例：**
```bash
git-configuration "John Doe" "john@example.com"
```

#### `git-create-repository`
创建新的 Git 仓库并初始化提交

```bash
git-create-repository <git_directory> [init_commit_message]
```

**功能：**
- 初始化 Git 仓库
- 创建 `.gitignore` 和 `README.md` 文件
- 自动添加并提交初始文件

**示例：**
```bash
git-create-repository ./my-project "Initial commit"
git-create-repository ./my-project  # 使用默认提交信息
```

#### `git-pull-remote`
从所有配置的远程仓库拉取指定分支

```bash
git-pull-remote <git_directory> [branch]
```

**功能：**
- 自动检测所有远程仓库
- 逐个从远程拉取更新
- 默认分支为 `master`

**示例：**
```bash
git-pull-remote ./my-project main
git-pull-remote ./my-project  # 默认拉取 master 分支
```

#### `git-push-remote`
提交更改并推送到所有配置的远程仓库

```bash
git-push-remote <git_directory> [commit_message]
```

**功能：**
- 可选：添加并提交所有更改
- 自动检测当前分支
- 先 `pull --rebase` 再 `push` 到所有远程仓库

**示例：**
```bash
git-push-remote ./my-project "Update documentation"
git-push-remote ./my-project  # 仅推送，不提交
```

### SSH 工具

#### `sshkey-configure`
配置 SSH 密钥（如果不存在则自动创建）

```bash
sshkey-configure
```

**功能：**
- 检查 `~/.ssh/id_rsa` 是否存在
- 不存在时交互式创建新密钥（RSA 2048位）
- 自动创建 `.ssh` 目录

**交互式提示：**
```
Please enter your email for the SSH key: your-email@example.com
```

**示例：**
```bash
sshkey-configure
# 然后查看公钥
cat ~/.ssh/id_rsa.pub
```

#### `open-ssh-proxy`
通过 SSH 建立 SOCKS 代理（监听端口 7070）

```bash
open-ssh-proxy
```

**前置条件：**
需要设置以下环境变量：
- `SSH_USER`: SSH 用户名
- `SSH_HOST`: SSH 服务器地址
- `SSH_PASSWORD`: SSH 密码

**示例：**
```bash
# 设置环境变量
export SSH_USER="username"
export SSH_HOST="example.com"
export SSH_PASSWORD="your_password"

# 启动代理
open-ssh-proxy

# 在另一个终端配置代理使用
export http_proxy=socks5://127.0.0.1:7070
export https_proxy=socks5://127.0.0.1:7070
```

### 项目创建工具

#### `create-book-project`
从模板创建书籍项目

```bash
create-book-project <project_directory> [project_name]
```

**功能：**
- 从 `template/book_proj.zip` 解压模板
- 自动创建项目目录
- 默认项目名为 `book_proj`

**示例：**
```bash
create-book-project ./projects my-book
create-book-project ./projects  # 使用默认名称 book_proj
```

#### `create-translation-project`
从模板创建翻译项目

```bash
create-translation-project <project_directory> [project_name]
```

**功能：**
- 从 `template/translation_proj.zip` 解压模板
- 自动创建项目目录
- 默认项目名为 `translation_proj`

**示例：**
```bash
create-translation-project ./projects my-translation
create-translation-project ./projects  # 使用默认名称 translation_proj
```

## 开发

### 运行测试

项目包含完整的单元测试覆盖：

```bash
# 使用 unittest 运行所有测试
python3 -m unittest discover -s test -p "test_*.py" -v

# 运行特定测试文件
python3 test/test_common.py

# 使用 pytest（需要安装开发依赖）
pytest -v
pytest test/test_common.py
pytest --cov=src --cov-report=html
```

### 测试覆盖

所有模块都有对应的单元测试：

- `test/test_common.py` - 公共工具函数测试
- `test/test_git_configuration.py` - Git 配置测试
- `test/test_git_create_repository.py` - Git 仓库创建测试
- `test/test_git_pull_remote.py` - Git 拉取测试
- `test/test_git_push_remote.py` - Git 推送测试
- `test/test_create_book_project.py` - 书籍项目创建测试
- `test/test_create_translation_project.py` - 翻译项目创建测试
- `test/test_sshkey_configure.py` - SSH 密钥配置测试
- `test/test_open_ssh_proxy.py` - SSH 代理测试

### 项目结构

```
pythonShell/
├── src/                              # 源代码目录
│   ├── common.py                    # 公共工具函数
│   ├── git_configuration.py         # Git 配置工具
│   ├── git_create_repository.py     # Git 仓库创建工具
│   ├── git_pull_remote.py           # Git 拉取工具
│   ├── git_push_remote.py           # Git 推送工具
│   ├── create_book_project.py       # 书籍项目创建工具
│   ├── create_translation_project.py # 翻译项目创建工具
│   ├── sshkey_configure.py          # SSH 密钥配置工具
│   ├── open_ssh_proxy.py            # SSH 代理工具
│   └── template/                    # 项目模板
│       ├── book_proj.zip           # 书籍项目模板
│       └── translation_proj.zip    # 翻译项目模板
├── test/                             # 单元测试目录
│   ├── test_common.py
│   ├── test_git_*.py
│   ├── test_create_*.py
│   └── test_ssh*.py
├── pyproject.toml                    # 项目配置文件
├── install.py                        # 安装脚本
├── uninstall.py                      # 卸载脚本
├── LICENSE                           # GPL-3.0 许可证
└── README.md                         # 项目文档
```

### 核心模块：`common.py`

提供两个核心工具函数：

#### `run_command(cmd, shell=False, timeout=300)`

安全执行系统命令，具有以下特性：

- **实时输出**：stdout 和 stderr 实时打印到终端
- **超时控制**：默认 300 秒超时，可自定义
- **跨平台**：支持 Windows、Linux、macOS
- **安全性**：默认 `shell=False`，避免 shell 注入
- **错误处理**：命令失败时抛出 `SubprocessError`

**参数：**
- `cmd` (str | list): 要执行的命令
- `shell` (bool): 是否通过 shell 执行，默认 False
- `timeout` (int): 超时时间（秒），None 表示无限制

**返回：**
- `int`: 命令退出码（0 表示成功）

**示例：**
```python
from common import run_command

# 列表形式（推荐，更安全）
run_command(['git', 'status'])

# 字符串形式（需要 shell=True）
run_command('echo "Hello World"', shell=True)

# 自定义超时
run_command(['long-running-task'], timeout=600)
```

#### `print_banner(message)`

打印居中的横幅消息，自动适应终端宽度

**参数：**
- `message` (str): 要显示的消息

**示例：**
```python
from common import print_banner

print_banner("Starting installation...")
# 输出：
# ##########################################################################
# #                      Starting installation...                        #
# ##########################################################################
```

## 依赖

### 运行时依赖

- Python >= 3.12
- pexpect >= 4.8.0（仅 `open-ssh-proxy` 命令需要）

### 开发依赖

- pytest >= 9.0.1
- pytest-cov >= 4.1.0
- pytest-mock >= 3.12.0
- ruff >= 0.1.0

安装开发依赖：
```bash
pip install -e ".[dev]"
```

## 常见问题

### 1. 路径包含中文字符导致安装失败

如果使用 `pip install -e .` 遇到 `UnicodeEncodeError`，请使用手动安装方式：

```bash
python install.py ~/.local/bin
```

### 2. `open-ssh-proxy` 提示缺少 pexpect 模块

```bash
pip install pexpect
```

### 3. 命令未找到

确保安装目录在 PATH 中：

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"

# 重新加载配置
source ~/.bashrc
```

### 4. Windows 下使用注意事项

- `open-ssh-proxy` 需要 Git Bash 或 WSL 环境
- `sshkey-configure` 需要 Git Bash 或 WSL 环境
- 其他命令可在 PowerShell 或 CMD 中使用

## 卸载

### 手动安装的卸载

```bash
python uninstall.py ~/.local/bin
```

### pip 安装的卸载

```bash
pip uninstall pythonshell
```

## 许可证

本项目采用 [GNU General Public License v3.0](LICENSE) 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request！

在提交 PR 前，请确保：
1. 所有测试通过：`python3 -m unittest discover -s test`
2. 代码符合规范（如果安装了 ruff）：`ruff check src test`
3. 添加了相应的单元测试

## 作者

**Jie Ling** - [jie.owl2008@gmail.com](mailto:jie.owl2008@gmail.com)

## 链接

- [GitHub 仓库](https://github.com/owlman/pythonShell)
- [问题反馈](https://github.com/owlman/pythonShell/issues)
- [更新日志](https://github.com/owlman/pythonShell/releases)

## 更新日志

### v0.1.0 (当前版本)

- ✨ 初始版本发布
- ✅ 完整的单元测试覆盖
- 📝 详细的文档说明
- 🔧 8 个实用命令行工具
- 🛡️ 跨平台支持（Linux、macOS、Windows）
