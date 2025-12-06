#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import git_create_repository


class TestGitCreateRepository(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('sys.argv', ['git-create-repository', '/tmp/test_repo'])
    @patch('git_create_repository.common.run_command')
    @patch('git_create_repository.common.print_banner')
    @patch('subprocess.check_output')
    @patch('os.chdir')
    @patch('os.path.exists')
    def test_create_repository_default_message(self, mock_exists, mock_chdir, mock_check_output, mock_banner, mock_run_command):
        mock_exists.return_value = False
        mock_check_output.return_value = "?? README.md\n?? .gitignore\n"
        
        with patch('os.makedirs'):
            with patch('builtins.open', create=True):
                git_create_repository.main()
        
        self.assertTrue(mock_run_command.called)
        calls = [call[0][0] for call in mock_run_command.call_args_list]
        self.assertTrue(any('git' in str(call) and 'init' in str(call) for call in calls))

    @patch('sys.argv', ['git-create-repository', '/tmp/test_repo', 'First commit'])
    @patch('git_create_repository.common.run_command')
    @patch('git_create_repository.common.print_banner')
    @patch('subprocess.check_output')
    @patch('os.chdir')
    @patch('os.path.exists')
    def test_create_repository_custom_message(self, mock_exists, mock_chdir, mock_check_output, mock_banner, mock_run_command):
        mock_exists.return_value = False
        mock_check_output.return_value = "?? README.md\n"
        
        with patch('os.makedirs'):
            with patch('builtins.open', create=True):
                git_create_repository.main()
        
        calls = [call[0][0] for call in mock_run_command.call_args_list]
        self.assertTrue(any('commit' in str(call) and 'First commit' in str(call) for call in calls))

    @patch('sys.argv', ['git-create-repository', '/tmp/test_repo'])
    @patch('git_create_repository.common.run_command')
    @patch('git_create_repository.common.print_banner')
    @patch('subprocess.check_output')
    @patch('os.chdir')
    @patch('os.path.exists')
    @patch('builtins.print')
    def test_no_changes_to_commit(self, mock_print, mock_exists, mock_chdir, mock_check_output, mock_banner, mock_run_command):
        mock_exists.return_value = False
        mock_check_output.return_value = ""
        
        with patch('os.makedirs'):
            with patch('builtins.open', create=True):
                git_create_repository.main()
        
        mock_print.assert_any_call("No files to commit.")

    @patch('sys.argv', ['git-create-repository'])
    @patch('builtins.print')
    def test_missing_arguments(self, mock_print):
        with self.assertRaises(SystemExit):
            git_create_repository.main()
        mock_print.assert_called_with("Usage: git-create-repository <git_directory> [init_commit_message]")


if __name__ == '__main__':
    unittest.main()
