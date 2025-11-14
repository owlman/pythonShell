import sys
import subprocess
import selectors
import time

def run_command(cmd, shell=False, timeout=300):
    """
    安全、跨平台实时执行命令：
        - Windows / Linux / macOS 全兼容
        - 实时输出 stdout / stderr
        - 支持总体 timeout（而非 select 的局部 timeout）
        - 默认避免 shell=True 注入风险
    """

    # ----------- CMD 预处理 ----------- #
    if isinstance(cmd, str) and not shell:
        import shlex
        cmd = shlex.split(cmd)

    # ----------- 启动子进程 ----------- #
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
            # 检查整体 timeout
            if timeout is not None and (time.time() - start_time) > timeout:
                popen.kill()
                raise subprocess.TimeoutExpired(cmd, timeout)

            # 等待输出，timeout 设置成 0.1 秒以保持实时流畅
            events = selector.select(timeout=0.1)

            # 读取输出事件
            for key, _ in events:
                data = key.fileobj.readline()
                if data:
                    if key.fileobj is popen.stdout:
                        sys.stdout.write(data)
                    else:
                        sys.stderr.write(data)
                    sys.stdout.flush()
                    sys.stderr.flush()

            # 如果进程结束且管道没有数据，就退出
            if popen.poll() is not None:
                # 继续读取残留输出
                for pipe in (popen.stdout, popen.stderr):
                    remaining = pipe.read()
                    if remaining:
                        if pipe is popen.stdout:
                            sys.stdout.write(remaining)
                        else:
                            sys.stderr.write(remaining)
                break

        # 返回码处理
        if popen.returncode != 0:
            raise subprocess.SubprocessError(
                f"Command '{cmd}' failed with exit code {popen.returncode}"
            )

        return popen.returncode

    finally:
        selector.unregister(popen.stdout)
        selector.unregister(popen.stderr)
        popen.stdout.close()
        popen.stderr.close()
        if popen.poll() is None:
            popen.kill()

# Print a banner with a message
def print_banner(message):
    bannerWidth = 90
    borderChar = "#"
    bannerBorder = bannerWidth * borderChar
    middleLine = borderChar + message.center(bannerWidth - 2) + borderChar 
    print(bannerBorder)
    print(middleLine)
    print(bannerBorder)
