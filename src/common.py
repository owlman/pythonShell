import sys
import subprocess
import selectors
import time
import shutil

def run_command(cmd, shell=False, timeout=300):
    """
    Execute a system command safely with real-time stdout/stderr output.

    Features:
        - Cross-platform support: Windows / Linux / macOS
        - Real-time printing of stdout and stderr
        - Enforces a total timeout for the command
        - Defaults to shell=False for security
        - Handles cleanup of subprocess and selector

    Args:
        cmd (str or list): Command to execute.
        shell (bool): Whether to run command through shell. Default is False.
        timeout (int or None): Maximum allowed execution time in seconds.
                               None disables the timeout.

    Returns:
        int: Exit code of the command (0 indicates success).

    Raises:
        subprocess.TimeoutExpired: If the command runs longer than the timeout.
        subprocess.SubprocessError: If the command exits with a non-zero status.
    """

    # If the command is a string and shell=False, split it into a list for safety
    if isinstance(cmd, str) and not shell:
        import shlex
        cmd = shlex.split(cmd)

    # Start the subprocess, capture both stdout and stderr
    popen = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True, 
        shell=shell
    )

    # Use selectors to monitor both stdout and stderr for real-time output
    selector = selectors.DefaultSelector()
    selector.register(popen.stdout, selectors.EVENT_READ)
    selector.register(popen.stderr, selectors.EVENT_READ)

    start_time = time.time()

    try:
        while True:
            # Check for overall timeout
            if timeout is not None and (time.time() - start_time) > timeout:
                raise subprocess.TimeoutExpired(cmd, timeout)

            # Wait for any output from stdout/stderr with 0.1s polling interval
            events = selector.select(timeout=0.1)
            for key, _ in events:
                data = key.fileobj.readline()
                if data:
                    # Print stdout/stderr immediately
                    if key.fileobj is popen.stdout:
                        sys.stdout.write(data)
                    else:
                        sys.stderr.write(data)
                    sys.stdout.flush()
                    sys.stderr.flush()

            # Exit the loop if the subprocess has finished
            if popen.poll() is not None:
                # Read and print any remaining output
                for pipe in (popen.stdout, popen.stderr):
                    remaining = pipe.read()
                    if remaining:
                        if pipe is popen.stdout:
                            sys.stdout.write(remaining)
                        else:
                            sys.stderr.write(remaining)
                break

        # Raise error if the command failed
        if popen.returncode != 0:
            raise subprocess.SubprocessError(
                f"Command '{cmd}' failed with exit code {popen.returncode}"
            )

        return popen.returncode

    finally:
        # Cleanup: unregister and close file objects
        for pipe in (popen.stdout, popen.stderr):
            try:
                selector.unregister(pipe)
            except Exception:
                pass
            pipe.close()
        # Ensure the subprocess is terminated
        if popen.poll() is None:
            popen.kill()


def print_banner(message):
    """
    Print a centered banner around a message, dynamically sized
    to fit the terminal width.

    Args:
        message (str): Message to display in the banner.
    """
    # Get terminal width, defaulting to 90 if detection fails
    width = shutil.get_terminal_size((90, 20)).columns
    borderChar = "#"
    bannerBorder = width * borderChar
    middleLine = borderChar + message.center(width - 2) + borderChar
    print(bannerBorder)
    print(middleLine)
    print(bannerBorder)
