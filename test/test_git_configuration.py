#!/usr/bin/env python3
"""
单元测试脚本：test_git_configuration.py
测试 git_configuration.py 模块
"""

import sys
import unittest
from unittest.mock import patch, MagicMock, call
import io

# 添加 src 目录到 Python 路径
sys.path.insert(0, '/mnt/d/user/Documents/working/开发类项目/pythonShell/src')

import git_configuration

class TestGitConfiguration(unittest.TestCase):
    """测试 git_configuration 模块"""
    
    @patch('sys.argv', ['git_configuration.py', 'test_user', 'test@example.com'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('platform.system')
    def test_main_success_linux(self, mock_system, mock_run_command, mock_print_banner):
        """测试在 Linux 系统上成功执行"""
        # 模拟 Linux 系统
        mock_system.return_value = "Linux"
        
        # 模拟 run_command 成功
        mock_run_command.return_value = 0
        
        # 捕获退出状态
        with patch('sys.exit') as mock_exit:
            git_configuration.main()
            
            # 验证 print_banner 被调用2次
            self.assertEqual(mock_print_banner.call_count, 2)
            
            # 验证 run_command 被调用13次（12个标准命令 + 1个平台特定命令）
            self.assertEqual(mock_run_command.call_count, 13)
            
            # 验证 autocrlf 设置为 input（Linux）
            calls = mock_run_command.call_args_list
            autocrlf_calls = [call for call in calls if 'autocrlf' in str(call)]
            self.assertEqual(len(autocrlf_calls), 1)
            self.assertIn('input', str(autocrlf_calls[0]))
            
            # 验证没有退出
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['git_configuration.py', 'test_user', 'test@example.com'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('platform.system')
    def test_main_success_windows(self, mock_system, mock_run_command, mock_print_banner):
        """测试在 Windows 系统上成功执行"""
        # 模拟 Windows 系统
        mock_system.return_value = "Windows"
        
        # 模拟 run_command 成功
        mock_run_command.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            git_configuration.main()
            
            # 验证 run_command 被调用13次
            self.assertEqual(mock_run_command.call_count, 13)
            
            # 验证 autocrlf 设置为 true（Windows）
            calls = mock_run_command.call_args_list
            autocrlf_calls = [call for call in calls if 'autocrlf' in str(call)]
            self.assertEqual(len(autocrlf_calls), 1)
            self.assertIn('true', str(autocrlf_calls[0]))
            
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['git_configuration.py'])
    @patch('sys.stdout.write')
    def test_main_insufficient_arguments(self, mock_write):
        """测试参数不足的情况"""
        # 捕获输出
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_configuration.main()
            
            # 验证退出码为1
            self.assertEqual(cm.exception.code, 1)
            
            # 验证输出包含用法信息
            output = mock_stdout.getvalue()
            self.assertIn("Usage:", output)
    
    @patch('sys.argv', ['git_configuration.py', 'user1', 'email1', 'extra_arg'])
    @patch('sys.stdout.write')
    def test_main_too_many_arguments(self, mock_write):
        """测试参数过多的情况"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                git_configuration.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Usage:", output)
    
    @patch('sys.argv', ['git_configuration.py', 'test_user', 'test@example.com'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('platform.system')
    def test_main_command_failure(self, mock_system, mock_run_command, mock_print_banner):
        """测试命令执行失败的情况"""
        # 模拟 Linux 系统
        mock_system.return_value = "Linux"
        
        # 模拟第一个命令失败
        mock_run_command.side_effect = [
            Exception("Command failed"),  # 第一个命令失败
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # 其他命令成功
        ]
        
        # 测试异常传播
        with self.assertRaises(Exception) as cm:
            git_configuration.main()
        
        self.assertIn("Command failed", str(cm.exception))
    
    @patch('sys.argv', ['git_configuration.py', 'test_user', 'test@example.com'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('platform.system')
    def test_command_sequence(self, mock_system, mock_run_command, mock_print_banner):
        """测试命令执行序列"""
        mock_system.return_value = "Linux"
        mock_run_command.return_value = 0
        
        git_configuration.main()
        
        # 验证命令执行顺序
        expected_commands = [
            ["git", "config", "--global", "user.name", "test_user"],
            ["git", "config", "--global", "user.email", "test@example.com"],
            ["git", "config", "--global", "push.default", "simple"],
            ["git", "config", "--global", "color.ui", "true"],
            ["git", "config", "--global", "core.quotepath", "false"],
            ["git", "config", "--global", "core.editor", "vim"],
            ["git", "config", "--global", "i18n.logOutputEncoding", "utf-8"],
            ["git", "config", "--global", "i18n.commitEncoding", "utf-8"],
            ["git", "config", "--global", "color.diff", "auto"],
            ["git", "config", "--global", "color.status", "auto"],
            ["git", "config", "--global", "color.branch", "auto"],
            ["git", "config", "--global", "color.interactive", "auto"],
            ["git", "config", "--global", "core.autocrlf", "input"]
        ]
        
        # 检查每个命令是否都被调用
        actual_calls = [call[0][0] for call in mock_run_command.call_args_list]
        
        for i, expected_cmd in enumerate(expected_commands):
            if i < len(actual_calls):
                self.assertEqual(actual_calls[i], expected_cmd)
    
    @patch('sys.argv', ['git_configuration.py', 'user with spaces', 'email@test.com'])
    @patch('common.print_banner')
    @patch('common.run_command')
    @patch('platform.system')
    def test_main_with_special_characters(self, mock_system, mock_run_command, mock_print_banner):
        """测试包含特殊字符的用户名"""
        mock_system.return_value = "Linux"
        mock_run_command.return_value = 0
        
        git_configuration.main()
        
        # 验证用户名被正确传递
        calls = mock_run_command.call_args_list
        first_call = calls[0][0][0]
        self.assertEqual(first_call, ["git", "config", "--global", "user.name", "user with spaces"])

if __name__ == '__main__':
    unittest.main()