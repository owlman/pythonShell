#!/usr/bin/env python3
"""
Script to fix encoding issues in test environment
"""

import os
import subprocess
import sys


def fix_locale_environment():
    """Set correct locale environment variables"""
    # Set available locale
    os.environ['LC_ALL'] = 'C.utf8'
    os.environ['LANG'] = 'C.utf8'
    os.environ['LANGUAGE'] = 'en_US:en'

    print("Locale environment variables have been set:")
    print(f"LC_ALL={os.environ['LC_ALL']}")
    print(f"LANG={os.environ['LANG']}")
    print(f"LANGUAGE={os.environ['LANGUAGE']}")

def check_python_encoding():
    """Check Python encoding settings"""
    print("\nPython encoding information:")
    print(f"Default encoding: {sys.getdefaultencoding()}")
    print(f"File system encoding: {sys.getfilesystemencoding()}")
    print(f"stdout encoding: {sys.stdout.encoding if hasattr(sys.stdout, 'encoding') else 'unknown'}")

def run_tests_with_fixed_locale():
    """Run tests with fixed locale"""
    print("\nRunning tests...")

    # Ensure using Python from project virtual environment
    venv_python = os.path.join(os.getcwd(), '.venv', 'bin', 'python')
    if not os.path.exists(venv_python):
        venv_python = 'python'  # Fallback to system Python

    try:
        # Set environment variables and run tests
        env = os.environ.copy()
        env['LC_ALL'] = 'C.utf8'
        env['LANG'] = 'C.utf8'
        env['LANGUAGE'] = 'en_US:en'

        # Run tests
        result = subprocess.run([
            venv_python, 'test/run_tests.py'
        ], env=env, cwd=os.getcwd(), capture_output=True, text=True)

        print("Test output:")
        print(result.stdout)
        if result.stderr:
            print("Error output:")
            print(result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def create_test_runner_script():
    """Create a test runner script with fixed encoding issues"""
    script_content = '''#!/usr/bin/env python3
        """
        Test runner script with fixed encoding issues
        """

        import os
        import sys
        import subprocess

        # Fix locale environment variables
        os.environ['LC_ALL'] = 'C.utf8'
        os.environ['LANG'] = 'C.utf8'
        os.environ['LANGUAGE'] = 'en_US:en'

        # Add src directory to Python path
        project_root = os.path.dirname(os.path.abspath(__file__))
        src_path = os.path.join(project_root, 'src')
        sys.path.insert(0, src_path)

        def main():
            """Run tests"""
            print("Running tests with fixed locale...")
            print(f"LC_ALL={os.environ.get('LC_ALL')}")
            
            # Run original test script
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

    # Set execution permissions
    os.chmod('run_tests_fixed.py', 0o755)
    print("Created fixed test runner script: run_tests_fixed.py")

def main():
    """Main function"""
    print("PythonShell Test Environment Encoding Issue Fix Tool")
    print("=" * 50)

    # Fix locale environment
    fix_locale_environment()

    # Check Python encoding
    check_python_encoding()

    # Create fixed test script
    create_test_runner_script()

    # Run tests
    success = run_tests_with_fixed_locale()

    if success:
        print("\n✅ Test environment encoding issues have been fixed, tests run successfully!")
    else:
        print("\n❌ Tests still have issues, please check detailed output.")

        # Provide manual run commands
        print("\nYou can try manually running the following commands:")
        print("export LC_ALL=C.utf8")
        print("export LANG=C.utf8")
        print("python test/run_tests.py")

if __name__ == '__main__':
    main()

