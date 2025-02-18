import subprocess

# Run a command in the shell
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            print(f"Error: Command '{command}' failed.")
            print(result.stderr)
        else:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
            print(f"Error: Command '{command}' failed.")
            exit(1) 

# Print a banner with a message
def print_banner(message):
    bannerWidth = 90
    borderChar = "#"
    bannerBorder = bannerWidth * borderChar
    middleLine = borderChar + message.center(bannerWidth - 2) + borderChar 
    print(bannerBorder)
    print(middleLine)
    print(bannerBorder)
