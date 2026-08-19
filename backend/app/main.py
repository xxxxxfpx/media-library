"""FastAPI 主应用"""

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.file import router as file_router
from app.api.guangyapan import router as guangyapan_router
from app.api.media import router as media_router
from app.api.system import router as system_router
from app.api.user import router as user_router
from app.logging_config import RequestLogMiddleware, get_request_id, setup_logging
from app.services.auth_service import AuthService
from config import get_config
from database.core import AsyncSessionLocal, init_db

config = get_config()
logger = logging.getLogger(__name__)
setup_logging(config)

start_time = datetime.now()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""

    # 安全校验：生产环境禁止空密钥/空管理员密码（失败即关闭）
    if not config.app.secret_key:
        raise RuntimeError(
            "app.secret_key 未配置，拒绝启动。请在 secrets/config.yaml 中配置安全随机密钥。"
        )
    # 二次应用日志配置：覆盖 uvicorn 在应用导入后注入的默认 dictConfig
    setup_logging(config)
    if config.app.debug:
        logger.warning("debug 模式已开启，仅限开发环境使用")
    if not config.app.admin_password:
        logger.warning("管理员密码为空，请尽快在配置中设置")

    await init_db()

    async with AsyncSessionLocal() as db:
        try:
            admin = await AuthService.get_user_by_username(db, config.app.admin_username)
            if not admin:
                await AuthService.create_user(
                    db,
                    username=config.app.admin_username,
                    password=config.app.admin_password,
                    is_admin=True
                )
                logger.info(f"管理员账户已创建: {config.app.admin_username}")
            await db.commit()
        except Exception as e:
            await db.rollback()
            logger.error(f"创建管理员账户失败: {e}")

    yield

    from app.api.file import close_http_client
    await close_http_client()
    logger.info("HTTP 客户端已关闭")


app = FastAPI(
    title=config.app.name,
    version=config.app.version,
    debug=config.app.debug,
    lifespan=lifespan,
)

# 配置 CORS：默认仅允许本地开发来源；生产环境通过 CORS_ORIGINS 环境变量显式指定
_cors_origins_env = os.environ.get("CORS_ORIGINS", "")
cors_origins = (
    [o.strip() for o in _cors_origins_env.split(",") if o.strip()]
    if _cors_origins_env
    else ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000", "http://127.0.0.1:8000"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLogMiddleware)


app.include_router(user_router)
app.include_router(media_router)
app.include_router(file_router)
app.include_router(guangyapan_router)
app.include_router(system_router, prefix="/api")


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "version": config.app.version}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    rid = request.scope.get("request_id") or get_request_id()
    logger.error(
        "未处理异常: %s | method=%s path=%s req_id=%s",
        exc, request.method, request.url.path, rid, exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc) if config.app.debug else "服务器内部错误"},
        headers={"X-Request-ID": rid},
    )
