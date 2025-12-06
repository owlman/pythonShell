#!/usr/bin/env python3

import os
import subprocess
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import git_pull_remote


class TestGitPullRemote(unittest.TestCase):

    @patch('sys.argv', ['git-pull-remote', '/tmp/test_repo'])
    @patch('git_pull_remote.common.run_command')
    @patch('git_pull_remote.common.print_banner')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.path.isdir', return_value=True)
    def test_pull_default_branch(self, mock_isdir, mock_chdir, mock_run, mock_check_output, mock_banner, mock_run_command):
        mock_check_output.return_value = "origin\nupstream\n"
        mock_run.return_value = MagicMock(returncode=0)

        git_pull_remote.main()

        self.assertTrue(mock_run_command.called)
        calls = [call[0][0] for call in mock_run_command.call_args_list]
        self.assertTrue(any('pull' in str(call) and 'master' in str(call) for call in calls))

    @patch('sys.argv', ['git-pull-remote', '/tmp/test_repo', 'develop'])
    @patch('git_pull_remote.common.run_command')
    @patch('git_pull_remote.common.print_banner')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.path.isdir', return_value=True)
    def test_pull_custom_branch(self, mock_isdir, mock_chdir, mock_run, mock_check_output, mock_banner, mock_run_command):
        mock_check_output.return_value = "origin\n"
        mock_run.return_value = MagicMock(returncode=0)

        git_pull_remote.main()

        calls = [call[0][0] for call in mock_run_command.call_args_list]
        self.assertTrue(any('pull' in str(call) and 'develop' in str(call) for call in calls))

    @patch('sys.argv', ['git-pull-remote', '/tmp/test_repo'])
    @patch('git_pull_remote.common.run_command')
    @patch('git_pull_remote.common.print_banner')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.path.isdir', return_value=True)
    def test_pull_multiple_remotes(self, mock_isdir, mock_chdir, mock_run, mock_check_output, mock_banner, mock_run_command):
        mock_check_output.return_value = "origin\nupstream\nfork\n"
        mock_run.return_value = MagicMock(returncode=0)

        git_pull_remote.main()

        self.assertEqual(mock_run_command.call_count, 3)

    @patch('sys.argv', ['git-pull-remote', '/invalid/path'])
    @patch('builtins.print')
    @patch('os.path.isdir', return_value=False)
    def test_invalid_directory(self, mock_isdir, mock_print):
        with self.assertRaises(SystemExit):
            git_pull_remote.main()
        mock_print.assert_any_call("Error: '/invalid/path' is not a valid directory.")

    @patch('sys.argv', ['git-pull-remote', '/tmp/not_a_repo'])
    @patch('git_pull_remote.common.print_banner')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_not_git_repository(self, mock_print, mock_isdir, mock_chdir, mock_run, mock_banner):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')

        with self.assertRaises(SystemExit):
            git_pull_remote.main()

        mock_print.assert_any_call("Error: Not a git repository.")

    @patch('sys.argv', ['git-pull-remote'])
    @patch('builtins.print')
    def test_missing_arguments(self, mock_print):
        with self.assertRaises(SystemExit):
            git_pull_remote.main()
        mock_print.assert_called_with("Usage: git-pull-remote <git_directory> [branch]")


if __name__ == '__main__':
    unittest.main()
