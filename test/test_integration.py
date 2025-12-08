"""
Integration tests for python-shell-utilities.
"""

import os
import tempfile
import unittest.mock as mock
from unittest import TestCase

import pytest

from src import common


class TestIntegration(TestCase):
    """Integration tests for the entire package."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_package_imports(self):
        """Test that all package modules can be imported."""
        from src import (
            common, git_configuration, git_create_repository,
            git_pull_remote, git_push_remote, open_ssh_proxy,
            sshkey_configure, create_book_project, create_translation_project
        )
        
        # Verify all modules are importable
        assert common is not None
        assert git_configuration is not None
        assert git_create_repository is not None
        assert git_pull_remote is not None
        assert git_push_remote is not None
        assert open_ssh_proxy is not None
        assert sshkey_configure is not None
        assert create_book_project is not None
        assert create_translation_project is not None

    def test_common_utilities_integration(self):
        """Test integration of common utilities with other modules."""
        # Test that print_banner can be used by other modules
        with mock.patch('builtins.print') as mock_print:
            common.print_banner("Integration Test")
            assert mock_print.call_count == 3

        # Test that run_command can execute real system commands
        result = common.run_command("echo 'integration test'")
        assert result == 0

    @mock.patch('src.git_configuration.common.run_command')
    @mock.patch('src.git_configuration.common.print_banner')
    def test_git_configuration_integration(self, mock_banner, mock_run_command):
        """Test git configuration integration."""
        from src import git_configuration
        
        with mock.patch('sys.argv', ['git-configuration', 'Integration', 'test@example.com']):
            git_configuration.main()
        
        # Verify the integration between git_configuration and common modules
        mock_run_command.assert_called()
        mock_banner.assert_called()

    def test_project_scaffolding_integration(self):
        """Test project scaffolding integration with file system."""
        from src import create_book_project, create_translation_project
        
        # Test that both scaffolding modules share common functionality
        assert hasattr(create_book_project, 'main')
        assert hasattr(create_translation_project, 'main')
        
        # Both should use the same common module
        assert create_book_project.common == create_translation_project.common

    @mock.patch('pexpect.spawn')
    def test_ssh_integration(self, mock_spawn):
        """Test SSH operations integration."""
        from src import open_ssh_proxy
        
        mock_child = mock.Mock()
        mock_child.expect = mock.Mock()
        mock_child.sendline = mock.Mock()
        mock_child.interact = mock.Mock()
        mock_spawn.return_value = mock_child
        mock_child.expect.side_effect = ["password:", None]
        
        with mock.patch('sys.argv', ['open-ssh-proxy', 'user', 'host', 'pass']):
            with pytest.raises(SystemExit):
                open_ssh_proxy.main()
        
        # Verify SSH proxy integration
        mock_spawn.assert_called_once()
        mock_child.interact.assert_called_once()

    def test_error_handling_integration(self):
        """Test error handling across different modules."""
        # Test that common.run_command properly handles errors
        import subprocess
        
        with pytest.raises(subprocess.SubprocessError):
            common.run_command("exit 1", shell=True)

    def test_cross_platform_integration(self):
        """Test cross-platform compatibility."""
        # Test that common utilities work across platforms
        result = common.run_command("pwd" if os.name != "nt" else "cd")
        assert result == 0
        
        # Test print_banner adapts to terminal width
        with mock.patch('shutil.get_terminal_size', return_value=mock.Mock(columns=60)):
            with mock.patch('builtins.print') as mock_print:
                common.print_banner("Cross-platform test")
                assert mock_print.call_count == 3

    @mock.patch('src.sshkey_configure.check_default_ssh_key')
    @mock.patch('src.sshkey_configure.common.run_command')
    @mock.patch('src.sshkey_configure.common.print_banner')
    @mock.patch('src.sshkey_configure.os.makedirs')
    @mock.patch('src.sshkey_configure.os.path.expanduser')
    @mock.patch('builtins.input', return_value='test@example.com')
    def test_ssh_key_integration(self, mock_input, mock_expanduser, mock_makedirs,
                                mock_banner, mock_run_command, mock_check_key):
        """Test SSH key configuration integration."""
        from src import sshkey_configure
        
        mock_expanduser.return_value = self.temp_dir
        mock_check_key.return_value = False
        
        sshkey_configure.main()
        
        # Verify integration between SSH key configuration and common utilities
        mock_run_command.assert_called_once()
        mock_banner.assert_called()  # Called twice: start and success

    def test_command_line_interface_integration(self):
        """Test command line interface integration."""
        # Test that all modules have proper main functions
        modules_to_test = [
            'git_configuration', 'git_create_repository',
            'git_pull_remote', 'git_push_remote', 'open_ssh_proxy',
            'sshkey_configure', 'create_book_project', 'create_translation_project'
        ]
        
        for module_name in modules_to_test:
            module = __import__(f'src.{module_name}', fromlist=['main'])
            assert hasattr(module, 'main')
            assert callable(module.main)