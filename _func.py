import sys
import subprocess

# Run a command in the shell
def run_command(cmd):
    try:
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for line in iter(popen.stdout.readline, b''):
            sys.stdout.write(line.decode('utf-8'))
            sys.stdout.flush()

        popen.wait()
    except subprocess.CalledProcessError as e:
            print(f"Error: Command '{cmd}' failed.")
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

import subprocess

