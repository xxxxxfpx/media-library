# coding: utf-8
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

from .models import (
    Base,
    MediaItem,
    ItemLinks,
    UserData,
    User,
    File,
    FileLink,
    Alias,
    MediaType,
    PersonType,
    ChapterMarkerType,
    ItemStatus,
    ShareLevel,
    FileType,
    ImageType,
)

from database.core import (
    engine,
    AsyncSessionLocal,
    Base,
    SessionManager,
    get_db_session,
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
    "engine",
    "AsyncSessionLocal",
    "SessionManager",
    "get_db_session",
]
