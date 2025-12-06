#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import git_configuration


class TestGitConfiguration(unittest.TestCase):

    @patch('sys.argv', ['git-configuration', 'testuser', 'test@example.com'])
    @patch('git_configuration.common.run_command')
    @patch('git_configuration.common.print_banner')
    @patch('platform.system', return_value='Linux')
    def test_configuration_linux(self, mock_platform, mock_banner, mock_run_command):
        git_configuration.main()
        
        self.assertTrue(mock_run_command.called)
        self.assertTrue(mock_banner.called)
        
        calls = [call[0][0] for call in mock_run_command.call_args_list]
        self.assertTrue(any('user.name' in str(call) and 'testuser' in str(call) for call in calls))
        self.assertTrue(any('user.email' in str(call) and 'test@example.com' in str(call) for call in calls))
        self.assertTrue(any('core.autocrlf' in str(call) and 'input' in str(call) for call in calls))

    @patch('sys.argv', ['git-configuration', 'testuser', 'test@example.com'])
    @patch('git_configuration.common.run_command')
    @patch('git_configuration.common.print_banner')
    @patch('platform.system', return_value='Windows')
    def test_configuration_windows(self, mock_platform, mock_banner, mock_run_command):
        git_configuration.main()
        
        calls = [call[0][0] for call in mock_run_command.call_args_list]
        self.assertTrue(any('core.autocrlf' in str(call) and 'true' in str(call) for call in calls))

    @patch('sys.argv', ['git-configuration'])
    @patch('builtins.print')
    def test_missing_arguments(self, mock_print):
        with self.assertRaises(SystemExit):
            git_configuration.main()
        mock_print.assert_called_with("Usage: git-configuration [user_name] [user_email]")

    @patch('sys.argv', ['git-configuration', 'onlyuser'])
    @patch('builtins.print')
    def test_incomplete_arguments(self, mock_print):
        with self.assertRaises(SystemExit):
            git_configuration.main()
        mock_print.assert_called_with("Usage: git-configuration [user_name] [user_email]")


if __name__ == '__main__':
    unittest.main()
