#!/usr/bin/env python3
"""
单元测试脚本：test_git_push_remote.py
测试 git_push_remote.py 模块
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import io
import subprocess

# 添加 src 目录到 Python 路径
sys.path.insert(0, '/mnt/d/user/Documents/working/开发类项目/pythonShell/src')

import git_push_remote

class TestGitPushRemote(unittest.TestCase):
    """测试 git_push_remote 模块"""
    
    @patch('sys.argv', ['git_push_remote.py', '/tmp/test_repo', 'Test commit message'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_success_with_commit(self, mock_getcwd, mock_chdir, mock_subprocess_run,
                                     mock_check_output, mock_run_command, mock_print_banner):
        """测试成功推送（有提交）"""
        # 模拟当前目录和目录切换
        mock_getcwd.return_value = '/original/path'
        
        # 模拟 git status 成功
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        
        # 模拟 git status --porcelain 有变化
        mock_check_output.side_effect = [
            "M  file1.txt\nA  file2.txt\n",  # git status --porcelain
            "origin\nupstream\n",            # git remote
            "main\n"                         # git branch --show-current
        ]
        
        # 模拟 run_command 成功
        mock_run_command.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            git_push_remote.main()
            
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
            
            # 验证提交相关命令
            expected_commit_calls = [
                call(["git", "add", "."]),
                call(["git", "commit", "-m", "Test commit message"])
            ]
            
            # 验证推送命令（2个远程仓库，每个2个命令）
            expected_push_calls = [
                call(["git", "pull", "--rebase", "origin", "main"]),
                call(["git", "push", "origin", "main"]),
                call(["git", "pull", "--rebase", "upstream", "main"]),
                call(["git", "push", "upstream", "main"])
            ]
            
            # 合并所有预期调用
            all_expected_calls = expected_commit_calls + expected_push_calls
            
            # 验证调用次数（2个提交命令 + 4个推送命令 = 6个）
            self.assertEqual(mock_run_command.call_count, 6)
            
            # 验证调用顺序
            actual_calls = [call[0][0] for call in mock_run_command.call_args_list]
            
            # 检查前2个是提交命令
            self.assertEqual(actual_calls[0], ["git", "add", "."])
            self.assertEqual(actual_calls[1], ["git", "commit", "-m", "Test commit message"])
            
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['git_push_remote.py', '/tmp/test_repo'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_success_no_commit(self, mock_getcwd, mock_chdir, mock_subprocess_run,
                                   mock_check_output, mock_run_command, mock_print_banner):
        """测试成功推送（无提交）"""
        mock_getcwd.return_value = '/original/path'
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        
        # 模拟 git remote 和 git branch
        mock_check_output.side_effect = [
            "origin\n",    # git remote
            "main\n"       # git branch --show-current
        ]
        
        mock_run_command.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            git_push_remote.main()
            
            # 验证没有提交命令（只有推送命令）
            commit_calls = [call for call in mock_run_command.call_args_list 
                          if 'commit' in str(call) or 'add' in str(call)]
            self.assertEqual(len(commit_calls), 0)
            
            # 验证只有推送命令（2个：pull --rebase 和 push）
            self.assertEqual(mock_run_command.call_count, 2)
            
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['git_push_remote.py', '/tmp/test_repo', ''])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_empty_commit_message(self, mock_getcwd, mock_chdir, mock_subprocess_run,
                                      mock_check_output, mock_run_command, mock_print_banner):
        """测试空提交消息（应跳过提交）"""
        mock_getcwd.return_value = '/original/path'
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        mock_check_output.side_effect = [
            "origin\n",
            "main\n"
        ]
        mock_run_command.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            git_push_remote.main()
            
            # 验证没有提交命令
            commit_calls = [call for call in mock_run_command.call_args_list 
                          if 'commit' in str(call) or 'add' in str(call)]
            self.assertEqual(len(commit_calls), 0)
            
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['git_push_remote.py'])
    @patch('sys.stdout.write')
    def test_main_insufficient_arguments(self, mock_write):
        """测试参数不足的情况"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_push_remote.main()
            
            # 脚本使用 exit() 无参数，但 unittest 会捕获为 SystemExit
            output = mock_stdout.getvalue()
            self.assertIn("Usage:", output)
    
    @patch('sys.argv', ['git_push_remote.py', 'dir1', 'msg1', 'extra'])
    @patch('sys.stdout.write')
    def test_main_too_many_arguments(self, mock_write):
        """测试参数过多的情况"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_push_remote.main()
            
            output = mock_stdout.getvalue()
            self.assertIn("Usage:", output)
    
    @patch('sys.argv', ['git_push_remote.py', '/tmp/nonexistent'])
    @patch('os.chdir')
    @patch('sys.stdout.write')
    def test_main_directory_not_found(self, mock_write, mock_chdir):
        """测试目录不存在"""
        mock_chdir.side_effect = FileNotFoundError
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_push_remote.main()
            
            output = mock_stdout.getvalue()
            self.assertIn("Error:", output)
            self.assertIn("not found", output)
    
    @patch('sys.argv', ['git_push_remote.py', '/tmp/test_repo'])
    @patch('common.print_banner')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_not_git_repository(self, mock_getcwd, mock_chdir, mock_subprocess_run,
                                    mock_print_banner):
        """测试非 Git 仓库目录"""
        mock_getcwd.return_value = '/original/path'
        
        # 模拟 git status 失败
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "git status")
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_push_remote.main()
            
            output = mock_stdout.getvalue()
            self.assertIn("Error: Not a git repository.", output)
    
    @patch('sys.argv', ['git_push_remote.py', '/tmp/test_repo', 'Test commit'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_no_changes_to_commit(self, mock_getcwd, mock_chdir, mock_subprocess_run,
                                      mock_check_output, mock_run_command, mock_print_banner):
        """测试没有变化可提交"""
        mock_getcwd.return_value = '/original/path'
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        
        # 模拟 git status --porcelain 无变化
        mock_check_output.side_effect = [
            "",           # git status --porcelain (无变化)
            "origin\n",   # git remote
            "main\n"      # git branch --show-current
        ]
        
        mock_run_command.return_value = 0
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            git_push_remote.main()
            
            output = mock_stdout.getvalue()
            self.assertIn("Error: No changes to commit.", output)
            
            # 验证没有提交命令
            commit_calls = [call for call in mock_run_command.call_args_list 
                          if 'commit' in str(call) or 'add' in str(call)]
            self.assertEqual(len(commit_calls), 0)
    
    @patch('sys.argv', ['git_push_remote.py', '/tmp/test_repo', 'Test commit'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_push_failure(self, mock_getcwd, mock_chdir, mock_subprocess_run,
                              mock_check_output, mock_run_command, mock_print_banner):
        """测试推送失败"""
        mock_getcwd.return_value = '/original/path'
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        mock_check_output.side_effect = [
            "M  file.txt\n",
            "origin\n",
            "main\n"
        ]
        
        # 模拟推送失败
        mock_run_command.side_effect = Exception("Push failed")
        
        with self.assertRaises(Exception) as cm:
            git_push_remote.main()
        
        self.assertIn("Push failed", str(cm.exception))
    
    @patch('sys.argv', ['git_push_remote.py', '/tmp/test_repo', 'Test commit'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_permission_error(self, mock_getcwd, mock_chdir, mock_subprocess_run,
                                  mock_check_output, mock_run_command, mock_print_banner):
        """测试权限错误"""
        mock_getcwd.return_value = '/original/path'
        
        # 模拟权限错误
        mock_chdir.side_effect = PermissionError
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_push_remote.main()
            
            output = mock_stdout.getvalue()
            self.assertIn("Error:", output)
            self.assertIn("permission", output)
    
    @patch('sys.argv', ['git_push_remote.py', '/tmp/test_repo', 'Test commit'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_no_remotes(self, mock_getcwd, mock_chdir, mock_subprocess_run,
                            mock_check_output, mock_run_command, mock_print_banner):
        """测试没有远程仓库"""
        mock_getcwd.return_value = '/original/path'
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        mock_check_output.side_effect = [
            "M  file.txt\n",
            "",           # 无远程仓库
            "main\n"
        ]
        
        mock_run_command.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            git_push_remote.main()
            
            # 验证没有推送命令（因为无远程仓库）
            push_calls = [call for call in mock_run_command.call_args_list 
                         if 'push' in str(call) or 'pull' in str(call)]
            self.assertEqual(len(push_calls), 0)
            
            # 验证只有提交命令
            self.assertEqual(mock_run_command.call_count, 2)  # git add 和 git commit
            
            mock_exit.assert_not_called()

if __name__ == '__main__':
    unittest.main()