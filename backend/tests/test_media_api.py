# coding: utf-8
"""
媒体 API 测试
=============
测试 /api/media 下的所有端点
"""

import pytest
from sqlalchemy import text

from tests.utils.db_helper import (
    query_media_item_by_id,
    count_table_rows,
    query_filelinks_by_item,
    query_itemlinks_by_item,
    query_aliases_by_item,
)


class TestMediaAPI:
    """媒体 API 测试类"""

    @pytest.mark.asyncio
    async def test_get_media_list_empty(self, app_client):
        """测试空数据库获取媒体列表"""
        response = await app_client.get("/api/media/list")
        assert response.status_code == 200
        data = response.json()

        # 验证返回结构
        assert "items" in data, "响应应包含 items"
        assert "total" in data, "响应应包含 total"
        assert "limit" in data, "响应应包含 limit"
        assert "offset" in data, "响应应包含 offset"
        assert data["items"] == [], "空数据库应返回空列表"

    @pytest.mark.asyncio
    async def test_get_media_list_with_data(self, app_client, db_session):
        """测试有数据时获取媒体列表"""
        # 插入测试数据
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, Overview, CommunityRating, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Movie', '测试电影', '这是一部测试电影', 8.5, 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        response = await app_client.get("/api/media/list")
        assert response.status_code == 200
        data = response.json()

        assert len(data["items"]) > 0, "应该返回测试数据"
        assert data["total"] >= 1, "total 应该 >= 1"

    @pytest.mark.asyncio
    async def test_get_media_list_with_types_filter(self, app_client, db_session):
        """测试类型过滤"""
        # 插入 Movie 和 Series 各一个
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Movie', '测试电影', 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Series', '测试剧集', 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        # 只获取 Movie
        response = await app_client.get("/api/media/list?types=Movie")
        assert response.status_code == 200
        data = response.json()

        assert len(data["items"]) == 1, "应该只返回 1 个 Movie"
        assert data["items"][0]["type"] == "Movie", "应该是 Movie 类型"

    @pytest.mark.asyncio
    async def test_get_media_list_pagination(self, app_client, db_session):
        """测试分页"""
        # 插入多个测试数据
        for i in range(15):
            await db_session.execute(text(f"""
                INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
                VALUES ('Movie', '测试电影{i}', 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
            """))
        await db_session.commit()

        # 测试第一页
        response = await app_client.get("/api/media/list?limit=10&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10, "应该返回 10 条"
        assert data["limit"] == 10
        assert data["offset"] == 0

        # 测试第二页
        response = await app_client.get("/api/media/list?limit=10&offset=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 5, "第二页应该返回剩余数据"

    @pytest.mark.asyncio
    async def test_get_media_list_search(self, app_client, db_session):
        """测试搜索功能"""
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Movie', '星际穿越', 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Movie', '盗梦空间', 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        response = await app_client.get("/api/media/list?search=星际")
        assert response.status_code == 200
        data = response.json()

        assert len(data["items"]) == 1, "应该只返回匹配的 1 条"
        assert "星际" in data["items"][0]["name"], "名称应该包含搜索关键词"

    @pytest.mark.asyncio
    async def test_get_media_list_exclude_deleted(self, app_client, db_session):
        """测试排除已删除项"""
        # 插入一个正常项和一个已删除项
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Movie', '正常电影', 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Movie', '已删除电影', 1, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        response = await app_client.get("/api/media/list")
        assert response.status_code == 200
        data = response.json()

        # 验证只返回未删除的
        names = [item["name"] for item in data["items"]]
        assert "正常电影" in names, "应该包含正常电影"
        assert "已删除电影" not in names, "不应该包含已删除电影"

    @pytest.mark.asyncio
    async def test_get_media_info_not_found(self, app_client):
        """测试获取不存在的媒体"""
        response = await app_client.get("/api/media/info?id=99999")
        # 可能返回 404 或空数据，取决于实现
        assert response.status_code in [404, 200]
        if response.status_code == 200:
            data = response.json()
            assert data is None or "detail" in data

    @pytest.mark.asyncio
    async def test_get_media_info_with_valid_id(self, app_client, db_session):
        """测试获取存在的媒体详情"""
        # 插入测试数据
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, Overview, CommunityRating, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Movie', '电影详情测试', '这是测试简介', 9.0, 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        # 获取 ID
        result = await db_session.execute(text("SELECT Id FROM MediaItems WHERE Name = '电影详情测试'"))
        item_id = result.scalar()

        response = await app_client.get(f"/api/media/info?id={item_id}")
        assert response.status_code == 200
        data = response.json()

        # 验证返回数据与数据库一致
        assert data["id"] == item_id
        assert data["name"] == "电影详情测试"
        assert data["overview"] == "这是测试简介"
        assert data["community_rating"] == 9.0

    @pytest.mark.asyncio
    async def test_get_media_stats_empty(self, app_client, auth_headers):
        """测试空数据库的统计"""
        response = await app_client.get("/api/media/stats", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        # 验证统计结构
        expected_fields = ["video_count", "audio_count", "image_count", "subtitle_count",
                           "movie_count", "series_count", "episode_count", "book_count", "source_count"]
        for field in expected_fields:
            assert field in data, f"统计应包含 {field}"

    @pytest.mark.asyncio
    async def test_get_media_stats_with_data(self, app_client, db_session, auth_headers):
        """测试有数据时的统计"""
        # 插入测试文件（Files 表只有 CreatedAt/UpdatedAt，没有 DateCreated/DateModified）
        await db_session.execute(text("""
            INSERT INTO Files (Type, Name, Path, CreatedAt, UpdatedAt)
            VALUES ('Video', 'test.mp4', '/path/test.mp4', datetime('now'), datetime('now'))
        """))
        # 插入测试媒体项
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Movie', '统计测试电影', 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        response = await app_client.get("/api/media/stats", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        # 验证 video_count >= 1
        assert data["video_count"] >= 1, "video_count 应该 >= 1"
        assert data["movie_count"] >= 1, "movie_count 应该 >= 1"

    @pytest.mark.asyncio
    async def test_get_media_stats_database_consistency(self, app_client, db_session, auth_headers):
        """测试统计数据与数据库一致性"""
        # 插入测试数据
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Movie', '一致性测试', 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        # 获取数据库中的实际数量
        result = await db_session.execute(
            text("SELECT COUNT(*) FROM MediaItems WHERE Type = 'Movie' AND IsDeleted = 0")
        )
        db_movie_count = result.scalar()

        # 获取 API 统计
        response = await app_client.get("/api/media/stats", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        # 验证一致性（API 可能返回的是所有类型，不只是 Movie）
        assert data["movie_count"] == db_movie_count, "movie_count 应该与数据库一致"

    @pytest.mark.asyncio
    async def test_media_list_with_links(self, app_client, db_session):
        """测试媒体列表包含关联信息"""
        # 插入测试数据
        await db_session.execute(text("""
            INSERT INTO MediaItems (Type, Name, IsDeleted, DateCreated, DateModified, CreatedAt, UpdatedAt)
            VALUES ('Movie', '关联测试电影', 0, datetime('now'), datetime('now'), datetime('now'), datetime('now'))
        """))
        await db_session.commit()

        response = await app_client.get("/api/media/list?limit=1")
        assert response.status_code == 200
        data = response.json()

        if len(data["items"]) > 0:
            item = data["items"][0]
            # 验证数据结构包含必要字段
            assert "id" in item
            assert "name" in item
            assert "type" in item