"""File API - 文件相关接口"""

import hashlib
import os
import random
import logging
import time
from logging.handlers import RotatingFileHandler
from urllib.parse import quote
import diskcache

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from database.models import File, FileLink, FileType
from database.core import get_db_session
from app.api.deps import get_user_id, get_user_id_from_token
from app.schemas.media import FileInfoDetail
from config import config

logger = logging.getLogger(__name__)

# 独立的 file_data 追踪日志
_file_data_log_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data", "log", "file_data.log"
)
os.makedirs(os.path.dirname(_file_data_log_path), exist_ok=True)
_file_data_logger = logging.getLogger("file_data.trace")
_file_data_logger.setLevel(logging.DEBUG)
_file_data_logger.propagate = False

class _FileIDFilter(logging.Filter):
    """自动注入 file_id，缺失时默认为 '-'"""
    def filter(self, record):
        if not hasattr(record, 'file_id'):
            record.file_id = '-'
        return True

_handler = RotatingFileHandler(_file_data_log_path, maxBytes=50 * 1024 * 1024, backupCount=3, encoding="utf-8")
_handler.setFormatter(logging.Formatter(
    "[%(asctime)s.%(msecs)03d] [%(levelname)s] [file_id=%(file_id)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))
_handler.addFilter(_FileIDFilter())
_file_data_logger.addHandler(_handler)

_cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "cache", "file_url")
os.makedirs(_cache_dir, exist_ok=True)
_url_cache = diskcache.Cache(_cache_dir)

_http_client: httpx.AsyncClient | None = None

def get_http_client() -> httpx.AsyncClient:
    """获取或创建全局 HTTP 客户端（连接复用）"""
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
        )
    return _http_client

async def close_http_client() -> None:
    """关闭全局 HTTP 客户端"""
    global _http_client
    if _http_client is not None:
        await _http_client.aclose()
        _http_client = None

router = APIRouter(prefix="/api/file", tags=["文件"])


async def get_webdav_redirect_url(file_path: str) -> str:
    # 对路径分段做 URL 编码，避免文件名中的 ? # & % 等字符破坏请求路径/查询
    encoded_prefix = quote(config.cloud_auth.prefix, safe="/ ")
    encoded_path = quote(file_path, safe="/ ")
    url = f'https://webdav.123pan.cn/webdav{encoded_prefix}/{encoded_path}'
    headers = {"Authorization": f"Basic {config.cloud_auth.basic_auth_token}"}
    client = get_http_client()
    response = await client.request("GET", url, headers=headers, follow_redirects=False)
    if response.status_code == 302:
        return response.headers.get("Location")
    raise Exception(f"WebDAV 路径 {file_path} 未返回重定向, status: {response.status_code}")


def _get_url_expire(url: str) -> float:
    """从 URL 参数 t 获取过期时间戳"""
    from urllib.parse import urlparse, parse_qs
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    expire_ts = params.get('t', ['0'])[0]
    return int(expire_ts)


def _cache_url(url: str, file_id: int) -> None:
    """缓存 URL，计算过期时间并存储"""
    from time import time
    expire_ts = _get_url_expire(url)
    expire_seconds = max(expire_ts - time() - 60, 60)
    _url_cache.set(f"file_url_{file_id}", url, expire=int(expire_seconds))


@router.get("/info", response_model=FileInfoDetail)
async def get_file_info(
    file_id: int = Query(..., description="文件ID"),
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    result = await db.execute(
        select(File, FileLink).join(FileLink, FileLink.FileId == File.Id).where(File.Id == file_id)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="文件不存在")
    file, file_link = row
    return FileInfoDetail(
        id=file.Id,
        name=file.Name,
        path=file.Path,
        type=file.Type.value if file.Type else None,
        item_id=file_link.ItemId,
        image_type=file_link.ImageType.value if file_link.ImageType else None,
        image_index=file_link.ImageIndex,
        size=file.Size,
        etag=file.Etag,
        ffmpeg=file.FFmpeg,
    )


@router.get("/data")
async def get_file_data(
    file_id: int = Query(..., description="文件ID"),
    user_id: int = Depends(get_user_id_from_token),
    db: AsyncSession = Depends(get_db_session),
):
    _trace = _file_data_logger
    _trace.info("=== START ===", extra={'file_id': file_id})

    cache_key = f"file_url_{file_id}"

    # STEP 1: 先查缓存（跳过 DB）
    t0 = time.perf_counter()
    redirect_url = _url_cache.get(cache_key)
    t1 = time.perf_counter()
    _trace.info(f"STEP 1/3: 查缓存 | 耗时={t1 - t0:.3f}s | 结果={'HIT' if redirect_url else 'MISS'}", extra={'file_id': file_id})

    if not redirect_url:
        # STEP 2: 缓存未命中，查 DB 获取 file_path
        t2 = time.perf_counter()
        result = await db.execute(select(File).where(File.Id == file_id))
        file = result.scalar_one_or_none()
        t3 = time.perf_counter()
        _trace.info(f"STEP 2/3: 数据库查询 | 耗时={t3 - t2:.3f}s | 结果={'FOUND' if file else 'NOT_FOUND'}", extra={'file_id': file_id})

        if not file:
            _trace.warning("→ 退出: 文件不存在", extra={'file_id': file_id})
            raise HTTPException(status_code=404, detail="文件不存在")

        file_path = file.Path
        _trace.info(f"  Path={file_path}", extra={'file_id': file_id})

        # STEP 3: 请求 WebDAV
        if config.cloud_auth.username:
            _trace.info(f"STEP 3/3: 请求 WebDAV | username={config.cloud_auth.username[:4]}**", extra={'file_id': file_id})
            t4 = time.perf_counter()
            try:
                redirect_url = await get_webdav_redirect_url(file_path)
                t5 = time.perf_counter()
                _trace.info(f"  WebDAV 响应耗时={t5 - t4:.3f}s | 结果={'SUCCESS' if redirect_url else 'EMPTY'}", extra={'file_id': file_id})
                if redirect_url:
                    _cache_url(redirect_url, file_id)
                    _trace.info(f"  URL 已写入缓存", extra={'file_id': file_id})
            except Exception as e:
                t5 = time.perf_counter()
                _trace.warning(f"  WebDAV 请求失败 | 耗时={t5 - t4:.3f}s | 错误={e}", extra={'file_id': file_id})

        if not redirect_url:
            if file.Type == FileType.Video:
                _trace.info("→ 无可用 URL, 使用视频降级地址", extra={'file_id': file_id})
                redirect_url = "https://v.lcc8.com/sv/video.php"
            else:
                # 降级随机图
                _trace.info("→ 无可用 URL, 使用随机降级图片", extra={'file_id': file_id})
                redirect_url = random.choice([
                    "https://api.r10086.com/桜道随机图片api接口.php?图片系列=少女写真1",
                    "https://cdn.seovx.com/?mom=302",
                    "https://www.dmoe.cc/random.php",
                ])
    else:
        _trace.info("→ 缓存命中, 跳过 DB+WebDAV", extra={'file_id': file_id})

    _trace.info(f"=== END === | 最终URL={redirect_url}", extra={'file_id': file_id})
    return RedirectResponse(url=redirect_url)
 
