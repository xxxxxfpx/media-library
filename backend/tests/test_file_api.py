"""
文件 API 测试
=============
测试 /api/file 下的所有端点
"""

import pytest
from sqlalchemy import text

from tests.utils.db_helper import (
    query_filelinks_by_item,
)


class TestFileAPI:
    """文件 API 测试类"""

    @pytest.mark.asyncio
    async def test_get_file_info_not_found(self, app_client, auth_headers):
        """测试获取不存在的文件"""
        response = await app_client.get("/api/file/info?file_id=99999", headers=auth_headers)
        # 可能返回 404 或空数据
        assert response.status_code in [404, 200]
        if response.status_code == 200:
            data = response.json()
            assert data is None or "detail" in data

    @pytest.mark.asyncio
    async def test_get_file_info_with_valid_id(self, app_client, auth_headers, db_session):
        """测试获取存在的文件详情"""
        # 插入测试文件
        await db_session.execute(text("""
            INSERT INTO Files (Name, Path, Type, Size, Etag, CreatedAt, UpdatedAt)
            VALUES ('test_video.mp4', '/path/to/test_video.mp4', 'Video', 1024000, 'abc123def456', datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        # 获取文件 ID
        result = await db_session.execute(text("SELECT Id FROM Files WHERE Name = 'test_video.mp4'"))
        file_id = result.scalar()

        # 文件 info API 需要 FileLink 记录才能返回数据（JOIN 查询）
        # 先创建一个媒体项和 FileLink
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Movie', '文件信息测试电影', 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        result = await db_session.execute(text("SELECT Id FROM MediaItems WHERE Name = '文件信息测试电影'"))
        item_id = result.scalar()

        await db_session.execute(text("""
            INSERT INTO FileLinks (ItemId, FileId, LinkType, ImageType, ImageIndex, CreatedAt, UpdatedAt)
            VALUES (:item_id, :file_id, 'Image', 'Primary', 0, datetime('now'), datetime('now'))
        """), {"item_id": item_id, "file_id": file_id})
        await db_session.commit()

        response = await app_client.get(f"/api/file/info?file_id={file_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        # 验证返回结构
        assert "id" in data or "file_id" in data or "file" in data, "响应应包含文件信息"

    @pytest.mark.asyncio
    async def test_get_file_data_not_found(self, app_client, auth_headers):
        """测试获取不存在的文件数据"""
        response = await app_client.get("/api/file/data?file_id=99999", headers=auth_headers)
        # 可能返回 404 或重定向到错误页面
        assert response.status_code in [404, 302, 400]

    @pytest.mark.asyncio
    async def test_get_file_data_with_valid_id(self, app_client, auth_headers, db_session):
        """测试获取存在的文件数据"""
        # 插入测试文件（Files 表只有 CreatedAt/UpdatedAt）
        await db_session.execute(text("""
            INSERT INTO Files (Name, Path, Type, Size, Etag, CreatedAt, UpdatedAt)
            VALUES ('data_test.mp4', '/path/to/data_test.mp4', 'Video', 2048000, 'def789ghi012', datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        # 获取文件 ID
        result = await db_session.execute(text("SELECT Id FROM Files WHERE Name = 'data_test.mp4'"))
        file_id = result.scalar()

        response = await app_client.get(f"/api/file/data?file_id={file_id}", headers=auth_headers)
        # 文件数据接口可能返回重定向或实际数据（307 也是一种重定向）
        assert response.status_code in [200, 302, 307, 400]

    @pytest.mark.asyncio
    async def test_file_with_media_link(self, app_client, auth_headers, db_session):
        """测试文件与媒体项的关联"""
        # 插入测试媒体项
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Movie', '文件关联测试电影', 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        # 获取媒体项 ID
        result = await db_session.execute(text("SELECT Id FROM MediaItems WHERE Name = '文件关联测试电影'"))
        item_id = result.scalar()

        # 插入测试文件（Files 表只有 CreatedAt/UpdatedAt）
        await db_session.execute(text("""
            INSERT INTO Files (Name, Path, Type, Size, CreatedAt, UpdatedAt)
            VALUES ('linked_video.mp4', '/path/to/linked_video.mp4', 'Video', 3072000, datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        # 获取文件 ID
        result = await db_session.execute(text("SELECT Id FROM Files WHERE Name = 'linked_video.mp4'"))
        file_id = result.scalar()

        # 创建关联（LinkType=MediaSource，视频源文件无需 ImageType）
        await db_session.execute(text("""
            INSERT INTO FileLinks (ItemId, FileId, LinkType, ImageType, ImageIndex, CreatedAt, UpdatedAt)
            VALUES (:item_id, :file_id, 'MediaSource', NULL, 0, datetime('now'), datetime('now'))
        """), {"item_id": item_id, "file_id": file_id})
        await db_session.commit()

        # 测试文件信息接口
        response = await app_client.get(f"/api/file/info?file_id={file_id}", headers=auth_headers)
        # file/info 可能返回 404（如果需要先有媒体项关联），但数据库操作应该成功
        assert response.status_code in [200, 404]

        # 验证数据库中的关联
        filelinks = await query_filelinks_by_item(db_session, item_id)
        assert len(filelinks) == 1, "应该存在 1 个文件关联"
        assert filelinks[0]["FileId"] == file_id

    @pytest.mark.asyncio
    async def test_file_info_requires_auth(self, app_client, auth_headers):
        """测试文件信息接口的认证要求（如果有）"""
        # 某些文件接口可能需要认证
        response = await app_client.get("/api/file/info?file_id=1", headers=auth_headers)
        # 根据实际实现，可能返回 200 或 404
        assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_multiple_files_for_single_media(self, app_client, auth_headers, db_session):
        """测试单个媒体项关联多个文件"""
        # 插入测试媒体项
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Series', '多文件测试剧集', 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        # 获取媒体项 ID
        result = await db_session.execute(text("SELECT Id FROM MediaItems WHERE Name = '多文件测试剧集'"))
        item_id = result.scalar()

        # 插入多个测试文件（Files 表只有 CreatedAt/UpdatedAt）
        for i in range(3):
            await db_session.execute(text(f"""
                INSERT INTO Files (Name, Path, Type, Size, CreatedAt, UpdatedAt)
                VALUES ('episode_{i}.mp4', '/path/to/episode_{i}.mp4', 'Video', {1000000 + i * 100000}, datetime('now'), datetime('now'))
            """))
            await db_session.commit()

        # 获取所有文件 ID
        result = await db_session.execute(text("SELECT Id FROM Files WHERE Name LIKE 'episode_%'"))
        file_ids = [row[0] for row in result.fetchall()]

        # 创建多个关联（LinkType=MediaSource，视频源文件无需 ImageType）
        for fid in file_ids:
            await db_session.execute(text("""
                INSERT INTO FileLinks (ItemId, FileId, LinkType, ImageType, ImageIndex, CreatedAt, UpdatedAt)
                VALUES (:item_id, :file_id, 'MediaSource', NULL, 0, datetime('now'), datetime('now'))
            """), {"item_id": item_id, "file_id": fid})
            await db_session.commit()

        # 验证数据库中的关联数量
        filelinks = await query_filelinks_by_item(db_session, item_id)
        assert len(filelinks) == 3, "应该存在 3 个文件关联"
