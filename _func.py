import sys
import subprocess

# Run a command in the shell
def run_command(cmd):
    try:
        popen = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,          # ✅ 必须加上
            text=True            # ✅ 自动处理 UTF-8 解码
        )
        for line in iter(popen.stdout.readline, ''):
            sys.stdout.write(line)
            sys.stdout.flush()

        for line in iter(popen.stderr.readline, ''):
            sys.stderr.write(line)
            sys.stderr.flush()

        returncode = popen.wait()
        if returncode != 0:
            print(f"Error: Command '{cmd}' failed with code {returncode}.")
            exit(1)

    except Exception as e:
        print(f"Exception while running '{cmd}': {e}")
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
