# coding: utf-8
"""
数据库验证辅助函数
==================
提供数据库结构验证和数据查询的辅助函数
"""

from typing import Optional, Dict, Any, List
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def verify_table_exists(session: AsyncSession, table_name: str) -> bool:
    """验证表是否存在"""
    result = await session.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' AND name=:name"),
        {"name": table_name}
    )
    return result.fetchone() is not None


async def verify_column_exists(
    session: AsyncSession,
    table_name: str,
    column_name: str
) -> Optional[Dict[str, Any]]:
    """验证列是否存在，返回列信息"""
    result = await session.execute(
        text(f"PRAGMA table_info({table_name})")
    )
    columns = result.fetchall()
    for col in columns:
        if col[1] == column_name:  # col[1] 是列名
            return {
                "name": col[1],
                "type": col[2],
                "nullable": not col[3],  # col[3] = 1 表示 NOT NULL
                "default": col[4],
                "primary_key": bool(col[5])  # col[5] = 1 表示 PK
            }
    return None


async def verify_index_exists(
    session: AsyncSession,
    table_name: str,
    index_name: str
) -> bool:
    """验证索引是否存在"""
    result = await session.execute(
        text("SELECT name FROM sqlite_master WHERE type='index' AND name=:name"),
        {"name": index_name}
    )
    return result.fetchone() is not None


async def get_table_columns(session: AsyncSession, table_name: str) -> List[Dict[str, Any]]:
    """获取表的所有列信息"""
    result = await session.execute(text(f"PRAGMA table_info({table_name})"))
    columns = result.fetchall()
    return [
        {
            "name": col[1],
            "type": col[2],
            "nullable": not col[3],
            "default": col[4],
            "primary_key": bool(col[5])
        }
        for col in columns
    ]


async def get_table_indexes(session: AsyncSession, table_name: str) -> List[Dict[str, Any]]:
    """获取表的所有索引"""
    result = await session.execute(
        text(f"PRAGMA index_list({table_name})")
    )
    indexes = result.fetchall()
    result_list = []
    for idx in indexes:
        index_name = idx[1]
        # 获取索引包含的列
        col_result = await session.execute(
            text(f"PRAGMA index_info({index_name})")
        )
        cols = col_result.fetchall()
        result_list.append({
            "name": index_name,
            "unique": bool(idx[2]),
            "columns": [col[2] for col in cols]  # col[2] 是列名
        })
    return result_list


async def query_user_by_id(session: AsyncSession, user_id: int) -> Optional[Dict[str, Any]]:
    """根据 ID 查询用户"""
    result = await session.execute(
        text("SELECT * FROM Users WHERE Id = :id"),
        {"id": user_id}
    )
    row = result.fetchone()
    if row:
        return dict(row._mapping)
    return None


async def query_user_by_name(session: AsyncSession, username: str) -> Optional[Dict[str, Any]]:
    """根据用户名查询用户"""
    result = await session.execute(
        text("SELECT * FROM Users WHERE Name = :name"),
        {"name": username}
    )
    row = result.fetchone()
    if row:
        return dict(row._mapping)
    return None


async def query_media_item_by_id(session: AsyncSession, item_id: int) -> Optional[Dict[str, Any]]:
    """根据 ID 查询媒体项"""
    result = await session.execute(
        text("SELECT * FROM MediaItems WHERE Id = :id"),
        {"id": item_id}
    )
    row = result.fetchone()
    if row:
        return dict(row._mapping)
    return None


async def query_userdata(
    session: AsyncSession,
    user_id: int,
    item_id: int
) -> Optional[Dict[str, Any]]:
    """查询用户数据"""
    result = await session.execute(
        text("SELECT * FROM UserData WHERE UserId = :user_id AND ItemId = :item_id"),
        {"user_id": user_id, "item_id": item_id}
    )
    row = result.fetchone()
    if row:
        return dict(row._mapping)
    return None


async def query_file_by_id(session: AsyncSession, file_id: int) -> Optional[Dict[str, Any]]:
    """根据 ID 查询文件"""
    result = await session.execute(
        text("SELECT * FROM Files WHERE Id = :id"),
        {"id": file_id}
    )
    row = result.fetchone()
    if row:
        return dict(row._mapping)
    return None


async def query_filelinks_by_item(session: AsyncSession, item_id: int) -> List[Dict[str, Any]]:
    """查询媒体项的所有文件关联"""
    result = await session.execute(
        text("SELECT * FROM FileLinks WHERE ItemId = :item_id"),
        {"item_id": item_id}
    )
    return [dict(row._mapping) for row in result.fetchall()]


async def query_itemlinks_by_item(session: AsyncSession, item_id: int) -> List[Dict[str, Any]]:
    """查询媒体项的所有关联"""
    result = await session.execute(
        text("SELECT * FROM ItemLinks WHERE ItemId = :item_id"),
        {"item_id": item_id}
    )
    return [dict(row._mapping) for row in result.fetchall()]


async def query_aliases_by_item(session: AsyncSession, item_id: int) -> List[Dict[str, Any]]:
    """查询媒体项的所有别名"""
    result = await session.execute(
        text("SELECT * FROM Aliases WHERE ItemId = :item_id"),
        {"item_id": item_id}
    )
    return [dict(row._mapping) for row in result.fetchall()]


async def get_all_tables(session: AsyncSession) -> List[str]:
    """获取所有表名"""
    result = await session.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    )
    return [row[0] for row in result.fetchall()]


async def count_table_rows(session: AsyncSession, table_name: str) -> int:
    """获取表的行数"""
    result = await session.execute(
        text(f"SELECT COUNT(*) FROM {table_name}")
    )
    return result.scalar() or 0