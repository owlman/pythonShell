import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}")
        print(result.stderr)
        exit()
    else:
        print(result.stdout)

def print_banner(message):
    n = len(message)
    print(n * '=')
    print(message+ (n - len(message) - 1) * ' ' + "=")
    print(n * '=')
