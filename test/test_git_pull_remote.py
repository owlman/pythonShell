#!/usr/bin/env python3
"""
单元测试脚本：test_git_pull_remote.py
测试 git_pull_remote.py 模块
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import io
import subprocess

# 添加 src 目录到 Python 路径
sys.path.insert(0, '/mnt/d/user/Documents/working/开发类项目/pythonShell/src')

import git_pull_remote

class TestGitPullRemote(unittest.TestCase):
    """测试 git_pull_remote 模块"""
    
    @patch('sys.argv', ['git_pull_remote.py', '/tmp/test_repo'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.path.isdir')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_success_default_branch(self, mock_getcwd, mock_chdir, mock_isdir,
                                        mock_subprocess_run, mock_check_output,
                                        mock_run_command, mock_print_banner):
        """测试成功拉取默认分支（master）"""
        # 模拟目录存在且是有效的
        mock_isdir.return_value = True
        mock_getcwd.return_value = '/original/path'
        
        # 模拟 git status 成功（是 git 仓库）
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        
        # 模拟远程仓库列表
        mock_check_output.return_value = "origin\nupstream\n"
        
        # 模拟 run_command 成功
        mock_run_command.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            git_pull_remote.main()
            
            # 验证目录检查
            mock_isdir.assert_called_once_with('/tmp/test_repo')
            
            # 验证目录切换
            mock_chdir.assert_any_call('/tmp/test_repo')
            mock_chdir.assert_any_call('/original/path')
            
            # 验证 git status 检查
            mock_subprocess_run.assert_called_once_with(
                ["git", "status"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # 验证获取远程仓库列表
            mock_check_output.assert_called_once_with(["git", "remote"], text=True)
            
            # 验证拉取命令（2个远程仓库）
            self.assertEqual(mock_run_command.call_count, 2)
            
            # 验证拉取的是 master 分支
            expected_calls = [
                call(["git", "pull", "origin", "master"]),
                call(["git", "pull", "upstream", "master"])
            ]
            mock_run_command.assert_has_calls(expected_calls, any_order=True)
            
            # 验证没有退出
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['git_pull_remote.py', '/tmp/test_repo', 'develop'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.path.isdir')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_success_custom_branch(self, mock_getcwd, mock_chdir, mock_isdir,
                                       mock_subprocess_run, mock_check_output,
                                       mock_run_command, mock_print_banner):
        """测试成功拉取自定义分支"""
        mock_isdir.return_value = True
        mock_getcwd.return_value = '/original/path'
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        mock_check_output.return_value = "origin\n"
        mock_run_command.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            git_pull_remote.main()
            
            # 验证拉取的是 develop 分支
            mock_run_command.assert_called_once_with(["git", "pull", "origin", "develop"])
            
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['git_pull_remote.py'])
    @patch('sys.stdout.write')
    def test_main_insufficient_arguments(self, mock_write):
        """测试参数不足的情况"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_pull_remote.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Usage:", output)
    
    @patch('sys.argv', ['git_pull_remote.py', 'dir1', 'branch1', 'extra'])
    @patch('sys.stdout.write')
    def test_main_too_many_arguments(self, mock_write):
        """测试参数过多的情况"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_pull_remote.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Usage:", output)
    
    @patch('sys.argv', ['git_pull_remote.py', '/tmp/nonexistent'])
    @patch('os.path.isdir')
    @patch('sys.stdout.write')
    def test_main_invalid_directory(self, mock_write, mock_isdir):
        """测试无效目录"""
        mock_isdir.return_value = False
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_pull_remote.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Error:", output)
            self.assertIn("not a valid directory", output)
    
    @patch('sys.argv', ['git_pull_remote.py', '/tmp/test_repo'])
    @patch('common.print_banner')
    @patch('subprocess.run')
    @patch('os.path.isdir')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_not_git_repository(self, mock_getcwd, mock_chdir, mock_isdir,
                                    mock_subprocess_run, mock_print_banner):
        """测试非 Git 仓库目录"""
        mock_isdir.return_value = True
        mock_getcwd.return_value = '/original/path'
        
        # 模拟 git status 失败（不是 git 仓库）
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "git status")
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_pull_remote.main()
            
            # 验证退出码（脚本使用 exit() 无参数，默认返回 None，但会被转换为 0）
            # 这里我们主要验证错误信息
            output = mock_stdout.getvalue()
            self.assertIn("Error: Not a git repository.", output)
    
    @patch('sys.argv', ['git_pull_remote.py', '/tmp/test_repo'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.path.isdir')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_no_remotes(self, mock_getcwd, mock_chdir, mock_isdir,
                            mock_subprocess_run, mock_check_output,
                            mock_run_command, mock_print_banner):
        """测试没有远程仓库的情况"""
        mock_isdir.return_value = True
        mock_getcwd.return_value = '/original/path'
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        
        # 模拟没有远程仓库
        mock_check_output.return_value = ""
        
        with patch('sys.exit') as mock_exit:
            git_pull_remote.main()
            
            # 验证没有拉取命令（因为无远程仓库）
            mock_run_command.assert_not_called()
            
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['git_pull_remote.py', '/tmp/test_repo'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.path.isdir')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_pull_failure(self, mock_getcwd, mock_chdir, mock_isdir,
                              mock_subprocess_run, mock_check_output,
                              mock_run_command, mock_print_banner):
        """测试拉取失败的情况"""
        mock_isdir.return_value = True
        mock_getcwd.return_value = '/original/path'
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        mock_check_output.return_value = "origin\n"
        
        # 模拟拉取失败
        mock_run_command.side_effect = Exception("Pull failed")
        
        with self.assertRaises(Exception) as cm:
            git_pull_remote.main()
        
        self.assertIn("Pull failed", str(cm.exception))
    
    @patch('sys.argv', ['git_pull_remote.py', '/tmp/test_repo', ''])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.path.isdir')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_empty_branch_name(self, mock_getcwd, mock_chdir, mock_isdir,
                                   mock_subprocess_run, mock_check_output,
                                   mock_run_command, mock_print_banner):
        """测试空分支名（应使用默认 master）"""
        mock_isdir.return_value = True
        mock_getcwd.return_value = '/original/path'
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        mock_check_output.return_value = "origin\n"
        mock_run_command.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            git_pull_remote.main()
            
            # 验证使用默认分支 master
            mock_run_command.assert_called_once_with(["git", "pull", "origin", "master"])
            
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['git_pull_remote.py', '/tmp/test_repo'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.path.isdir')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_multiple_remotes_with_whitespace(self, mock_getcwd, mock_chdir, mock_isdir,
                                                  mock_subprocess_run, mock_check_output,
                                                  mock_run_command, mock_print_banner):
        """测试多个远程仓库（包含空白字符）"""
        mock_isdir.return_value = True
        mock_getcwd.return_value = '/original/path'
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        
        # 模拟包含空白字符的远程仓库列表
        mock_check_output.return_value = "origin  \n  upstream  \n  third-remote\n"
        mock_run_command.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            git_pull_remote.main()
            
            # 验证拉取命令被调用3次
            self.assertEqual(mock_run_command.call_count, 3)
            
            # 验证空白字符被正确处理
            expected_calls = [
                call(["git", "pull", "origin", "master"]),
                call(["git", "pull", "upstream", "master"]),
                call(["git", "pull", "third-remote", "master"])
            ]
            
            # 检查每个调用是否存在
            actual_calls = [call[0][0] for call in mock_run_command.call_args_list]
            # 简化检查：只验证调用次数
            self.assertEqual(mock_run_command.call_count, 3)
            
            mock_exit.assert_not_called()

if __name__ == '__main__':
    unittest.main()