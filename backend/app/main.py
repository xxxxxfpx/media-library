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


_LLM_TXT_CONTENT = """# Media Library Agent API Guide

## 概述

本系统是一个媒体库管理平台，支持从网页爬取视频、图片、简介等信息并入库。
作为 Agent，你的任务是：访问用户提供的 URL，提取媒体信息，通过本 API 入库。

## 认证

API 使用 Bearer Token 认证。先调用 `POST /api/user/login` 获取 access_token。
将 token 放入 `Authorization: Bearer <token>` 请求头。

```bash
# Step 1: 登录获取 token
curl -X POST http://localhost:8000/api/user/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "admin", "password": "your_password"}'
# 返回 {"access_token": "eyJ...", "token_type": "bearer"}

# Step 2: 带 token 访问 API
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/media/list
```

## Agent 数据规范

Agent 入库的媒体项统一使用以下规范：

| 字段 | 值 | 说明 |
|------|-----|------|
| source_name | "Agent" | 固定值，标识为 Agent 来源 |
| source_id | tag 名 | 如 "户外"、"美食"，作为唯一标识 |
| source_link | 原始网页 URL | 媒体来源页面地址 |

所有 Agent 来源的媒体项都归入 `source_name = "Agent"` 的 Source 分组，
通过 `source_id`（即 tag 名）区分不同分类。

## 媒体类型

创建时使用 `type` 字段指定类型：

- `Movie` — 电影
- `Series` — 系列
- `Episode` — 剧集
- `Season` — 季
- `BoxSet` — 合集
- `Genre` — 类型/流派
- `Tag` — 标签
- `Person` — 人物
- `Studio` — 工作室
- `Source` — 来源

## 1. 创建媒体项（核心接口）

`POST /api/media/batch`

这是主要的入库接口。一次请求可批量创建媒体项、文件、关联关系。

### 请求体结构

```json
{
  "source_name": "Agent",
  "items": [
    {
      "temp_id": "item-1",
      "source_info": {
        "source_id": "户外",
        "source_link": "https://example.com/video/123"
      },
      "attrs": {
        "type": "Movie",
        "name": "视频标题",
        "overview": "视频简介描述...",
        "tagline": "宣传标语（可选）",
        "premiere_date": "2024-01-01T00:00:00Z",
        "community_rating": 8.5
      }
    }
  ],
  "files": [
    {
      "temp_id": "file-1",
      "attrs": {
        "name": "video.mp4",
        "path": "/path/to/video",
        "url": "https://cdn.example.com/video.mp4",
        "provider": "guan",
        "type": "Video",
        "size": 123456789
      }
    }
  ],
  "item_links": [],
  "file_links": [
    {
      "item": "item-1",
      "file": "file-1",
      "link_type": "MediaSource"
    }
  ]
}
```

### 字段说明

**source_info.source_id** — Agent 使用 tag 名作为 ID，如 "户外"、"科技"。
用于去重，相同 source_name + source_id + type 的项不会重复创建。

**attrs 字段**：
- `name` (string) — 媒体名称（必填）
- `overview` (string) — 简介
- `tagline` (string) — 标语
- `premiere_date` (ISO 8601) — 发布日期
- `community_rating` (float 0-10) — 社区评分
- `type` (enum) — 媒体类型（必填）

**file_links.link_type**：
- `MediaSource` — 媒体源文件
- `Image` — 图片文件
- `Chapter` — 章节文件

## 2. 上传图片到云盘（处理加密图片）

`POST /api/drives/guangyapan/upload-bytes`

当图片 URL 是密文/加密内容，无法直接下载时，使用此接口。
先通过浏览器工具提取图片的 base64 数据，再提交上传。

### 请求体

```json
{
  "file_data": "base64编码的图片数据...",
  "name": "image.jpg",
  "parent_id": ""
}
```

### 响应

```json
{
  "id": 1,
  "provider": "guangyapan",
  "provider_file_id": "xxx",
  "url": "https://...可播放URL...",
  "mode": "upload",
  "name": "image.jpg",
  "size": 12345,
  "status": "ready"
}
```

上传成功后，将返回的 `url` 填入媒体项的 `files[].attrs.url` 字段即可。

## 3. 离线下载 URL（m3u8/mp4）

`POST /api/drives/guangyapan/offline/create`

对于公开可访问的视频 URL（m3u8、mp4），可直接提交离线下载任务：

```json
{
  "url": "https://example.com/video.m3u8",
  "parent_id": "",
  "name": "video.mp4"
}
```

## 4. 查询已有媒体

`GET /api/media/list?search=关键词&limit=50`

`GET /api/media/info?id=123`

`GET /api/media/stats`

## 完整示例：Agent 爬取流程

```bash
# Step 1: 登录获取 token
curl -X POST http://localhost:8000/api/user/login \\
  -d '{"username":"admin","password":"xxx"}'
# 记下返回的 access_token

# Step 2: 上传图片（如果图片是加密的）
curl -H "Authorization: Bearer <token>" -X POST http://localhost:8000/api/drives/guangyapan/upload-bytes \\
  -d '{"file_data":"<base64>","name":"cover.jpg"}'
# 记下返回的 url

# Step 3: 创建媒体项
curl -H "Authorization: Bearer <token>" -X POST http://localhost:8000/api/media/batch \\
  -H "Content-Type: application/json" \\
  -d '{
    "source_name": "Agent",
    "items": [{
      "temp_id": "item-1",
      "source_info": {"source_id": "户外", "source_link": "https://example.com/video"},
      "attrs": {"type": "Movie", "name": "视频标题", "overview": "简介..."}
    }],
    "files": [{
      "temp_id": "file-1",
      "attrs": {"name": "cover.jpg", "url": "上传返回的url", "type": "Image", "provider": "guangyapan"}
    }],
    "file_links": [{"item": "item-1", "file": "file-1", "link_type": "Image", "image_type": "Primary"}]
  }'
```

## 注意事项

1. 所有 Agent 来源的媒体统一使用 `source_name: "Agent"`
2. `source_id` 使用 tag 名（如 "户外"），便于分类和去重
3. `source_link` 保存原始网页 URL
4. 图片文件使用 `link_type: "Image"` + `image_type: "Primary"` 标记封面
5. 视频文件使用 `link_type: "MediaSource"`
6. base64 图片上传上限 50MB
7. 媒体创建接口需要管理员权限
8. 不要提交广告/营销信息，只提取核心内容
"""


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
