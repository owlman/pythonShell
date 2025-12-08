"""
Test module for SSH operations functionality.
"""

import os
import tempfile
import unittest.mock as mock
from unittest import TestCase

import pytest

from src import open_ssh_proxy, sshkey_configure


class TestSSHKeyConfigure(TestCase):
    """Test cases for sshkey_configure functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.mock_ssh_dir = os.path.join(self.temp_dir, '.ssh')

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @mock.patch('src.sshkey_configure.check_default_ssh_key')
    @mock.patch('src.sshkey_configure.common.run_command')
    @mock.patch('src.sshkey_configure.common.print_banner')
    @mock.patch('src.sshkey_configure.os.makedirs')
    @mock.patch('src.sshkey_configure.os.path.expanduser')
    @mock.patch('sys.platform', 'linux')
    def test_main_key_already_exists(self, mock_expanduser, mock_makedirs, 
                                    mock_banner, mock_run_command, mock_check_key):
        """Test main function when SSH key already exists."""
        mock_expanduser.return_value = self.mock_ssh_dir
        mock_check_key.return_value = True
        
        sshkey_configure.main()
        
        # Should not run ssh-keygen if key exists
        mock_run_command.assert_not_called()
        mock_banner.assert_called()

    @mock.patch('src.sshkey_configure.check_default_ssh_key')
    @mock.patch('src.sshkey_configure.common.run_command')
    @mock.patch('src.sshkey_configure.common.print_banner')
    @mock.patch('src.sshkey_configure.os.makedirs')
    @mock.patch('src.sshkey_configure.os.path.expanduser')
    @mock.patch('builtins.input', return_value='test@example.com')
    @mock.patch('sys.platform', 'linux')
    def test_main_create_new_key(self, mock_input, mock_expanduser, mock_makedirs,
                                mock_banner, mock_run_command, mock_check_key):
        """Test main function creating new SSH key."""
        mock_expanduser.return_value = self.mock_ssh_dir
        mock_check_key.return_value = False
        
        sshkey_configure.main()
        
        # Should run ssh-keygen with correct parameters
        expected_cmd = ['ssh-keygen', '-t', 'rsa', '-C', 'test@example.com', 
                       '-f', os.path.join(self.mock_ssh_dir, 'id_rsa'), '-N', '']
        mock_run_command.assert_called_once_with(expected_cmd)
        mock_banner.assert_called()

    @mock.patch('src.sshkey_configure.common.print_banner')
    @mock.patch('sys.platform', 'win32')
    def test_main_windows_warning(self, mock_banner):
        """Test main function shows warning on Windows."""
        with mock.patch('builtins.print') as mock_print:
            sshkey_configure.main()
            
            # Should print Windows warning
            mock_print.assert_any_call(
                "Warning: This script may not work on Windows without Git Bash or WSL."
            )

    def test_check_default_ssh_key_exists(self):
        """Test check_default_ssh_key when keys exist."""
        # Create mock SSH key files
        private_key = os.path.join(self.mock_ssh_dir, 'id_rsa')
        public_key = os.path.join(self.mock_ssh_dir, 'id_rsa.pub')
        
        os.makedirs(self.mock_ssh_dir, exist_ok=True)
        with open(private_key, 'w') as f:
            f.write('mock private key')
        with open(public_key, 'w') as f:
            f.write('mock public key')
        
        with mock.patch('src.sshkey_configure.os.path.expanduser', return_value=self.mock_ssh_dir):
            result = sshkey_configure.check_default_ssh_key()
            assert result is True

    def test_check_default_ssh_key_missing(self):
        """Test check_default_ssh_key when keys don't exist."""
        with mock.patch('src.sshkey_configure.os.path.expanduser', return_value=self.mock_ssh_dir):
            result = sshkey_configure.check_default_ssh_key()
            assert result is False

    def test_check_default_ssh_key_partial(self):
        """Test check_default_ssh_key when only one key file exists."""
        # Create only private key
        private_key = os.path.join(self.mock_ssh_dir, 'id_rsa')
        os.makedirs(self.mock_ssh_dir, exist_ok=True)
        with open(private_key, 'w') as f:
            f.write('mock private key')
        
        with mock.patch('src.sshkey_configure.os.path.expanduser', return_value=self.mock_ssh_dir):
            result = sshkey_configure.check_default_ssh_key()
            assert result is False


class TestOpenSSHProxy(TestCase):
    """Test cases for open_ssh_proxy functionality."""

    @mock.patch('pexpect.spawn')
    def test_main_successful_connection(self, mock_spawn):
        """Test successful SSH proxy connection."""
        mock_child = mock.Mock()
        mock_child.expect = mock.Mock()
        mock_child.sendline = mock.Mock()
        mock_child.interact = mock.Mock()
        mock_spawn.return_value = mock_child
        
        # Mock the expect sequence
        mock_child.expect.side_effect = ["password:", None]  # First expect password, then exit
        
        with mock.patch('sys.argv', ['open-ssh-proxy', 'testuser', 'testhost', 'testpass']):
            with pytest.raises(SystemExit):
                open_ssh_proxy.main()
        
        # Verify the correct SSH command was spawned
        mock_spawn.assert_called_once_with("ssh -D 7070 testuser@testhost")
        mock_child.sendline.assert_called_once_with("testpass")
        mock_child.interact.assert_called_once()

    @mock.patch('pexpect.spawn')
    def test_main_pexpect_error(self, mock_spawn):
        """Test handling of pexpect errors."""
        import pexpect
        mock_spawn.side_effect = pexpect.ExceptionPexpect("Test error")
        
        with mock.patch('sys.argv', ['open-ssh-proxy', 'testuser', 'testhost', 'testpass']):
            with pytest.raises(SystemExit) as exc_info:
                open_ssh_proxy.main()
        
        assert exc_info.value.code == 1

    @mock.patch('sys.argv', ['open-ssh-proxy'])
    def test_main_invalid_args(self):
        """Test main function with invalid arguments."""
        with pytest.raises(SystemExit) as exc_info:
            open_ssh_proxy.main()
        
        assert exc_info.value.code == 1

    @mock.patch('sys.argv', ['open-ssh-proxy', '', 'testhost', 'testpass'])
    def test_main_empty_user(self):
        """Test main function with empty username."""
        with pytest.raises(SystemExit) as exc_info:
            open_ssh_proxy.main()
        
        assert exc_info.value.code == 1

    @mock.patch('sys.argv', ['open-ssh-proxy', 'testuser', '', 'testpass'])
    def test_main_empty_host(self):
        """Test main function with empty host."""
        with pytest.raises(SystemExit) as exc_info:
            open_ssh_proxy.main()
        
        assert exc_info.value.code == 1

    @mock.patch('sys.argv', ['open-ssh-proxy', 'testuser', 'testhost', ''])
    def test_main_empty_password(self):
        """Test main function with empty password."""
        with pytest.raises(SystemExit) as exc_info:
            open_ssh_proxy.main()
        
        assert exc_info.value.code == 1

    @mock.patch('pexpect.spawn')
    def test_main_complex_credentials(self, mock_spawn):
        """Test main function with complex username and password."""
        mock_child = mock.Mock()
        mock_child.expect = mock.Mock()
        mock_child.sendline = mock.Mock()
        mock_child.interact = mock.Mock()
        mock_spawn.return_value = mock_child
        
        mock_child.expect.side_effect = ["password:", None]
        
        with mock.patch('sys.argv', ['open-ssh-proxy', 'user@domain', '192.168.1.1', 'P@ssw0rd!']):
            with pytest.raises(SystemExit):
                open_ssh_proxy.main()
        
        # Should handle complex credentials correctly
        mock_spawn.assert_called_once_with("ssh -D 7070 user@domain@192.168.1.1")
        mock_child.sendline.assert_called_once_with("P@ssw0rd!")