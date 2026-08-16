"""统一日志配置与全链路 request_id 追踪

设计要点：
- 单一事实来源：logging.config.dictConfig 声明式配置，幂等可重复调用
- request_id 通过 contextvars 传播，纯 ASGI 中间件保证同 task 内可见
- 敏感信息脱敏（password/token/Authorization）
- 级别联动：config.logging.level 未配置时自动随 app.debug 切换
- 独立的 file_data 追踪日志（保留 file_id 维度，propagate=False）
"""

import logging
import logging.config
import os
import re
import time
import uuid
from contextvars import ContextVar

_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ==================== request_id 上下文 ====================

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


def get_request_id() -> str:
    """读取当前上下文的 request_id，无请求上下文时返回 '-'"""
    return request_id_var.get()


# ==================== Filters ====================


class RequestIDFilter(logging.Filter):
    """自动注入当前请求的 request_id，缺失时默认为 '-'"""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True


class FileIDFilter(logging.Filter):
    """自动注入 file_id，缺失时默认为 '-'"""

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "file_id"):
            record.file_id = "-"
        return True


# ==================== 敏感信息脱敏 ====================

_BEARER_PATTERN = re.compile(r"(?i)\b(?:Bearer|Basic)\s+\S+")
_AUTH_PATTERN = re.compile(
    r"(?i)(authorization)\s*[=:]\s*(?!Bearer\b|Basic\b)\S+(?:\s+\S+)?"
)
_KEY_VALUE_PATTERN = re.compile(
    r"(?i)(access_token|refresh_token|password|passwd|token)\s*[=:]\s*\S+"
)


class SensitiveFormatter(logging.Formatter):
    """格式化后对消息中的敏感值脱敏（password/token/Authorization/Bearer）"""

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        message = _BEARER_PATTERN.sub(
            lambda m: m.group(0).split(None, 1)[0] + " ***", message
        )
        message = _AUTH_PATTERN.sub(r"\1: ***", message)
        message = _KEY_VALUE_PATTERN.sub(r"\1=***", message)
        return message


# ==================== 统一配置 ====================

_APP_FORMAT = (
    "[%(asctime)s.%(msecs)03d] [%(levelname)-7s] [req_id=%(request_id)s] "
    "[%(name)s] %(message)s"
)
_FILE_DATA_FORMAT = (
    "[%(asctime)s.%(msecs)03d] [%(levelname)s] [req_id=%(request_id)s] "
    "[file_id=%(file_id)s] %(message)s"
)
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def resolve_level(cfg) -> str:
    """解析日志级别名：config.logging.level 优先，否则联动 app.debug"""
    return (cfg.logging.level or ("DEBUG" if cfg.app.debug else "INFO")).upper()


def setup_logging(cfg) -> None:
    """初始化全局日志配置（幂等，可重复调用）。

    支持任意带 `.logging` 与 `.app.debug` 属性的配置对象，
    便于测试注入假配置。
    """
    level_name = resolve_level(cfg)

    app_log_path = cfg.logging.file_path
    if not os.path.isabs(app_log_path):
        app_log_path = os.path.join(_BACKEND_DIR, app_log_path)
    file_data_log_path = os.path.join(_BACKEND_DIR, "data", "log", "file_data.log")

    for path in (app_log_path, file_data_log_path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    root_handlers = ["console"]
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "level": level_name,
            "formatter": "app",
            "filters": ["request_id"],
        },
        "file_data": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "file_data",
            "filters": ["request_id", "file_id"],
            "filename": file_data_log_path,
            "maxBytes": cfg.logging.rotate_max_bytes,
            "backupCount": cfg.logging.backup_count,
            "encoding": "utf-8",
        },
    }
    if cfg.logging.file_enabled:
        root_handlers.append("app_file")
        handlers["app_file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": level_name,
            "formatter": "app",
            "filters": ["request_id"],
            "filename": app_log_path,
            "maxBytes": cfg.logging.rotate_max_bytes,
            "backupCount": cfg.logging.backup_count,
            "encoding": "utf-8",
        }

    config_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "app": {
                "()": SensitiveFormatter,
                "format": _APP_FORMAT,
                "datefmt": _DATE_FORMAT,
            },
            "file_data": {
                "()": SensitiveFormatter,
                "format": _FILE_DATA_FORMAT,
                "datefmt": _DATE_FORMAT,
            },
        },
        "filters": {
            "request_id": {"()": RequestIDFilter},
            "file_id": {"()": FileIDFilter},
        },
        "handlers": handlers,
        "loggers": {
            "": {"handlers": root_handlers, "level": level_name, "propagate": False},
            "file_data.trace": {"handlers": ["file_data"], "level": "DEBUG", "propagate": False},
            "sqlalchemy.engine": {"level": "DEBUG" if cfg.app.debug else "WARNING", "propagate": True},
            "uvicorn": {"level": "WARNING", "propagate": True},
            "uvicorn.error": {"level": "WARNING", "propagate": True},
            "uvicorn.access": {"level": "CRITICAL", "propagate": False},
            "httpx": {"level": "WARNING", "propagate": True},
        },
    }

    logging.config.dictConfig(config_dict)
    logging.getLogger("app.logging").info(
        "日志系统已初始化 | level=%s | app_log=%s | file_data_log=%s",
        level_name, app_log_path, file_data_log_path,
    )


# ==================== 请求访问日志中间件 ====================

_middleware_logger = logging.getLogger("app.middleware")


class RequestLogMiddleware:
    """纯 ASGI 请求日志中间件。

    在进入下游前生成 request_id 并写入 contextvars，沿同一调用链
    自动关联该请求的全部业务/DB/出站日志；同时记录访问明细并返回
    X-Request-ID 响应头。
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        rid = uuid.uuid4().hex[:12]
        token = request_id_var.set(rid)
        # 写入 scope：ServerErrorMiddleware 的全局异常处理器在 contextvar
        # 复位之后才执行，需通过 scope 传递 request_id
        scope["request_id"] = rid

        start = time.perf_counter()
        status_code = 500
        path = scope.get("path", "-")
        method = scope.get("method", "-")
        seen_start = False

        def send_wrapper(message):
            nonlocal status_code, seen_start
            if message["type"] == "http.response.start":
                status_code = message["status"]
                seen_start = True
                headers = message.get("headers", [])
                # 去重：下游（如全局异常处理器）可能已设置 X-Request-ID
                if not any(k.lower() == b"x-request-id" for k, _ in headers):
                    message["headers"] = headers + [(b"x-request-id", rid.encode())]
            return send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            # 未处理异常交给外层 ServerErrorMiddleware 兜底（此处不吞异常，
            # 仅记录访问行，异常详情由全局异常处理记录）
            duration_ms = (time.perf_counter() - start) * 1000
            if not seen_start:
                status_code = 500
            # 在复位 request_id 之前记录，保证过滤器的 [req_id=] 与实际一致
            _middleware_logger.info(
                "REQUEST %s %s status=%s duration=%.0fms req_id=%s",
                method, path, status_code, duration_ms, rid,
            )
            request_id_var.reset(token)
