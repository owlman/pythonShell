#!/usr/bin/env python3
"""
单元测试脚本：test_open_ssh_proxy.py
测试 open_ssh_proxy.py 模块
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import io

# 添加 src 目录到 Python 路径
sys.path.insert(0, '/mnt/d/user/Documents/working/开发类项目/pythonShell/src')

import open_ssh_proxy

class TestOpenSshProxy(unittest.TestCase):
    """测试 open_ssh_proxy 模块"""
    
    @patch('os.getenv')
    @patch('pexpect.spawn')
    def test_main_success(self, mock_spawn, mock_getenv):
        """测试成功连接 SSH 代理"""
        # 模拟环境变量
        mock_getenv.side_effect = lambda var: {
            "SSH_USER": "testuser",
            "SSH_HOST": "example.com",
            "SSH_PASSWORD": "testpass"
        }.get(var)
        
        # 模拟 pexpect 子进程
        mock_child = MagicMock()
        mock_spawn.return_value = mock_child
        
        # 模拟 expect 成功
        mock_child.expect.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            open_ssh_proxy.main()
            
            # 验证环境变量检查
            self.assertEqual(mock_getenv.call_count, 3)
            
            # 验证 pexpect.spawn 调用
            mock_spawn.assert_called_once_with("ssh -D 7070 testuser@example.com")
            
            # 验证 expect 和 sendline
            mock_child.expect.assert_called_once_with("password:")
            mock_child.sendline.assert_called_once_with("testpass")
            
            # 验证 interact 被调用
            mock_child.interact.assert_called_once()
            
            mock_exit.assert_not_called()
    
    @patch('os.getenv')
    def test_main_missing_ssh_user(self, mock_getenv):
        """测试缺少 SSH_USER 环境变量"""
        # 模拟缺少 SSH_USER
        mock_getenv.side_effect = lambda var: {
            "SSH_USER": None,
            "SSH_HOST": "example.com",
            "SSH_PASSWORD": "testpass"
        }.get(var)
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                open_ssh_proxy.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Please set SSH_USER", output)
    
    @patch('os.getenv')
    def test_main_missing_ssh_host(self, mock_getenv):
        """测试缺少 SSH_HOST 环境变量"""
        mock_getenv.side_effect = lambda var: {
            "SSH_USER": "testuser",
            "SSH_HOST": None,
            "SSH_PASSWORD": "testpass"
        }.get(var)
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                open_ssh_proxy.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Please set SSH_HOST", output)
    
    @patch('os.getenv')
    def test_main_missing_ssh_password(self, mock_getenv):
        """测试缺少 SSH_PASSWORD 环境变量"""
        mock_getenv.side_effect = lambda var: {
            "SSH_USER": "testuser",
            "SSH_HOST": "example.com",
            "SSH_PASSWORD": None
        }.get(var)
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                open_ssh_proxy.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Please set SSH_PASSWORD", output)
    
    @patch('os.getenv')
    def test_main_all_env_vars_missing(self, mock_getenv):
        """测试所有环境变量都缺失"""
        mock_getenv.return_value = None
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                open_ssh_proxy.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Please set SSH_USER", output)
            self.assertIn("SSH_HOST", output)
            self.assertIn("SSH_PASSWORD", output)
    
    @patch('os.getenv')
    @patch('pexpect.spawn')
    def test_main_pexpect_exception(self, mock_spawn, mock_getenv):
        """测试 pexpect 异常"""
        mock_getenv.side_effect = lambda var: {
            "SSH_USER": "testuser",
            "SSH_HOST": "example.com",
            "SSH_PASSWORD": "testpass"
        }.get(var)
        
        # 模拟 pexpect 异常
        mock_child = MagicMock()
        mock_spawn.return_value = mock_child
        mock_child.expect.side_effect = Exception("pexpect error")
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                open_ssh_proxy.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("An error occurred", output)
    
    @patch('os.getenv')
    @patch('pexpect.spawn')
    def test_main_pexpect_timeout(self, mock_spawn, mock_getenv):
        """测试 pexpect 超时"""
        mock_getenv.side_effect = lambda var: {
            "SSH_USER": "testuser",
            "SSH_HOST": "example.com",
            "SSH_PASSWORD": "testpass"
        }.get(var)
        
        mock_child = MagicMock()
        mock_spawn.return_value = mock_child
        
        # 模拟 pexpect.exceptions.TIMEOUT
        from pexpect import exceptions
        mock_child.expect.side_effect = exceptions.TIMEOUT("Timeout")
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                open_ssh_proxy.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("An error occurred", output)
    
    @patch('os.getenv')
    @patch('pexpect.spawn')
    def test_main_pexpect_eof(self, mock_spawn, mock_getenv):
        """测试 pexpect EOF"""
        mock_getenv.side_effect = lambda var: {
            "SSH_USER": "testuser",
            "SSH_HOST": "example.com",
            "SSH_PASSWORD": "testpass"
        }.get(var)
        
        mock_child = MagicMock()
        mock_spawn.return_value = mock_child
        
        # 模拟 pexpect.exceptions.EOF
        from pexpect import exceptions
        mock_child.expect.side_effect = exceptions.EOF("EOF")
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                open_ssh_proxy.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("An error occurred", output)
    
    @patch('os.getenv')
    @patch('pexpect.spawn')
    @patch('builtins.print')
    def test_main_connection_message(self, mock_print, mock_spawn, mock_getenv):
        """测试连接消息"""
        mock_getenv.side_effect = lambda var: {
            "SSH_USER": "alice",
            "SSH_HOST": "server.com",
            "SSH_PASSWORD": "secret"
        }.get(var)
        
        mock_child = MagicMock()
        mock_spawn.return_value = mock_child
        mock_child.expect.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            open_ssh_proxy.main()
            
            # 验证连接消息
            connection_calls = [
                call for call in mock_print.call_args_list
                if "Connecting to" in str(call) and "alice@server.com" in str(call)
            ]
            self.assertGreater(len(connection_calls), 0)
            
            mock_exit.assert_not_called()
    
    @patch('os.getenv')
    @patch('pexpect.spawn')
    def test_main_ssh_command_format(self, mock_spawn, mock_getenv):
        """测试 SSH 命令格式"""
        mock_getenv.side_effect = lambda var: {
            "SSH_USER": "user",
            "SSH_HOST": "host.with.port:2222",
            "SSH_PASSWORD": "pass"
        }.get(var)
        
        mock_child = MagicMock()
        mock_spawn.return_value = mock_child
        mock_child.expect.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            open_ssh_proxy.main()
            
            # 验证 SSH 命令格式
            mock_spawn.assert_called_once_with("ssh -D 7070 user@host.with.port:2222")
            
            mock_exit.assert_not_called()
    
    @patch('os.getenv')
    @patch('pexpect.spawn')
    def test_main_empty_password(self, mock_spawn, mock_getenv):
        """测试空密码"""
        mock_getenv.side_effect = lambda var: {
            "SSH_USER": "testuser",
            "SSH_HOST": "example.com",
            "SSH_PASSWORD": ""  # 空密码
        }.get(var)
        
        mock_child = MagicMock()
        mock_spawn.return_value = mock_child
        mock_child.expect.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            open_ssh_proxy.main()
            
            # 验证发送空密码
            mock_child.sendline.assert_called_once_with("")
            
            mock_exit.assert_not_called()
    
    @patch('os.getenv')
    @patch('pexpect.spawn')
    def test_main_special_characters_in_credentials(self, mock_spawn, mock_getenv):
        """测试凭证中的特殊字符"""
        mock_getenv.side_effect = lambda var: {
            "SSH_USER": "user@domain",
            "SSH_HOST": "host#special",
            "SSH_PASSWORD": "pass$word&123"
        }.get(var)
        
        mock_child = MagicMock()
        mock_spawn.return_value = mock_child
        mock_child.expect.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            open_ssh_proxy.main()
            
            # 验证 SSH 命令包含特殊字符
            mock_spawn.assert_called_once_with("ssh -D 7070 user@domain@host#special")
            
            # 验证发送包含特殊字符的密码
            mock_child.sendline.assert_called_once_with("pass$word&123")
            
            mock_exit.assert_not_called()
    
    @patch('os.getenv')
    @patch('pexpect.spawn')
    def test_main_interact_exception(self, mock_spawn, mock_getenv):
        """测试 interact 异常"""
        mock_getenv.side_effect = lambda var: {
            "SSH_USER": "testuser",
            "SSH_HOST": "example.com",
            "SSH_PASSWORD": "testpass"
        }.get(var)
        
        mock_child = MagicMock()
        mock_spawn.return_value = mock_child
        mock_child.expect.return_value = 0
        mock_child.interact.side_effect = Exception("Interact failed")
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                open_ssh_proxy.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("An error occurred", output)

if __name__ == '__main__':
    unittest.main()