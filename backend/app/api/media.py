"""Media API - 媒体相关接口"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MediaItem, ItemLinks, File, FileLink, Alias, UserData, MediaType
from database.core import get_db_session
from app.api.deps import get_user_id, get_admin_id
from app.services.media_service import (
    get_media_list_cached, get_media_info, get_media_info_cached, get_media_stats,
    create_media_batch, create_media_item, create_item_link, delete_item_link,
    delete_media_item, invalidate_response_cache,
)
from app.schemas.media import MediaListResponse, MediaItemResponse, MediaStatsResponse
from app.schemas.create import MediaBatchCreate, SingleItemCreate, SingleItemLinkCreate

router = APIRouter(prefix="/api/media", tags=["媒体"])


@router.get("/list", response_model=MediaListResponse)
async def get_list(
    types: Optional[str] = Query(None, description="媒体类型，逗号分隔"),
    favorite: bool = Query(False, description="仅收藏"),
    has_playback: bool = Query(False, description="仅播放过"),
    has_rating: bool = Query(False, description="仅评分过"),
    sort_by: str = Query("date_created", description="排序字段"),
    limit: int = Query(50, description="每页数量"),
    offset: int = Query(0, description="偏移量"),
    item_ids: Optional[str] = Query(None, description="媒体ID列表，逗号分隔"),
    linked_item_ids: Optional[str] = Query(None, description="关联媒体ID列表，逗号分隔"),
    search: Optional[str] = Query(None, description="搜索关键词，匹配名称、简介、标语、别名"),
    cursor: Optional[str] = Query(None, description="keyset 游标（上一页返回的 next_cursor），用于高效翻页"),
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    return await get_media_list_cached(
        db=db,
        user_id=user_id,
        types=types,
        favorite=favorite,
        has_playback=has_playback,
        has_rating=has_rating,
        sort_by=sort_by,
        limit=limit,
        offset=offset,
        item_ids=item_ids,
        linked_item_ids=linked_item_ids,
        search=search,
        cursor=cursor,
    )


@router.get("/info", response_model=MediaItemResponse)
async def get_info(
    id: int = Query(..., description="媒体ID"),
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    result = await get_media_info_cached(db, id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="媒体不存在")
    return result


@router.get("/stats", response_model=MediaStatsResponse)
async def get_stats(
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    return await get_media_stats(db)


@router.post("/batch")
async def create_batch(
    data: MediaBatchCreate,
    strict_graph: bool = Query(True, description="是否要求 items 图连通，默认 True"),
    db: AsyncSession = Depends(get_db_session),
    admin_id: int = Depends(get_admin_id),
):
    """批量创建媒体项及关联数据（需要管理员权限）"""
    try:
        result = await create_media_batch(db, data, strict_graph=strict_graph)
        invalidate_response_cache()
        return result
    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/items", status_code=201)
async def create_item(
    data: SingleItemCreate,
    db: AsyncSession = Depends(get_db_session),
    admin_id: int = Depends(get_admin_id),
):
    try:
        result = await create_media_item(db, data)
        invalidate_response_cache()
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/items/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db_session),
    admin_id: int = Depends(get_admin_id),
):
    try:
        await delete_media_item(db, item_id)
        invalidate_response_cache()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/items/{item_id}/links", status_code=201)
async def add_item_link(
    item_id: int,
    data: SingleItemLinkCreate,
    db: AsyncSession = Depends(get_db_session),
    admin_id: int = Depends(get_admin_id),
):
    try:
        result = await create_item_link(db, item_id, data)
        invalidate_response_cache()
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/items/{item_id}/links/{linked_item_id}", status_code=204)
async def remove_item_link(
    item_id: int,
    linked_item_id: int,
    db: AsyncSession = Depends(get_db_session),
    admin_id: int = Depends(get_admin_id),
):
    removed = await delete_item_link(db, item_id, linked_item_id)
    if not removed:
        raise HTTPException(status_code=404, detail="关联不存在")
    invalidate_response_cache()
