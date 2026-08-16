"""
日志系统单元测试
=================
覆盖 request_id 中间件、上下文传播、脱敏、幂等性与级别联动。
"""

import logging
from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.logging_config import (
    RequestLogMiddleware,
    SensitiveFormatter,
    get_request_id,
    resolve_level,
    setup_logging,
)


def _fake_config(debug: bool = True, level=None):
    return SimpleNamespace(
        logging=SimpleNamespace(
            level=level,
            file_enabled=False,
            file_path="",
            rotate_max_bytes=1024,
            backup_count=1,
        ),
        app=SimpleNamespace(debug=debug),
    )


# ==================== request_id 中间件 ====================


def _make_trace_app() -> FastAPI:
    """带 RequestLogMiddleware 的最小应用，路由回显当前 request_id"""
    app = FastAPI()
    app.add_middleware(RequestLogMiddleware)

    @app.get("/echo")
    async def echo():
        return {"request_id": get_request_id()}

    return app


@pytest.mark.asyncio
async def test_middleware_sets_request_id_and_header():
    app = _make_trace_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp1 = await client.get("/echo")
        resp2 = await client.get("/echo")

    assert resp1.status_code == 200
    rid1 = resp1.json()["request_id"]
    rid_header1 = resp1.headers.get("X-Request-ID")
    assert rid1 != "-"
    assert rid_header1 == rid1

    rid2 = resp2.json()["request_id"]
    assert rid2 != "-"
    assert rid1 != rid2, "两次请求应生成不同的 request_id"


@pytest.mark.asyncio
async def test_request_id_default_outside_request():
    assert get_request_id() == "-"


@pytest.mark.asyncio
async def test_real_app_health_returns_request_id(app_client):
    resp = await app_client.get("/health")
    assert resp.status_code == 200
    assert resp.headers.get("X-Request-ID")


@pytest.mark.asyncio
async def test_middleware_no_duplicate_request_id_on_error():
    """异常处理器已设置 X-Request-ID 时，中间件不应重复追加，且值应为实际 rid"""
    from fastapi import Request
    from fastapi.responses import JSONResponse

    app = FastAPI()
    app.add_middleware(RequestLogMiddleware)

    @app.exception_handler(Exception)
    async def handler(request: Request, exc: Exception):
        return JSONResponse(status_code=500, content={"detail": "boom"},
                            headers={"X-Request-ID": request.scope.get("request_id", "-")})

    @app.get("/boom")
    async def boom():
        raise RuntimeError("boom")

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/boom")

    assert resp.status_code == 500
    rid_list = resp.headers.get_list("X-Request-ID")
    assert len(rid_list) == 1, f"不应重复 X-Request-ID: {rid_list}"
    assert rid_list[0] != "-"


# ==================== 敏感信息脱敏 ====================


def test_sensitive_formatter_masks_values():
    formatter = SensitiveFormatter(fmt="%(message)s")
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname=__file__, lineno=1,
        msg="password=abc123 token=secret Authorization: Bearer eyJhbGci", args=(), exc_info=None,
    )
    out = formatter.format(record)
    assert "abc123" not in out
    assert "secret" not in out
    assert "eyJhbGci" not in out
    assert "password=***" in out
    assert "token=***" in out
    assert "Bearer ***" in out


def test_sensitive_formatter_masks_authorization_token_scheme():
    formatter = SensitiveFormatter(fmt="%(message)s")
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname=__file__, lineno=1,
        msg="Authorization: Token abc123def", args=(), exc_info=None,
    )
    out = formatter.format(record)
    assert "abc123def" not in out
    assert out == "Authorization: ***"


def test_sensitive_formatter_keeps_normal_text():
    formatter = SensitiveFormatter(fmt="%(message)s")
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname=__file__, lineno=1,
        msg="正常消息: 创建媒体成功 items=3", args=(), exc_info=None,
    )
    assert formatter.format(record) == "正常消息: 创建媒体成功 items=3"


# ==================== 级别联动 ====================


def test_resolve_level_links_to_debug():
    assert resolve_level(_fake_config(debug=True)) == "DEBUG"
    assert resolve_level(_fake_config(debug=False)) == "INFO"


def test_resolve_level_explicit_overrides():
    cfg = _fake_config(debug=False, level="WARNING")
    assert resolve_level(cfg) == "WARNING"


# ==================== 幂等性 ====================


def test_setup_logging_idempotent():
    setup_logging(_fake_config(debug=True))
    count1 = len(logging.getLogger().handlers)
    setup_logging(_fake_config(debug=True))
    count2 = len(logging.getLogger().handlers)
    assert count2 == count1, "重复调用不应重复添加 handler"
    # 恢复为应用真实配置，避免影响其他测试
    from config import get_config
    setup_logging(get_config())
