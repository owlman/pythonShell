"""
Pytest configuration and fixtures for python-shell-utilities tests.
"""

import os
import tempfile
import shutil

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_ssh_dir(temp_dir):
    """Create a mock SSH directory for tests."""
    ssh_dir = os.path.join(temp_dir, '.ssh')
    os.makedirs(ssh_dir, exist_ok=True)
    return ssh_dir


@pytest.fixture
def mock_project_template(temp_dir):
    """Create a mock project template for tests."""
    import zipfile
    
    template_path = os.path.join(temp_dir, 'template.zip')
    with zipfile.ZipFile(template_path, 'w') as zf:
        zf.writestr("test_project/test_file.txt", "Test content")
        zf.writestr("test_project/README.md", "# Test Project")
    
    return template_path


@pytest.fixture(autouse=True)
def mock_sys_argv():
    """Mock sys.argv to prevent interference with actual command line arguments."""
    import sys
    original_argv = sys.argv
    sys.argv = ['test']
    yield
    sys.argv = original_argv


@pytest.fixture
def mock_terminal_size():
    """Mock terminal size for consistent testing."""
    import shutil
    original_get_terminal_size = shutil.get_terminal_size
    
    def mock_size(columns=80, lines=24):
        return shutil.os.terminal_size((columns, lines))
    
    shutil.get_terminal_size = mock_size
    yield mock_size
    shutil.get_terminal_size = original_get_terminal_size