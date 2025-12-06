#!/usr/bin/env python3
"""
简单的编码测试脚本
"""

import os
import sys

# 修复locale编码问题
os.environ['LC_ALL'] = 'C.utf8'
os.environ['LANG'] = 'C.utf8'
os.environ['LANGUAGE'] = 'en_US:en'

def test_encoding():
    """测试编码是否正确"""
    print("编码测试:")
    print(f"默认编码: {sys.getdefaultencoding()}")
    print(f"文件系统编码: {sys.getfilesystemencoding()}")
    print(f"stdout编码: {sys.stdout.encoding if hasattr(sys.stdout, 'encoding') else '未知'}")
    
    # 测试中文字符
    try:
        test_str = "测试中文字符"
        print(f"中文字符测试: {test_str}")
        return True
    except Exception as e:
        print(f"中文字符测试失败: {e}")
        return False

def test_imports():
    """测试模块导入"""
    print("\n模块导入测试:")
    
    try:
        # 测试导入common模块
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
        import common
        print("✅ common模块导入成功")
        
        # 测试common模块功能
        common.print_banner("测试横幅")
        print("✅ common.print_banner功能正常")
        
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False

if __name__ == '__main__':
    print("PythonShell 编码修复验证")
    print("=" * 40)
    
    encoding_ok = test_encoding()
    imports_ok = test_imports()
    
    if encoding_ok and imports_ok:
        print("\n✅ 所有测试通过！编码问题已修复。")
        sys.exit(0)
    else:
        print("\n❌ 仍有问题需要解决。")
        sys.exit(1)