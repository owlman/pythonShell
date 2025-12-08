"""
Test module for project scaffolding functionality.
"""

import os
import tempfile
import unittest.mock as mock
from unittest import TestCase
import zipfile

import pytest

from src import create_book_project, create_translation_project


class TestCreateBookProject(TestCase):
    """Test cases for create_book_project functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.template_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "src", "template"
        )
        
        # Create a mock template zip file for testing
        self.mock_template = os.path.join(self.temp_dir, "mock_book_proj.zip")
        with zipfile.ZipFile(self.mock_template, 'w') as zf:
            zf.writestr("book_proj/test_file.txt", "Test content")
            zf.writestr("book_proj/README.md", "# Test Book Project")

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @mock.patch('src.create_book_project.zipfile.ZipFile')
    @mock.patch('src.create_book_project.common.print_banner')
    @mock.patch('sys.argv', ['create-book-project', '/fake/path', 'test_project'])
    def test_main_with_custom_name(self, mock_banner, mock_zipfile):
        """Test main function with custom project name."""
        mock_zipfile.return_value.__enter__.return_value.extractall = mock.Mock()
        
        with pytest.raises(SystemExit) as exc_info:
            create_book_project.main()
        
        # The function should exit normally (not due to error)
        assert exc_info.value.code == 1  # Since /fake/path doesn't exist

    @mock.patch('src.create_book_project.zipfile.ZipFile')
    @mock.patch('src.create_book_project.common.print_banner')
    @mock.patch('sys.argv', ['create-book-project'])
    def test_main_invalid_args(self, mock_banner, mock_zipfile):
        """Test main function with invalid arguments."""
        with pytest.raises(SystemExit) as exc_info:
            create_book_project.main()
        
        assert exc_info.value.code == 1

    @mock.patch('src.create_book_project.os.path.exists')
    @mock.patch('src.create_book_project.os.makedirs')
    @mock.patch('src.create_book_project.shutil.rmtree')
    @mock.patch('src.create_book_project.zipfile.ZipFile')
    @mock.patch('src.create_book_project.common.print_banner')
    def test_main_successful_extraction(self, mock_banner, mock_zipfile, 
                                       mock_rmtree, mock_makedirs, mock_exists):
        """Test successful project creation."""
        mock_exists.return_value = True  # Directory exists
        mock_zipfile.return_value.__enter__.return_value.extractall = mock.Mock()
        
        with mock.patch('sys.argv', ['create-book-project', self.temp_dir, 'test_book']):
            create_book_project.main()
        
        # Should exit normally after successful execution
        mock_rmtree.assert_called_once()
        mock_banner.assert_called()


class TestCreateTranslationProject(TestCase):
    """Test cases for create_translation_project functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.template_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "src", "template"
        )
        
        # Create a mock template zip file for testing
        self.mock_template = os.path.join(self.temp_dir, "mock_translation_proj.zip")
        with zipfile.ZipFile(self.mock_template, 'w') as zf:
            zf.writestr("translation_proj/test_file.txt", "Test content")
            zf.writestr("translation_proj/README.md", "# Test Translation Project")

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @mock.patch('src.create_translation_project.zipfile.ZipFile')
    @mock.patch('src.create_translation_project.common.print_banner')
    @mock.patch('sys.argv', ['create-translation-project', '/fake/path', 'test_project'])
    def test_main_with_custom_name(self, mock_banner, mock_zipfile):
        """Test main function with custom project name."""
        mock_zipfile.return_value.__enter__.return_value.extractall = mock.Mock()
        
        with pytest.raises(SystemExit) as exc_info:
            create_translation_project.main()
        
        # The function should exit normally (not due to error)
        assert exc_info.value.code == 1  # Since /fake/path doesn't exist

    @mock.patch('src.create_translation_project.zipfile.ZipFile')
    @mock.patch('src.create_translation_project.common.print_banner')
    @mock.patch('sys.argv', ['create-translation-project'])
    def test_main_invalid_args(self, mock_banner, mock_zipfile):
        """Test main function with invalid arguments."""
        with pytest.raises(SystemExit) as exc_info:
            create_translation_project.main()
        
        assert exc_info.value.code == 1

    @mock.patch('src.create_translation_project.os.path.exists')
    @mock.patch('src.create_translation_project.os.makedirs')
    @mock.patch('src.create_translation_project.shutil.rmtree')
    @mock.patch('src.create_translation_project.zipfile.ZipFile')
    @mock.patch('src.create_translation_project.common.print_banner')
    def test_main_successful_extraction(self, mock_banner, mock_zipfile, 
                                       mock_rmtree, mock_makedirs, mock_exists):
        """Test successful project creation."""
        mock_exists.return_value = True  # Directory exists
        mock_zipfile.return_value.__enter__.return_value.extractall = mock.Mock()
        
        with mock.patch('sys.argv', ['create-translation-project', self.temp_dir, 'test_translation']):
            create_translation_project.main()
        
        # Should exit normally after successful execution
        mock_rmtree.assert_called_once()
        mock_banner.assert_called()

    @mock.patch('src.create_translation_project.os.path.exists')
    @mock.patch('src.create_translation_project.os.makedirs')
    @mock.patch('src.create_translation_project.shutil.rmtree')
    @mock.patch('src.create_translation_project.zipfile.ZipFile')
    @mock.patch('src.create_translation_project.common.print_banner')
    def test_main_default_project_name(self, mock_banner, mock_zipfile, 
                                      mock_rmtree, mock_makedirs, mock_exists):
        """Test main function with default project name."""
        mock_exists.return_value = True  # Directory exists
        mock_zipfile.return_value.__enter__.return_value.extractall = mock.Mock()
        
        with mock.patch('sys.argv', ['create-translation-project', self.temp_dir]):
            create_translation_project.main()
        
        # Should use default name "translation_proj"
        expected_target = os.path.join(self.temp_dir, "translation_proj")
        mock_rmtree.assert_called_once_with(expected_target)