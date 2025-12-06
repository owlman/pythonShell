#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import create_book_project


class TestCreateBookProject(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('sys.argv', ['create-book-project', '/tmp/test_project'])
    @patch('create_book_project.common.print_banner')
    @patch('zipfile.ZipFile')
    @patch('os.path.exists')
    def test_create_project_default_name(self, mock_exists, mock_zipfile, mock_banner):
        mock_exists.return_value = False
        mock_zip_instance = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip_instance
        
        with patch('os.makedirs') as mock_makedirs:
            with patch('shutil.rmtree') as mock_rmtree:
                create_book_project.main()
        
        mock_makedirs.assert_called()
        mock_banner.assert_called()

    @patch('sys.argv', ['create-book-project', '/tmp/test_project', 'my_book'])
    @patch('create_book_project.common.print_banner')
    @patch('zipfile.ZipFile')
    @patch('os.path.exists')
    def test_create_project_custom_name(self, mock_exists, mock_zipfile, mock_banner):
        mock_exists.side_effect = [True, True]
        mock_zip_instance = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip_instance
        
        with patch('shutil.rmtree') as mock_rmtree:
            create_book_project.main()
        
        mock_rmtree.assert_called()
        mock_banner.assert_called()

    @patch('sys.argv', ['create-book-project'])
    @patch('builtins.print')
    def test_missing_arguments(self, mock_print):
        with self.assertRaises(SystemExit):
            create_book_project.main()
        mock_print.assert_called_with("Usage: create-book-project <project_directory> [project_name]")

    @patch('sys.argv', ['create-book-project', '/tmp/test', 'name', 'extra'])
    @patch('builtins.print')
    def test_too_many_arguments(self, mock_print):
        with self.assertRaises(SystemExit):
            create_book_project.main()
        mock_print.assert_called_with("Usage: create-book-project <project_directory> [project_name]")

    @patch('sys.argv', ['create-book-project', '/tmp/test_project'])
    @patch('create_book_project.common.print_banner')
    @patch('zipfile.ZipFile')
    @patch('builtins.print')
    def test_extraction_failure(self, mock_print, mock_zipfile, mock_banner):
        mock_zipfile.side_effect = Exception("Extraction failed")
        
        with patch('os.path.exists', return_value=False):
            with patch('os.makedirs'):
                with self.assertRaises(SystemExit):
                    create_book_project.main()


if __name__ == '__main__':
    unittest.main()
