#!/usr/bin/env python3
"""
单元测试脚本：test_create_translation_project.py
测试 create_translation_project.py 模块
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import io
import tempfile
import shutil
import zipfile

# 添加 src 目录到 Python 路径
sys.path.insert(0, '/mnt/d/user/Documents/working/开发类项目/pythonShell/src')

import create_translation_project

class TestCreateTranslationProject(unittest.TestCase):
    """测试 create_translation_project 模块"""
    
    def setUp(self):
        """测试前准备临时目录"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
    
    def tearDown(self):
        """测试后清理"""
        os.chdir(self.original_cwd)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @patch('sys.argv', ['create_translation_project.py', '/tmp/projects'])
    @patch('common.print_banner')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.rmtree')
    @patch('zipfile.ZipFile')
    def test_main_success_default_name(self, mock_zipfile, mock_rmtree, mock_makedirs,
                                      mock_exists, mock_print_banner):
        """测试成功创建项目（使用默认项目名）"""
        # 模拟路径存在性
        mock_exists.side_effect = lambda path: False if 'translation_proj' in path else True
        
        # 模拟 ZipFile
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        with patch('sys.exit') as mock_exit:
            create_translation_project.main()
            
            # 验证目录创建（模拟的 exists 返回 False，所以应该调用 makedirs）
            mock_makedirs.assert_called_once_with('/tmp/projects')
            
            # 验证目标目录被删除（如果存在）
            expected_target = '/tmp/projects/translation_proj'
            mock_exists.assert_any_call(expected_target)
            
            # 验证 ZipFile 被调用
            mock_zipfile.assert_called_once()
            
            # 验证解压
            mock_zip.extractall.assert_called_once_with(expected_target)
            
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['create_translation_project.py', '/tmp/projects', 'my_translation'])
    @patch('common.print_banner')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.rmtree')
    @patch('zipfile.ZipFile')
    def test_main_success_custom_name(self, mock_zipfile, mock_rmtree, mock_makedirs,
                                     mock_exists, mock_print_banner):
        """测试成功创建项目（使用自定义项目名）"""
        mock_exists.side_effect = lambda path: False if 'my_translation' in path else True
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        with patch('sys.exit') as mock_exit:
            create_translation_project.main()
            
            # 验证目标目录路径包含自定义名称
            expected_target = '/tmp/projects/my_translation'
            mock_exists.assert_any_call(expected_target)
            
            mock_zip.extractall.assert_called_once_with(expected_target)
            
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['create_translation_project.py'])
    @patch('sys.stdout.write')
    def test_main_insufficient_arguments(self, mock_write):
        """测试参数不足的情况"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                create_translation_project.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Usage:", output)
    
    @patch('sys.argv', ['create_translation_project.py', 'dir1', 'name1', 'extra'])
    @patch('sys.stdout.write')
    def test_main_too_many_arguments(self, mock_write):
        """测试参数过多的情况"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                create_translation_project.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Usage:", output)
    
    @patch('sys.argv', ['create_translation_project.py', '/tmp/projects', ''])
    @patch('common.print_banner')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.rmtree')
    @patch('zipfile.ZipFile')
    def test_main_empty_project_name(self, mock_zipfile, mock_rmtree, mock_makedirs,
                                    mock_exists, mock_print_banner):
        """测试空项目名（应使用默认名）"""
        mock_exists.side_effect = lambda path: False if 'translation_proj' in path else True
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        with patch('sys.exit') as mock_exit:
            create_translation_project.main()
            
            # 验证使用默认项目名
            expected_target = '/tmp/projects/translation_proj'
            mock_exists.assert_any_call(expected_target)
            
            mock_zip.extractall.assert_called_once_with(expected_target)
            
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['create_translation_project.py', '/tmp/projects'])
    @patch('common.print_banner')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.rmtree')
    @patch('zipfile.ZipFile')
    def test_main_existing_target_directory(self, mock_zipfile, mock_rmtree, mock_makedirs,
                                          mock_exists, mock_print_banner):
        """测试目标目录已存在（应被删除）"""
        # 模拟目标目录已存在
        mock_exists.side_effect = lambda path: True if 'translation_proj' in path else False
        
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        with patch('sys.exit') as mock_exit:
            create_translation_project.main()
            
            # 验证删除目录
            expected_target = '/tmp/projects/translation_proj'
            mock_rmtree.assert_called_once_with(expected_target)
            
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['create_translation_project.py', '/tmp/projects'])
    @patch('common.print_banner')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.rmtree')
    @patch('zipfile.ZipFile')
    def test_main_zip_extraction_failure(self, mock_zipfile, mock_rmtree, mock_makedirs,
                                        mock_exists, mock_print_banner):
        """测试 ZIP 解压失败"""
        mock_exists.side_effect = lambda path: False
        
        # 模拟解压失败
        mock_zipfile.side_effect = zipfile.BadZipFile("Invalid zip file")
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                create_translation_project.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Failed to extract template", output)
    
    @patch('sys.argv', ['create_translation_project.py', '/tmp/projects'])
    @patch('common.print_banner')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.rmtree')
    def test_main_template_not_found(self, mock_rmtree, mock_makedirs, mock_exists,
                                    mock_print_banner):
        """测试模板文件不存在"""
        mock_exists.side_effect = lambda path: False
        
        # 模拟文件路径
        with patch('os.path.dirname') as mock_dirname:
            with patch('os.path.abspath') as mock_abspath:
                mock_abspath.return_value = '/path/to/src/create_translation_project.py'
                mock_dirname.return_value = '/path/to/src'
                
                # 模拟 zipfile.ZipFile 抛出文件不存在异常
                with patch('zipfile.ZipFile') as mock_zipfile:
                    mock_zipfile.side_effect = FileNotFoundError("No such file")
                    
                    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                        with self.assertRaises(SystemExit) as cm:
                            create_translation_project.main()
                        
                        self.assertEqual(cm.exception.code, 1)
                        output = mock_stdout.getvalue()
                        self.assertIn("Failed to extract template", output)
    
    def test_real_directory_creation(self):
        """测试实际目录创建（集成测试）"""
        test_project_path = os.path.join(self.temp_dir, "test_projects")
        
        # 模拟命令行参数
        with patch('sys.argv', ['create_translation_project.py', test_project_path, 'test_trans']):
            # 模拟 common.print_banner
            with patch('common.print_banner') as mock_banner:
                # 模拟文件操作
                with patch('os.path.exists') as mock_exists:
                    mock_exists.return_value = False
                    
                    with patch('os.makedirs') as mock_makedirs:
                        with patch('shutil.rmtree') as mock_rmtree:
                            with patch('zipfile.ZipFile') as mock_zipfile:
                                mock_zip = MagicMock()
                                mock_zipfile.return_value.__enter__.return_value = mock_zip
                                
                                create_translation_project.main()
                
                # 验证目录创建被调用
                mock_makedirs.assert_called_once_with(test_project_path)
                
                # 验证解压被调用
                expected_target = os.path.join(test_project_path, 'test_trans')
                mock_zip.extractall.assert_called_once_with(expected_target)
    
    @patch('sys.argv', ['create_translation_project.py', '/tmp/projects'])
    @patch('common.print_banner')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.rmtree')
    @patch('zipfile.ZipFile')
    def test_main_project_directory_already_exists(self, mock_zipfile, mock_rmtree,
                                                  mock_makedirs, mock_exists,
                                                  mock_print_banner):
        """测试项目目录已存在（不应重复创建）"""
        # 模拟项目目录已存在
        mock_exists.side_effect = lambda path: True
        
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        with patch('sys.exit') as mock_exit:
            create_translation_project.main()
            
            # 验证 makedirs 没有被调用（因为目录已存在）
            mock_makedirs.assert_not_called()
            
            mock_exit.assert_not_called()
    
    @patch('sys.argv', ['create_translation_project.py', '/tmp/projects'])
    @patch('common.print_banner')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.rmtree')
    @patch('zipfile.ZipFile')
    def test_main_script_name_extraction(self, mock_zipfile, mock_rmtree, mock_makedirs,
                                        mock_exists, mock_print_banner):
        """测试脚本名提取"""
        mock_exists.return_value = False
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        # 模拟 os.path.basename
        with patch('os.path.basename') as mock_basename:
            mock_basename.return_value = 'create-translation-project'
            
            create_translation_project.main()
            
            # 验证 print_banner 被调用2次
            self.assertEqual(mock_print_banner.call_count, 2)
            
            # 验证第一次调用包含脚本名
            first_call = mock_print_banner.call_args_list[0]
            self.assertIn('create-translation-project', str(first_call))

if __name__ == '__main__':
    unittest.main()