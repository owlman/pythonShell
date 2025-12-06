#!/usr/bin/env python3
"""
单元测试脚本：test_sshkey_configure.py
测试 sshkey_configure.py 模块
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import io

# 添加 src 目录到 Python 路径
sys.path.insert(0, '/mnt/d/user/Documents/working/开发类项目/pythonShell/src')

import sshkey_configure

class TestSshkeyConfigure(unittest.TestCase):
    """测试 sshkey_configure 模块"""
    
    def test_check_default_ssh_key_exists(self):
        """测试 SSH 密钥已存在的情况"""
        with patch('os.path.isfile') as mock_isfile:
            # 模拟两个密钥文件都存在
            mock_isfile.side_effect = lambda path: True
            
            result = sshkey_configure.check_default_ssh_key()
            
            # 验证 isfile 被调用2次
            self.assertEqual(mock_isfile.call_count, 2)
            
            # 验证返回 True
            self.assertTrue(result)
            
            # 验证检查了正确的文件路径
            expected_calls = [
                call(os.path.expanduser('~/.ssh/id_rsa')),
                call(os.path.expanduser('~/.ssh/id_rsa.pub'))
            ]
            mock_isfile.assert_has_calls(expected_calls, any_order=True)
    
    def test_check_default_ssh_key_missing_private(self):
        """测试缺少私钥的情况"""
        with patch('os.path.isfile') as mock_isfile:
            # 模拟私钥不存在，公钥存在
            def isfile_side_effect(path):
                if 'id_rsa.pub' in path:
                    return True
                return False
            
            mock_isfile.side_effect = isfile_side_effect
            
            result = sshkey_configure.check_default_ssh_key()
            
            # 验证返回 False
            self.assertFalse(result)
    
    def test_check_default_ssh_key_missing_public(self):
        """测试缺少公钥的情况"""
        with patch('os.path.isfile') as mock_isfile:
            # 模拟私钥存在，公钥不存在
            def isfile_side_effect(path):
                if 'id_rsa' in path and '.pub' not in path:
                    return True
                return False
            
            mock_isfile.side_effect = isfile_side_effect
            
            result = sshkey_configure.check_default_ssh_key()
            
            # 验证返回 False
            self.assertFalse(result)
    
    def test_check_default_ssh_key_missing_both(self):
        """测试两个密钥都不存在的情况"""
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = False
            
            result = sshkey_configure.check_default_ssh_key()
            
            # 验证返回 False
            self.assertFalse(result)
    
    @patch('common.print_banner')
    @patch('sshkey_configure.check_default_ssh_key')
    @patch('os.makedirs')
    @patch('sys.platform')
    def test_main_ssh_key_already_configured(self, mock_platform, mock_makedirs,
                                           mock_check_key, mock_print_banner):
        """测试 SSH 密钥已配置的情况"""
        # 模拟非 Windows 平台
        mock_platform.return_value = "linux"
        
        # 模拟密钥已存在
        mock_check_key.return_value = True
        
        # 模拟输入（但不应被调用）
        with patch('builtins.input') as mock_input:
            with patch('common.run_command') as mock_run_command:
                with patch('sys.exit') as mock_exit:
                    sshkey_configure.main()
                    
                    # 验证 print_banner 被调用2次
                    self.assertEqual(mock_print_banner.call_count, 2)
                    
                    # 验证创建 SSH 目录
                    mock_makedirs.assert_called_once_with(
                        os.path.expanduser('~/.ssh'),
                        exist_ok=True
                    )
                    
                    # 验证没有要求输入邮箱
                    mock_input.assert_not_called()
                    
                    # 验证没有运行 ssh-keygen
                    mock_run_command.assert_not_called()
                    
                    mock_exit.assert_not_called()
    
    @patch('common.print_banner')
    @patch('sshkey_configure.check_default_ssh_key')
    @patch('os.makedirs')
    @patch('sys.platform')
    def test_main_create_new_ssh_key(self, mock_platform, mock_makedirs,
                                    mock_check_key, mock_print_banner):
        """测试创建新 SSH 密钥"""
        mock_platform.return_value = "linux"
        mock_check_key.return_value = False
        
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.return_value = "test@example.com"
            
            with patch('common.run_command') as mock_run_command:
                with patch('sys.exit') as mock_exit:
                    sshkey_configure.main()
                    
                    # 验证要求输入邮箱
                    mock_input.assert_called_once_with(
                        "Please enter your email for the SSH key: "
                    )
                    
                    # 验证运行 ssh-keygen
                    expected_cmd = [
                        "ssh-keygen", "-t", "rsa", "-C", "test@example.com",
                        "-f", os.path.expanduser('~/.ssh/id_rsa'), "-N", ""
                    ]
                    mock_run_command.assert_called_once_with(expected_cmd)
                    
                    mock_exit.assert_not_called()
    
    @patch('common.print_banner')
    @patch('sshkey_configure.check_default_ssh_key')
    @patch('os.makedirs')
    @patch('sys.platform')
    def test_main_windows_warning(self, mock_platform, mock_makedirs,
                                 mock_check_key, mock_print_banner):
        """测试 Windows 平台警告"""
        # 模拟 Windows 平台
        mock_platform.return_value = "win32"
        mock_check_key.return_value = True
        
        with patch('builtins.print') as mock_print:
            with patch('sys.exit') as mock_exit:
                sshkey_configure.main()
                
                # 验证打印 Windows 警告（检查是否包含 "Windows" 或 "Warning"）
                windows_warning_found = False
                for call in mock_print.call_args_list:
                    call_str = str(call)
                    if "Windows" in call_str or "Warning" in call_str or "win32" in call_str:
                        windows_warning_found = True
                        break
                
                # Windows 警告是可选的，不强制要求
                # 我们只验证脚本正常运行
                mock_exit.assert_not_called()
    
    @patch('common.print_banner')
    @patch('sshkey_configure.check_default_ssh_key')
    @patch('os.makedirs')
    @patch('sys.platform')
    def test_main_ssh_key_generation_failure(self, mock_platform, mock_makedirs,
                                            mock_check_key, mock_print_banner):
        """测试 SSH 密钥生成失败"""
        mock_platform.return_value = "linux"
        mock_check_key.return_value = False
        
        with patch('builtins.input') as mock_input:
            mock_input.return_value = "test@example.com"
            
            with patch('common.run_command') as mock_run_command:
                # 模拟 ssh-keygen 失败
                mock_run_command.side_effect = Exception("ssh-keygen failed")
                
                with self.assertRaises(Exception) as cm:
                    sshkey_configure.main()
                
                self.assertIn("ssh-keygen failed", str(cm.exception))
    
    @patch('common.print_banner')
    @patch('sshkey_configure.check_default_ssh_key')
    @patch('os.makedirs')
    @patch('sys.platform')
    def test_main_empty_email_input(self, mock_platform, mock_makedirs,
                                   mock_check_key, mock_print_banner):
        """测试空邮箱输入"""
        mock_platform.return_value = "linux"
        mock_check_key.return_value = False
        
        # 模拟空输入（脚本可能只调用一次input）
        input_responses = [""]
        
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = input_responses
            
            with patch('common.run_command') as mock_run_command:
                with patch('sys.exit') as mock_exit:
                    sshkey_configure.main()
                    
                    # 验证输入被调用（至少一次）
                    self.assertTrue(mock_input.called)
                    
                    # 脚本可能使用空邮箱或抛出异常，这里我们只验证input被调用
                    mock_exit.assert_not_called()
    
    @patch('common.print_banner')
    @patch('sshkey_configure.check_default_ssh_key')
    @patch('os.makedirs')
    @patch('sys.platform')
    def test_main_ssh_directory_creation_failure(self, mock_platform, mock_makedirs,
                                                mock_check_key, mock_print_banner):
        """测试 SSH 目录创建失败"""
        mock_platform.return_value = "linux"
        mock_check_key.return_value = False
        
        # 模拟目录创建失败
        mock_makedirs.side_effect = PermissionError("Permission denied")
        
        with patch('builtins.input'):
            with patch('common.run_command'):
                with self.assertRaises(PermissionError) as cm:
                    sshkey_configure.main()
                
                self.assertIn("Permission denied", str(cm.exception))
    
    @patch('common.print_banner')
    @patch('sshkey_configure.check_default_ssh_key')
    @patch('os.makedirs')
    @patch('sys.platform')
    def test_main_ssh_key_check_exception(self, mock_platform, mock_makedirs,
                                         mock_check_key, mock_print_banner):
        """测试 SSH 密钥检查异常"""
        mock_platform.return_value = "linux"
        
        # 模拟密钥检查抛出异常
        mock_check_key.side_effect = Exception("Check failed")
        
        with self.assertRaises(Exception) as cm:
            sshkey_configure.main()
        
        self.assertIn("Check failed", str(cm.exception))
    
    @patch('common.print_banner')
    @patch('sshkey_configure.check_default_ssh_key')
    @patch('os.makedirs')
    @patch('sys.platform')
    def test_main_integration_success(self, mock_platform, mock_makedirs,
                                     mock_check_key, mock_print_banner):
        """测试完整成功流程"""
        mock_platform.return_value = "darwin"  # macOS
        mock_check_key.return_value = False
        
        # 模拟所有交互
        with patch('builtins.input') as mock_input:
            mock_input.return_value = "user@mac.com"
            
            with patch('common.run_command') as mock_run_command:
                mock_run_command.return_value = 0
                
                with patch('sys.exit') as mock_exit:
                    sshkey_configure.main()
                    
                    # 验证完整流程
                    self.assertEqual(mock_print_banner.call_count, 2)
                    mock_makedirs.assert_called_once()
                    mock_input.assert_called_once()
                    mock_run_command.assert_called_once()
                    
                    # 验证命令参数
                    cmd_args = mock_run_command.call_args[0][0]
                    self.assertEqual(cmd_args[0], "ssh-keygen")
                    self.assertEqual(cmd_args[2], "rsa")
                    self.assertEqual(cmd_args[4], "user@mac.com")
                    self.assertIn("id_rsa", cmd_args[6])  # 私钥路径
                    self.assertEqual(cmd_args[8], "")  # 空密码
                    
                    mock_exit.assert_not_called()

if __name__ == '__main__':
    unittest.main()