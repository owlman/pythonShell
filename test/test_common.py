#!/usr/bin/env python3

import os
import subprocess
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import common

class TestRunCommand(unittest.TestCase):

    @patch('common.run_command')
    def test_run_command_success(self, mock_run):
        mock_run.return_value = 0
        result = common.run_command(['echo', 'test'])
        self.assertEqual(result, 0)

    @patch('common.run_command')
    def test_run_command_failure(self, mock_run):
        mock_run.side_effect = subprocess.SubprocessError("Command failed")
        with self.assertRaises(subprocess.SubprocessError):
            common.run_command(['false'])

    def test_run_command_real_success(self):
        result = common.run_command(['echo', 'test'])
        self.assertEqual(result, 0)

    def test_run_command_real_failure(self):
        with self.assertRaises(subprocess.SubprocessError):
            common.run_command(['false'])


class TestPrintBanner(unittest.TestCase):

    @patch('builtins.print')
    @patch('shutil.get_terminal_size')
    def test_print_banner(self, mock_terminal_size, mock_print):
        mock_terminal_size.return_value = MagicMock(columns=80)

        common.print_banner("Test Message")

        self.assertEqual(mock_print.call_count, 3)
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('#' in str(call) for call in calls))

    @patch('builtins.print')
    @patch('shutil.get_terminal_size')
    def test_print_banner_custom_width(self, mock_terminal_size, mock_print):
        mock_terminal_size.return_value = MagicMock(columns=60)

        common.print_banner("Short")

        self.assertEqual(mock_print.call_count, 3)


if __name__ == '__main__':
    unittest.main()
