import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            print(f"Error: Command '{command}' failed.")
            print(result.stderr)
        else:
            print(result.stdout)
    except FileNotFoundError:
        print(f"Error: Command '{command}' not found.")
    

def print_banner(message):
    bannerWidth = 100
    borderChar = "#"
    bannerBorder = bannerWidth * borderChar
    middleLine = borderChar + message.center(bannerWidth - 2) + borderChar 
    print(bannerBorder)
    print(middleLine)
    print(bannerBorder)
