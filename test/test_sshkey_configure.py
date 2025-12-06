#!/usr/bin/env python3

import os
import sys
import unittest
from unittest.mock import MagicMock, mock_open, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import sshkey_configure


class TestSSHKeyConfigure(unittest.TestCase):

    @patch('sshkey_configure.check_default_ssh_key', return_value=True)
    @patch('sshkey_configure.common.print_banner')
    @patch('builtins.print')
    def test_ssh_key_already_configured(self, mock_print, mock_banner, mock_check):
        sshkey_configure.main()

        mock_print.assert_called_with("SSH key has been configured.")
        mock_banner.assert_called()

    @patch('os.makedirs')
    @patch('builtins.input', return_value='test@example.com')
    @patch('sshkey_configure.common.print_banner')
    @patch('sshkey_configure.common.run_command')
    @patch('sshkey_configure.check_default_ssh_key', return_value=False)
    def test_generate_new_ssh_key(self, mock_check, mock_run_command, mock_banner, mock_input, mock_makedirs):
        sshkey_configure.main()

        mock_input.assert_called_once()
        mock_run_command.assert_called_once()
        call_args = mock_run_command.call_args[0][0]
        self.assertIn('ssh-keygen', call_args)
        self.assertIn('test@example.com', call_args)

    @patch('os.path.isfile')
    @patch('os.path.expanduser')
    def test_check_default_ssh_key_exists(self, mock_expanduser, mock_isfile):
        mock_expanduser.return_value = '/home/user/.ssh'
        mock_isfile.return_value = True

        result = sshkey_configure.check_default_ssh_key()

        self.assertTrue(result)
        self.assertEqual(mock_isfile.call_count, 2)

    @patch('os.path.isfile')
    @patch('os.path.expanduser')
    def test_check_default_ssh_key_missing(self, mock_expanduser, mock_isfile):
        mock_expanduser.return_value = '/home/user/.ssh'
        mock_isfile.side_effect = [True, False]

        result = sshkey_configure.check_default_ssh_key()

        self.assertFalse(result)

    @patch('sys.platform', 'win32')
    @patch('sshkey_configure.check_default_ssh_key', return_value=True)
    @patch('sshkey_configure.common.print_banner')
    @patch('builtins.print')
    def test_windows_warning(self, mock_print, mock_banner, mock_check):
        sshkey_configure.main()

        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Windows' in str(call) for call in calls))

    @patch('os.makedirs')
    @patch('builtins.input', return_value='user@domain.com')
    @patch('sshkey_configure.common.print_banner')
    @patch('sshkey_configure.common.run_command')
    @patch('sshkey_configure.check_default_ssh_key', return_value=False)
    def test_ssh_directory_creation(self, mock_check, mock_run_command, mock_banner, mock_input, mock_makedirs):
        sshkey_configure.main()

        mock_makedirs.assert_called_once()
        args = mock_makedirs.call_args
        self.assertTrue('.ssh' in str(args))


if __name__ == '__main__':
    unittest.main()
