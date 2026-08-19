"""
光芽云盘单例配置测试
====================
覆盖配置密文加解密、单例读写服务，以及 /api/drives/guangyapan/config 接口。
"""

import pytest
from sqlalchemy import delete, select

from app.api.guangyapan import decrypt_value, encrypt_value
from app.services.guangyapan_config_service import get_or_create_config
from database.models import GuangYaPanConfig


@pytest.fixture(autouse=True)
async def _clear_config(db_session):
    """每个测试前后清空单例配置表，避免 Id=1 行互相干扰。"""
    await db_session.execute(delete(GuangYaPanConfig))
    await db_session.commit()
    yield
    await db_session.execute(delete(GuangYaPanConfig))
    await db_session.commit()


class TestGuangYaPanCrypto:
    """配置密文加解密"""

    @pytest.mark.asyncio
    async def test_encrypt_decrypt_roundtrip(self):
        secret = "super-secret-access-token"
        encrypted = encrypt_value(secret)
        assert encrypted != secret
        assert decrypt_value(encrypted) == secret

    @pytest.mark.asyncio
    async def test_none_passthrough(self):
        assert encrypt_value(None) is None
        assert encrypt_value("") is None
        assert decrypt_value(None) is None

    @pytest.mark.asyncio
    async def test_decrypt_invalid_raises(self):
        with pytest.raises(RuntimeError):
            decrypt_value("not-a-valid-ciphertext")


class TestGuangYaPanConfigService:
    """单例配置的读写服务"""

    @pytest.mark.asyncio
    async def test_get_or_create_is_singleton(self, db_session):
        first = await get_or_create_config(db_session)
        await db_session.flush()
        second = await get_or_create_config(db_session)
        assert first.Id == 1
        assert second.Id == 1

    @pytest.mark.asyncio
    async def test_get_config_missing_returns_none(self, db_session):
        await get_or_create_config(db_session)
        await db_session.flush()
        # 显式删除后查询应为 None
        await db_session.execute(delete(GuangYaPanConfig))
        await db_session.commit()
        from app.services.guangyapan_config_service import get_config

        assert await get_config(db_session) is None


class TestGuangYaPanConfigAPI:
    """配置接口（需管理员令牌）"""

    @pytest.mark.asyncio
    async def test_put_then_get_config(self, app_client, auth_headers, db_session):
        payload = {
            "access_token": "x" * 40,
            "client_id": "my-client",
            "device_id": "dev-001",
            "default_parent_id": "offline-root-123",
        }
        resp = await app_client.put(
            "/api/drives/guangyapan/config", json=payload, headers=auth_headers
        )
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["configured"] is True
        assert body["client_id"] == "my-client"
        assert body["default_parent_id"] == "offline-root-123"

        # 落库且密文可解密
        cfg = await db_session.scalar(
            select(GuangYaPanConfig).where(GuangYaPanConfig.Id == 1)
        )
        assert cfg is not None
        assert decrypt_value(cfg.AccessTokenEncrypted) == "x" * 40
        assert cfg.ClientId == "my-client"
        assert cfg.DefaultParentId == "offline-root-123"

        # GET 反映已配置状态
        resp2 = await app_client.get(
            "/api/drives/guangyapan/config", headers=auth_headers
        )
        assert resp2.status_code == 200
        assert resp2.json()["configured"] is True

    @pytest.mark.asyncio
    async def test_config_unauthorized(self, app_client):
        resp = await app_client.get("/api/drives/guangyapan/config")
        assert resp.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_put_requires_admin(self, app_client):
        # 普通未鉴权请求应被拒绝（管理员端点）
        resp = await app_client.put(
            "/api/drives/guangyapan/config",
            json={"access_token": "x" * 40},
        )
        assert resp.status_code in (401, 403)
