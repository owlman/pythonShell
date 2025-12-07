#!/usr/bin/env python3
"""
Simple encoding test script
"""

import os
import sys

# Fix locale encoding issues
os.environ['LC_ALL'] = 'C.utf8'
os.environ['LANG'] = 'C.utf8'
os.environ['LANGUAGE'] = 'en_US:en'

def test_encoding():
    """Test if encoding is correct"""
    print("Encoding test:")
    print(f"Default encoding: {sys.getdefaultencoding()}")
    print(f"File system encoding: {sys.getfilesystemencoding()}")
    print(f"stdout encoding: {sys.stdout.encoding if hasattr(sys.stdout, 'encoding') else 'unknown'}")

    # Test Chinese characters
    try:
        test_str = "测试中文字符"
        print(f"Chinese character test: {test_str}")
        return True
    except Exception as e:
        print(f"Chinese character test failed: {e}")
        return False

def test_imports():
    """Test module imports"""
    print("\nModule import test:")

    try:
        # Test importing common module
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
        import common
        print("✅ common module imported successfully")

        # Test common module functionality
        common.print_banner("Test banner")
        print("✅ common.print_banner function works properly")

        return True
    except Exception as e:
        print(f"❌ Module import failed: {e}")
        return False

if __name__ == '__main__':
    print("PythonShell Encoding Fix Verification")
    print("=" * 40)

    encoding_ok = test_encoding()
    imports_ok = test_imports()

    if encoding_ok and imports_ok:
        print("\n✅ All tests passed! Encoding issues have been fixed.")
        sys.exit(0)
    else:
        print("\n❌ There are still issues to be resolved.")
        sys.exit(1)
