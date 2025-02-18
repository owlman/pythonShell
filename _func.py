import sys
import subprocess

# Run a command in the shell
def run_command(cmd):
    try:
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in iter(popen.stdout.readline, b''):
            sys.stdout.write(line.decode('utf-8'))
            sys.stdout.flush()
        
        for line in iter(popen.stderr.readline, b''):
            sys.stderr.write(line.decode('utf-8'))
            sys.stderr.flush()
            
        returncode = popen.wait()
        if returncode != 0:
            print(f"Error: Command '{cmd}' failed.")
            exit(1)
    
    except subprocess.CalledProcessError as e:
            print(f"Error: Command '{cmd}' failed.")
            exit(1) 
    finally:
        if popen.stdout:
            popen.stdout.close()
        if popen.stderr:
            popen.stderr.close()
        
# Print a banner with a message
def print_banner(message):
    bannerWidth = 90
    borderChar = "#"
    bannerBorder = bannerWidth * borderChar
    middleLine = borderChar + message.center(bannerWidth - 2) + borderChar 
    print(bannerBorder)
    print(middleLine)
    print(bannerBorder)

