"""
Test module for common utility functions.
"""

import os
import subprocess
import tempfile
import unittest.mock as mock
from unittest import TestCase

import pytest

from src.common import print_banner, run_command


class TestRunCommand(TestCase):
    """Test cases for the run_command function."""

    def test_run_command_success_string(self):
        """Test running a simple successful command as string."""
        result = run_command("echo 'Hello, World!'")
        assert result == 0

    def test_run_command_success_list(self):
        """Test running a simple successful command as list."""
        result = run_command(["echo", "Hello, World!"])
        assert result == 0

    def test_run_command_failure(self):
        """Test running a command that fails."""
        with pytest.raises(subprocess.SubprocessError):
            run_command("exit 1", shell=True)

    def test_run_command_timeout(self):
        """Test command timeout functionality."""
        with pytest.raises(subprocess.TimeoutExpired):
            run_command("sleep 10", shell=True, timeout=1)

    def test_run_command_with_shell_true(self):
        """Test running command with shell=True."""
        result = run_command("echo 'test'", shell=True)
        assert result == 0


class TestPrintBanner(TestCase):
    """Test cases for the print_banner function."""

    @mock.patch('shutil.get_terminal_size')
    @mock.patch('builtins.print')
    def test_print_banner_default_width(self, mock_print, mock_terminal_size):
        """Test print_banner with default terminal width."""
        mock_terminal_size.return_value = mock.Mock(columns=80)
        
        print_banner("Test Message")
        
        # Verify print was called 3 times (top border, message, bottom border)
        assert mock_print.call_count == 3
        
        # Check that the border has the correct length
        border_calls = [call for call in mock_print.call_args_list if call.args and '#' in call.args[0]]
        assert len(border_calls) == 2
        assert len(border_calls[0].args[0]) == 80  # Should be exactly 80 characters

    @mock.patch('shutil.get_terminal_size')
    @mock.patch('builtins.print')
    def test_print_banner_custom_width(self, mock_print, mock_terminal_size):
        """Test print_banner with custom terminal width."""
        mock_terminal_size.return_value = mock.Mock(columns=60)
        
        print_banner("Custom Test")
        
        assert mock_print.call_count == 3
        border_calls = [call for call in mock_print.call_args_list if call.args and '#' in call.args[0]]
        assert len(border_calls) == 2

    @mock.patch('shutil.get_terminal_size')
    @mock.patch('builtins.print')
    def test_print_banner_long_message(self, mock_print, mock_terminal_size):
        """Test print_banner with a long message."""
        mock_terminal_size.return_value = mock.Mock(columns=40)
        
        long_message = "This is a very long message that should be truncated or handled properly"
        print_banner(long_message)
        
        assert mock_print.call_count == 3
        # Check that the border has the correct length
        border_calls = [call for call in mock_print.call_args_list if call.args and '#' in call.args[0]]
        assert len(border_calls) == 2
        assert len(border_calls[0].args[0]) == 40  # Should be exactly 40 characters