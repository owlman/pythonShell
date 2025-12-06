#!/usr/bin/env python3
"""
修复测试环境编码问题的脚本
"""

import os
import sys
import subprocess
import shutil

def fix_locale_environment():
    """设置正确的locale环境变量"""
    # 设置可用的locale
    os.environ['LC_ALL'] = 'C.utf8'
    os.environ['LANG'] = 'C.utf8'
    os.environ['LANGUAGE'] = 'en_US:en'
    
    print("已设置locale环境变量:")
    print(f"LC_ALL={os.environ['LC_ALL']}")  
    print(f"LANG={os.environ['LANG']}")
    print(f"LANGUAGE={os.environ['LANGUAGE']}")

def check_python_encoding():
    """检查Python编码设置"""
    print("\nPython编码信息:")
    print(f"默认编码: {sys.getdefaultencoding()}")
    print(f"文件系统编码: {sys.getfilesystemencoding()}")
    print(f"stdout编码: {sys.stdout.encoding if hasattr(sys.stdout, 'encoding') else '未知'}")

def run_tests_with_fixed_locale():
    """使用修复的locale运行测试"""
    print("\n正在运行测试...")
    
    # 确保使用项目虚拟环境中的Python
    venv_python = os.path.join(os.getcwd(), '.venv', 'bin', 'python')
    if not os.path.exists(venv_python):
        venv_python = 'python'  # 回退到系统Python
    
    try:
        # 设置环境变量并运行测试
        env = os.environ.copy()
        env['LC_ALL'] = 'C.utf8'
        env['LANG'] = 'C.utf8'
        env['LANGUAGE'] = 'en_US:en'
        
        # 运行测试
        result = subprocess.run([
            venv_python, 'test/run_tests.py'
        ], env=env, cwd=os.getcwd(), capture_output=True, text=True)
        
        print("测试输出:")
        print(result.stdout)
        if result.stderr:
            print("错误输出:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"运行测试时出错: {e}")
        return False

def create_test_runner_script():
    """创建一个修复了编码问题的测试运行脚本"""
    script_content = '''#!/usr/bin/env python3
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
    '''
    
    with open('run_tests_fixed.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # 设置执行权限
    os.chmod('run_tests_fixed.py', 0o755)
    print("已创建修复版测试运行脚本: run_tests_fixed.py")

def main():
    """主函数"""
    print("PythonShell 测试环境编码问题修复工具")
    print("=" * 50)
    
    # 修复locale环境
    fix_locale_environment()
    
    # 检查Python编码
    check_python_encoding()
    
    # 创建修复版测试脚本
    create_test_runner_script()
    
    # 运行测试
    success = run_tests_with_fixed_locale()
    
    if success:
        print("\n✅ 测试环境编码问题已修复，测试运行成功！")
    else:
        print("\n❌ 测试仍有问题，请检查详细输出。")
        
        # 提供手动运行命令
        print("\n可以尝试手动运行以下命令:")
        print("export LC_ALL=C.utf8")
        print("export LANG=C.utf8") 
        print("python test/run_tests.py")

if __name__ == '__main__':
    main()