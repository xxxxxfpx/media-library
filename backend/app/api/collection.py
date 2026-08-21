"""采集管理 API - 苹果CMS V10 采集源配置与采集执行"""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_admin_id, get_db_session
from app.services import collection_service
from app.services.maccms_client import MaccmsError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/collection", tags=["collection"])


# ======================================================================
# 请求/响应模型
# ======================================================================

class SourceCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="采集源名称")
    base_url: str = Field(..., min_length=1, max_length=500, description="API基础URL")
    auto_collect: bool = Field(default=False, description="自动轮询采集开关")
    interval_minutes: int = Field(default=60, ge=1, le=10080, description="轮询间隔(分钟)")
    sort_order: str = Field(default="time", description="排序方式: time/id/hits")
    enabled: bool = Field(default=True, description="是否启用")


class SourceUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    base_url: str | None = Field(None, min_length=1, max_length=500)
    auto_collect: bool | None = None
    interval_minutes: int | None = Field(None, ge=1, le=10080)
    sort_order: str | None = None
    enabled: bool | None = None


class SourceToggleRequest(BaseModel):
    enabled: bool | None = None
    auto_collect: bool | None = None


class TriggerCollectRequest(BaseModel):
    """触发采集请求"""
    max_items: int | None = Field(default=None, ge=1, le=10000, description="最大采集数量，None表示全量")


# ======================================================================
# 路由
# ======================================================================

@router.get("/sources")
async def list_sources(
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> list[dict[str, Any]]:
    """获取所有采集源列表"""
    try:
        return await collection_service.list_sources(db)
    except Exception as e:
        logger.exception("获取采集源列表失败")
        raise HTTPException(status_code=500, detail=f"获取采集源列表失败: {str(e)}")


@router.post("/sources")
async def create_source(
    data: SourceCreateRequest,
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """创建采集源"""
    return await collection_service.create_source(
        db,
        name=data.name,
        base_url=data.base_url,
        auto_collect=data.auto_collect,
        interval_minutes=data.interval_minutes,
        sort_order=data.sort_order,
        enabled=data.enabled,
    )


@router.get("/sources/{source_id}")
async def get_source(
    source_id: int,
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """获取单个采集源详情"""
    result = await collection_service.get_source(db, source_id)
    if not result:
        raise HTTPException(status_code=404, detail="采集源不存在")
    return result


@router.put("/sources/{source_id}")
async def update_source(
    source_id: int,
    data: SourceUpdateRequest,
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """更新采集源配置"""
    kwargs = data.model_dump(exclude_unset=True)
    # 将字段名映射到 ORM 字段名
    field_map = {
        "name": "Name",
        "base_url": "BaseUrl",
        "enabled": "Enabled",
        "auto_collect": "AutoCollect",
        "interval_minutes": "IntervalMinutes",
        "sort_order": "SortOrder",
    }
    orm_kwargs = {field_map[k]: v for k, v in kwargs.items() if k in field_map}
    try:
        return await collection_service.update_source(db, source_id, **orm_kwargs)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/sources/{source_id}")
async def delete_source(
    source_id: int,
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    """删除采集源"""
    try:
        await collection_service.delete_source(db, source_id)
        return {"message": "删除成功"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/sources/{source_id}/test")
async def test_source(
    source_id: int,
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """测试采集源连通性"""
    try:
        return await collection_service.test_source(db, source_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MaccmsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sources/{source_id}/trigger")
async def trigger_collect(
    source_id: int,
    data: TriggerCollectRequest | None = None,
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """手动触发采集"""
    try:
        max_items = data.max_items if data else None
        result = await collection_service.trigger_collect(db, source_id, trigger_type="manual", max_items=max_items)
        return result
    except ValueError as e:
        if "正在运行中" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/sources/{source_id}/toggle")
async def toggle_source(
    source_id: int,
    data: SourceToggleRequest,
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """启用/停用采集源或自动采集"""
    kwargs = data.model_dump(exclude_unset=True)
    field_map = {
        "enabled": "Enabled",
        "auto_collect": "AutoCollect",
    }
    orm_kwargs = {field_map[k]: v for k, v in kwargs.items() if k in field_map}
    try:
        return await collection_service.update_source(db, source_id, **orm_kwargs)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/logs")
async def list_logs(
    source_id: int | None = Query(None, description="按采集源ID筛选"),
    limit: int = Query(50, ge=1, le=500),
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> list[dict[str, Any]]:
    """获取采集日志列表"""
    return await collection_service.list_logs(db, source_id=source_id, limit=limit)


@router.get("/sources/{source_id}/status")
async def get_source_status(
    source_id: int,
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """获取采集源实时状态（运行中任务的进度）"""
    status = await collection_service.get_running_status(db, source_id)
    if status is None:
        # 获取最新历史状态
        logs = await collection_service.list_logs(db, source_id=source_id, limit=1)
        if logs:
            log = logs[0]
            return {
                "status": log.get("status"),
                "started_at": log.get("started_at"),
                "finished_at": log.get("finished_at"),
                "total": log.get("total_fetched", 0),
                "new_count": log.get("new_count", 0),
                "update_count": log.get("update_count", 0),
                "error_count": log.get("error_count", 0),
                "error_message": log.get("error_message"),
            }
        return {"status": "idle", "message": "暂无采集记录"}
    return status


@router.post("/sources/{source_id}/stop")
async def stop_source_collect(
    source_id: int,
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """停止正在运行的采集任务"""
    try:
        return await collection_service.stop_collect(db, source_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
