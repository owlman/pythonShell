#!/usr/bin/env python
"""
    Created on 2016-5-13
    
    @author: lingjie
    @name:   git_commit
"""

import os
import sys
import time
import subprocess

# 检查参数数量
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: git_commit.py <git_dir> [commit_message]")
    exit(1)

# 打印标题
title = "=    Starting " + sys.argv[0] + "......    ="
n = len(title)
print(n * '=')
print(title)
print(n * '=')

# 检查并切换到工作目录
git_dir = sys.argv[1]
if not os.path.isdir(git_dir):
    print(f"Error: Directory '{git_dir}' does not exist.")
    exit(1)
os.chdir(git_dir)
print("work_dir: " + git_dir)

# 获取提交信息
commit_message = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] else "committed at " + time.strftime("%Y-%m-%d", time.localtime())

# 执行 git 命令
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: Git command failed with exit code {e.returncode}")
    exit(1)

# 打印完成信息
print("Commit is complete!")
print(n * '=')
print("=     Done!" + (n - len("=     Done!") - 1) * ' ' + "=")
print(n * '=')
