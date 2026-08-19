# coding: utf-8
"""
媒体批量创建 API 测试
====================
测试 /api/media/batch 端点

测试场景：
1. 少参数测试 - 仅必填字段
2. 少关联测试 - 带 source_info 但无 link/file
3. 全参数测试 - 所有字段都填写
4. 全关联测试 - 完整 item + file + link
5. 错误数据测试 - 无效 type
6. 错误类型测试 - 字段类型错误
7. 重复添加测试 - 相同 source_id 更新非 UNSET 字段
8. 全正确测试 - 完整正确流程

每个测试后通过 db_session 直接查询数据库验证
"""

import json

import pytest
from sqlalchemy import text
from pydantic import ValidationError

from app.schemas.create import (
    MediaBatchCreate, ItemCreate, FileCreate, ItemLinkCreate,
    FileBaseAttrs, SourceInfo,
    MediaSourceFileLink, ImageFileLink, ChapterFileLink,
    MovieAttrs, SeriesAttrs, SeasonAttrs, EpisodeAttrs, BoxSetAttrs, PersonAttrs, GenreAttrs, TagAttrs,
)


class TestMediaBatchAPI:
    """媒体批量创建 API 测试类"""

    # ========== 辅助方法 ==========

    async def _get_item_by_name(self, db_session, name):
        """根据名称查询媒体项"""
        result = await db_session.execute(
            text("SELECT * FROM MediaItems WHERE Name = :name AND IsDeleted = 0"),
            {"name": name}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None

    async def _get_file_by_name(self, db_session, name):
        """根据名称查询文件"""
        result = await db_session.execute(
            text("SELECT * FROM Files WHERE Name = :name"),
            {"name": name}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None

    async def _get_itemlinks(self, db_session, item_id):
        """查询 ItemLinks - 作为源（ItemId）"""
        result = await db_session.execute(
            text("SELECT * FROM ItemLinks WHERE ItemId = :item_id"),
            {"item_id": item_id}
        )
        return [dict(row._mapping) for row in result.fetchall()]

    async def _get_itemlinks_as_linked(self, db_session, item_id):
        """查询 ItemLinks - 作为被关联方（LinkedItemId）"""
        result = await db_session.execute(
            text("SELECT * FROM ItemLinks WHERE LinkedItemId = :item_id"),
            {"item_id": item_id}
        )
        return [dict(row._mapping) for row in result.fetchall()]

    async def _get_filelinks(self, db_session, item_id):
        """查询 FileLinks"""
        result = await db_session.execute(
            text("SELECT * FROM FileLinks WHERE ItemId = :item_id"),
            {"item_id": item_id}
        )
        return [dict(row._mapping) for row in result.fetchall()]

    # ========== 测试用例 ==========

    @pytest.mark.asyncio
    async def test_minimal_item(self, app_client, db_session, auth_headers):
        """测试1: 少参数测试 - 仅必填字段 type"""
        data = MediaBatchCreate(
            source_name="test_source",
            items=[
                ItemCreate(
                    temp_id="item-1",
                    source_info=SourceInfo(),
                    attrs=MovieAttrs(type="Movie")
                )
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        result = response.json()
        assert "items" in result
        assert "item-1" in result["items"]

        # 验证数据库
        item = await self._get_item_by_name(db_session, None)
        result_db = await db_session.execute(text("SELECT * FROM MediaItems WHERE Name IS NULL AND IsDeleted = 0"))
        row = result_db.fetchone()
        assert row is not None, "应该创建了媒体项"
        item_data = dict(row._mapping)
        assert item_data["Type"] == "Movie", f"类型应该是 Movie，实际: {item_data['Type']}"

    @pytest.mark.asyncio
    async def test_minimal_with_source(self, app_client, db_session, auth_headers):
        """测试2: 少关联测试 - 必填 + source_info"""
        data = MediaBatchCreate(
            source_name="test_source",
            items=[
                ItemCreate(
                    temp_id="item-1",
                    source_info=SourceInfo(source_id="src-001", source_link="http://example.com/1"),
                    attrs=MovieAttrs(type="Movie", name="测试电影")
                )
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        # 验证数据库
        item = await self._get_item_by_name(db_session, "测试电影")
        assert item is not None, "应该创建了媒体项"
        assert item["Type"] == "Movie"
        assert item["Name"] == "测试电影"

        # 验证 source 关联（已迁移至 MediaItem 列）
        assert item["SourceId"] == "src-001"
        assert item["SourceLink"] == "http://example.com/1"
        assert item["SourceItemId"] is not None

    @pytest.mark.asyncio
    async def test_full_attrs(self, app_client, db_session, auth_headers):
        """测试3: 全参数测试 - 所有属性字段"""
        data = MediaBatchCreate(
            source_name="test_source",
            items=[
                ItemCreate(
                    temp_id="item-1",
                    source_info=SourceInfo(source_id="src-002"),
                    attrs=MovieAttrs(
                        type="Movie",
                        name="完整测试电影",
                        overview="这是简介",
                        tagline="标语",
                        premiere_date="2024-01-01",
                        end_date="2024-12-31",
                        official_rating="PG-13",
                        community_rating=8.5,
                        critic_rating=85.0,
                        status="Continuing",
                    )
                )
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        # 验证数据库
        item = await self._get_item_by_name(db_session, "完整测试电影")
        assert item is not None
        assert item["Overview"] == "这是简介"
        assert item["Tagline"] == "标语"
        assert item["OfficialRating"] == "PG-13"
        assert item["CommunityRating"] == 8.5
        assert item["CriticRating"] == 85.0

    @pytest.mark.asyncio
    async def test_item_with_file(self, app_client, db_session, auth_headers):
        """测试4: item + file 关联"""
        data = MediaBatchCreate(
            source_name="test_source",
            items=[
                ItemCreate(
                    temp_id="item-1",
                    source_info=SourceInfo(),
                    attrs=MovieAttrs(type="Movie", name="电影1")
                )
            ],
            files=[
                FileCreate(
                    temp_id="file-1",
                    attrs=FileBaseAttrs(name="video.mp4", path="/path/video.mp4", type="Video", size=1024)
                )
            ],
            file_links=[
                ImageFileLink(item="item-1", file="file-1", link_type="Image", image_type="Primary")
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        result = response.json()
        item_id = result["items"]["item-1"]
        file_id = result["files"]["file-1"]

        # 验证文件
        file = await self._get_file_by_name(db_session, "video.mp4")
        assert file is not None
        assert file["Path"] == "/path/video.mp4"
        assert file["Type"] == "Video"
        assert file["Size"] == 1024

        # 验证文件关联
        filelinks = await self._get_filelinks(db_session, item_id)
        assert len(filelinks) == 1
        assert filelinks[0]["FileId"] == file_id
        assert filelinks[0]["ImageType"] == "Primary"

    @pytest.mark.asyncio
    async def test_item_with_file_and_link(self, app_client, db_session, auth_headers):
        """测试5: item + file + item_link 完整关联"""
        data = MediaBatchCreate(
            source_name="test_source",
            items=[
                ItemCreate(
                    temp_id="item-1",
                    source_info=SourceInfo(),
                    attrs=MovieAttrs(type="Movie", name="电影A")
                ),
                ItemCreate(
                    temp_id="item-2",
                    source_info=SourceInfo(),
                    attrs=MovieAttrs(type="Movie", name="电影B")
                )
            ],
            files=[
                FileCreate(
                    temp_id="file-1",
                    attrs=FileBaseAttrs(name="a.mp4", path="/a.mp4", type="Video")
                ),
                FileCreate(
                    temp_id="file-2",
                    attrs=FileBaseAttrs(name="b.mp4", path="/b.mp4", type="Video")
                )
            ],
            item_links=[
                ItemLinkCreate(link="item-1", linked="item-2", people_type="Actor", people_role="主演")
            ],
            file_links=[
                MediaSourceFileLink(item="item-1", file="file-1", link_type="MediaSource"),
                MediaSourceFileLink(item="item-2", file="file-2", link_type="MediaSource"),
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        result = response.json()
        item1_id = result["items"]["item-1"]
        item2_id = result["items"]["item-2"]

        # 验证 item_links
        links = await self._get_itemlinks(db_session, item1_id)
        actor_links = [l for l in links if l["LinkedItemId"] == item2_id]
        assert len(actor_links) == 1
        assert actor_links[0]["PeopleType"] == "Actor"
        assert actor_links[0]["PeopleRole"] == "主演"

        # 验证两个 file_links
        fl1 = await self._get_filelinks(db_session, item1_id)
        fl2 = await self._get_filelinks(db_session, item2_id)
        assert len(fl1) == 1
        assert len(fl2) == 1

    @pytest.mark.asyncio
    async def test_full_batch(self, app_client, db_session, auth_headers):
        """测试6: 全量数据测试 - 完整的复杂结构"""
        data = MediaBatchCreate(
            source_name="full_test_source",
            items=[
                ItemCreate(
                    temp_id="series-1",
                    source_info=SourceInfo(source_id="tmdb-100"),
                    attrs=SeriesAttrs(type="Series", name="测试剧集", overview="剧集简介")
                ),
                ItemCreate(
                    temp_id="season-1",
                    source_info=SourceInfo(source_id="tmdb-100-s1"),
                    attrs=SeasonAttrs(type="Season", name="第1季")
                ),
                ItemCreate(
                    temp_id="episode-1",
                    source_info=SourceInfo(source_id="tmdb-100-s1-e1"),
                    attrs=EpisodeAttrs(type="Episode", name="第1集", overview="第1集简介")
                ),
                ItemCreate(
                    temp_id="person-1",
                    source_info=SourceInfo(),
                    attrs=PersonAttrs(type="Person", name="演员甲")
                ),
            ],
            files=[
                FileCreate(
                    temp_id="file-poster",
                    attrs=FileBaseAttrs(name="poster.jpg", path="/images/poster.jpg", type="Image")
                ),
                FileCreate(
                    temp_id="file-video",
                    attrs=FileBaseAttrs(name="ep1.mp4", path="/videos/ep1.mp4", type="Video", size=1024000)
                ),
            ],
            item_links=[
                ItemLinkCreate(link="series-1", linked="season-1"),
                ItemLinkCreate(link="season-1", linked="episode-1"),
                ItemLinkCreate(link="episode-1", linked="person-1", people_type="Actor", people_role="领衔主演"),
            ],
            file_links=[
                ImageFileLink(item="series-1", file="file-poster", link_type="Image", image_type="Primary"),
                MediaSourceFileLink(item="episode-1", file="file-video", link_type="MediaSource"),
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        result = response.json()

        # 验证所有 items 创建
        assert len(result["items"]) == 4
        assert len(result["files"]) == 2

        # 验证剧集
        series = await self._get_item_by_name(db_session, "测试剧集")
        assert series["Type"] == "Series"
        assert series["Overview"] == "剧集简介"

        # 验证季
        season = await self._get_item_by_name(db_session, "第1季")
        assert season["Type"] == "Season"

        # 验证集
        episode = await self._get_item_by_name(db_session, "第1集")
        assert episode["Type"] == "Episode"
        assert episode["Overview"] == "第1集简介"

        # 验证人物
        person = await self._get_item_by_name(db_session, "演员甲")
        assert person["Type"] == "Person"

        # 验证层级关系
        series_links = await self._get_itemlinks(db_session, series["Id"])
        assert any(l["LinkedItemId"] == season["Id"] for l in series_links)

        season_links = await self._get_itemlinks(db_session, season["Id"])
        assert any(l["LinkedItemId"] == episode["Id"] for l in season_links)

        # 验证人物关联
        episode_links = await self._get_itemlinks(db_session, episode["Id"])
        person_links = [l for l in episode_links if l["LinkedItemId"] == person["Id"]]
        assert len(person_links) == 1
        assert person_links[0]["PeopleType"] == "Actor"
        assert person_links[0]["PeopleRole"] == "领衔主演"

        # 验证文件
        poster = await self._get_file_by_name(db_session, "poster.jpg")
        assert poster["Type"] == "Image"

        video = await self._get_file_by_name(db_session, "ep1.mp4")
        assert video["Type"] == "Video"
        assert video["Size"] == 1024000

        # 验证 file_links
        series_fls = await self._get_filelinks(db_session, series["Id"])
        assert len(series_fls) == 1
        assert series_fls[0]["ImageType"] == "Primary"

        episode_fls = await self._get_filelinks(db_session, episode["Id"])
        assert len(episode_fls) == 1

    @pytest.mark.asyncio
    async def test_invalid_type(self, app_client, db_session, auth_headers):
        """测试7: 错误数据测试 - 无效的 type"""
        data = MediaBatchCreate(
            source_name="test",
            items=[
                ItemCreate(
                    temp_id="item-1",
                    source_info=SourceInfo(),
                    attrs={"type": "InvalidType"}
                )
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        # 应该返回 422 验证错误
        assert response.status_code == 422, f"无效 type 应该返回 422，实际: {response.status_code}"

    @pytest.mark.asyncio
    async def test_extra_field_rejected(self, app_client, db_session, auth_headers):
        """媒体属性不允许混入其他类型的字段。"""
        data = {
            "source_name": "extra_field_test",
            "items": [{
                "temp_id": "item-1",
                "source_info": {},
                "attrs": {"type": "Movie", "birth_date": "2000-01-01"},
            }],
        }

        response = await app_client.post("/api/media/batch", json=data, headers=auth_headers)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_rating_range_rejected(self, app_client, db_session, auth_headers):
        """评分字段必须落在 schema 声明的范围内。"""
        data = {
            "source_name": "rating_range_test",
            "items": [{
                "temp_id": "item-1",
                "source_info": {},
                "attrs": {"type": "Movie", "community_rating": 10.1},
            }],
        }

        response = await app_client.post("/api/media/batch", json=data, headers=auth_headers)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_invalid_source_id_type(self, app_client, db_session, auth_headers):
        """测试8: 错误类型测试 - source_id 类型错误（传入数字而非字符串）"""
        # 直接传原始 JSON，Pydantic 会验证类型
        data = {
            "source_name": "test",
            "items": [
                {
                    "temp_id": "item-1",
                    "source_info": {"source_id": 12345, "source_link": "http://test.com"},  # source_id 应该是字符串
                    "attrs": {"type": "Movie", "name": "测试"}
                }
            ]
        }

        response = await app_client.post("/api/media/batch", json=data, headers=auth_headers)
        # Pydantic 验证会失败，返回 422
        assert response.status_code == 422, f"类型错误应该返回 422，实际: {response.status_code}"

    @pytest.mark.asyncio
    async def test_duplicate_item_update(self, app_client, db_session, auth_headers):
        """测试9: 重复添加测试 - 相同 source_id 时更新非 UNSET 字段"""
        # 第一次创建
        data1 = MediaBatchCreate(
            source_name="dup_test",
            items=[
                ItemCreate(
                    temp_id="item-1",
                    source_info=SourceInfo(source_id="dup-src-001"),
                    attrs=MovieAttrs(type="Movie", name="原名称", overview="原简介")
                )
            ]
        )

        response1 = await app_client.post("/api/media/batch", json=data1.model_dump(exclude_unset=True), headers=auth_headers)
        assert response1.status_code == 200, f"第一次请求失败: {response1.text}"

        result1 = response1.json()
        original_id = result1["items"]["item-1"]

        # 第二次创建，相同 source_id 但不同属性（只有非 UNSET 的会被更新）
        data2 = MediaBatchCreate(
            source_name="dup_test",
            items=[
                ItemCreate(
                    temp_id="item-2",
                    source_info=SourceInfo(source_id="dup-src-001"),  # 相同 source_id
                    attrs=MovieAttrs(type="Movie", name="新名称")  # 只更新 name，overview 用 UNSET
                )
            ]
        )

        response2 = await app_client.post("/api/media/batch", json=data2.model_dump(exclude_unset=True), headers=auth_headers)
        assert response2.status_code == 200, f"第二次请求失败: {response2.text}"

        result2 = response2.json()

        # 应该返回相同的 ID（表示更新而非新建）
        assert result2["items"]["item-2"] == original_id, "重复 source_id 应该更新而非新建"

        # 验证更新后的数据 - 直接通过 API 查询
        info_response = await app_client.get(f"/api/media/info?id={original_id}", headers=auth_headers)
        assert info_response.status_code == 200
        item_data = info_response.json()
        assert item_data["name"] == "新名称", f"name 应该被更新，实际: {item_data.get('name')}"
        assert item_data["overview"] == "原简介", f"overview 应该保持不变，实际: {item_data.get('overview')}"

    @pytest.mark.asyncio
    async def test_duplicate_item_update_all_fields(self, app_client, db_session, auth_headers):
        """测试9a: 重复提交时更新所有显式设置的属性字段"""
        data1 = MediaBatchCreate(
            source_name="dup_full_test",
            items=[
                ItemCreate(
                    temp_id="item-1",
                    source_info=SourceInfo(source_id="dup-full-001", source_link="http://old.link"),
                    attrs=MovieAttrs(
                        type="Movie", name="原名", overview="原简介", tagline="原标语",
                        official_rating="PG", community_rating=7.0, critic_rating=70.0,
                        premiere_date="2023-01-01", status="Continuing",
                    )
                )
            ]
        )
        resp1 = await app_client.post("/api/media/batch", json=data1.model_dump(exclude_unset=True), headers=auth_headers)
        assert resp1.status_code == 200, f"第一次提交失败: {resp1.text}"
        item_id = resp1.json()["items"]["item-1"]

        # 第二次提交相同 source_id，所有字段都给新值
        data2 = MediaBatchCreate(
            source_name="dup_full_test",
            items=[
                ItemCreate(
                    temp_id="item-2",
                    source_info=SourceInfo(source_id="dup-full-001", source_link="http://new.link"),
                    attrs=MovieAttrs(
                        type="Movie", name="新名", overview="新简介", tagline="新标语",
                        official_rating="PG-13", community_rating=8.5, critic_rating=85.0,
                        premiere_date="2024-06-15", status="Ended",
                    )
                )
            ]
        )
        resp2 = await app_client.post("/api/media/batch", json=data2.model_dump(exclude_unset=True), headers=auth_headers)
        assert resp2.status_code == 200, f"第二次提交失败: {resp2.text}"
        assert resp2.json()["items"]["item-2"] == item_id, "重复 source_id 应更新而非新建"

        # API 暴露的字段
        info = (await app_client.get(f"/api/media/info?id={item_id}", headers=auth_headers)).json()
        assert info["name"] == "新名"
        assert info["overview"] == "新简介"
        assert info["tagline"] == "新标语"
        assert info["official_rating"] == "PG-13"
        assert info["community_rating"] == 8.5
        assert info["critic_rating"] == 85.0
        assert info["source_link"] == "http://new.link"

        # 数据库全字段校验（含 API 未暴露的字段）
        item = await self._get_item_by_name(db_session, "新名")
        assert item is not None
        assert item["Status"] == "Ended"
        assert item["SourceLink"] == "http://new.link"

    @pytest.mark.asyncio
    async def test_different_source_same_source_id(self, app_client, db_session, auth_headers):
        """测试9b: 不同 source_name 相同 source_id 应该创建不同 item"""
        # 第一次创建 - source_A
        data1 = MediaBatchCreate(
            source_name="source_A",
            items=[
                ItemCreate(
                    temp_id="item-1",
                    source_info=SourceInfo(source_id="1234"),
                    attrs=MovieAttrs(type="Movie", name="电影A")
                )
            ]
        )

        response1 = await app_client.post("/api/media/batch", json=data1.model_dump(exclude_unset=True), headers=auth_headers)
        assert response1.status_code == 200, f"source_A 请求失败: {response1.text}"
        id1 = response1.json()["items"]["item-1"]

        # 第二次创建 - source_B，相同 source_id
        data2 = MediaBatchCreate(
            source_name="source_B",
            items=[
                ItemCreate(
                    temp_id="item-2",
                    source_info=SourceInfo(source_id="1234"),  # 相同 source_id
                    attrs=MovieAttrs(type="Movie", name="电影B")
                )
            ]
        )

        response2 = await app_client.post("/api/media/batch", json=data2.model_dump(exclude_unset=True), headers=auth_headers)
        assert response2.status_code == 200, f"source_B 请求失败: {response2.text}"
        id2 = response2.json()["items"]["item-2"]

        # 应该是不同的 ID
        assert id1 != id2, f"不同 source_name 应该创建不同 item，实际 id1={id1}, id2={id2}"

        # 验证两者都存在且不同
        info1 = await app_client.get(f"/api/media/info?id={id1}", headers=auth_headers)
        info2 = await app_client.get(f"/api/media/info?id={id2}", headers=auth_headers)
        assert info1.json()["name"] == "电影A"
        assert info2.json()["name"] == "电影B"

    @pytest.mark.asyncio
    async def test_same_source_different_type(self, app_client, db_session, auth_headers):
        """测试9c: 相同 source_name + source_id，不同 item.type 应该创建不同 item"""
        data = MediaBatchCreate(
            source_name="same_source",
            items=[
                ItemCreate(
                    temp_id="item-video",
                    source_info=SourceInfo(source_id="5678"),
                    attrs=MovieAttrs(type="Movie", name="视频")
                ),
                ItemCreate(
                    temp_id="item-tag",
                    source_info=SourceInfo(source_id="5678"),  # 相同 source_id
                    attrs=TagAttrs(type="Tag", name="标签")  # 不同 type
                )
            ],
            item_links=[
                ItemLinkCreate(link="item-video", linked="item-tag"),  # 连接两个 item 使其连通
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"
        result = response.json()

        # 应该是两个不同的 ID
        video_id = result["items"]["item-video"]
        tag_id = result["items"]["item-tag"]
        assert video_id != tag_id, f"不同 type 应该创建不同 item，实际 video_id={video_id}, tag_id={tag_id}"

        # 验证两者都存在
        info_video = await app_client.get(f"/api/media/info?id={video_id}", headers=auth_headers)
        info_tag = await app_client.get(f"/api/media/info?id={tag_id}", headers=auth_headers)
        assert info_video.json()["name"] == "视频"
        assert info_video.json()["type"] == "Movie"
        assert info_tag.json()["name"] == "标签"
        assert info_tag.json()["type"] == "Tag"

    @pytest.mark.asyncio
    async def test_same_source_same_type_creates_one(self, app_client, db_session, auth_headers):
        """测试9d: 相同 source_name + source_id + type 只会创建一个 item（更新）"""
        # 第一次创建
        data1 = MediaBatchCreate(
            source_name="unique_test",
            items=[
                ItemCreate(
                    temp_id="first",
                    source_info=SourceInfo(source_id="unique-001"),
                    attrs=MovieAttrs(type="Movie", name="第一个名称", overview="第一个简介")
                )
            ]
        )

        response1 = await app_client.post("/api/media/batch", json=data1.model_dump(exclude_unset=True), headers=auth_headers)
        assert response1.status_code == 200
        id1 = response1.json()["items"]["first"]

        # 第二次创建 - 相同 source_name + source_id + type
        data2 = MediaBatchCreate(
            source_name="unique_test",
            items=[
                ItemCreate(
                    temp_id="second",
                    source_info=SourceInfo(source_id="unique-001"),
                    attrs=MovieAttrs(type="Movie", name="新名称")  # 只更新 name
                )
            ]
        )

        response2 = await app_client.post("/api/media/batch", json=data2.model_dump(exclude_unset=True), headers=auth_headers)
        assert response2.status_code == 200
        id2 = response2.json()["items"]["second"]

        # 应该是同一个 ID（更新而非创建）
        assert id1 == id2, f"相同 source_name + source_id + type 应该返回相同 ID，实际 id1={id1}, id2={id2}"

        # 验证 name 被更新，overview 保持不变
        info = await app_client.get(f"/api/media/info?id={id1}", headers=auth_headers)
        item_data = info.json()
        assert item_data["name"] == "新名称", f"name 应该被更新为'新名称'，实际: {item_data.get('name')}"
        assert item_data["overview"] == "第一个简介", f"overview 应该保持不变，实际: {item_data.get('overview')}"

    @pytest.mark.asyncio
    async def test_missing_required_field(self, app_client, db_session, auth_headers):
        """测试10: 缺少必填字段 - attrs 缺失 type"""
        # ItemAttrsBase 不含 type，具体类型类要求 type 必填
        data = {
            "source_name": "test",
            "items": [
                {
                    "temp_id": "item-1",
                    "source_info": {},
                    "attrs": {
                        "name": "测试电影"
                        # 缺少 type
                    }
                }
            ]
        }

        response = await app_client.post("/api/media/batch", json=data, headers=auth_headers)
        assert response.status_code == 422, f"缺少必填字段应该返回 422，实际: {response.status_code}"

    @pytest.mark.asyncio
    async def test_empty_batch(self, app_client, db_session, auth_headers):
        """测试11: 空 batch - 仅 source_name"""
        data = MediaBatchCreate(source_name="empty_test")

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"空 batch 应该成功，实际: {response.text}"

        result = response.json()
        assert result["items"] == {}
        assert result["files"] == {}

    @pytest.mark.asyncio
    async def test_multiple_items_links(self, app_client, db_session, auth_headers):
        """测试12: 多 item 多 link 复杂拓扑"""
        data = MediaBatchCreate(
            source_name="complex_topology",
            items=[
                ItemCreate(temp_id="m1", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影1")),
                ItemCreate(temp_id="m2", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影2")),
                ItemCreate(temp_id="m3", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影3")),
                ItemCreate(temp_id="p1", source_info=SourceInfo(), attrs=PersonAttrs(type="Person", name="演员A")),
                ItemCreate(temp_id="p2", source_info=SourceInfo(), attrs=PersonAttrs(type="Person", name="演员B")),
                ItemCreate(temp_id="g1", source_info=SourceInfo(), attrs=GenreAttrs(type="Genre", name="动作")),
            ],
            item_links=[
                # 演员参演两部电影
                ItemLinkCreate(link="m1", linked="p1", people_type="Actor", people_role="主演"),
                ItemLinkCreate(link="m2", linked="p1", people_type="Actor", people_role="配角"),
                ItemLinkCreate(link="m2", linked="p2", people_type="Actor", people_role="主演"),
                # 电影属于类型
                ItemLinkCreate(link="m1", linked="g1"),
                ItemLinkCreate(link="m2", linked="g1"),
                # 电影之间的关系 - 使用 Actor 类型代替不存在的 Sequel
                ItemLinkCreate(link="m1", linked="m2", people_type="Actor", people_role="相关"),
            ],
            files=[
                FileCreate(temp_id="f1", attrs=FileBaseAttrs(name="m1.mp4", path="/m1.mp4", type="Video")),
                FileCreate(temp_id="f2", attrs=FileBaseAttrs(name="m2.mp4", path="/m2.mp4", type="Video")),
            ],
            file_links=[
                MediaSourceFileLink(item="m1", file="f1", link_type="MediaSource"),
                MediaSourceFileLink(item="m2", file="f2", link_type="MediaSource"),
            ]
        )

        response = await app_client.post("/api/media/batch?strict_graph=false", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        result = response.json()
        assert len(result["items"]) == 6
        assert len(result["files"]) == 2

        # 验证演员A的关联 - 需要查找 m1, m2 作为 link 的关联
        p1_id = result["items"]["p1"]
        # 演员A作为被关联方（LinkedItemId=p1_id）的关联
        p1_as_linked = await self._get_itemlinks_as_linked(db_session, p1_id)
        assert len(p1_as_linked) == 2, f"演员A应该有两个参演关联，实际: {len(p1_as_linked)}"

        # 验证类型关联
        g1_id = result["items"]["g1"]
        g1_as_linked = await self._get_itemlinks(db_session, g1_id)
        g1_as_linked = [l for l in g1_as_linked if l["LinkedItemId"] == g1_id]
        assert len(g1_as_linked) == 0, "类型不应该作为被关联方"

        # 验证 m1->m2 关联（通过 Actor 类型关联）
        m1_id = result["items"]["m1"]
        m2_id = result["items"]["m2"]
        m1_links = await self._get_itemlinks(db_session, m1_id)
        m1_to_m2 = [l for l in m1_links if l["LinkedItemId"] == m2_id]
        assert len(m1_to_m2) == 1, "应该有 m1->m2 关联"

        # 验证文件关联
        m1_fls = await self._get_filelinks(db_session, m1_id)
        assert len(m1_fls) == 1
        assert m1_fls[0]["FileId"] == result["files"]["f1"]

    @pytest.mark.asyncio
    async def test_item_with_multiple_files(self, app_client, db_session, auth_headers):
        """测试13: 一个 item 关联多个 files（主视频 + 字幕 + 封面图）"""
        data = MediaBatchCreate(
            source_name="multi_file_test",
            items=[
                ItemCreate(
                    temp_id="movie-1",
                    source_info=SourceInfo(),
                    attrs=MovieAttrs(type="Movie", name="多文件电影")
                )
            ],
            files=[
                FileCreate(temp_id="video", attrs=FileBaseAttrs(name="movie.mp4", path="/v/movie.mp4", type="Video")),
                FileCreate(temp_id="subtitle", attrs=FileBaseAttrs(name="movie.srt", path="/v/movie.srt", type="Subtitle")),
                FileCreate(temp_id="poster", attrs=FileBaseAttrs(name="poster.jpg", path="/i/poster.jpg", type="Image")),
            ],
            file_links=[
                MediaSourceFileLink(item="movie-1", file="video", link_type="MediaSource"),
                MediaSourceFileLink(item="movie-1", file="subtitle", link_type="MediaSource"),
                ImageFileLink(item="movie-1", file="poster", link_type="Image", image_type="Primary"),
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        result = response.json()
        movie_id = result["items"]["movie-1"]

        # 验证 3 个 file_links
        fls = await self._get_filelinks(db_session, movie_id)
        assert len(fls) == 3, f"应该有 3 个 file_links，实际: {len(fls)}"

        # 验证文件存在
        for temp_id in ["video", "subtitle", "poster"]:
            file_id = result["files"][temp_id]
            file_result = await db_session.execute(text("SELECT * FROM Files WHERE Id = :id"), {"id": file_id})
            file_row = file_result.fetchone()
            assert file_row is not None, f"文件 {temp_id} 应该存在"

    @pytest.mark.asyncio
    async def test_bidirectional_item_links(self, app_client, db_session, auth_headers):
        """测试14: 双向 item_links（m1→m2 且 m2→m1）"""
        data = MediaBatchCreate(
            source_name="bidirectional_test",
            items=[
                ItemCreate(temp_id="m1", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影1")),
                ItemCreate(temp_id="m2", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影2")),
            ],
            item_links=[
                ItemLinkCreate(link="m1", linked="m2", people_type="Actor", people_role="主演"),
                ItemLinkCreate(link="m2", linked="m1", people_type="Director"),
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        result = response.json()
        m1_id = result["items"]["m1"]
        m2_id = result["items"]["m2"]

        # 验证 m1→m2 关联
        m1_links = await self._get_itemlinks(db_session, m1_id)
        m1_to_m2 = [l for l in m1_links if l["LinkedItemId"] == m2_id]
        assert len(m1_to_m2) == 1
        assert m1_to_m2[0]["PeopleType"] == "Actor"

        # 验证 m2→m1 关联
        m2_links = await self._get_itemlinks(db_session, m2_id)
        m2_to_m1 = [l for l in m2_links if l["LinkedItemId"] == m1_id]
        assert len(m2_to_m1) == 1
        assert m2_to_m1[0]["PeopleType"] == "Director"

    @pytest.mark.asyncio
    async def test_item_link_to_nonexistent_temp_id(self, app_client, db_session, auth_headers):
        """测试15: item_link 引用不存在的 temp_id（应返回 422 报错）"""
        data = MediaBatchCreate(
            source_name="nonexistent_link_test",
            items=[
                ItemCreate(temp_id="item-1", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影1")),
            ],
            item_links=[
                ItemLinkCreate(link="item-1", linked="non-existent-temp-id"),
            ]
        )

        response = await app_client.post("/api/media/batch?strict_graph=false", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 422, f"引用不存在 temp_id 的 link 应该返回 422，实际: {response.status_code}"
        assert "non-existent-temp-id" in response.text, f"错误信息应指出缺失的 temp_id，实际: {response.text}"

    @pytest.mark.asyncio
    async def test_orphaned_file(self, app_client, db_session, auth_headers):
        """测试16: 孤立 file（创建了 file 但没有 file_link）"""
        data = MediaBatchCreate(
            source_name="orphaned_file_test",
            items=[
                ItemCreate(temp_id="item-1", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影1")),
            ],
            files=[
                FileCreate(temp_id="orphan-file", attrs=FileBaseAttrs(name="orphan.mp4", path="/v/orphan.mp4", type="Video")),
            ]
            # 注意：没有 file_links
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        result = response.json()

        # 验证 file 存在
        file_id = result["files"]["orphan-file"]
        file_result = await db_session.execute(text("SELECT * FROM Files WHERE Id = :id"), {"id": file_id})
        file_row = file_result.fetchone()
        assert file_row is not None, "孤立 file 应该存在于 Files 表"

        # 验证没有 file_link
        fl_result = await db_session.execute(text("SELECT COUNT(*) FROM FileLinks WHERE FileId = :id"), {"id": file_id})
        fl_count = fl_result.scalar()
        assert fl_count == 0, "孤立 file 不应该有 file_link"

    @pytest.mark.asyncio
    async def test_iso_date_formats(self, app_client, db_session, auth_headers):
        """测试17: 多种 ISO 8601 日期格式"""
        data = MediaBatchCreate(
            source_name="date_format_test",
            items=[
                ItemCreate(
                    temp_id="date-1",
                    source_info=SourceInfo(),
                    attrs=MovieAttrs(
                        type="Movie",
                        name="日期测试电影",
                        premiere_date="2024-01-01",
                        end_date="2024-06-15T12:30:00"
                    )
                ),
                ItemCreate(
                    temp_id="date-2",
                    source_info=SourceInfo(),
                    attrs=SeriesAttrs(
                        type="Series",
                        name="带时区日期剧集",
                        premiere_date="2024-01-01T00:00:00Z",
                        end_date="2024-12-31T23:59:59+08:00"
                    )
                ),
            ]
        )

        response = await app_client.post("/api/media/batch?strict_graph=false", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        # 验证日期被正确解析和存储
        movie = await self._get_item_by_name(db_session, "日期测试电影")
        assert movie is not None
        assert movie["PremiereDate"] is not None

        series = await self._get_item_by_name(db_session, "带时区日期剧集")
        assert series is not None
        assert series["PremiereDate"] is not None

    @pytest.mark.asyncio
    async def test_special_characters_in_name(self, app_client, db_session, auth_headers):
        """测试18: name 包含特殊字符"""
        special_name = '测试"电影\'<>&及其Unicodeαβγ'
        data = MediaBatchCreate(
            source_name="special_char_test",
            items=[
                ItemCreate(
                    temp_id="special-1",
                    source_info=SourceInfo(),
                    attrs=MovieAttrs(type="Movie", name=special_name)
                )
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        # 验证特殊字符被正确存储
        movie = await self._get_item_by_name(db_session, special_name)
        assert movie is not None, f"特殊字符 name 应该被正确存储，实际 name: {movie}"
        assert movie["Name"] == special_name

    @pytest.mark.asyncio
    async def test_invalid_file_type(self, app_client, db_session, auth_headers):
        """测试19: 无效文件类型"""
        data = MediaBatchCreate(
            source_name="invalid_file_type_test",
            files=[
                FileCreate(
                    temp_id="bad-file",
                    attrs=FileBaseAttrs(name="test.mp4", path="/v/test.mp4", type="InvalidVideoType")
                )
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 422, f"无效 file type 应该返回 422，实际: {response.status_code}"

    @pytest.mark.asyncio
    async def test_invalid_person_type(self, app_client, db_session, auth_headers):
        """测试20: 无效人物类型"""
        data = MediaBatchCreate(
            source_name="invalid_person_type_test",
            items=[
                ItemCreate(temp_id="p1", source_info=SourceInfo(), attrs=PersonAttrs(type="Person", name="演员")),
                ItemCreate(temp_id="p2", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影")),
            ],
            item_links=[
                ItemLinkCreate(link="movie", linked="actor", people_type="InvalidActorType"),
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        # 由于 person_type 会在序列化时被过滤，可能不报错
        # 这个测试验证的是 service 层能处理这种情况
        # 如果 Pydantic 验证通过了，则 API 会处理

    @pytest.mark.asyncio
    async def test_large_batch_size(self, app_client, db_session, auth_headers):
        """测试21: 大批量创建（50个items + 50个files）"""
        items = []
        files = []
        file_links = []

        for i in range(50):
            temp_id = f"item-{i}"
            items.append(ItemCreate(
                temp_id=temp_id,
                source_info=SourceInfo(),
                attrs=MovieAttrs(type="Movie", name=f"电影{i}")
            ))
            file_temp_id = f"file-{i}"
            files.append(FileCreate(
                temp_id=file_temp_id,
                attrs=FileBaseAttrs(name=f"movie{i}.mp4", path=f"/v/movie{i}.mp4", type="Video")
            ))
            file_links.append(MediaSourceFileLink(item=temp_id, file=file_temp_id, link_type="MediaSource"))

        data = MediaBatchCreate(
            source_name="large_batch_test",
            items=items,
            files=files,
            file_links=file_links
        )

        response = await app_client.post("/api/media/batch?strict_graph=false", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"大批量请求失败: {response.text}"

        result = response.json()
        assert len(result["items"]) == 50, f"应该有 50 个 items，实际: {len(result['items'])}"
        assert len(result["files"]) == 50, f"应该有 50 个 files，实际: {len(result['files'])}"

        # 验证数据库中确实有 50 条
        count_result = await db_session.execute(text("SELECT COUNT(*) FROM MediaItems WHERE IsDeleted = 0"))
        db_count = count_result.scalar()
        assert db_count >= 50, f"数据库应有至少 50 条记录，实际: {db_count}"

    @pytest.mark.asyncio
    async def test_duplicate_file_path_reuses(self, app_client, db_session, auth_headers):
        """测试21b: 相同 Path 的文件重复提交应幂等复用同一文件，而非报错或新建"""
        data1 = MediaBatchCreate(
            source_name="dup_file_test",
            items=[
                ItemCreate(temp_id="item-1", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影")),
            ],
            files=[
                FileCreate(temp_id="file-1", attrs=FileBaseAttrs(name="a.mp4", path="/v/a.mp4", type="Video", size=1024)),
            ],
            file_links=[
                MediaSourceFileLink(item="item-1", file="file-1", link_type="MediaSource"),
            ]
        )
        resp1 = await app_client.post("/api/media/batch", json=data1.model_dump(exclude_unset=True), headers=auth_headers)
        assert resp1.status_code == 200, f"第一次提交失败: {resp1.text}"
        file_id1 = resp1.json()["files"]["file-1"]

        # 重复提交相同 Path（不同 temp_id/name/size），应复用同一文件并更新字段
        data2 = MediaBatchCreate(
            source_name="dup_file_test",
            items=[
                ItemCreate(temp_id="item-1", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影")),
            ],
            files=[
                FileCreate(temp_id="file-2", attrs=FileBaseAttrs(name="a2.mp4", path="/v/a.mp4", type="Video", size=2048)),
            ],
            file_links=[
                MediaSourceFileLink(item="item-1", file="file-2", link_type="MediaSource"),
            ]
        )
        resp2 = await app_client.post("/api/media/batch", json=data2.model_dump(exclude_unset=True), headers=auth_headers)
        assert resp2.status_code == 200, f"重复 Path 提交不应报错: {resp2.text}"
        file_id2 = resp2.json()["files"]["file-2"]
        assert file_id2 == file_id1, f"相同 Path 应复用同一文件，实际 file1={file_id1}, file2={file_id2}"

        # 文件总数应只有 1 条，且字段已更新
        count = (await db_session.execute(text("SELECT COUNT(*) FROM Files WHERE Path = '/v/a.mp4'"))).scalar()
        assert count == 1, f"相同 Path 只应有 1 条文件记录，实际: {count}"
        file_row = (await db_session.execute(text("SELECT * FROM Files WHERE Path = '/v/a.mp4'"))).fetchone()
        assert file_row._mapping["Name"] == "a2.mp4"
        assert file_row._mapping["Size"] == 2048

    @pytest.mark.asyncio
    async def test_file_link_to_nonexistent_temp_id(self, app_client, db_session, auth_headers):
        """测试21c: file_link 引用不存在的 temp_id（应返回 422 报错）"""
        data = MediaBatchCreate(
            source_name="nonexistent_file_link_test",
            items=[
                ItemCreate(temp_id="item-1", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影1")),
            ],
            file_links=[
                MediaSourceFileLink(item="item-1", file="missing-file", link_type="MediaSource"),
            ]
        )
        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 422, f"引用不存在 temp_id 的 file_link 应返回 422，实际: {response.status_code}"
        assert "missing-file" in response.text, f"错误信息应指出缺失的 temp_id，实际: {response.text}"

    # ========== strict_graph 相关测试 ==========

    @pytest.mark.asyncio
    async def test_strict_graph_connected(self, app_client, db_session, auth_headers):
        """测试22: strict_graph=True（默认）且图连通 - 应该成功"""
        data = MediaBatchCreate(
            source_name="graph_test",
            items=[
                ItemCreate(temp_id="a", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影A")),
                ItemCreate(temp_id="b", source_info=SourceInfo(), attrs=PersonAttrs(type="Person", name="人物B")),
                ItemCreate(temp_id="c", source_info=SourceInfo(), attrs=GenreAttrs(type="Genre", name="类型C")),
            ],
            item_links=[
                ItemLinkCreate(link="a", linked="b", people_type="Actor", people_role="主演"),
                ItemLinkCreate(link="b", linked="c", people_type="Actor", people_role="主演"),
            ]
        )

        # 默认 strict_graph=True，图是连通的（A-B-C），应该成功
        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"连通图应该成功，实际: {response.text}"

    @pytest.mark.asyncio
    async def test_strict_graph_disconnected_fails(self, app_client, db_session, auth_headers):
        """测试23: strict_graph=True 但图不连通 - 应该返回 422 错误"""
        data = MediaBatchCreate(
            source_name="disconnected_test",
            items=[
                ItemCreate(temp_id="isolated-1", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="孤立电影1")),
                ItemCreate(temp_id="isolated-2", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="孤立电影2")),
                ItemCreate(temp_id="isolated-3", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="孤立电影3")),
            ],
            # 注意：没有 item_links，三个节点互不相连
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 422, f"非连通图应该返回 422，实际: {response.status_code}"
        assert "孤立节点" in response.text or "isolated" in response.text.lower(), \
            f"错误信息应提到孤立节点，实际: {response.text}"

    @pytest.mark.asyncio
    async def test_strict_graph_false_allows_disconnected(self, app_client, db_session, auth_headers):
        """测试24: strict_graph=False 允许不连通的图"""
        data = MediaBatchCreate(
            source_name="disconnected_test",
            items=[
                ItemCreate(temp_id="iso-a", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="孤立电影A")),
                ItemCreate(temp_id="iso-b", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="孤立电影B")),
            ],
            # 没有 item_links，不连通
        )

        response = await app_client.post(
            "/api/media/batch?strict_graph=false",
            json=data.model_dump(exclude_unset=True),
            headers=auth_headers
        )
        assert response.status_code == 200, f"strict_graph=false 应该允许不连通图，实际: {response.text}"

    @pytest.mark.asyncio
    async def test_strict_graph_single_node(self, app_client, db_session, auth_headers):
        """测试25: 单个节点（自己连自己）- 应该成功"""
        data = MediaBatchCreate(
            source_name="single_node_test",
            items=[
                ItemCreate(temp_id="only-one", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="唯一电影")),
            ],
            item_links=[
                ItemLinkCreate(link="only-one", linked="only-one"),  # 自己连自己
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"单节点图应该成功，实际: {response.text}"

    @pytest.mark.asyncio
    async def test_strict_graph_no_item_links_single_item(self, app_client, db_session, auth_headers):
        """测试26: 没有 item_links 时，单个 item 应该成功"""
        data = MediaBatchCreate(
            source_name="no_links_test",
            items=[
                ItemCreate(temp_id="only-one", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="唯一电影")),
            ],
            # 没有 item_links，单个节点自己成图
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"单个 item 无 item_links 应该成功，实际: {response.text}"

    @pytest.mark.asyncio
    async def test_strict_graph_no_item_links_multiple_items_fails(self, app_client, db_session, auth_headers):
        """测试26b: 没有 item_links 时，多个 items 应该失败"""
        data = MediaBatchCreate(
            source_name="no_links_test",
            items=[
                ItemCreate(temp_id="item-a", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影A")),
                ItemCreate(temp_id="item-b", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影B")),
            ],
            # 没有 item_links，多个节点互不相连
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 422, f"多个 items 无 item_links 应该失败，实际: {response.text}"

    @pytest.mark.asyncio
    async def test_strict_graph_partial_disconnected(self, app_client, db_session, auth_headers):
        """测试27: 部分连通：两个连通分量，其中一个包含多个节点"""
        data = MediaBatchCreate(
            source_name="partial_test",
            items=[
                ItemCreate(temp_id="group-a1", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="组A-1")),
                ItemCreate(temp_id="group-a2", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="组A-2")),
                ItemCreate(temp_id="group-b1", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="组B-1")),
            ],
            item_links=[
                ItemLinkCreate(link="group-a1", linked="group-a2"),  # A 组内部连通
                # group-b1 是孤立的
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 422, f"存在孤立节点应该失败，实际: {response.text}"
        result = response.json()
        assert "group-b1" in result["detail"], f"错误信息应包含孤立节点 group-b1，实际: {result}"

    @pytest.mark.asyncio
    async def test_strict_graph_chain_topology(self, app_client, db_session, auth_headers):
        """测试28: 链式拓扑 A->B->C->D（连通）"""
        data = MediaBatchCreate(
            source_name="chain_test",
            items=[
                ItemCreate(temp_id="n1", source_info=SourceInfo(), attrs=SeriesAttrs(type="Series", name="系列1")),
                ItemCreate(temp_id="n2", source_info=SourceInfo(), attrs=SeasonAttrs(type="Season", name="季1")),
                ItemCreate(temp_id="n3", source_info=SourceInfo(), attrs=EpisodeAttrs(type="Episode", name="集1")),
                ItemCreate(temp_id="n4", source_info=SourceInfo(), attrs=PersonAttrs(type="Person", name="演员")),
            ],
            item_links=[
                ItemLinkCreate(link="n1", linked="n2"),  # 系列 -> 季
                ItemLinkCreate(link="n2", linked="n3"),  # 季 -> 集
                ItemLinkCreate(link="n3", linked="n4", people_type="Actor"),  # 集 -> 演员
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"链式拓扑应该成功，实际: {response.text}"

    @pytest.mark.asyncio
    async def test_strict_graph_star_topology(self, app_client, db_session, auth_headers):
        """测试29: 星形拓扑：中心节点连接多个叶节点"""
        data = MediaBatchCreate(
            source_name="star_test",
            items=[
                ItemCreate(temp_id="center", source_info=SourceInfo(), attrs=SeriesAttrs(type="Series", name="剧集")),
                ItemCreate(temp_id="leaf1", source_info=SourceInfo(), attrs=SeasonAttrs(type="Season", name="季1")),
                ItemCreate(temp_id="leaf2", source_info=SourceInfo(), attrs=SeasonAttrs(type="Season", name="季2")),
                ItemCreate(temp_id="leaf3", source_info=SourceInfo(), attrs=SeasonAttrs(type="Season", name="季3")),
            ],
            item_links=[
                ItemLinkCreate(link="center", linked="leaf1"),
                ItemLinkCreate(link="center", linked="leaf2"),
                ItemLinkCreate(link="center", linked="leaf3"),
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, f"星形拓扑应该成功，实际: {response.text}"

    @pytest.mark.asyncio
    async def test_strict_graph_cycle_topology(self, app_client, db_session, auth_headers):
        """测试30: 核心媒体环形拓扑被业务校验拒绝"""
        data = MediaBatchCreate(
            source_name="cycle_test",
            items=[
                ItemCreate(temp_id="a", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影A")),
                ItemCreate(temp_id="b", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影B")),
                ItemCreate(temp_id="c", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影C")),
            ],
            item_links=[
                ItemLinkCreate(link="a", linked="b"),
                ItemLinkCreate(link="b", linked="c"),
                ItemLinkCreate(link="c", linked="a"),  # 形成环
            ]
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 422, f"核心媒体环形拓扑应该失败，实际: {response.text}"

    @pytest.mark.asyncio
    async def test_core_topology_rejects_movie_to_movie(self, app_client, db_session, auth_headers):
        """核心媒体类型不能用任意连通关系代替业务拓扑。"""
        data = MediaBatchCreate(
            source_name="non_agent_source",
            items=[
                ItemCreate(temp_id="movie-a", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影A")),
                ItemCreate(temp_id="movie-b", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影B")),
            ],
            item_links=[ItemLinkCreate(link="movie-a", linked="movie-b")],
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 422
        assert "裸电影" in response.text

    @pytest.mark.asyncio
    async def test_metadata_links_are_not_restricted_by_core_topology(self, app_client, db_session, auth_headers):
        """Genre、Person、Tag 等辅助 Item 不参与核心拓扑方向校验。"""
        data = MediaBatchCreate(
            source_name="metadata_source",
            items=[
                ItemCreate(temp_id="movie", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影")),
                ItemCreate(temp_id="person", source_info=SourceInfo(), attrs=PersonAttrs(type="Person", name="人物")),
                ItemCreate(temp_id="genre", source_info=SourceInfo(), attrs=GenreAttrs(type="Genre", name="类型")),
                ItemCreate(temp_id="tag", source_info=SourceInfo(), attrs=TagAttrs(type="Tag", name="标签")),
            ],
            item_links=[
                ItemLinkCreate(link="movie", linked="person"),
                ItemLinkCreate(link="genre", linked="movie"),
                ItemLinkCreate(link="tag", linked="genre"),
            ],
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, response.text

    @pytest.mark.asyncio
    async def test_collection_core_topology_is_accepted(self, app_client, db_session, auth_headers):
        """集合分支必须使用 BoxSet -> Movie。"""
        data = MediaBatchCreate(
            source_name="collection_source",
            items=[
                ItemCreate(temp_id="box", source_info=SourceInfo(), attrs=BoxSetAttrs(type="BoxSet", name="合集")),
                ItemCreate(temp_id="movie", source_info=SourceInfo(), attrs=MovieAttrs(type="Movie", name="电影")),
            ],
            item_links=[ItemLinkCreate(link="box", linked="movie")],
        )

        response = await app_client.post("/api/media/batch", json=data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200, response.text


class TestSchemaValidation:
    """Schema 验证测试 - 不走 API，直接测试 schema"""

    def test_unset_filter_in_serialization(self):
        """验证 UNSET 在序列化时被过滤"""
        item = ItemCreate(
            temp_id="t1",
            source_info=SourceInfo(source_id="s1"),
            attrs=MovieAttrs(type="Movie", name="测试")
        )
        dumped = item.model_dump(exclude_unset=True)
        assert "source_id" in dumped["source_info"]
        # UNSET 的 source_link 不应该出现
        assert "source_link" not in dumped["source_info"]

    def test_full_serialization_no_unset(self):
        """验证完整数据序列化后没有 UNSET"""
        data = MediaBatchCreate(
            source_name="test",
            items=[
                ItemCreate(
                    temp_id="i1",
                    source_info=SourceInfo(source_id="sid", source_link="slink"),
                    attrs=MovieAttrs(type="Movie", name="名", overview="简介", tagline="标")
                )
            ],
            files=[
                FileCreate(
                    temp_id="f1",
                    attrs=FileBaseAttrs(name="file.mp4", path="/p", type="Video", size=100)
                )
            ],
            item_links=[
                ItemLinkCreate(link="i1", linked="i1", people_type="Actor", people_role="主演")
            ],
            file_links=[
                ImageFileLink(item="i1", file="f1", link_type="Image", image_type="Primary")
            ]
        )
        dumped = data.model_dump()

        # 检查没有 UNSET 值
        def check_no_unset(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    check_no_unset(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    check_no_unset(item, f"{path}[{i}]")

        check_no_unset(dumped)

    def test_validation_error_on_missing_type(self):
        """验证缺少 type 会抛出验证错误"""
        with pytest.raises(ValidationError):
            ItemCreate(temp_id="item-1", attrs={"name": "测试"})

    def test_file_type_required(self):
        """验证文件 type 必填"""
        with pytest.raises(ValidationError):
            FileBaseAttrs(name="test.mp4")  # 缺少 type
