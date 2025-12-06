#!/usr/bin/env python3
"""
修复了编码问题的测试运行脚本
"""

import os
import sys
import subprocess

# 修复locale环境变量
os.environ['LC_ALL'] = 'C.utf8'
os.environ['LANG'] = 'C.utf8'
os.environ['LANGUAGE'] = 'en_US:en'

# 添加src目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

def main():
    """运行测试"""
    print("使用修复的locale运行测试...")
    print(f"LC_ALL={os.environ.get('LC_ALL')}")
    
    # 运行原始测试脚本
    test_script = os.path.join(project_root, 'test', 'run_tests.py')
    
    try:
        result = subprocess.run([sys.executable, test_script] + sys.argv[1:], 
                              cwd=project_root, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        return e.returncode

if __name__ == '__main__':
    sys.exit(main())
