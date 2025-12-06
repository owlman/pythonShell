#!/usr/bin/env python3

import os
import subprocess
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import git_push_remote


class TestGitPushRemote(unittest.TestCase):

    @patch('sys.argv', ['git-push-remote', '/tmp/test_repo'])
    @patch('git_push_remote.common.run_command')
    @patch('git_push_remote.common.print_banner')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    def test_push_without_commit(self, mock_chdir, mock_run, mock_check_output, mock_banner, mock_run_command):
        mock_run.return_value = MagicMock(returncode=0)
        mock_check_output.side_effect = [
            "origin\nupstream\n",
            "main\n"
        ]

        git_push_remote.main()

        self.assertTrue(mock_run_command.called)
        calls = [call[0][0] for call in mock_run_command.call_args_list]
        self.assertTrue(any('push' in str(call) for call in calls))

    @patch('sys.argv', ['git-push-remote', '/tmp/test_repo', 'Update files'])
    @patch('git_push_remote.common.run_command')
    @patch('git_push_remote.common.print_banner')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('builtins.print')
    def test_push_with_commit(self, mock_print, mock_chdir, mock_run, mock_check_output, mock_banner, mock_run_command):
        mock_run.return_value = MagicMock(returncode=0)
        mock_check_output.side_effect = [
            "M  file.txt\n",
            "origin\n",
            "main\n"
        ]

        git_push_remote.main()

        calls = [call[0][0] for call in mock_run_command.call_args_list]
        self.assertTrue(any('commit' in str(call) and 'Update files' in str(call) for call in calls))
        self.assertTrue(any('add' in str(call) for call in calls))

    @patch('sys.argv', ['git-push-remote', '/tmp/test_repo', 'Commit message'])
    @patch('git_push_remote.common.run_command')
    @patch('git_push_remote.common.print_banner')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('builtins.print')
    def test_no_changes_to_commit(self, mock_print, mock_chdir, mock_run, mock_check_output, mock_banner, mock_run_command):
        mock_run.return_value = MagicMock(returncode=0)
        mock_check_output.side_effect = [
            "",
            "origin\n",
            "main\n"
        ]

        git_push_remote.main()

        mock_print.assert_any_call("Error: No changes to commit.")

    @patch('sys.argv', ['git-push-remote', '/tmp/test_repo'])
    @patch('git_push_remote.common.run_command')
    @patch('git_push_remote.common.print_banner')
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    @patch('os.chdir')
    def test_push_multiple_remotes(self, mock_chdir, mock_run, mock_check_output, mock_banner, mock_run_command):
        mock_run.return_value = MagicMock(returncode=0)
        mock_check_output.side_effect = [
            "origin\nupstream\nfork\n",
            "main\n"
        ]

        git_push_remote.main()

        calls = [call[0][0] for call in mock_run_command.call_args_list]
        push_calls = [call for call in calls if 'push' in str(call)]
        self.assertEqual(len(push_calls), 3)

    @patch('sys.argv', ['git-push-remote', '/invalid/path'])
    @patch('git_push_remote.common.print_banner')
    @patch('builtins.print')
    @patch('os.chdir')
    def test_invalid_directory(self, mock_chdir, mock_print, mock_banner):
        mock_chdir.side_effect = FileNotFoundError()

        with self.assertRaises(SystemExit):
            git_push_remote.main()

        mock_print.assert_any_call("Error: Directory '/invalid/path' not found.")

    @patch('sys.argv', ['git-push-remote', '/tmp/not_a_repo'])
    @patch('git_push_remote.common.print_banner')
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('builtins.print')
    def test_not_git_repository(self, mock_print, mock_chdir, mock_run, mock_banner):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')

        with self.assertRaises(SystemExit):
            git_push_remote.main()

        mock_print.assert_any_call("Error: Not a git repository.")

    @patch('sys.argv', ['git-push-remote'])
    @patch('builtins.print')
    def test_missing_arguments(self, mock_print):
        with self.assertRaises(SystemExit):
            git_push_remote.main()


if __name__ == '__main__':
    unittest.main()
