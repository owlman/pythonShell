import sys
import subprocess

def run_command(cmd):
    try:
        # Run the command and capture both stdout and stderr
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Read and print stdout in real-time
        for line in iter(popen.stdout.readline, b''):
            sys.stdout.write(line.decode('utf-8', errors='replace'))
            sys.stdout.flush()
        
        # Read and print stderr in real-time
        for line in iter(popen.stderr.readline, b''):
            sys.stderr.write(line.decode('utf-8', errors='replace'))
            sys.stderr.flush()
        
        # Wait for the process to complete and get the return code
        return_code = popen.wait()
        
        # Check if the command failed (non-zero return code)
        if return_code != 0:
            print(f"Error: Command '{' '.join(cmd)}' failed with return code {return_code}.")
            exit(return_code)
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)
    finally:
        # Ensure that the file descriptors are closed
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

