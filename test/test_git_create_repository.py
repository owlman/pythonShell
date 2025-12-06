#!/usr/bin/env python3
"""
单元测试脚本：test_git_create_repository.py
测试 git_create_repository.py 模块
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import io
import tempfile
import shutil

# 添加 src 目录到 Python 路径
sys.path.insert(0, '/mnt/d/user/Documents/working/开发类项目/pythonShell/src')

import git_create_repository

class TestGitCreateRepository(unittest.TestCase):
    """测试 git_create_repository 模块"""
    
    def setUp(self):
        """测试前准备临时目录"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
    
    def tearDown(self):
        """测试后清理"""
        os.chdir(self.original_cwd)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @patch('sys.argv', ['git_create_repository.py', '/tmp/test_repo'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_create_new_repo_no_commit(self, mock_getcwd, mock_chdir, mock_makedirs, 
                                           mock_exists, mock_check_output, mock_run_command, 
                                           mock_print_banner):
        """测试创建新仓库（无初始提交）"""
        # 模拟目录不存在
        mock_exists.side_effect = lambda path: False if '.git' in path else True
        mock_getcwd.return_value = '/original/path'
        mock_check_output.return_value = ""  # 无文件需要提交
        
        # 模拟文件打开
        with patch('builtins.open', mock_open()) as mock_file:
            git_create_repository.main()
            
            # 验证目录创建
            mock_makedirs.assert_called_once_with('/tmp/test_repo', exist_ok=True)
            
            # 验证目录切换（注意：实际代码中会先切换到项目目录，最后切换回原始目录）
        # 检查是否调用了 chdir
        self.assertTrue(mock_chdir.called)
        # 检查是否至少有一次切换到项目目录
        project_dir_calls = [call for call in mock_chdir.call_args_list if call[0][0] == '/tmp/test_repo']
        self.assertGreater(len(project_dir_calls), 0)
        
        # 验证 git init 被调用（因为 .git 不存在）
        mock_run_command.assert_any_call(["git", "init"])
        
        # 验证 .gitignore 和 README.md 被创建
        self.assertEqual(mock_file.call_count, 2)
        
        # 验证 git 命令序列
        expected_calls = [
            call(["git", "init"]),
            call(["git", "status"]),
            call(["git", "add", "."])
        ]
        mock_run_command.assert_has_calls(expected_calls, any_order=False)
            
            # 验证没有提交（因为无文件变化）
            commit_calls = [call for call in mock_run_command.call_args_list 
                          if 'commit' in str(call)]
            self.assertEqual(len(commit_calls), 0)
    
    @patch('sys.argv', ['git_create_repository.py', '/tmp/test_repo', 'Custom commit message'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_create_new_repo_with_commit(self, mock_getcwd, mock_chdir, mock_makedirs,
                                             mock_exists, mock_check_output, mock_run_command,
                                             mock_print_banner):
        """测试创建新仓库（有初始提交）"""
        mock_exists.side_effect = lambda path: False if '.git' in path else True
        mock_getcwd.return_value = '/original/path'
        mock_check_output.return_value = "M  test.txt\n"  # 有文件需要提交
        
        with patch('builtins.open', mock_open()):
            git_create_repository.main()
            
            # 验证提交被调用
            commit_calls = [call for call in mock_run_command.call_args_list 
                          if 'commit' in str(call)]
            self.assertEqual(len(commit_calls), 1)
            
            # 验证提交消息
            commit_call = commit_calls[0]
            self.assertEqual(commit_call[0][0], ["git", "commit", "-m", "Custom commit message"])
    
    @patch('sys.argv', ['git_create_repository.py', '/tmp/test_repo'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_existing_repo(self, mock_getcwd, mock_chdir, mock_makedirs,
                               mock_exists, mock_check_output, mock_run_command,
                               mock_print_banner):
        """测试已存在的仓库"""
        mock_exists.side_effect = lambda path: True  # .git 已存在
        mock_getcwd.return_value = '/original/path'
        mock_check_output.return_value = ""
        
        with patch('builtins.open', mock_open()):
            git_create_repository.main()
            
            # 验证 git init 没有被调用（因为 .git 已存在）
            init_calls = [call for call in mock_run_command.call_args_list 
                         if 'init' in str(call)]
            self.assertEqual(len(init_calls), 0)
    
    @patch('sys.argv', ['git_create_repository.py'])
    @patch('sys.stdout.write')
    def test_main_insufficient_arguments(self, mock_write):
        """测试参数不足的情况"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_create_repository.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Usage:", output)
    
    @patch('sys.argv', ['git_create_repository.py', 'dir1', 'msg1', 'extra'])
    @patch('sys.stdout.write')
    def test_main_too_many_arguments(self, mock_write):
        """测试参数过多的情况"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_create_repository.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Usage:", output)
    
    @patch('sys.argv', ['git_create_repository.py', '/tmp/test_repo'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_default_commit_message(self, mock_getcwd, mock_chdir, mock_makedirs,
                                        mock_exists, mock_check_output, mock_run_command,
                                        mock_print_banner):
        """测试默认提交消息"""
        mock_exists.side_effect = lambda path: False if '.git' in path else True
        mock_getcwd.return_value = '/original/path'
        mock_check_output.return_value = "M  test.txt\n"
        
        with patch('builtins.open', mock_open()):
            git_create_repository.main()
            
            # 验证默认提交消息
            commit_calls = [call for call in mock_run_command.call_args_list 
                          if 'commit' in str(call)]
            self.assertEqual(len(commit_calls), 1)
            self.assertEqual(commit_calls[0][0][0], ["git", "commit", "-m", "Initial commit"])
    
    @patch('sys.argv', ['git_create_repository.py', '/tmp/test_repo', ''])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_empty_commit_message(self, mock_getcwd, mock_chdir, mock_makedirs,
                                      mock_exists, mock_check_output, mock_run_command,
                                      mock_print_banner):
        """测试空提交消息（应使用默认消息）"""
        mock_exists.side_effect = lambda path: False if '.git' in path else True
        mock_getcwd.return_value = '/original/path'
        mock_check_output.return_value = "M  test.txt\n"
        
        with patch('builtins.open', mock_open()):
            git_create_repository.main()
            
            # 验证使用默认提交消息
            commit_calls = [call for call in mock_run_command.call_args_list 
                          if 'commit' in str(call)]
            self.assertEqual(len(commit_calls), 1)
            self.assertEqual(commit_calls[0][0][0], ["git", "commit", "-m", "Initial commit"])
    
    @patch('sys.argv', ['git_create_repository.py', '/tmp/test_repo'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('subprocess.check_output')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_main_command_failure(self, mock_getcwd, mock_chdir, mock_makedirs,
                                 mock_exists, mock_check_output, mock_run_command,
                                 mock_print_banner):
        """测试命令执行失败"""
        mock_exists.side_effect = lambda path: False if '.git' in path else True
        mock_getcwd.return_value = '/original/path'
        mock_check_output.return_value = ""
        
        # 模拟 git init 失败
        mock_run_command.side_effect = Exception("Git init failed")
        
        with patch('builtins.open', mock_open()):
            with self.assertRaises(Exception) as cm:
                git_create_repository.main()
            
            self.assertIn("Git init failed", str(cm.exception))
    
    def test_real_directory_creation(self):
        """测试实际目录创建（集成测试）"""
        test_repo_path = os.path.join(self.temp_dir, "test_repo")
        
        # 模拟命令行参数
        with patch('sys.argv', ['git_create_repository.py', test_repo_path, 'Test commit']):
            # 模拟 common 模块的函数
            with patch('common.print_banner') as mock_banner:
                with patch('common.run_command') as mock_run:
                    mock_run.return_value = 0
                    
                    # 模拟 subprocess.check_output
                    with patch('subprocess.check_output') as mock_check:
                        mock_check.return_value = "M  test.txt\n"
                        
                        git_create_repository.main()
        
        # 验证目录被创建
        self.assertTrue(os.path.exists(test_repo_path))

if __name__ == '__main__':
    unittest.main()
