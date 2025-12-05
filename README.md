# PythonShell

![Python Version](https://img.shields.io/badge/Python-3.12+-blue) ![License](https://img.shields.io/badge/License-GPLv3-green)  

PythonShell 是一个 Python 自动化脚本集合，包含 Git 配置、SSH 管理、项目创建等日常开发工具。

## 功能特性

### Git 操作工具

- `git-configuration`: Git 配置管理
- `git-create-repo`: 创建 Git 仓库
- `git-pull-remote`: 从远程仓库拉取更新
- `git-push-remote`: 推送更新到远程仓库

### 项目管理工具

- `create-book-project`: 创建书籍项目模板
- `create-translation-project`: 创建翻译项目模板

### SSH 工具

- `ssh-key-configure`: SSH 密钥配置
- `open-ssh-proxy`: 开启 SSH 代理

## 安装

### 从源码安装

```bash
git clone https://github.com/owlman/pythonShell.git
cd pythonShell
python -m pip install -e .
```

### 使用安装脚本

```bash
python install.py <install_path>
```

## 使用方法

安装完成后，所有脚本都可以作为命令行工具直接使用：

```bash
# Git 配置
git-configuration

# 创建书籍项目
create-book-project

# SSH 密钥配置
ssh-key-configure
```

## 开发环境

- Python 3.12+
- 依赖项：pexpect>=4.8.0

## 测试

```bash
python -m pytest
```

## 联系方式

如果您对这个项目感兴趣或有任何建议，可以通过以下方式联系我：

- 邮箱: [jie.owl2008@gmail.com](mailto:jie.owl2008@gmail.com)
- 微博: [@凌杰_owlman](https://weibo.com/u/1670107570)
- Twitter/X: [@lingjieowl](https://x.com/lingjieowl)

## 版权声明

Copyright (C) 2016 Jie Ling.

本程序是自由软件；您可以根据自由软件基金会发布的 GNU 通用公共许可证条款（第 2 版或（根据您的选择）任何更高版本）重新分发和/或修改它。

本程序发布的目的是希望它能够有用，但不提供任何担保；甚至不对适销性或特定用途适用性提供默示担保。有关详细信息，请参阅 GNU 通用公共许可证。

您应该随本程序收到一份 GNU 通用公共许可证；如果没有，请写信给自由软件基金会，Inc.，51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA。
