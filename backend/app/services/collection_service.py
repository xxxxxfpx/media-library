"""
CollectionService - 苹果CMS采集服务
======================================

管理采集源CRUD、执行采集任务、APScheduler定时调度。

核心流程：
1. 为每个采集源创建/查找 MediaType.Source 的 MediaItem 作为来源锚点
2. 增量采集：计算 h 参数（基于上次成功采集时间）
3. 拉取列表 → 批量获取详情 → 解析播放地址
4. 去重入库：(SourceItemId, SourceId, Type) 唯一索引
5. 创建 File + FileLink 关联封面和播放源
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import (
    CollectionLog,
    CollectionSource,
    File,
    FileLink,
    FileLinkType,
    FileType,
    ImageType,
    MediaItem,
    MediaType,
)

from .maccms_client import MaccmsClient, MaccmsError

logger = logging.getLogger(__name__)

# 全局APScheduler实例（懒加载）
_scheduler = None


# ======================================================================
# CRUD 操作
# ======================================================================

async def list_sources(db: AsyncSession) -> list[dict[str, Any]]:
    """获取所有采集源列表"""
    result = await db.execute(
        select(CollectionSource).order_by(CollectionSource.Id.desc())
    )
    sources = result.scalars().all()
    return [_source_to_dict(s) for s in sources]


async def get_source(db: AsyncSession, source_id: int) -> dict[str, Any] | None:
    """获取单个采集源"""
    result = await db.execute(
        select(CollectionSource).where(CollectionSource.Id == source_id)
    )
    source = result.scalar_one_or_none()
    return _source_to_dict(source) if source else None


async def create_source(
    db: AsyncSession,
    name: str,
    base_url: str,
    auto_collect: bool = False,
    interval_minutes: int = 60,
    enabled: bool = True,
    sort_order: str = "time",
) -> dict[str, Any]:
    """创建采集源（同时创建/查找对应的 Source 类型 MediaItem）"""
    # 创建 Source 类型锚点
    await _ensure_source_anchor(db, name)

    cs = CollectionSource(
        Name=name,
        BaseUrl=base_url,
        Enabled=enabled,
        AutoCollect=auto_collect,
        IntervalMinutes=interval_minutes,
        SortOrder=sort_order,
    )
    db.add(cs)
    await db.commit()
    await db.refresh(cs)

    # 如果开启了自动采集，注册调度器任务
    if auto_collect and enabled:
        _add_scheduler_job(cs)

    return _source_to_dict(cs)


async def update_source(
    db: AsyncSession,
    source_id: int,
    **kwargs: Any,
) -> dict[str, Any]:
    """更新采集源配置"""
    result = await db.execute(
        select(CollectionSource).where(CollectionSource.Id == source_id)
    )
    cs = result.scalar_one_or_none()
    if not cs:
        raise ValueError(f"采集源不存在: id={source_id}")

    for key in ("Name", "BaseUrl", "Enabled", "AutoCollect", "IntervalMinutes", "SortOrder"):
        if key in kwargs:
            setattr(cs, key, kwargs[key])

    cs.UpdatedAt = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(cs)

    # 同步调度器
    _sync_scheduler_job(cs)

    return _source_to_dict(cs)


async def delete_source(db: AsyncSession, source_id: int) -> None:
    """删除采集源（同时移除调度器任务）"""
    result = await db.execute(
        select(CollectionSource).where(CollectionSource.Id == source_id)
    )
    cs = result.scalar_one_or_none()
    if not cs:
        raise ValueError(f"采集源不存在: id={source_id}")

    # 移除调度器任务
    _remove_scheduler_job(source_id)

    await db.delete(cs)
    await db.commit()


async def test_source(db: AsyncSession, source_id: int) -> dict[str, Any]:
    """测试采集源连通性"""
    result = await db.execute(
        select(CollectionSource).where(CollectionSource.Id == source_id)
    )
    cs = result.scalar_one_or_none()
    if not cs:
        raise ValueError(f"采集源不存在: id={source_id}")

    client = MaccmsClient(cs.BaseUrl)
    try:
        info = client.test_connection()
        # 更新状态
        cs.LastStatus = "success"
        cs.LastError = None
        cs.UpdatedAt = datetime.now(timezone.utc)
        await db.commit()
        return info
    except MaccmsError as e:
        cs.LastStatus = "failed"
        cs.LastError = str(e)
        cs.UpdatedAt = datetime.now(timezone.utc)
        await db.commit()
        raise


# ======================================================================
# 采集执行
# ======================================================================

async def trigger_collect(
    db: AsyncSession,
    source_id: int,
    trigger_type: str = "manual",
) -> dict[str, Any]:
    """触发一次采集（手动或自动）。

    如果采集源正在运行中（LastStatus=running），则拒绝触发。

    Args:
        db: 数据库会话
        source_id: 采集源ID
        trigger_type: auto/manual

    Returns:
        {"log_id": int, "status": str}
    """
    result = await db.execute(
        select(CollectionSource).where(CollectionSource.Id == source_id)
    )
    cs = result.scalar_one_or_none()
    if not cs:
        raise ValueError(f"采集源不存在: id={source_id}")

    # 工作状态检查：防止重复触发
    if cs.LastStatus == "running":
        raise ValueError("采集源正在运行中，请等待完成后再触发")

    # 创建日志
    log = CollectionLog(
        SourceId=source_id,
        TriggerType=trigger_type,
        Status="running",
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)

    # 更新采集源状态
    cs.LastStatus = "running"
    cs.LastError = None
    cs.UpdatedAt = datetime.now(timezone.utc)
    await db.commit()

    # 后台执行采集
    import asyncio
    asyncio.create_task(_run_collected(source_id, log.Id))

    return {"log_id": log.Id, "status": "running"}


async def _run_collected(source_id: int, log_id: int) -> None:
    """实际采集执行（在后台任务中运行，同步HTTP请求放入线程池）"""
    import asyncio

    from database.core import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                select(CollectionSource).where(CollectionSource.Id == source_id)
            )
            cs = result.scalar_one_or_none()
            log_result = await db.execute(
                select(CollectionLog).where(CollectionLog.Id == log_id)
            )
            log = log_result.scalar_one_or_none()

            if not cs or not log:
                return

            # 计算增量 h 参数
            h = None
            if cs.LastCollectedAt:
                last = cs.LastCollectedAt
                if last.tzinfo is None:
                    last = last.replace(tzinfo=timezone.utc)
                delta = datetime.now(timezone.utc) - last
                h = max(1, int(delta.total_seconds() / 3600) + 1)  # +1h 冗余

            # 在线程池中执行阻塞的HTTP请求
            loop = asyncio.get_running_loop()
            vod_details, total_fetched, max_item_id = await loop.run_in_executor(
                None, _do_collect_sync, str(cs.BaseUrl), h, cs.SortOrder, cs.LastMaxItemId
            )

            # 入库在异步上下文执行
            source_anchor = await _ensure_source_anchor(db, cs.Name)

            new_count = 0
            update_count = 0
            error_count = 0
            progress_max_id = cs.LastMaxItemId
            progress_checkpoint = 0  # 每50条更新一次进度

            for vod in vod_details:
                try:
                    result = await _upsert_vod(db, source_anchor.Id, vod)
                    if result == "new":
                        new_count += 1
                    elif result == "update":
                        update_count += 1

                    # 实时更新进度：每50条或每批更新 LastMaxItemId
                    vid = vod.get("vod_id", 0)
                    if vid and vid > progress_max_id:
                        progress_max_id = vid
                    progress_checkpoint += 1

                    if progress_checkpoint >= 50:
                        cs.LastMaxItemId = progress_max_id
                        cs.UpdatedAt = datetime.now(timezone.utc)
                        log.TotalFetched = progress_checkpoint
                        await db.commit()
                        progress_checkpoint = 0

                except Exception:
                    error_count += 1
                    logger.warning("入库失败 vod_id=%s", vod.get("vod_id"), exc_info=True)

            # 最终状态更新
            log.Status = "success"
            log.FinishedAt = datetime.now(timezone.utc)
            log.NewCount = new_count
            log.UpdateCount = update_count
            log.ErrorCount = error_count
            log.TotalFetched = total_fetched
            log.UpdatedAt = datetime.now(timezone.utc)

            cs.LastCollectedAt = datetime.now(timezone.utc)
            cs.LastStatus = "success"
            cs.LastError = None
            if max_item_id > cs.LastMaxItemId:
                cs.LastMaxItemId = max_item_id
            cs.UpdatedAt = datetime.now(timezone.utc)
            await db.commit()

        except Exception as e:
            logger.exception("采集失败 source_id=%s", source_id)
            async with AsyncSessionLocal() as db2:
                log_result2 = await db2.execute(
                    select(CollectionLog).where(CollectionLog.Id == log_id)
                )
                log2 = log_result2.scalar_one_or_none()
                if log2:
                    log2.Status = "failed"
                    log2.FinishedAt = datetime.now(timezone.utc)
                    log2.ErrorMessage = str(e)
                    log2.UpdatedAt = datetime.now(timezone.utc)

                cs_result2 = await db2.execute(
                    select(CollectionSource).where(CollectionSource.Id == source_id)
                )
                cs2 = cs_result2.scalar_one_or_none()
                if cs2:
                    cs2.LastStatus = "failed"
                    cs2.LastError = str(e)
                    cs2.UpdatedAt = datetime.now(timezone.utc)
                await db2.commit()


def _do_collect_sync(
    base_url: str,
    h: int | None,
    order: str | None = None,
    last_max_item_id: int = 0,
) -> tuple[list[dict[str, Any]], int, int]:
    """同步抓取苹果CMS数据（在线程池中执行，避免阻塞事件循环）。

    统一使用 iter_by_id_range 按 ID 范围遍历：
    - 全量采集（last_max_item_id=0）：从 ID=1 开始遍历到当前最大值
    - 增量采集（last_max_item_id>0）：从 last_max_item_id+1 开始遍历到当前最大值

    优势：
    - 不依赖分页顺序，稳定可靠
    - 可断点续传
    - 直接获取完整详情，无需二次请求

    Args:
        base_url: 采集源API基础URL
        h: 增量小时数（保留参数）
        order: 排序方式（保留参数）
        last_max_item_id: 上次遍历到的最大vod_id（游标）

    Returns:
        (vod_details_list, total_fetched_count, max_item_id_seen)
    """
    client = MaccmsClient(base_url)
    total_fetched = 0
    max_item_id = last_max_item_id

    try:
        start_id = last_max_item_id + 1
        if last_max_item_id == 0:
            logger.info("全量采集: 使用ID范围遍历, start_id=1")
        else:
            logger.info("增量采集: start_id=%s", start_id)

        details: list[dict[str, Any]] = []
        for item in client.iter_by_id_range(start_id=start_id):
            total_fetched += 1
            vid = item.get("vod_id", 0)
            if vid > max_item_id:
                max_item_id = vid
            details.append(item)

        logger.info("采集完成: 获取%s条, 最大ID=%s", total_fetched, max_item_id)
        return details, total_fetched, max_item_id

    finally:
        client.close()


async def _upsert_vod(
    db: AsyncSession,
    source_item_id: int,
    vod: dict[str, Any],
) -> str:
    """新增或更新一条视频数据。

    Returns:
        "new" / "update"
    """
    vod_id = str(vod.get("vod_id", ""))
    if not vod_id:
        return "skip"

    # 去重查找
    result = await db.execute(
        select(MediaItem).where(
            MediaItem.SourceItemId == source_item_id,
            MediaItem.SourceId == vod_id,
            MediaItem.Type == MediaType.Movie,
            not MediaItem.IsDeleted,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        # 更新现有
        created_time = _parse_vod_date(vod.get("vod_time"))
        if created_time and existing.StartDate and created_time > existing.StartDate:
            # 内容有更新才更新
            existing.Name = vod.get("vod_name") or existing.Name
            existing.Overview = _strip_html(vod.get("vod_content", "")) or existing.Overview
            if vod.get("vod_remarks"):
                existing.Tagline = vod["vod_remarks"]
            if vod.get("vod_score"):
                try:
                    score = float(vod["vod_score"])
                    if 0 <= score <= 10:
                        existing.CommunityRating = score
                except (ValueError, TypeError):
                    pass
            existing.UpdatedAt = datetime.now(timezone.utc)
            await _sync_files(db, existing.Id, vod)
            return "update"
        return "skip"
    else:
        # 创建新
        name = vod.get("vod_name", "")
        if not name:
            return "skip"

        overview = _strip_html(vod.get("vod_content", ""))
        year = vod.get("vod_year", "")
        start_date = None
        if year and year.isdigit():
            start_date = datetime(int(year), 1, 1, tzinfo=timezone.utc)

        community_rating = None
        if vod.get("vod_score"):
            try:
                score = float(vod["vod_score"])
                if 0 <= score <= 10:
                    community_rating = score
            except (ValueError, TypeError):
                pass

        item = MediaItem(
            Type=MediaType.Movie,
            Name=name,
            Overview=overview or None,
            Tagline=vod.get("vod_remarks") or None,
            StartDate=start_date,
            CommunityRating=community_rating,
            SourceItemId=source_item_id,
            SourceId=vod_id,
        )
        db.add(item)
        await db.flush()

        # 创建封面
        vod_pic = vod.get("vod_pic", "")
        if vod_pic:
            await _ensure_file_link(db, item.Id, vod_pic, FileType.Image, FileLinkType.Image, ImageType.Primary, name or "cover")

        # 创建播放源
        play_urls = _parse_play_urls(vod)
        for src in play_urls:
            for ep in src.get("episodes", []):
                await _ensure_file_link(db, item.Id, ep["url"], FileType.Video, FileLinkType.MediaSource, None, ep.get("name", "") or "video")

        await db.commit()
        return "new"


async def _sync_files(db: AsyncSession, item_id: int, vod: dict[str, Any]) -> None:
    """同步视频的文件关联（更新时刷新）"""
    # 封面
    vod_pic = vod.get("vod_pic", "")
    if vod_pic:
        await _ensure_file_link(db, item_id, vod_pic, FileType.Image, FileLinkType.Image, ImageType.Primary, vod.get("vod_name", "") or "cover")

    # 播放源
    play_urls = _parse_play_urls(vod)
    for src in play_urls:
        for ep in src.get("episodes", []):
            await _ensure_file_link(db, item_id, ep["url"], FileType.Video, FileLinkType.MediaSource, None, ep.get("name", "") or "video")


async def _ensure_file_link(
    db: AsyncSession,
    item_id: int,
    url: str,
    file_type: FileType,
    link_type: FileLinkType,
    image_type: ImageType | None,
    name: str,
) -> None:
    """确保 File 和 FileLink 存在（基于 Path 去重）"""
    # 查找或创建 File
    result = await db.execute(select(File).where(File.Path == url))
    f = result.scalar_one_or_none()
    if not f:
        f = File(
            Name=name,
            Path=url,
            Type=file_type,
        )
        db.add(f)
        await db.flush()

    # 查找或创建 FileLink
    link_q = select(FileLink).where(
        FileLink.ItemId == item_id,
        FileLink.FileId == f.Id,
        FileLink.LinkType == link_type,
    )
    if image_type:
        link_q = link_q.where(FileLink.ImageType == image_type)
    result2 = await db.execute(link_q)
    existing_link = result2.scalar_one_or_none()

    if not existing_link:
        link = FileLink(
            ItemId=item_id,
            FileId=f.Id,
            LinkType=link_type,
            ImageType=image_type,
        )
        db.add(link)


async def _ensure_source_anchor(db: AsyncSession, name: str) -> MediaItem:
    """确保 MediaType.Source 的锚点 MediaItem 存在"""
    result = await db.execute(
        select(MediaItem).where(
            MediaItem.Name == name,
            MediaItem.Type == MediaType.Source,
            not MediaItem.IsDeleted,
        )
    )
    anchor = result.scalar_one_or_none()
    if not anchor:
        anchor = MediaItem(Type=MediaType.Source, Name=name)
        db.add(anchor)
        await db.flush()
    return anchor


# ======================================================================
# 日志查询
# ======================================================================

async def list_logs(
    db: AsyncSession,
    source_id: int | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """获取采集日志列表"""
    query = select(CollectionLog)
    if source_id:
        query = query.where(CollectionLog.SourceId == source_id)
    query = query.order_by(CollectionLog.StartedAt.desc()).limit(limit)
    result = await db.execute(query)
    logs = result.scalars().all()
    return [_log_to_dict(log) for log in logs]


# ======================================================================
# 调度器管理
# ======================================================================

def start_scheduler() -> None:
    """启动 APScheduler 并注册所有自动采集任务"""
    global _scheduler
    if _scheduler is not None and _scheduler.running:
        return

    try:
        from apscheduler.jobstores.memory import MemoryJobStore
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
    except ImportError as e:
        logger.warning("APScheduler 未安装，定时采集功能不可用: %s", e)
        return

    _scheduler = AsyncIOScheduler(
        jobstores={"default": MemoryJobStore()},
        # 使用 datetime.timezone.utc 对象，避免 Docker slim 镜像中 zoneinfo 缺数据
        timezone=timezone.utc,
    )
    _scheduler.start()
    logger.info("采集调度器已启动")

    # 从数据库加载所有启用自动采集的源
    import asyncio
    asyncio.create_task(_load_auto_jobs())


async def _load_auto_jobs() -> None:
    """从数据库加载所有自动采集源并注册调度任务"""
    global _scheduler
    if _scheduler is None:
        return
    try:
        from database.core import AsyncSessionLocal
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(CollectionSource).where(
                    CollectionSource.Enabled,
                    CollectionSource.AutoCollect,
                )
            )
            sources = result.scalars().all()
            for cs in sources:
                _add_scheduler_job(cs)
            logger.info("已加载 %d 个自动采集源", len(sources))
    except Exception:
        logger.exception("加载自动采集任务失败")


def stop_scheduler() -> None:
    """停止 APScheduler"""
    global _scheduler
    if _scheduler is not None and _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("采集调度器已停止")
    _scheduler = None


def _add_scheduler_job(cs: CollectionSource) -> None:
    """为采集源注册定时任务"""
    global _scheduler
    if _scheduler is None or not _scheduler.running:
        return
    if not cs.Enabled or not cs.AutoCollect:
        return

    job_id = f"collect_{cs.Id}"
    # 移除已存在的同ID任务
    try:
        _scheduler.remove_job(job_id)
    except Exception:
        pass

    interval = max(1, cs.IntervalMinutes)
    _scheduler.add_job(
        _auto_collect_task,
        "interval",
        minutes=interval,
        id=job_id,
        replace_existing=True,
        kwargs={"source_id": cs.Id},
    )
    logger.info("已注册自动采集任务: source=%s(%s) interval=%dm", cs.Id, cs.Name, interval)


def _remove_scheduler_job(source_id: int) -> None:
    """移除采集源的定时任务"""
    global _scheduler
    if _scheduler is None:
        return
    job_id = f"collect_{source_id}"
    try:
        _scheduler.remove_job(job_id)
    except Exception:
        pass


def _sync_scheduler_job(cs: CollectionSource) -> None:
    """根据采集源状态同步调度任务"""
    if cs.Enabled and cs.AutoCollect:
        _add_scheduler_job(cs)
    else:
        _remove_scheduler_job(cs.Id)


async def _auto_collect_task(source_id: int) -> None:
    """APScheduler 回调：自动触发采集"""
    from database.core import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        try:
            await trigger_collect(db, source_id, trigger_type="auto")
        except Exception:
            logger.exception("自动采集失败 source_id=%s", source_id)


# ======================================================================
# 工具函数
# ======================================================================

def _source_to_dict(cs: CollectionSource) -> dict[str, Any]:
    return {
        "id": cs.Id,
        "name": cs.Name,
        "base_url": cs.BaseUrl,
        "enabled": cs.Enabled,
        "auto_collect": cs.AutoCollect,
        "interval_minutes": cs.IntervalMinutes,
        "sort_order": cs.SortOrder,
        "last_max_item_id": cs.LastMaxItemId,
        "last_collected_at": cs.LastCollectedAt.isoformat() if cs.LastCollectedAt else None,
        "last_status": cs.LastStatus,
        "last_error": cs.LastError,
        "created_at": cs.CreatedAt.isoformat() if cs.CreatedAt else None,
        "updated_at": cs.UpdatedAt.isoformat() if cs.UpdatedAt else None,
    }


def _log_to_dict(log: CollectionLog) -> dict[str, Any]:
    return {
        "id": log.Id,
        "source_id": log.SourceId,
        "trigger_type": log.TriggerType,
        "started_at": log.StartedAt.isoformat() if log.StartedAt else None,
        "finished_at": log.FinishedAt.isoformat() if log.FinishedAt else None,
        "status": log.Status,
        "new_count": log.NewCount,
        "update_count": log.UpdateCount,
        "error_count": log.ErrorCount,
        "total_fetched": log.TotalFetched,
        "error_message": log.ErrorMessage,
        "details": log.Details,
        "created_at": log.CreatedAt.isoformat() if log.CreatedAt else None,
    }


def _strip_html(text: str) -> str:
    """移除HTML标签"""
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text).strip()


def _parse_vod_date(date_str: str | None) -> datetime | None:
    """解析苹果CMS的 vod_time 字段（格式：2024-01-01 12:00:00）"""
    if not date_str:
        return None
    try:
        # 尝试解析 "2024-01-01 12:00:00"
        from datetime import datetime as dt
        dt_obj = dt.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt_obj.replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    try:
        # 尝试只有日期
        from datetime import datetime as dt
        dt_obj = dt.strptime(date_str, "%Y-%m-%d")
        return dt_obj.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _parse_play_urls(vod: dict[str, Any]) -> list[dict[str, Any]]:
    """解析播放地址（复用 MaccmsClient 逻辑但不实例化HTTP连接）"""
    play_from = vod.get("vod_play_from", "")
    play_url = vod.get("vod_play_url", "")
    if not play_from or not play_url:
        return []

    sources = play_from.split("$$$")
    urls = play_url.split("$$$")

    result: list[dict[str, Any]] = []
    for src, url_str in zip(sources, urls):
        episodes: list[dict[str, str]] = []
        for item in url_str.split("#"):
            if "$" in item:
                name, url = item.split("$", 1)
                episodes.append({"name": name.strip(), "url": url.strip()})
            else:
                episodes.append({"name": "", "url": item.strip()})
        result.append({"source": src, "episodes": episodes})
    return result
