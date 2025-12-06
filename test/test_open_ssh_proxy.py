#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    import open_ssh_proxy
    PEXPECT_AVAILABLE = True
except ImportError:
    PEXPECT_AVAILABLE = False


@unittest.skipIf(not PEXPECT_AVAILABLE, "pexpect module not available")
class TestOpenSSHProxy(unittest.TestCase):

    @patch.dict(os.environ, {
        'SSH_USER': 'testuser',
        'SSH_HOST': 'testhost.com',
        'SSH_PASSWORD': 'testpass'
    })
    @patch('pexpect.spawn')
    @patch('builtins.print')
    def test_successful_connection(self, mock_print, mock_spawn):
        mock_child = MagicMock()
        mock_spawn.return_value = mock_child
        
        open_ssh_proxy.main()
        
        mock_spawn.assert_called_once_with("ssh -D 7070 testuser@testhost.com")
        mock_child.expect.assert_called_once_with("password:")
        mock_child.sendline.assert_called_once_with("testpass")
        mock_child.interact.assert_called_once()

    @patch.dict(os.environ, {}, clear=True)
    @patch('builtins.print')
    def test_missing_environment_variables(self, mock_print):
        with self.assertRaises(SystemExit):
            open_ssh_proxy.main()
        
        mock_print.assert_called_with("Please set SSH_USER, SSH_HOST, and SSH_PASSWORD environment variables.")

    @patch.dict(os.environ, {
        'SSH_USER': 'testuser',
        'SSH_HOST': 'testhost.com'
    })
    @patch('builtins.print')
    def test_missing_password(self, mock_print):
        with self.assertRaises(SystemExit):
            open_ssh_proxy.main()
        
        mock_print.assert_called_with("Please set SSH_USER, SSH_HOST, and SSH_PASSWORD environment variables.")

    @patch.dict(os.environ, {
        'SSH_USER': 'testuser',
        'SSH_HOST': 'testhost.com',
        'SSH_PASSWORD': 'testpass'
    })
    @patch('pexpect.spawn')
    @patch('builtins.print')
    def test_connection_failure(self, mock_print, mock_spawn):
        mock_spawn.side_effect = Exception("Connection failed")
        
        with self.assertRaises(SystemExit):
            open_ssh_proxy.main()

    @patch.dict(os.environ, {
        'SSH_USER': 'testuser',
        'SSH_HOST': 'testhost.com',
        'SSH_PASSWORD': 'testpass'
    })
    @patch('pexpect.spawn')
    @patch('builtins.print')
    def test_password_prompt_timeout(self, mock_print, mock_spawn):
        mock_child = MagicMock()
        mock_child.expect.side_effect = Exception("Timeout")
        mock_spawn.return_value = mock_child
        
        with self.assertRaises(SystemExit):
            open_ssh_proxy.main()


if __name__ == '__main__':
    unittest.main()
