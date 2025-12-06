#!/usr/bin/env python3

import os
import sys
import unittest
from unittest.mock import MagicMock, patch, call
import pexpect

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import open_ssh_proxy


class TestOpenSSHProxy(unittest.TestCase):

    @patch('open_ssh_proxy.pexpect.spawn')
    @patch('open_ssh_proxy.os.sys.argv', ['open_ssh_proxy.py', 'testuser', 'testhost', 'testpass'])
    def test_main_success(self, mock_spawn):
        # 设置模拟的 SSH 进程
        mock_child = MagicMock()
        mock_child.expect.return_value = None
        mock_child.interact.return_value = None
        mock_spawn.return_value = mock_child

        # 调用主函数
        open_ssh_proxy.main()

        # 验证是否正确调用了 spawn
        mock_spawn.assert_called_once_with("ssh -D 7070 testuser@testhost")
        
        # 验证是否正确调用了 expect 和 interact
        mock_child.expect.assert_called_once_with("password:")
        mock_child.sendline.assert_called_once_with("testpass")
        mock_child.interact.assert_called_once()

    @patch('open_ssh_proxy.os.sys.argv', ['open_ssh_proxy.py'])
    @patch('builtins.print')
    def test_main_missing_arguments(self, mock_print):
        with self.assertRaises(SystemExit) as cm:
            open_ssh_proxy.main()
        
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_called_with("Usage: open-ssh-proxy <user_name> <host_address> <password>")

    @patch('open_ssh_proxy.os.sys.argv', ['open_ssh_proxy.py', '', 'testhost', 'testpass'])
    @patch('builtins.print')
    def test_main_empty_user(self, mock_print):
        with self.assertRaises(SystemExit) as cm:
            open_ssh_proxy.main()
        
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_called_with("Please set SSH_USER, SSH_HOST, and SSH_PASSWORD environment variables.")

    @patch('open_ssh_proxy.os.sys.argv', ['open_ssh_proxy.py', 'testuser', '', 'testpass'])
    @patch('builtins.print')
    def test_main_empty_host(self, mock_print):
        with self.assertRaises(SystemExit) as cm:
            open_ssh_proxy.main()
        
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_called_with("Please set SSH_USER, SSH_HOST, and SSH_PASSWORD environment variables.")

    @patch('open_ssh_proxy.os.sys.argv', ['open_ssh_proxy.py', 'testuser', 'testhost', ''])
    @patch('builtins.print')
    def test_main_empty_password(self, mock_print):
        with self.assertRaises(SystemExit) as cm:
            open_ssh_proxy.main()
        
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_called_with("Please set SSH_USER, SSH_HOST, and SSH_PASSWORD environment variables.")

    @patch('open_ssh_proxy.pexpect.spawn')
    @patch('open_ssh_proxy.os.sys.argv', ['open_ssh_proxy.py', 'testuser', 'testhost', 'testpass'])
    @patch('builtins.print')
    def test_main_pexpect_exception(self, mock_print, mock_spawn):
        # 设置 spawn 抛出异常
        mock_spawn.side_effect = pexpect.ExceptionPexpect("Connection failed")
        
        with self.assertRaises(SystemExit) as cm:
            open_ssh_proxy.main()
        
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Connecting to testuser@testhost...")
        mock_print.assert_any_call("An error occurred: Connection failed")

    @patch('open_ssh_proxy.pexpect.spawn')
    @patch('open_ssh_proxy.os.sys.argv', ['open_ssh_proxy.py', 'testuser', 'testhost', 'testpass'])
    @patch('builtins.print')
    def test_main_connection_message(self, mock_print, mock_spawn):
        # 设置模拟的 SSH 进程
        mock_child = MagicMock()
        mock_child.expect.return_value = None
        mock_child.interact.return_value = None
        mock_spawn.return_value = mock_child

        # 调用主函数
        open_ssh_proxy.main()

        # 验证连接消息是否正确打印
        mock_print.assert_any_call("Connecting to testuser@testhost...")


if __name__ == '__main__':
    unittest.main()