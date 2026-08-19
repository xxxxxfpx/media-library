# coding: utf-8
"""
数据库初始化测试
================
测试数据库表的创建、删除和结构验证
"""

import pytest
from sqlalchemy import text

from database.core import engine, Base, init_db, AsyncSessionLocal
from tests.utils.db_helper import (
    get_all_tables,
    get_table_columns,
    get_table_indexes,
)


# 预期的表名列表（根据实际模型）
EXPECTED_TABLES = [
    "Users",
    "MediaItems",
    "Files",
    "FileLinks",
    "ItemLinks",
    "UserData",
    "Aliases",
]


# Users 表的预期列
USERS_EXPECTED_COLUMNS = {
    "Id": {"type": "INTEGER", "primary_key": True},
    "Name": {"type": "VARCHAR(255)", "nullable": False},
    "PasswordHash": {"type": "VARCHAR(255)", "nullable": False},
    "Salt": {"type": "VARCHAR(255)", "nullable": False},
    "Email": {"type": "VARCHAR(255)", "nullable": True},
    "IsAdmin": {"type": "BOOLEAN", "nullable": False},
    "IsActive": {"type": "BOOLEAN", "nullable": False},
    "Setting": {"type": "TEXT", "nullable": True},
    "CreatedAt": {"type": "DATETIME", "nullable": False},
    "UpdatedAt": {"type": "DATETIME", "nullable": False},
}


# MediaItems 表的关键列（视频化精简后，无 AlbumId/DisplayOrder）
MEDIAITEMS_KEY_COLUMNS = [
    "Id", "Type", "Name", "Overview", "Tagline",
    "PremiereDate", "EndDate", "StartDate",
    "OfficialRating", "CustomRating", "CommunityRating", "CriticRating",
    "Status", "ChannelNumber",
    "DateCreated", "DateModified",
    "CreatedAt", "UpdatedAt", "IsDeleted",
    "PresentationUniqueKey", "LockedFields",
    "SourceId", "SourceLink", "SourceItemId",
]


# Files 表的关键列
FILES_KEY_COLUMNS = [
    "Id", "Etag", "Size", "Name", "SortName", "Path",
    "CloudId", "Type", "FFmpeg", "CreatedAt", "UpdatedAt",
]


class TestDatabaseInit:
    """数据库初始化测试类"""

    @pytest.mark.asyncio
    async def test_drop_and_recreate_tables(self):
        """测试删除和重建所有表"""
        # 1. 先创建表（确保有表可删）
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # 2. 验证表已创建
        async with AsyncSessionLocal() as session:
            tables_before = await get_all_tables(session)
            assert len(tables_before) >= len(EXPECTED_TABLES), f"创建后应有 {len(EXPECTED_TABLES)} 个表"

        # 3. 删除所有表
        async with engine.begin() as conn:
            await conn.execute(text("PRAGMA foreign_keys = OFF"))
            for table in reversed(EXPECTED_TABLES):
                await conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
            await conn.execute(text("PRAGMA foreign_keys = ON"))

        # 4. 验证所有表已删除
        async with AsyncSessionLocal() as session:
            tables_after = await get_all_tables(session)
            assert len(tables_after) == 0, f"所有表应已删除，实际剩余: {tables_after}"

        # 5. 重建所有表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # 6. 验证所有表已重建
        async with AsyncSessionLocal() as session:
            tables_rebuilt = await get_all_tables(session)
            for expected_table in EXPECTED_TABLES:
                assert expected_table in tables_rebuilt, f"表 {expected_table} 应该存在"

    @pytest.mark.asyncio
    async def test_users_table_structure(self, db_session):
        """测试 Users 表结构"""
        columns = await get_table_columns(db_session, "Users")
        column_names = [col["name"] for col in columns]

        for expected_col in USERS_EXPECTED_COLUMNS.keys():
            assert expected_col in column_names, f"Users 表应包含列: {expected_col}"

        id_col = next((c for c in columns if c["name"] == "Id"), None)
        assert id_col is not None, "Id 列应该存在"
        assert id_col["primary_key"], "Id 应该是主键"

    @pytest.mark.asyncio
    async def test_media_items_table_structure(self, db_session):
        """测试 MediaItems 表结构"""
        columns = await get_table_columns(db_session, "MediaItems")
        column_names = [col["name"] for col in columns]

        for expected_col in MEDIAITEMS_KEY_COLUMNS:
            assert expected_col in column_names, f"MediaItems 表应包含列: {expected_col}"

        id_col = next((c for c in columns if c["name"] == "Id"), None)
        assert id_col is not None, "Id 列应该存在"
        assert id_col["primary_key"], "Id 应该是主键"

    @pytest.mark.asyncio
    async def test_files_table_structure(self, db_session):
        """测试 Files 表结构"""
        columns = await get_table_columns(db_session, "Files")
        column_names = [col["name"] for col in columns]

        for expected_col in FILES_KEY_COLUMNS:
            assert expected_col in column_names, f"Files 表应包含列: {expected_col}"

    @pytest.mark.asyncio
    async def test_file_links_table_structure(self, db_session):
        """测试 FileLinks 表结构"""
        columns = await get_table_columns(db_session, "FileLinks")
        column_names = [col["name"] for col in columns]

        expected_cols = ["Id", "ItemId", "FileId", "LinkType", "ImageType", "ImageIndex",
                         "ChapterIndex", "ChapterName", "StartPositionTicks", "MarkerType",
                         "CreatedAt", "UpdatedAt"]
        for expected_col in expected_cols:
            assert expected_col in column_names, f"FileLinks 表应包含列: {expected_col}"

    @pytest.mark.asyncio
    async def test_item_links_table_structure(self, db_session):
        """测试 ItemLinks 表结构"""
        columns = await get_table_columns(db_session, "ItemLinks")
        column_names = [col["name"] for col in columns]

        expected_cols = ["Id", "ItemId", "LinkedItemId", "PeopleType", "PeopleRole",
                         "Order", "CreatedAt", "UpdatedAt"]
        for expected_col in expected_cols:
            assert expected_col in column_names, f"ItemLinks 表应包含列: {expected_col}"

    @pytest.mark.asyncio
    async def test_user_data_table_structure(self, db_session):
        """测试 UserData 表结构"""
        columns = await get_table_columns(db_session, "UserData")
        column_names = [col["name"] for col in columns]

        expected_cols = ["UserId", "ItemId", "PlaybackPositionTicks",
                         "PlayCount", "IsPlayed", "Rating", "PlaybackRate", "LastPlayedAt", "FavoritedAt",
                         "CreatedAt", "UpdatedAt"]
        for expected_col in expected_cols:
            assert expected_col in column_names, f"UserData 表应包含列: {expected_col}"

    @pytest.mark.asyncio
    async def test_aliases_table_structure(self, db_session):
        """测试 Aliases 表结构"""
        columns = await get_table_columns(db_session, "Aliases")
        column_names = [col["name"] for col in columns]

        expected_cols = ["ItemId", "Name", "Source", "CreatedAt", "UpdatedAt"]
        for expected_col in expected_cols:
            assert expected_col in column_names, f"Aliases 表应包含列: {expected_col}"

    @pytest.mark.asyncio
    async def test_users_indexes(self, db_session):
        """测试 Users 表的索引"""
        indexes = await get_table_indexes(db_session, "Users")
        index_names = [idx["name"] for idx in indexes]

        name_indexes = [n for n in index_names if "name" in n.lower()]
        assert len(name_indexes) > 0, "Users 表应有 Name 列的索引"

    @pytest.mark.asyncio
    async def test_media_items_indexes(self, db_session):
        """测试 MediaItems 表的索引"""
        indexes = await get_table_indexes(db_session, "MediaItems")
        index_names = [idx["name"] for idx in indexes]

        type_indexes = [n for n in index_names if "type" in n.lower()]
        assert len(type_indexes) > 0, "MediaItems 表应有 Type 列的索引"

        delete_indexes = [n for n in index_names if "delete" in n.lower()]
        assert len(delete_indexes) > 0, "MediaItems 表应有 IsDeleted 列的索引"

    @pytest.mark.asyncio
    async def test_files_indexes(self, db_session):
        """测试 Files 表的索引"""
        indexes = await get_table_indexes(db_session, "Files")
        index_names = [idx["name"] for idx in indexes]

        path_indexes = [n for n in index_names if "path" in n.lower()]
        assert len(path_indexes) > 0, "Files 表应有 Path 列的索引"

        cloud_indexes = [n for n in index_names if "cloud" in n.lower()]
        assert len(cloud_indexes) > 0, "Files 表应有 CloudId 列的索引"
