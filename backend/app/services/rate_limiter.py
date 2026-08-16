"""登录限流服务 - 内存滑动窗口

按 IP + 用户名维度限制失败登录尝试，防止暴力破解。
单进程内存实现，适合当前部署规模（SQLite 单实例）。
"""

import time
import threading
from collections import deque
from typing import Dict, Tuple


class SlidingWindowLimiter:
    """基于滑动窗口的限流器"""

    def __init__(self, max_attempts: int = 5, window_seconds: int = 60):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._records: Dict[str, deque] = {}
        self._lock = threading.Lock()

    def _cleanup(self, key: str) -> deque:
        now = time.monotonic()
        window_start = now - self.window_seconds
        with self._lock:
            records = self._records.get(key)
            if records is None:
                records = deque()
                self._records[key] = records
            # 移除窗口外的记录
            while records and records[0] < window_start:
                records.popleft()
            # 清理空记录，防止内存无限增长
            if not records:
                self._records.pop(key, None)
        return records

    def record_failure(self, key: str) -> None:
        records = self._cleanup(key)
        with self._lock:
            records.append(time.monotonic())

    def is_blocked(self, key: str) -> bool:
        records = self._cleanup(key)
        return len(records) >= self.max_attempts

    def reset(self, key: str) -> None:
        with self._lock:
            self._records.pop(key, None)


_login_limiter = SlidingWindowLimiter(max_attempts=5, window_seconds=60)


def login_failure_key(ip: str, username: str) -> str:
    """生成限流 key：IP + 用户名"""
    return f"{ip}|{username or '-'}"


def record_login_failure(ip: str, username: str) -> None:
    _login_limiter.record_failure(login_failure_key(ip, username))


def is_login_blocked(ip: str, username: str) -> bool:
    return _login_limiter.is_blocked(login_failure_key(ip, username))


def reset_login_failures(ip: str, username: str) -> None:
    _login_limiter.reset(login_failure_key(ip, username))
