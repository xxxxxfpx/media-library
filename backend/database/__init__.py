"""
Database Package - 数据库包
============================

Emby Server 数据库访问层，提供：
- SQLAlchemy ORM 模型
- 会话管理器
- 依赖注入支持

作者：数据库架构团队
版本：3.0.0 (移除 UserLike，精简枚举导出)
"""

from database.core import (
    AsyncSessionLocal,
    engine,
    get_db_session,
)

from .models import (
    Alias,
    Base,
    ChapterMarkerType,
    File,
    FileLink,
    FileLinkType,
    FileType,
    ImageType,
    ItemLinks,
    ItemStatus,
    MediaItem,
    MediaType,
    PersonType,
    ShareLevel,
    User,
    UserData,
)

__all__ = [
    "Base",
    "User",
    "MediaItem",
    "ItemLinks",
    "UserData",
    "File",
    "FileLink",
    "Alias",
    "MediaType",
    "PersonType",
    "ChapterMarkerType",
    "ItemStatus",
    "ShareLevel",
    "FileType",
    "ImageType",
    "FileLinkType",
    "engine",
    "AsyncSessionLocal",
    "get_db_session",
]
