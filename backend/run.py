"""
媒体库管理系统启动脚本
仅启动后端服务，开启热加载

用法: python run.py
"""

import subprocess
import sys
import os
import time
import signal


class Colors:
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    END = "\033[0m"


def log(msg, color=Colors.GREEN):
    print(f"{color}[启动器]{Colors.END} {msg}")


def start_backend():
    """启动后端 (FastAPI + Uvicorn)"""
    from config import get_config
    cfg = get_config()
    log("启动后端服务...", Colors.BLUE)
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", cfg.app.host, "--port", str(cfg.app.port), "--reload"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
    )


def main():
    from config import get_config
    cfg = get_config()
    log("=" * 50)
    log("媒体库管理系统启动器")
    display_host = "localhost" if cfg.app.host in ("0.0.0.0", "127.0.0.1") else cfg.app.host
    log(f"后端: http://{display_host}:{cfg.app.port}")
    log("=" * 50)

    backend_proc = None

    try:
        backend_proc = start_backend()
        log("后端服务已启动！按 Ctrl+C 停止")
        log("-" * 50)

        import threading

        def stream_output(process, prefix, color):
            try:
                for line in process.stdout:
                    print(f"{color}[{prefix}]{Colors.END} {line}", end="")
            except Exception:
                pass

        backend_thread = threading.Thread(
            target=stream_output,
            args=(backend_proc, "后端", Colors.BLUE),
            daemon=True
        )
        backend_thread.start()

        while True:
            status = backend_proc.poll()
            if status is not None:
                if status in (0, 1):
                    log("检测到后端热重载，正在重启...", Colors.GREEN)
                    time.sleep(2)
                    backend_proc = start_backend()
                    backend_thread = threading.Thread(
                        target=stream_output,
                        args=(backend_proc, "后端", Colors.BLUE),
                        daemon=True
                    )
                    backend_thread.start()
                else:
                    log(f"后端进程异常退出 (代码: {status})", Colors.RED)
                    break
            time.sleep(0.5)

    except KeyboardInterrupt:
        log("\n收到停止信号，正在关闭服务...", Colors.RED)
    finally:
        if backend_proc:
            log("停止后端服务...", Colors.BLUE)
            if sys.platform == "win32":
                backend_proc.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                backend_proc.terminate()
            backend_proc.wait(timeout=5)
        log("所有服务已停止")


if __name__ == "__main__":
    main()
