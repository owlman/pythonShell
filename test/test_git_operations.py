"""
Test module for Git operations functionality.
"""

import os
import platform
import tempfile
import unittest.mock as mock
from unittest import TestCase

import pytest

from src import git_configuration, git_create_repository, git_pull_remote, git_push_remote


class TestGitConfiguration(TestCase):
    """Test cases for git_configuration functionality."""

    @mock.patch('src.git_configuration.common.run_command')
    @mock.patch('src.git_configuration.common.print_banner')
    def test_main_linux_commands(self, mock_banner, mock_run_command):
        """Test git configuration commands on Linux."""
        # Mock platform.system() to return Linux
        with mock.patch('platform.system', return_value='Linux'):
            with mock.patch('sys.argv', ['git-configuration', 'Test User', 'test@example.com']):
                git_configuration.main()
        
        # Verify all expected commands were called
        expected_calls = [
            ['git', 'config', '--global', 'user.name', 'Test User'],
            ['git', 'config', '--global', 'user.email', 'test@example.com'],
            ['git', 'config', '--global', 'push.default', 'simple'],
            ['git', 'config', '--global', 'color.ui', 'true'],
            ['git', 'config', '--global', 'core.quotepath', 'false'],
            ['git', 'config', '--global', 'core.editor', 'vim'],
            ['git', 'config', '--global', 'i18n.logOutputEncoding', 'utf-8'],
            ['git', 'config', '--global', 'i18n.commitEncoding', 'utf-8'],
            ['git', 'config', '--global', 'color.diff', 'auto'],
            ['git', 'config', '--global', 'color.status', 'auto'],
            ['git', 'config', '--global', 'color.branch', 'auto'],
            ['git', 'config', '--global', 'color.interactive', 'auto'],
            ['git', 'config', '--global', 'core.autocrlf', 'input']  # Linux setting
        ]
        
        assert mock_run_command.call_count == len(expected_calls)
        mock_banner.assert_called()

    @mock.patch('src.git_configuration.common.run_command')
    @mock.patch('src.git_configuration.common.print_banner')
    def test_main_windows_commands(self, mock_banner, mock_run_command):
        """Test git configuration commands on Windows."""
        # Mock platform.system() to return Windows
        with mock.patch('platform.system', return_value='Windows'):
            with mock.patch('sys.argv', ['git-configuration', 'Test User', 'test@example.com']):
                git_configuration.main()
        
        # Verify Windows-specific autocrlf setting
        windows_calls = [call for call in mock_run_command.call_args_list 
                        if 'core.autocrlf' in str(call)]
        assert len(windows_calls) == 1
        assert 'true' in str(windows_calls[0])  # Windows uses 'true'

    @mock.patch('src.git_configuration.common.print_banner')
    @mock.patch('sys.argv', ['git-configuration'])
    def test_main_invalid_args(self, mock_banner):
        """Test main function with invalid arguments."""
        with pytest.raises(SystemExit) as exc_info:
            git_configuration.main()
        
        assert exc_info.value.code == 1


class TestGitCreateRepository(TestCase):
    """Test cases for git_create_repository functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @mock.patch('src.git_create_repository.common.run_command')
    @mock.patch('src.git_create_repository.common.print_banner')
    @mock.patch('src.git_create_repository.os.makedirs')
    @mock.patch('src.git_create_repository.os.getcwd')
    @mock.patch('src.git_create_repository.os.chdir')
    @mock.patch('src.git_create_repository.os.path.exists')
    @mock.patch('src.git_create_repository.subprocess.check_output')
    def test_main_successful_creation(self, mock_check_output, mock_exists, mock_chdir, mock_getcwd, 
                                      mock_makedirs, mock_banner, mock_run_command):
        """Test successful repository creation."""
        mock_getcwd.return_value = '/current/dir'
        mock_exists.side_effect = lambda path: False if path == '.git' else True
        mock_check_output.return_value = 'M file.txt\n'  # Git status showing changes
        
        with mock.patch('sys.argv', ['git-create-repo', self.temp_dir]):
            git_create_repository.main()
        
        # Verify git commands were called
        assert mock_run_command.call_count >= 3  # init, status, add, commit
        mock_banner.assert_called()

    @mock.patch('src.git_create_repository.common.run_command')
    @mock.patch('src.git_create_repository.common.print_banner')
    @mock.patch('src.git_create_repository.os.makedirs')
    @mock.patch('src.git_create_repository.os.getcwd')
    @mock.patch('src.git_create_repository.os.chdir')
    @mock.patch('src.git_create_repository.os.path.exists')
    @mock.patch('src.git_create_repository.subprocess.check_output')
    def test_main_with_custom_name(self, mock_check_output, mock_exists, mock_chdir, mock_getcwd,
                                   mock_makedirs, mock_banner, mock_run_command):
        """Test repository creation with custom name."""
        mock_getcwd.return_value = '/current/dir'
        mock_exists.side_effect = lambda path: False if path == '.git' else True
        mock_check_output.return_value = 'M file.txt\n'  # Git status showing changes
        
        with mock.patch('sys.argv', ['git-create-repo', self.temp_dir, 'my-repo']):
            git_create_repository.main()
        
        # Should still execute the same git commands
        assert mock_run_command.call_count >= 3
        mock_banner.assert_called()

    @mock.patch('src.git_create_repository.common.print_banner')
    @mock.patch('sys.argv', ['git-create-repo'])
    def test_main_invalid_args(self, mock_banner):
        """Test main function with invalid arguments."""
        with pytest.raises(SystemExit) as exc_info:
            git_create_repository.main()
        
        assert exc_info.value.code == 1


class TestGitPullRemote(TestCase):
    """Test cases for git_pull_remote functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @mock.patch('src.git_pull_remote.common.run_command')
    @mock.patch('src.git_pull_remote.common.print_banner')
    @mock.patch('src.git_pull_remote.os.path.isdir')
    @mock.patch('src.git_pull_remote.os.getcwd')
    @mock.patch('src.git_pull_remote.os.chdir')
    @mock.patch('src.git_pull_remote.subprocess.run')
    @mock.patch('src.git_pull_remote.subprocess.check_output')
    def test_main_successful_pull(self, mock_check_output, mock_run, mock_chdir, 
                                  mock_getcwd, mock_isdir, mock_banner, mock_run_command):
        """Test successful git pull."""
        mock_isdir.return_value = True
        mock_getcwd.return_value = '/current/dir'
        mock_check_output.return_value = 'origin\nupstream\n'  # List of remotes
        
        with mock.patch('sys.argv', ['git-pull-remote', self.temp_dir, 'main']):
            git_pull_remote.main()
        
        # Verify git pull command was called for each remote
        assert mock_run_command.call_count == 2  # One for each remote
        mock_banner.assert_called()

    @mock.patch('src.git_pull_remote.common.print_banner')
    @mock.patch('sys.argv', ['git-pull-remote'])
    def test_main_invalid_args(self, mock_banner):
        """Test main function with invalid arguments."""
        with pytest.raises(SystemExit) as exc_info:
            git_pull_remote.main()
        
        assert exc_info.value.code == 1

    @mock.patch('src.git_pull_remote.common.run_command')
    @mock.patch('src.git_pull_remote.common.print_banner')
    @mock.patch('src.git_pull_remote.os.path.isdir')
    @mock.patch('src.git_pull_remote.os.getcwd')
    @mock.patch('src.git_pull_remote.os.chdir')
    @mock.patch('src.git_pull_remote.subprocess.run')
    @mock.patch('src.git_pull_remote.subprocess.check_output')
    def test_main_different_remote_branch(self, mock_check_output, mock_run, mock_chdir, 
                                          mock_getcwd, mock_isdir, mock_banner, mock_run_command):
        """Test git pull with different remote and branch."""
        mock_isdir.return_value = True
        mock_getcwd.return_value = '/current/dir'
        mock_check_output.return_value = 'upstream\n'  # Single remote
        
        with mock.patch('sys.argv', ['git-pull-remote', self.temp_dir, 'develop']):
            git_pull_remote.main()
        
        mock_run_command.assert_called_once_with(['git', 'pull', 'upstream', 'develop'])
        mock_banner.assert_called()


class TestGitPushRemote(TestCase):
    """Test cases for git_push_remote functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @mock.patch('src.git_push_remote.common.run_command')
    @mock.patch('src.git_push_remote.common.print_banner')
    @mock.patch('src.git_push_remote.os.getcwd')
    @mock.patch('src.git_push_remote.os.chdir')
    @mock.patch('src.git_push_remote.subprocess.run')
    @mock.patch('src.git_push_remote.subprocess.check_output')
    def test_main_successful_push(self, mock_check_output, mock_run, mock_chdir, 
                                  mock_getcwd, mock_banner, mock_run_command):
        """Test successful git push."""
        mock_getcwd.return_value = '/current/dir'
        mock_check_output.side_effect = [
            'origin\n',  # git remote
            'main\n'     # git branch --show-current
        ]
        
        with mock.patch('sys.argv', ['git-push-remote', self.temp_dir]):
            git_push_remote.main()
        
        # Verify git push command was called
        assert mock_run_command.call_count >= 2  # pull and push for each remote
        mock_banner.assert_called()

    @mock.patch('src.git_push_remote.common.print_banner')
    @mock.patch('sys.argv', ['git-push-remote'])
    def test_main_invalid_args(self, mock_banner):
        """Test main function with invalid arguments."""
        with pytest.raises(SystemExit) as exc_info:
            git_push_remote.main()
        
        assert exc_info.value.code == 1

    @mock.patch('src.git_push_remote.common.run_command')
    @mock.patch('src.git_push_remote.common.print_banner')
    @mock.patch('src.git_push_remote.os.getcwd')
    @mock.patch('src.git_push_remote.os.chdir')
    @mock.patch('src.git_push_remote.subprocess.run')
    @mock.patch('src.git_push_remote.subprocess.check_output')
    def test_main_different_remote_branch(self, mock_check_output, mock_run, mock_chdir, 
                                          mock_getcwd, mock_banner, mock_run_command):
        """Test git push with different remote and branch."""
        mock_getcwd.return_value = '/current/dir'
        mock_check_output.side_effect = [
            'upstream\n',  # git remote
            'feature-branch\n'  # git branch --show-current
        ]
        
        with mock.patch('sys.argv', ['git-push-remote', self.temp_dir]):
            git_push_remote.main()
        
        # Verify git push command was called
        assert mock_run_command.call_count >= 2  # pull and push
        mock_banner.assert_called()