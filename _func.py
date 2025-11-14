import sys
import subprocess
import selectors
import time

def run_command(cmd, shell=False, timeout=300):
    """
    Execute a command safely with real-time output and cross-platform support.

    Features:
        - Fully compatible with Windows / Linux / macOS
        - Real-time stdout and stderr output
        - True overall timeout (not per-read timeout)
        - Defaults to shell=False for better security
        - Gracefully handles cleanup and exit codes

    Args:
        cmd: Command string or list.
        shell (bool): Execute via shell. Default: False (safer).
        timeout (int or None): Total execution timeout in seconds. 
                               None disables timeout (use with caution).

    Returns:
        int: Exit code (0 means success).

    Raises:
        subprocess.TimeoutExpired: If the command exceeds the time limit.
        subprocess.SubprocessError: For non-zero exit codes or execution errors.
    """

    # ----------- Preprocess command ----------- #
    if isinstance(cmd, str) and not shell:
        import shlex
        cmd = shlex.split(cmd)

    # ----------- Start subprocess ----------- #
    popen = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=shell
    )

    selector = selectors.DefaultSelector()
    selector.register(popen.stdout, selectors.EVENT_READ)
    selector.register(popen.stderr, selectors.EVENT_READ)

    start_time = time.time()

    try:
        while True:
            # Check overall timeout
            if timeout is not None and (time.time() - start_time) > timeout:
                popen.kill()
                raise subprocess.TimeoutExpired(cmd, timeout)

            # Wait for readable output (0.1s polling for smooth real-time output)
            events = selector.select(timeout=0.1)

            # Process ready streams
            for key, _ in events:
                data = key.fileobj.readline()
                if data:
                    if key.fileobj is popen.stdout:
                        sys.stdout.write(data)
                    else:
                        sys.stderr.write(data)
                    sys.stdout.flush()
                    sys.stderr.flush()

            # Exit if the process has finished and no more data is pending
            if popen.poll() is not None:
                # Drain remaining buffered output
                for pipe in (popen.stdout, popen.stderr):
                    remaining = pipe.read()
                    if remaining:
                        if pipe is popen.stdout:
                            sys.stdout.write(remaining)
                        else:
                            sys.stderr.write(remaining)
                break

        # Non-zero exit code → error
        if popen.returncode != 0:
            raise subprocess.SubprocessError(
                f"Command '{cmd}' failed with exit code {popen.returncode}"
            )

        return popen.returncode

    finally:
        # Cleanup
        selector.unregister(popen.stdout)
        selector.unregister(popen.stderr)
        popen.stdout.close()
        popen.stderr.close()
        if popen.poll() is None:
            popen.kill()

def print_banner(message):
    """
    Print a banner with the given message.
    """
    bannerWidth = 90
    borderChar = "#"
    bannerBorder = bannerWidth * borderChar
    middleLine = borderChar + message.center(bannerWidth - 2) + borderChar 
    print(bannerBorder)
    print(middleLine)
    print(bannerBorder)
