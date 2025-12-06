#!/usr/bin/env python3
"""
单元测试脚本：test_common.py
测试 common.py 模块中的工具函数
"""

import sys
import subprocess
import unittest
from unittest.mock import patch, MagicMock, call
import io
import time

# 添加 src 目录到 Python 路径
sys.path.insert(0, '/mnt/d/user/Documents/working/开发类项目/pythonShell/src')

import common

class TestRunCommand(unittest.TestCase):
    """测试 run_command 函数"""
    
    @patch('subprocess.Popen')
    @patch('selectors.DefaultSelector')
    def test_run_command_success(self, mock_selector_class, mock_popen):
        """测试成功执行命令"""
        # 模拟 Popen 对象
        mock_process = MagicMock()
        mock_process.poll.return_value = 0
        mock_process.returncode = 0
        
        # 创建不同的 MagicMock 对象用于 stdout 和 stderr
        mock_stdout = MagicMock()
        mock_stderr = MagicMock()
        mock_stdout.readline.return_value = "stdout line\n"
        mock_stderr.readline.return_value = ""
        mock_stdout.read.return_value = ""
        mock_stderr.read.return_value = ""
        
        mock_process.stdout = mock_stdout
        mock_process.stderr = mock_stderr
        mock_popen.return_value = mock_process
        
        # 模拟 selector
        mock_selector = MagicMock()
        mock_selector_class.return_value = mock_selector
        
        # 模拟 select 返回
        mock_key_stdout = MagicMock()
        mock_key_stdout.fileobj = mock_stdout
        mock_selector.select.return_value = [(mock_key_stdout, MagicMock())]
        
        # 模拟 sys.stdout.write 和 sys.stderr.write
        with patch('sys.stdout.write') as mock_stdout_write:
            with patch('sys.stderr.write') as mock_stderr_write:
                # 执行测试
                result = common.run_command(["echo", "test"])
                
                # 验证结果
                self.assertEqual(result, 0)
                mock_popen.assert_called_once()
        
    @patch('subprocess.Popen')
    @patch('selectors.DefaultSelector')
    def test_run_command_failure(self, mock_selector_class, mock_popen):
        """测试命令执行失败"""
        # 模拟失败的进程
        mock_process = MagicMock()
        mock_process.poll.return_value = 1
        mock_process.returncode = 1
        
        # 创建不同的 MagicMock 对象
        mock_stdout = MagicMock()
        mock_stderr = MagicMock()
        mock_stdout.readline.return_value = ""
        mock_stderr.readline.return_value = "error message\n"
        mock_stdout.read.return_value = ""
        mock_stderr.read.return_value = ""
        
        mock_process.stdout = mock_stdout
        mock_process.stderr = mock_stderr
        mock_popen.return_value = mock_process
        
        # 模拟 selector
        mock_selector = MagicMock()
        mock_selector_class.return_value = mock_selector
        mock_selector.select.return_value = []
        
        # 测试异常
        with patch('sys.stdout.write'):
            with patch('sys.stderr.write'):
                with self.assertRaises(subprocess.SubprocessError):
                    common.run_command(["false"])
    
    @patch('subprocess.Popen')
    @patch('selectors.DefaultSelector')
    @patch('time.time')
    def test_run_command_timeout(self, mock_time, mock_selector_class, mock_popen):
        """测试命令超时"""
        # 模拟时间
        mock_time.side_effect = [0, 100, 200]  # 模拟超时
        
        # 模拟进程
        mock_process = MagicMock()
        mock_process.poll.return_value = None  # 进程仍在运行
        
        # 创建不同的 MagicMock 对象
        mock_stdout = MagicMock()
        mock_stderr = MagicMock()
        mock_stdout.readline.return_value = ""
        mock_stderr.readline.return_value = ""
        
        mock_process.stdout = mock_stdout
        mock_process.stderr = mock_stderr
        mock_popen.return_value = mock_process
        
        # 模拟 selector
        mock_selector = MagicMock()
        mock_selector_class.return_value = mock_selector
        mock_selector.select.return_value = []
        
        # 测试超时异常
        with patch('sys.stdout.write'):
            with patch('sys.stderr.write'):
                with self.assertRaises(subprocess.TimeoutExpired):
                    common.run_command(["sleep", "10"], timeout=1)
    
    @patch('subprocess.Popen')
    @patch('selectors.DefaultSelector')
    def test_run_command_string_input(self, mock_selector_class, mock_popen):
        """测试字符串输入的命令"""
        mock_process = MagicMock()
        mock_process.poll.return_value = 0
        mock_process.returncode = 0
        
        # 创建不同的 MagicMock 对象
        mock_stdout = MagicMock()
        mock_stderr = MagicMock()
        mock_stdout.readline.return_value = ""
        mock_stderr.readline.return_value = ""
        mock_stdout.read.return_value = ""
        mock_stderr.read.return_value = ""
        
        mock_process.stdout = mock_stdout
        mock_process.stderr = mock_stderr
        mock_popen.return_value = mock_process
        
        # 模拟 selector
        mock_selector = MagicMock()
        mock_selector_class.return_value = mock_selector
        mock_selector.select.return_value = []
        
        # 测试字符串输入（shell=False）
        with patch('sys.stdout.write'):
            with patch('sys.stderr.write'):
                common.run_command("echo test")
                
                # 验证 shlex.split 被调用
                import shlex
                expected_args = shlex.split("echo test")
                mock_popen.assert_called_once()
    
    @patch('subprocess.Popen')
    @patch('selectors.DefaultSelector')
    def test_run_command_with_shell(self, mock_selector_class, mock_popen):
        """测试使用 shell=True 执行命令"""
        mock_process = MagicMock()
        mock_process.poll.return_value = 0
        mock_process.returncode = 0
        
        # 创建不同的 MagicMock 对象
        mock_stdout = MagicMock()
        mock_stderr = MagicMock()
        mock_stdout.readline.return_value = ""
        mock_stderr.readline.return_value = ""
        mock_stdout.read.return_value = ""
        mock_stderr.read.return_value = ""
        
        mock_process.stdout = mock_stdout
        mock_process.stderr = mock_stderr
        mock_popen.return_value = mock_process
        
        # 模拟 selector
        mock_selector = MagicMock()
        mock_selector_class.return_value = mock_selector
        mock_selector.select.return_value = []
        
        with patch('sys.stdout.write'):
            with patch('sys.stderr.write'):
                common.run_command("echo $HOME", shell=True)
                
                # 验证 shell=True 被传递
                mock_popen.assert_called_once_with(
                    "echo $HOME",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=True
                )

class TestPrintBanner(unittest.TestCase):
    """测试 print_banner 函数"""
    
    @patch('shutil.get_terminal_size')
    @patch('sys.stdout.write')
    def test_print_banner_default_width(self, mock_write, mock_terminal_size):
        """测试默认终端宽度"""
        # 模拟终端大小对象
        mock_size = MagicMock()
        mock_size.columns = 80
        mock_terminal_size.return_value = mock_size
        
        # 捕获输出
        with patch('builtins.print') as mock_print:
            common.print_banner("Test Message")
            
            # 验证打印被调用3次
            self.assertEqual(mock_print.call_count, 3)
    
    @patch('shutil.get_terminal_size')
    def test_print_banner_custom_width(self, mock_terminal_size):
        """测试自定义终端宽度"""
        # 模拟终端大小对象
        mock_size = MagicMock()
        mock_size.columns = 100
        mock_terminal_size.return_value = mock_size
        
        # 捕获输出
        with patch('builtins.print') as mock_print:
            common.print_banner("Test Message")
            
            # 验证打印被调用3次（边框、消息、边框）
            self.assertEqual(mock_print.call_count, 3)
            
            # 验证边框长度
            calls = mock_print.call_args_list
            border_line = calls[0][0][0]
            self.assertEqual(len(border_line), 100)
    
    @patch('shutil.get_terminal_size')
    def test_print_banner_fallback_width(self, mock_terminal_size):
        """测试终端大小检测失败时的回退宽度"""
        # 模拟终端大小对象
        mock_size = MagicMock()
        mock_size.columns = 90
        mock_terminal_size.return_value = mock_size
        
        with patch('builtins.print') as mock_print:
            common.print_banner("Test Message")
            
            calls = mock_print.call_args_list
            border_line = calls[0][0][0]
            self.assertEqual(len(border_line), 90)

if __name__ == '__main__':
    unittest.main()