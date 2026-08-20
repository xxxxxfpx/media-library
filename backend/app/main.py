"""FastAPI 主应用"""

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

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


# ── SPA 静态文件托管（单镜像模式下由 FastAPI 直接托管前端 dist） ──
# 仅当镜像内包含前端构建产物时才启用（开发模式无 static 目录，不影响）
_STATIC_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "static")
)

# /llm.txt 必须在 SPA fallback 之前注册，否则会被 /{full_path:path} 拦截
# 放在 if 块外确保开发模式（无 static 目录）也能注册
@app.get("/llm.txt", include_in_schema=False)
async def llm_txt():
    """为 AI Agent 提供的 API 文档（Markdown 格式），无需认证。"""
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(_LLM_TXT_CONTENT, media_type="text/plain; charset=utf-8")


if os.path.isdir(_STATIC_DIR):
    # Vite 产出的带哈希资源放在 /assets 下，文件名含内容哈希，
    # 可安全地长缓存（immutable）；index.html 必须每次回源校验，否则部署后浏览器持续使用旧入口
    _assets_dir = os.path.join(_STATIC_DIR, "assets")
    if os.path.isdir(_assets_dir):

        class _ImmutableStaticFiles(StaticFiles):
            """带内容哈希的静态资源：一年强缓存"""

            async def get_response(self, path, scope):
                response = await super().get_response(path, scope)
                response.headers["Cache-Control"] = (
                    "public, max-age=31536000, immutable"
                )
                return response

        app.mount(
            "/assets",
            _ImmutableStaticFiles(directory=_assets_dir),
            name="spa-assets",
        )

    @app.get("/", include_in_schema=False)
    async def spa_index():
        """首页：服务 index.html"""
        return FileResponse(
            os.path.join(_STATIC_DIR, "index.html"),
            headers={"Cache-Control": "no-cache"},
        )

    @app.api_route(
        "/{full_path:path}",
        methods=["GET", "HEAD"],
        include_in_schema=False,
    )
    async def spa_fallback(full_path: str):
        """SPA 路由回退 + 根级静态资源服务。

        - 若文件在静态目录中存在（如 favicon.svg、robots.txt），直接返回文件；
        - 否则视为 SPA 前端路由（如 /media/123、/settings），返回 index.html。

        API 路由与 /assets 挂载已在上方匹配，此处不会被误命中。
        """
        candidate = os.path.abspath(os.path.join(_STATIC_DIR, full_path))
        # 安全：防止路径穿越
        if candidate.startswith(_STATIC_DIR) and os.path.isfile(candidate):
            # 根级静态资源（favicon 等）短缓存即可
            return FileResponse(
                candidate, headers={"Cache-Control": "public, max-age=86400"}
            )
        return FileResponse(
            os.path.join(_STATIC_DIR, "index.html"),
            headers={"Cache-Control": "no-cache"},
        )


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "version": config.app.version}


_LLM_DOC_PATH = os.path.join(os.path.dirname(__file__), "llm_agent_doc.md")


def _load_llm_doc() -> str:
    """加载 Agent API 文档；文件缺失时返回占位提示。"""
    try:
        with open(_LLM_DOC_PATH, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return "# Media Library Agent API Guide\n\n文档加载失败，请稍后重试。\n"


_LLM_TXT_CONTENT = _load_llm_doc()


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
