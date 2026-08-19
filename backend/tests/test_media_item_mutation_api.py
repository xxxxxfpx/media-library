# coding: utf-8
"""单 Item 及 ItemLinks 局部修改接口测试。"""

import pytest
from sqlalchemy import text


class TestMediaItemMutationAPI:
    @pytest.mark.asyncio
    async def test_create_link_unlink_and_protect_metadata_delete(
        self, app_client, auth_headers, db_session
    ):
        tag_response = await app_client.post(
            "/api/media/items",
            json={
                "source_name": "manual",
                "source_info": {"source_id": "tag-1"},
                "attrs": {"type": "Tag", "name": "喜欢"},
            },
            headers=auth_headers,
        )
        assert tag_response.status_code == 201, tag_response.text
        tag_id = tag_response.json()["id"]

        movie_response = await app_client.post(
            "/api/media/items",
            json={
                "source_name": "manual",
                "source_info": {"source_id": "movie-1"},
                "attrs": {"type": "Movie", "name": "测试电影"},
            },
            headers=auth_headers,
        )
        assert movie_response.status_code == 201, movie_response.text
        movie_id = movie_response.json()["id"]

        link_response = await app_client.post(
            f"/api/media/items/{movie_id}/links",
            json={"linked_item_id": tag_id},
            headers=auth_headers,
        )
        assert link_response.status_code == 201, link_response.text

        protected_response = await app_client.delete(
            f"/api/media/items/{tag_id}", headers=auth_headers
        )
        assert protected_response.status_code == 403

        unlink_response = await app_client.delete(
            f"/api/media/items/{movie_id}/links/{tag_id}", headers=auth_headers
        )
        assert unlink_response.status_code == 204
        link_count = await db_session.execute(
            text("SELECT COUNT(*) FROM ItemLinks WHERE ItemId = :item AND LinkedItemId = :tag"),
            {"item": movie_id, "tag": tag_id},
        )
        assert link_count.scalar_one() == 0

        tag_info = await app_client.get(f"/api/media/info?id={tag_id}", headers=auth_headers)
        assert tag_info.status_code == 200

        delete_response = await app_client.delete(
            f"/api/media/items/{movie_id}", headers=auth_headers
        )
        assert delete_response.status_code == 204
        movie_info = await app_client.get(f"/api/media/info?id={movie_id}", headers=auth_headers)
        assert movie_info.status_code == 404
