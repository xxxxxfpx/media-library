"""媒体业务逻辑服务层"""

import logging
import time
from collections import defaultdict
from typing import Optional, List, Dict, Any

from sqlalchemy import select, func, or_, text, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MediaItem, ItemLinks, File, FileLink, Alias, UserData, MediaType, FileLinkType
from app.schemas.media import serialize_links, serialize_files, serialize_alias, serialize_userdata, serialize_item
from app.schemas.media import LinkItem, FileInfo, AliasItem, UserDataInfo, MediaItemResponse
from config import config as _app_config

logger = logging.getLogger(__name__)


def parse_types(types_str: Optional[str]) -> Optional[List[MediaType]]:
    if not types_str:
        return None
    result = []
    for t in types_str.split(","):
        t = t.strip()
        if t:
            try:
                result.append(MediaType(t))
            except ValueError:
                pass
    return result if result else None


def _infer_link_type(image_type=None, chapter_index=None) -> FileLinkType:
    """根据字段组合推断 FileLinkType：ChapterIndex 优先，其次 ImageType，否则 MediaSource"""
    if chapter_index is not None:
        return FileLinkType.Chapter
    if image_type is not None:
        return FileLinkType.Image
    return FileLinkType.MediaSource


async def fetch_links_batch(db: AsyncSession, item_ids: List[int]) -> Dict[int, list[LinkItem]]:
    if not item_ids:
        return {}
    # 优化方案：两步查询，避免 SQLite 优化器选择以 MediaItems 为驱动表导致的性能问题
    # 第一步：先获取 ItemLinks（以 ItemId 为索引过滤）
    links_result = await db.execute(
        select(ItemLinks).where(ItemLinks.ItemId.in_(item_ids))
    )
    links = links_result.scalars().all()
    if not links:
        return {}
    # 第二步：获取关联的 MediaItems
    linked_item_ids = list(set([link.LinkedItemId for link in links]))
    media_result = await db.execute(
        select(MediaItem).where(MediaItem.Id.in_(linked_item_ids), MediaItem.IsDeleted == False)
    )
    media_map = {m.Id: m for m in media_result.scalars().all()}
    # 组合结果
    grouped = defaultdict(list)
    for link in links:
        linked_item = media_map.get(link.LinkedItemId)
        if linked_item:
            grouped[link.ItemId].append((link, linked_item))
    return {item_id: serialize_links(links_list) for item_id, links_list in grouped.items()}


async def fetch_files_batch(db: AsyncSession, item_ids: List[int]) -> Dict[int, list[FileInfo]]:
    if not item_ids:
        return {}
    # 显式列选择：避开 FFmpeg 大 JSON 字段，列表页不需要完整探针数据
    result = await db.execute(
        select(
            File.Id, File.Name, File.SortName, File.Path, File.Size,
            File.Type, File.Etag,
            FileLink.ItemId, FileLink.FileId, FileLink.LinkType, FileLink.ImageType, FileLink.ImageIndex,
            FileLink.ChapterIndex, FileLink.ChapterName, FileLink.StartPositionTicks, FileLink.MarkerType,
        )
        .join(FileLink, FileLink.FileId == File.Id)
        .where(FileLink.ItemId.in_(item_ids))
    )
    grouped = defaultdict(list)
    for row in result:
        file = File(
            Id=row.Id, Name=row.Name, SortName=row.SortName, Path=row.Path, Size=row.Size,
            Type=row.Type, Etag=row.Etag,
        )
        file_link = FileLink(
            ItemId=row.ItemId, FileId=row.FileId, LinkType=row.LinkType,
            ImageType=row.ImageType, ImageIndex=row.ImageIndex, ChapterIndex=row.ChapterIndex,
            ChapterName=row.ChapterName, StartPositionTicks=row.StartPositionTicks,
            MarkerType=row.MarkerType,
        )
        grouped[file_link.ItemId].append((file, file_link))
    return {item_id: serialize_files(files) for item_id, files in grouped.items()}


async def fetch_userdata_batch(db: AsyncSession, item_ids: List[int], user_id: Optional[int]) -> Dict[int, Optional[UserDataInfo]]:
    if not item_ids or user_id is None:
        return {}
    result = await db.execute(
        select(UserData)
        .where(UserData.ItemId.in_(item_ids), UserData.UserId == user_id)
    )
    return {ud.ItemId: serialize_userdata(ud) for ud in result.scalars().all()}


async def fetch_alias_batch(db: AsyncSession, item_ids: List[int]) -> Dict[int, list[AliasItem]]:
    if not item_ids:
        return {}
    result = await db.execute(
        select(Alias)
        .where(Alias.ItemId.in_(item_ids))
    )
    grouped = defaultdict(list)
    for alias in result.scalars().all():
        grouped[alias.ItemId].append(alias)
    return {item_id: serialize_alias(aliases) for item_id, aliases in grouped.items()}


async def fetch_has_children_batch(db: AsyncSession, item_ids: List[int]) -> set[int]:
    """批量查询哪些 item 有子项（作为 LinkedItemId 出现在 ItemLinks 中）"""
    if not item_ids:
        return set()
    result = await db.execute(
        select(ItemLinks.LinkedItemId).distinct().where(
            ItemLinks.LinkedItemId.in_(item_ids),
            ItemLinks.ItemId != ItemLinks.LinkedItemId,  # 排除自关联
        )
    )
    return {row[0] for row in result.all()}


async def fetch_source_names_batch(db: AsyncSession, item_ids: List[int]) -> Dict[int, str]:
    """批量查询 items 的 source_name（通过 SourceItemId 关联 Source 类型 MediaItem）"""
    if not item_ids:
        return {}
    result = await db.execute(
        select(MediaItem.Id, MediaItem.SourceItemId)
        .where(MediaItem.Id.in_(item_ids), MediaItem.SourceItemId.isnot(None))
    )
    source_ids = [row.SourceItemId for row in result.all()]
    if not source_ids:
        return {}
    src_result = await db.execute(
        select(MediaItem.Id, MediaItem.Name).where(
            MediaItem.Id.in_(source_ids),
            MediaItem.Type == MediaType.Source,
        )
    )
    src_map = {row.Id: row.Name for row in src_result.all()}
    return {row.Id: src_map.get(row.SourceItemId) for row in result.all()}


# ==================== 搜索优化 ====================
# SQLite 使用 FTS5 trigram 虚拟表（media_item_fts），PostgreSQL 使用 pg_trgm GIN 索引。
# trigram 要求关键词 >= 3 字符才能命中索引；短词（常见中文 2 字词）回退 LIKE。

_FTS_MIN_LENGTH = 3
_fts_available: bool | None = None


# ==================== diskcache 缓存（统一惰性初始化） ====================
# get_media_info / get_media_list 的响应缓存与 get_media_stats 的统计缓存共用
# 同一惰性初始化机制，仅缓存目录名不同。仅生产（debug=False）启用，
# 避免每次请求重复查询数据库。写操作（create_media_batch）成功后主动失效。

_cache_instances: dict = {}


def _get_cache(name: str):
    """惰性初始化指定名称的 diskcache 缓存（同名只创建一次）"""
    if name not in _cache_instances:
        import os
        import diskcache
        cache_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data", "cache", name,
        )
        os.makedirs(cache_dir, exist_ok=True)
        _cache_instances[name] = diskcache.Cache(cache_dir)
    return _cache_instances[name]


def _cache_enabled() -> bool:
    """生产模式启用缓存；debug（开发/测试）禁用保证数据一致性"""
    return not _app_config.app.debug


async def _cache_get(key: str):
    if not _cache_enabled():
        return None
    return _get_cache("media_response").get(key)


async def _cache_set(key: str, value, expire: int = 30) -> None:
    if not _cache_enabled():
        return
    _get_cache("media_response").set(key, value, expire=expire)


def invalidate_response_cache() -> None:
    """媒体数据变更后失效全部响应缓存"""
    cache = _cache_instances.get("media_response")
    if cache is not None:
        cache.clear()


async def _is_fts_available(db: AsyncSession) -> bool:
    """检测当前 SQLite 连接是否已有 FTS5 虚拟表（惰性缓存，避免每次搜索都查 sqlite_master）"""
    global _fts_available
    if _app_config.database.type != "sqlite":
        return False
    if _fts_available is None:
        result = await db.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='media_item_fts'")
        )
        _fts_available = result.scalar() is not None
    return _fts_available


def _escape_fts_phrase(term: str) -> str:
    """转义 FTS5 短语：双引号内包裹 + 内部引号翻倍，避免语法注入"""
    escaped = term.replace('"', '""')
    return f'"{escaped}"'


async def _search_condition(db: AsyncSession, search: str):
    """
    构造搜索过滤条件。

    - SQLite + FTS 可用且关键词 >= 3 字符：Name/Overview/Tagline 走 FTS5 MATCH，
      Alias 仍走 LIKE（别名索引已建 B-tree，前缀场景可用）。
    - 其余场景回退 LIKE（兼容短词与 PostgreSQL）。
    """
    pattern = f"%{search}%"

    if len(search.strip()) >= _FTS_MIN_LENGTH and await _is_fts_available(db):
        try:
            fts_phrase = _escape_fts_phrase(search.strip())
            fts_match = select(MediaItem.Id).where(
                MediaItem.Id.in_(
                    select(text("rowid"))
                    .select_from(text("media_item_fts"))
                    .where(text("media_item_fts MATCH :term"))
                ).params(term=fts_phrase)
            )
            return or_(
                MediaItem.Id.in_(fts_match),
                Alias.Name.ilike(pattern),
            )
        except Exception:
            # FTS 查询失败（如版本/表结构异常）回退 LIKE
            pass

    return or_(
        MediaItem.Name.ilike(pattern),
        MediaItem.Overview.ilike(pattern),
        MediaItem.Tagline.ilike(pattern),
        Alias.Name.ilike(pattern),
    )


async def get_media_list(
    db: AsyncSession,
    user_id: int,
    types: Optional[str] = None,
    favorite: bool = False,
    has_playback: bool = False,
    has_rating: bool = False,
    sort_by: str = "date_created",
    limit: int = 50,
    offset: int = 0,
    item_ids: Optional[str] = None,
    linked_item_ids: Optional[str] = None,
    search: Optional[str] = None,
    cursor: Optional[str] = None,
) -> dict:
    query = select(MediaItem).where(MediaItem.IsDeleted == False)
    total_query = select(func.count()).select_from(MediaItem).where(MediaItem.IsDeleted == False)

    has_user_filter = favorite or has_playback or has_rating
    if has_user_filter:
        query = query.join(UserData, MediaItem.Id == UserData.ItemId).where(
            UserData.UserId == user_id
        )
        total_query = total_query.join(UserData, MediaItem.Id == UserData.ItemId).where(
            UserData.UserId == user_id
        )
        if favorite:
            query = query.where(UserData.FavoritedAt.isnot(None))
            total_query = total_query.where(UserData.FavoritedAt.isnot(None))
        if has_playback:
            query = query.where(UserData.LastPlayedAt.isnot(None))
            total_query = total_query.where(UserData.LastPlayedAt.isnot(None))
        if has_rating:
            query = query.where(UserData.Rating.isnot(None))
            total_query = total_query.where(UserData.Rating.isnot(None))

    if search:
        search_condition = await _search_condition(db, search)
        query = query.outerjoin(Alias, MediaItem.Id == Alias.ItemId)
        total_query = total_query.outerjoin(Alias, MediaItem.Id == Alias.ItemId)
        query = query.where(search_condition)
        total_query = total_query.where(search_condition)

    type_list = parse_types(types)
    if type_list and item_ids:
        id_list = [int(id.strip()) for id in item_ids.split(",") if id.strip().isdigit()]
        if id_list:
            query = query.where(
                MediaItem.Id.in_(id_list),
                MediaItem.Type.in_(type_list)
            )
            total_query = total_query.where(
                MediaItem.Id.in_(id_list),
                MediaItem.Type.in_(type_list)
            )
    else:
        if type_list:
            query = query.where(MediaItem.Type.in_(type_list))
            total_query = total_query.where(MediaItem.Type.in_(type_list))

        if item_ids:
            id_list = [int(id.strip()) for id in item_ids.split(",") if id.strip().isdigit()]
            if id_list:
                query = query.where(MediaItem.Id.in_(id_list))
                total_query = total_query.where(MediaItem.Id.in_(id_list))

    has_linked_ids = False
    if linked_item_ids:
        linked_ids = [int(id.strip()) for id in linked_item_ids.split(",") if id.strip().isdigit()]
        has_linked_ids = len(linked_ids) > 0
        if linked_ids:
            if sort_by == "order":
                # 使用 ItemLinks.Order 排序
                query = query.join(ItemLinks, MediaItem.Id == ItemLinks.ItemId).where(ItemLinks.LinkedItemId.in_(linked_ids))
                total_query = total_query.join(ItemLinks, MediaItem.Id == ItemLinks.ItemId).where(ItemLinks.LinkedItemId.in_(linked_ids))
                if type_list:
                    query = query.where(MediaItem.Type.in_(type_list))
                    total_query = total_query.where(MediaItem.Type.in_(type_list))
            else:
                subq = select(ItemLinks.ItemId).where(ItemLinks.LinkedItemId.in_(linked_ids))
                if type_list:
                    query = query.where(
                        MediaItem.Id.in_(subq),
                        MediaItem.Type.in_(type_list)
                    )
                    total_query = total_query.where(
                        MediaItem.Id.in_(subq),
                        MediaItem.Type.in_(type_list)
                    )
                else:
                    query = query.where(MediaItem.Id.in_(subq))
                    total_query = total_query.where(MediaItem.Id.in_(subq))

    sort_mapping = {
        "date_created": MediaItem.DateCreated,
        "name": MediaItem.Name,
        "community_rating": MediaItem.CommunityRating,
        "critic_rating": MediaItem.CriticRating,
    }
    if has_user_filter:
        sort_mapping["favorited_at"] = UserData.FavoritedAt
        sort_mapping["last_played"] = UserData.LastPlayedAt
        sort_mapping["user_rating"] = UserData.Rating

    # ---------- 分页 ----------
    # 优先使用 keyset（游标）分页：仅 date_created / order 排序支持；
    # 其余排序回退到 offset 分页，保持向后兼容。
    cursor_enabled = cursor is not None and (sort_by == "date_created" or (sort_by == "order" and has_linked_ids))

    if sort_by == "order" and has_linked_ids:
        # 使用 ItemLinks.Order 升序排列（select 元组以获取 Order 用于生成游标）
        query = query.add_columns(ItemLinks.Order)
        query = query.order_by(ItemLinks.Order.asc(), ItemLinks.Id.asc())
        if cursor_enabled:
            try:
                c_order, c_item_id = cursor.split("|", 1)
                c_order = int(c_order)
                c_item_id = int(c_item_id)
            except (ValueError, AttributeError):
                cursor_enabled = False
            else:
                # 键集谓词：(Order > c_order) OR (Order == c_order AND Id > c_item_id)
                query = query.where(
                    or_(
                        ItemLinks.Order > c_order,
                        (ItemLinks.Order == c_order) & (ItemLinks.Id > c_item_id),
                    )
                )
        if not cursor_enabled:
            query = query.limit(limit).offset(offset)
        else:
            query = query.limit(limit)
    else:
        order_col = sort_mapping.get(sort_by, MediaItem.DateCreated)
        # 统一加 Id 作为次排序键，保证稳定排序
        query = query.order_by(order_col.desc(), MediaItem.Id.desc())
        if cursor_enabled:
            from datetime import datetime, timezone
            try:
                c_dt, c_id = cursor.split("|", 1)
                c_dt = datetime.fromisoformat(c_dt.replace(" ", "T").replace("Z", "+00:00"))
                c_id = int(c_id)
            except (ValueError, AttributeError):
                cursor_enabled = False
            else:
                # 键集谓词：(DateCreated < c_dt) OR (DateCreated == c_dt AND Id < c_id)
                query = query.where(
                    or_(
                        order_col < c_dt,
                        (order_col == c_dt) & (MediaItem.Id < c_id),
                    )
                )
        if not cursor_enabled:
            query = query.limit(limit).offset(offset)
        else:
            query = query.limit(limit)

    total_result = await db.execute(total_query)
    total = total_result.scalar() or 0

    result = await db.execute(query)
    if sort_by == "order" and has_linked_ids:
        rows = result.all()
        items = [r[0] for r in rows]
        order_map = {r[0].Id: r[1] for r in rows}
    else:
        items = result.scalars().all()
        order_map = None

    item_ids_list = [item.Id for item in items]

    links_map = await fetch_links_batch(db, item_ids_list)
    files_map = await fetch_files_batch(db, item_ids_list)
    userdata_map = await fetch_userdata_batch(db, item_ids_list, user_id)
    alias_map = await fetch_alias_batch(db, item_ids_list)
    has_children_set = await fetch_has_children_batch(db, item_ids_list)
    source_names_map = await fetch_source_names_batch(db, item_ids_list)

    media_list = []
    for item in items:
        data = serialize_item(item).model_dump()
        data['source_name'] = source_names_map.get(item.Id)
        entry = MediaItemResponse(
            **data,
            links=links_map.get(item.Id, []),
            files=files_map.get(item.Id, []),
            userdata=userdata_map.get(item.Id, None),
            alias=alias_map.get(item.Id, []),
            has_children=item.Id in has_children_set,
        )
        media_list.append(entry)

    # keyset 下一页游标（仅 date_created / order 排序生成）
    # 注意：游标时间格式用空格分隔（与 SQLite 存储格式一致），避免字符串比较歧义
    next_cursor = None
    if items:
        last = items[-1]
        if sort_by == "order" and has_linked_ids and order_map is not None:
            next_cursor = f"{order_map.get(last.Id) or 0}|{last.Id}"
        else:
            next_cursor = f"{last.DateCreated.strftime('%Y-%m-%d %H:%M:%S.%f')}|{last.Id}"

    return {
        "items": media_list,
        "total": total,
        "limit": limit,
        "offset": offset,
        "next_cursor": next_cursor,
    }


async def get_media_list_cached(
    db: AsyncSession,
    user_id: int,
    types: Optional[str] = None,
    favorite: bool = False,
    has_playback: bool = False,
    has_rating: bool = False,
    sort_by: str = "date_created",
    limit: int = 50,
    offset: int = 0,
    item_ids: Optional[str] = None,
    linked_item_ids: Optional[str] = None,
    search: Optional[str] = None,
    cursor: Optional[str] = None,
) -> dict:
    """带缓存的媒体列表。

    仅缓存无用户过滤（非 favorite/has_playback/has_rating）的查询；
    用户个性化查询每次实时计算，避免串数据。
    """
    if favorite or has_playback or has_rating or search or item_ids:
        return await get_media_list(
            db=db, user_id=user_id, types=types, favorite=favorite,
            has_playback=has_playback, has_rating=has_rating, sort_by=sort_by,
            limit=limit, offset=offset, item_ids=item_ids,
            linked_item_ids=linked_item_ids, search=search, cursor=cursor,
        )

    cache_key = (f"media_list_{user_id}_{types or ''}_{sort_by}_{limit}_{offset}_"
                 f"{linked_item_ids or ''}_{cursor or ''}")
    cached = await _cache_get(cache_key)
    if cached is not None:
        return cached

    result = await get_media_list(
        db=db, user_id=user_id, types=types, favorite=favorite,
        has_playback=has_playback, has_rating=has_rating, sort_by=sort_by,
        limit=limit, offset=offset, item_ids=item_ids,
        linked_item_ids=linked_item_ids, search=search, cursor=cursor,
    )
    # 序列化为纯 dict 再缓存（避免 Pydantic 模型进 diskcache 的 pickle 兼容问题）
    await _cache_set(cache_key, {
        "items": [item.model_dump() for item in result["items"]],
        "total": result["total"],
        "limit": result["limit"],
        "offset": result["offset"],
        "next_cursor": result["next_cursor"],
    }, expire=30)
    return result


async def get_media_info(db: AsyncSession, id: int, user_id: int) -> Optional[MediaItemResponse]:
    result = await db.execute(
        select(MediaItem).where(MediaItem.Id == id, MediaItem.IsDeleted == False)
    )
    item = result.scalar_one_or_none()
    if not item:
        return None

    links_result = await db.execute(
        select(ItemLinks, MediaItem)
        .join(MediaItem, ItemLinks.LinkedItemId == MediaItem.Id)
        .where(ItemLinks.ItemId == id, MediaItem.IsDeleted == False)
    )
    link_rows = links_result.all()
    linked_item_ids = [m.Id for _, m in link_rows]
    primary_images_map = {}
    if linked_item_ids:
        img_result = await db.execute(
            select(FileLink.ItemId, FileLink.FileId)
            .where(
                FileLink.ItemId.in_(linked_item_ids),
                FileLink.LinkType.in_([FileLinkType.Image, FileLinkType.Chapter])
            )
        )
        for item_id, file_id in img_result.all():
            if item_id not in primary_images_map:
                primary_images_map[item_id] = str(file_id)
    links = serialize_links(link_rows, primary_images_map)

    files_result = await db.execute(
        select(File, FileLink)
        .join(FileLink, FileLink.FileId == File.Id)
        .where(FileLink.ItemId == id)
    )
    files = serialize_files(files_result)

    userdata = None
    if user_id is not None:
        ud_result = await db.execute(
            select(UserData)
            .where(UserData.ItemId == id, UserData.UserId == user_id)
        )
        userdata = serialize_userdata(ud_result.scalar_one_or_none())

    alias_result = await db.execute(
        select(Alias).where(Alias.ItemId == id)
    )
    alias = serialize_alias(alias_result.scalars().all())

    has_children = await db.execute(
        select(True).where(
            select(ItemLinks).where(ItemLinks.LinkedItemId == id).exists()
        )
    )
    has_children_val = has_children.scalar() is True

    # 获取 source_name（通过 SourceItemId 关联）
    source_name = None
    if item.SourceItemId is not None:
        src_result = await db.execute(
            select(MediaItem.Name).where(
                MediaItem.Id == item.SourceItemId,
                MediaItem.Type == MediaType.Source,
            )
        )
        source_name = src_result.scalar_one_or_none()

    data = serialize_item(item).model_dump()
    data['source_name'] = source_name
    return MediaItemResponse(
        **data,
        links=links,
        files=files,
        userdata=userdata,
        alias=alias,
        has_children=has_children_val,
    )


async def get_media_info_cached(db: AsyncSession, id: int, user_id: int) -> Optional[MediaItemResponse]:
    """带缓存的媒体详情（供 API 层调用）"""
    cache_key = f"media_info_{id}_{user_id}"
    cached = await _cache_get(cache_key)
    if cached is not None:
        return MediaItemResponse(**cached)
    response = await get_media_info(db, id, user_id)
    if response is not None:
        await _cache_set(cache_key, response.model_dump(), expire=30)
    return response


def _check_graph_connectivity(item_ids: set[str], item_links: list | None) -> list[str]:
    """
    检查图是否连通，返回孤立的 temp_id 列表

    找出所有连通分量，分量大小为 1 且 degree=0 的节点视为孤立节点

    规则：
    - 空 item_ids: 无孤立节点
    - 空的 item_links 或 None: 如果只有1个节点则连通，否则所有节点都孤立
    """
    if not item_ids:
        return []

    if not item_links:
        if len(item_ids) == 1:
            return []
        return list(item_ids)

    graph: dict[str, set[str]] = {tid: set() for tid in item_ids}
    for link in item_links:
        if link.link in graph and link.linked in graph:
            graph[link.link].add(link.linked)
            graph[link.linked].add(link.link)

    unvisited = set(item_ids)
    isolated = []

    while unvisited:
        start = next(iter(unvisited))
        visited = set()
        queue = [start]

        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)

        unvisited -= visited

        if len(visited) == 1:
            node = next(iter(visited))
            if len(graph[node]) == 0:
                isolated.append(node)

    return isolated


async def create_media_batch(
    db: AsyncSession,
    data: "MediaBatchCreate",
    strict_graph: bool = True,
) -> dict:
    """
    批量创建媒体项及关联数据

    流程：
    1. 先创建所有 items（MediaItem），建立 temp_id → real_id 映射
    2. 再创建所有 files（File），更新映射
    3. 创建 item_links（ItemLinks）
    4. 创建 file_links（FileLinks）

    重复处理：source_name + source_id 存在则更新已设置字段

    参数：
        strict_graph: 是否要求传入的 items 图是连通的。默认 True（严格模式），
                      所有 items 必须通过 item_links 互相连通
    """
    _t0 = time.perf_counter()
    from app.schemas.create import MediaBatchCreate
    from database.models import MediaType, FileType, PersonType, ImageType, ItemStatus, FileLinkType
    from datetime import datetime, timezone
    import json

    # 日期解析辅助函数
    def parse_datetime(val):
        if val is None:
            return None
        if isinstance(val, datetime):
            return val
        if isinstance(val, str):
            # 尝试解析 ISO 格式日期
            try:
                return datetime.fromisoformat(val.replace('Z', '+00:00'))
            except ValueError:
                return None
        return None

    # JSON 序列化辅助函数
    def to_json(val):
        if val is None:
            return None
        if isinstance(val, list):
            return json.dumps(val, ensure_ascii=False)
        return val

    # temp_id → real_id 映射
    item_temp_to_id: dict[str, int] = {}
    file_temp_to_id: dict[str, int] = {}

    now = datetime.now(timezone.utc)

    # 0. 图连通性检查（strict_graph 模式）
    if strict_graph and data.items and len(data.items) > 0:
        item_ids = {item.temp_id for item in data.items}
        isolated = _check_graph_connectivity(item_ids, data.item_links)
        if isolated:
            raise ValueError(
                f"strict_graph=True 要求所有 items 连通，但发现孤立节点: {isolated}。"
                "请确保通过 item_links 将所有媒体项连接起来，或使用 strict_graph=False 禁用此检查。"
            )

    # 0b. 校验关联引用的 temp_id 均存在，避免数据静默丢失
    item_temp_ids = {item.temp_id for item in data.items}
    file_temp_ids = {file.temp_id for file in data.files}
    missing_refs = []
    for link in data.item_links:
        if link.link not in item_temp_ids or link.linked not in item_temp_ids:
            missing_refs.append(f"item_link: {link.link} -> {link.linked}")
    for f_link in data.file_links:
        if f_link.item not in item_temp_ids or f_link.file not in file_temp_ids:
            missing_refs.append(f"file_link: item={f_link.item} file={f_link.file}")
    if missing_refs:
        shown = ", ".join(missing_refs[:10])
        if len(missing_refs) > 10:
            shown += f" 等共 {len(missing_refs)} 处"
        raise ValueError(f"item_links/file_links 引用了不存在的 temp_id: {shown}")

    # 获取或创建 source_name 对应的 source item
    source_name = data.source_name
    source_item_result = await db.execute(
        select(MediaItem.Id).where(
            MediaItem.Name == source_name,
            MediaItem.Type == MediaType.Source,
            MediaItem.IsDeleted == False
        )
    )
    source_item_id = source_item_result.scalar_one_or_none()

    if source_item_id is None:
        source_item = MediaItem(
            Type=MediaType.Source,
            Name=source_name,
        )
        db.add(source_item)
        await db.flush()
        source_item_id = source_item.Id

    # 预查询：按 (source_id, type) 批量查找已存在 items，消除逐条 SELECT 的 N+1
    item_key_existing: dict[tuple, MediaItem] = {}
    item_key_created: dict[tuple, MediaItem] = {}
    dedup_keys = []
    for item_data in data.items:
        attrs = item_data.attrs
        source_info = item_data.source_info
        source_id = source_info.source_id if source_info and source_info.is_set("source_id") else None
        item_type = attrs.type if attrs.is_set("type") else None
        if source_id and source_item_id and item_type:
            dedup_keys.append((source_id, MediaType(item_type)))
    if dedup_keys:
        uniq_keys = list(dict.fromkeys(dedup_keys))
        conditions = [
            and_(
                MediaItem.SourceItemId == source_item_id,
                MediaItem.SourceId == key[0],
                MediaItem.Type == key[1],
                MediaItem.IsDeleted == False,
            )
            for key in uniq_keys
        ]
        result = await db.execute(select(MediaItem).where(or_(*conditions)))
        for item in result.scalars().all():
            item_key_existing[(item.SourceId, item.Type)] = item

    # 1. 创建或查找 Items
    for item_data in data.items:
        attrs = item_data.attrs
        source_info = item_data.source_info
        source_id = source_info.source_id if source_info and source_info.is_set("source_id") else None
        source_link = source_info.source_link if source_info and source_info.is_set("source_link") else None
        item_type = attrs.type if attrs.is_set("type") else None
        dedup_key = (source_id, MediaType(item_type)) if (source_id and source_item_id and item_type) else None

        existing = item_key_existing.get(dedup_key) if dedup_key else None
        if existing is None and dedup_key:
            existing = item_key_created.get(dedup_key)

        if existing:
            # 更新现有 item（仅更新显式设置的字段，未设置的保持原值）
            if attrs.is_set("name"):
                existing.Name = attrs.name
            if attrs.is_set("overview"):
                existing.Overview = attrs.overview
            if attrs.is_set("tagline"):
                existing.Tagline = attrs.tagline
            if attrs.is_set("official_rating"):
                existing.OfficialRating = attrs.official_rating
            if attrs.is_set("community_rating"):
                existing.CommunityRating = attrs.community_rating
            if attrs.is_set("critic_rating"):
                existing.CriticRating = attrs.critic_rating
            if attrs.is_set("premiere_date"):
                existing.PremiereDate = parse_datetime(attrs.premiere_date)
            if attrs.is_set("end_date"):
                existing.EndDate = parse_datetime(attrs.end_date)
            if attrs.is_set("production_locations"):
                existing.ProductionLocations = to_json(attrs.production_locations)
            if attrs.is_set("remote_trailers"):
                existing.RemoteTrailers = to_json(attrs.remote_trailers)
            if attrs.is_set("status"):
                existing.Status = ItemStatus(attrs.status) if attrs.status else None
            if attrs.is_set("preferred_metadata_language"):
                existing.PreferredMetadataLanguage = attrs.preferred_metadata_language
            if attrs.is_set("preferred_metadata_country_code"):
                existing.PreferredMetadataCountryCode = attrs.preferred_metadata_country_code
            if source_info and source_info.is_set("source_link"):
                existing.SourceLink = source_link
            existing.DateModified = now
            await db.flush()
            item_temp_to_id[item_data.temp_id] = existing.Id
        else:
            # 创建新 item
            item = MediaItem(
                Type=MediaType(attrs.type) if attrs.is_set("type") else MediaType.Source,
                Name=attrs.name if attrs.is_set("name") else None,
                Overview=attrs.overview if attrs.is_set("overview") else None,
                Tagline=attrs.tagline if attrs.is_set("tagline") else None,
                OfficialRating=attrs.official_rating if attrs.is_set("official_rating") else None,
                CommunityRating=attrs.community_rating if attrs.is_set("community_rating") else None,
                CriticRating=attrs.critic_rating if attrs.is_set("critic_rating") else None,
                PremiereDate=parse_datetime(attrs.premiere_date) if attrs.is_set("premiere_date") else None,
                EndDate=parse_datetime(attrs.end_date) if attrs.is_set("end_date") else None,
                ProductionLocations=to_json(attrs.production_locations) if attrs.is_set("production_locations") else None,
                RemoteTrailers=to_json(attrs.remote_trailers) if attrs.is_set("remote_trailers") else None,
                Status=ItemStatus(attrs.status) if attrs.status and attrs.is_set("status") else None,
                PreferredMetadataLanguage=attrs.preferred_metadata_language if attrs.is_set("preferred_metadata_language") else None,
                PreferredMetadataCountryCode=attrs.preferred_metadata_country_code if attrs.is_set("preferred_metadata_country_code") else None,
                SourceItemId=source_item_id if source_id else None,
                SourceId=source_id,
                SourceLink=source_link,
            )
            try:
                async with db.begin_nested():
                    db.add(item)
                    await db.flush()
            except IntegrityError:
                # 并发场景：另一个请求已创建相同 source_name + source_id + item_type
                # SAVEPOINT 已回滚当前 item，外层事务保持完整；重新查找并复用其 id
                result = await db.execute(
                    select(MediaItem).where(
                        MediaItem.SourceItemId == source_item_id,
                        MediaItem.SourceId == source_id,
                        MediaItem.Type == item_type,
                        MediaItem.IsDeleted == False,
                    ).limit(1)
                )
                found = result.scalar_one_or_none()
                if found:
                    item_temp_to_id[item_data.temp_id] = found.Id
                    if dedup_key:
                        item_key_created[dedup_key] = found
                    continue
                raise
            else:
                item_temp_to_id[item_data.temp_id] = item.Id
                if dedup_key:
                    item_key_created[dedup_key] = item

    # 预查询：按 Path 批量查找已存在的 Files
    file_path_existing: dict[str, File] = {}
    file_path_created: dict[str, File] = {}
    dedup_paths = [f.attrs.path for f in data.files if f.attrs.path is not None]
    if dedup_paths:
        result = await db.execute(
            select(File).where(File.Path.in_(list(dict.fromkeys(dedup_paths))))
        )
        for file in result.scalars().all():
            file_path_existing[file.Path] = file

    # 2. 创建 Files（按 Path 去重，重复提交幂等复用）
    for file_data in data.files:
        attrs = file_data.attrs
        existing = None
        if attrs.path is not None:
            existing = file_path_existing.get(attrs.path)
            if existing is None:
                existing = file_path_created.get(attrs.path)
        if existing:
            if attrs.is_set("name"):
                existing.Name = attrs.name
            if attrs.is_set("size"):
                existing.Size = attrs.size
            if attrs.is_set("etag"):
                existing.Etag = attrs.etag
            if attrs.is_set("type"):
                existing.Type = FileType(attrs.type)
            if attrs.is_set("ffmpeg"):
                existing.FFmpeg = to_json(attrs.ffmpeg)
            existing.UpdatedAt = now
            await db.flush()
            file_temp_to_id[file_data.temp_id] = existing.Id
        else:
            file = File(
                Name=attrs.name if attrs.is_set("name") else None,
                Path=attrs.path if attrs.is_set("path") else None,
                Type=FileType(attrs.type) if attrs.is_set("type") else FileType.Other,
                Size=attrs.size if attrs.is_set("size") else None,
                Etag=attrs.etag if attrs.is_set("etag") else None,
                FFmpeg=to_json(attrs.ffmpeg),
            )
            try:
                async with db.begin_nested():
                    db.add(file)
                    await db.flush()
            except IntegrityError:
                # 并发场景：Path 唯一约束冲突，复用已存在的文件
                existing_file = None
                if attrs.path is not None:
                    res = await db.execute(
                        select(File).where(File.Path == attrs.path).limit(1)
                    )
                    existing_file = res.scalar_one_or_none()
                if existing_file:
                    file_temp_to_id[file_data.temp_id] = existing_file.Id
                    if attrs.path is not None:
                        file_path_created[attrs.path] = existing_file
                    continue
                raise
            else:
                file_temp_to_id[file_data.temp_id] = file.Id
                if attrs.path is not None:
                    file_path_created[attrs.path] = file

    # 预查询：批量查找已存在的 ItemLinks
    link_existing: dict[tuple, ItemLinks] = {}
    link_created: dict[tuple, ItemLinks] = {}
    link_pairs = [
        (item_temp_to_id[link_data.link], item_temp_to_id[link_data.linked])
        for link_data in data.item_links
    ]
    if link_pairs:
        uniq_pairs = list(dict.fromkeys(link_pairs))
        conditions = [
            and_(ItemLinks.ItemId == pair[0], ItemLinks.LinkedItemId == pair[1])
            for pair in uniq_pairs
        ]
        result = await db.execute(select(ItemLinks).where(or_(*conditions)))
        for link in result.scalars().all():
            link_existing[(link.ItemId, link.LinkedItemId)] = link

    # 3. 创建 ItemLinks
    for link_data in data.item_links:
        pair = (item_temp_to_id[link_data.link], item_temp_to_id[link_data.linked])
        existing = link_existing.get(pair)
        if existing is None:
            existing = link_created.get(pair)

        if existing:
            if link_data.is_set("people_type"):
                existing.PeopleType = PersonType(link_data.people_type) if link_data.people_type else None
            if link_data.is_set("people_role"):
                existing.PeopleRole = link_data.people_role
            existing.UpdatedAt = now
        else:
            new_link = ItemLinks(
                ItemId=pair[0],
                LinkedItemId=pair[1],
                PeopleType=PersonType(link_data.people_type) if link_data.people_type and link_data.is_set("people_type") else None,
                PeopleRole=link_data.people_role if link_data.is_set("people_role") else None,
            )
            db.add(new_link)
            link_created[pair] = new_link

    # 预查询：批量查找已存在的 FileLinks
    file_link_existing: dict[tuple, FileLink] = {}
    file_link_created: dict[tuple, FileLink] = {}
    file_link_pairs = [
        (item_temp_to_id[f_link.item], file_temp_to_id[f_link.file])
        for f_link in data.file_links
    ]
    if file_link_pairs:
        uniq_pairs = list(dict.fromkeys(file_link_pairs))
        conditions = [
            and_(FileLink.ItemId == pair[0], FileLink.FileId == pair[1])
            for pair in uniq_pairs
        ]
        result = await db.execute(select(FileLink).where(or_(*conditions)))
        for f_link in result.scalars().all():
            file_link_existing[(f_link.ItemId, f_link.FileId)] = f_link

    # 4. 创建 FileLinks
    for f_link_data in data.file_links:
        pair = (item_temp_to_id[f_link_data.item], file_temp_to_id[f_link_data.file])
        existing = file_link_existing.get(pair)
        if existing is None:
            existing = file_link_created.get(pair)

        # 解析字段值
        image_type_val = ImageType(f_link_data.image_type) if f_link_data.image_type and f_link_data.is_set("image_type") else None
        chapter_index_val = f_link_data.chapter_index if f_link_data.is_set("chapter_index") else None

        # 推断 LinkType
        link_type = _infer_link_type(image_type_val, chapter_index_val)

        if existing:
            if f_link_data.is_set("image_type"):
                existing.ImageType = image_type_val
            if f_link_data.is_set("image_index"):
                existing.ImageIndex = f_link_data.image_index
            if f_link_data.is_set("chapter_index"):
                existing.ChapterIndex = chapter_index_val
            if f_link_data.is_set("chapter_name"):
                existing.ChapterName = f_link_data.chapter_name
            if f_link_data.is_set("start_position_ticks"):
                existing.StartPositionTicks = f_link_data.start_position_ticks
            if f_link_data.is_set("marker_type"):
                existing.MarkerType = f_link_data.marker_type
            existing.LinkType = link_type
            existing.UpdatedAt = now
        else:
            new_fl = FileLink(
                ItemId=pair[0],
                FileId=pair[1],
                LinkType=link_type,
                ImageType=image_type_val,
                ImageIndex=f_link_data.image_index if f_link_data.is_set("image_index") else 0,
                ChapterIndex=chapter_index_val,
                ChapterName=f_link_data.chapter_name if f_link_data.is_set("chapter_name") else None,
                StartPositionTicks=f_link_data.start_position_ticks if f_link_data.is_set("start_position_ticks") else None,
                MarkerType=f_link_data.marker_type if f_link_data.is_set("marker_type") else None,
            )
            db.add(new_fl)
            file_link_created[pair] = new_fl

    await db.commit()

    logger.info(
        "批量创建媒体完成 | source=%s items=%d files=%d item_links=%d file_links=%d 耗时=%.0fms",
        (source_name or "")[:40], len(item_temp_to_id), len(file_temp_to_id),
        len(data.item_links), len(data.file_links),
        (time.perf_counter() - _t0) * 1000,
    )

    return {
        "items": {temp_id: real_id for temp_id, real_id in item_temp_to_id.items()},
        "files": {temp_id: real_id for temp_id, real_id in file_temp_to_id.items()},
    }


async def get_media_stats(db: AsyncSession) -> dict:
    # 统计结果缓存 60s，避免首页每次全表 group by；
    # debug 模式（开发/测试）禁用缓存，保证数据一致性
    from config import config as _config
    if not _config.app.debug:
        cache = _get_cache("media_stats")
        cached = cache.get("media_stats")
        if cached is not None:
            return cached

    # 统计 File 类型（视频、音频、图片等）
    result = await db.execute(
        select(File.Type, func.count())
        .group_by(File.Type)
    )
    # key 转为枚举值字符串（兼容已精简的枚举）
    file_counts = {row[0].value if hasattr(row[0], "value") else row[0]: row[1] for row in result.all()}

    # 统计 MediaItem 类型
    result = await db.execute(
        select(MediaItem.Type, func.count())
        .where(MediaItem.IsDeleted == False)
        .group_by(MediaItem.Type)
    )
    media_counts = {row[0].value if hasattr(row[0], "value") else row[0]: row[1] for row in result.all()}

    stats = {
        # File 类型统计（首页卡片用）
        "video_count": file_counts.get("Video", 0),
        # 音乐/电子书卡片保留字段（视频库恒为 0，兼容现有前端）
        "audio_count": file_counts.get("Audio", 0),
        "image_count": file_counts.get("Image", 0),
        "subtitle_count": file_counts.get("Subtitle", 0),
        # MediaItem 类型统计
        "movie_count": media_counts.get("Movie", 0),
        "series_count": media_counts.get("Series", 0),
        "episode_count": media_counts.get("Episode", 0),
        "book_count": media_counts.get("Book", 0),
        "source_count": media_counts.get("Source", 0),
    }
    if not _config.app.debug:
        cache.set("media_stats", stats, expire=60)
    return stats
