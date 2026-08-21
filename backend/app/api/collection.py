"""采集管理 API - 苹果CMS V10 采集源配置与采集执行"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_admin_id, get_db_session
from app.services import collection_service
from app.services.maccms_client import MaccmsError

router = APIRouter(prefix="/collection", tags=["collection"])


# ======================================================================
# 请求/响应模型
# ======================================================================

class SourceCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="采集源名称")
    base_url: str = Field(..., min_length=1, max_length=500, description="API基础URL")
    auto_collect: bool = Field(default=False, description="自动轮询采集开关")
    interval_minutes: int = Field(default=60, ge=1, le=10080, description="轮询间隔(分钟)")
    enabled: bool = Field(default=True, description="是否启用")


class SourceUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    base_url: str | None = Field(None, min_length=1, max_length=500)
    auto_collect: bool | None = None
    interval_minutes: int | None = Field(None, ge=1, le=10080)
    enabled: bool | None = None


class SourceToggleRequest(BaseModel):
    enabled: bool | None = None
    auto_collect: bool | None = None


# ======================================================================
# 路由
# ======================================================================

@router.get("/sources")
async def list_sources(
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> list[dict[str, Any]]:
    """获取所有采集源列表"""
    return await collection_service.list_sources(db)


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
    user_id: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """手动触发采集"""
    try:
        log_id = await collection_service.trigger_collect(db, source_id, trigger_type="manual")
        return {"log_id": log_id, "status": "running"}
    except ValueError as e:
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
