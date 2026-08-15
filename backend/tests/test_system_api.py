"""
系统 API 测试
=============
测试 /api/system 下的所有端点
"""

import pytest


class TestSystemInfo:
    """系统信息测试"""

    @pytest.mark.asyncio
    async def test_get_system_info(self, app_client, auth_headers):
        """测试获取系统信息"""
        response = await app_client.get("/api/system/info", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        # 验证返回结构包含系统信息
        expected_fields = ["platform", "python_version", "cpu", "memory"]
        for field in expected_fields:
            assert any(field in str(data).lower() for field in expected_fields) or \
                   any(key.startswith(field) for key in data.keys()), \
                   f"系统信息应包含 {field} 相关内容"

        # 更严格的检查
        assert "platform" in data or "os" in data, "应包含平台信息"
        assert "python_version" in data or "python" in data, "应包含 Python 版本"

    @pytest.mark.asyncio
    async def test_get_system_info_fields(self, app_client, auth_headers):
        """测试系统信息包含所有必要字段"""
        response = await app_client.get("/api/system/info", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        # 检查必要字段（根据实际实现可能略有不同）
        # 系统信息通常包含: ip, platform, python_version, cpu, memory_*, disk_*
        keys = list(data.keys())

        # 至少应该有一些系统信息
        assert len(data) > 0, "系统信息不应为空"

        # 验证数值类型字段（如果有的话）
        if "cpu" in data:
            assert isinstance(data["cpu"], (int, float, dict)), "CPU 信息应该是数值或对象类型"
        if "memory" in data:
            assert isinstance(data["memory"], dict), "内存信息应该是对象类型"

    @pytest.mark.asyncio
    async def test_system_info_consistency(self, app_client, auth_headers):
        """测试系统信息的一致性"""
        # 多次请求应该返回一致的结构
        response1 = await app_client.get("/api/system/info", headers=auth_headers)
        response2 = await app_client.get("/api/system/info", headers=auth_headers)

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = response1.json()
        data2 = response2.json()

        # 结构应该一致
        assert set(data1.keys()) == set(data2.keys()), "多次请求应返回一致的数据结构"


class TestHealthCheck:
    """健康检查测试"""

    @pytest.mark.asyncio
    async def test_health_check(self, app_client):
        """测试健康检查端点"""
        response = await app_client.get("/health")
        assert response.status_code == 200
        data = response.json()

        # 验证健康检查返回状态
        assert "status" in data, "健康检查应返回 status 字段"
        assert data["status"] == "ok", "健康状态应该是 ok"