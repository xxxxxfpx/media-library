"""
pytest 配置文件
===============
提供测试所需的 fixtures 和配置
"""

import asyncio
import os
import sys
from pathlib import Path

import pytest

# 设置环境变量指向测试配置文件
os.environ['CONFIG_PATH'] = os.path.join(os.path.dirname(__file__), '..', 'env.yaml')

# 添加项目根目录到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# 确保数据库目录存在（CI 环境可能不存在）
db_dir = Path(__file__).parent.parent / "data" / "database"
db_dir.mkdir(parents=True, exist_ok=True)

from httpx import ASGITransport, AsyncClient, Timeout
from sqlalchemy import text

from app.main import app
from database.core import AsyncSessionLocal, Base, engine

# ==================== Fixtures ====================

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环（session 级别）"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def clean_db():
    """每个测试前清理数据库（删除所有数据）"""
    try:
        async with engine.begin() as conn:
            # 禁用外键约束
            await conn.execute(text("PRAGMA foreign_keys = OFF"))
            # 删除所有表的数据（按依赖顺序，避免外键约束）
            tables = ["UserItemShares", "Aliases", "ItemLinks", "FileLinks",
                      "UserData", "Files", "MediaItems", "Users"]
            for table in tables:
                try:
                    await conn.execute(text(f"DELETE FROM {table}"))
                except Exception:
                    pass  # 表不存在就跳过
            # 重新启用外键约束
            await conn.execute(text("PRAGMA foreign_keys = ON"))
    except Exception as e:
        pytest.fail(f"清理数据库失败: {e}")
    yield


@pytest.fixture(scope="function")
async def init_database():
    """完全重建数据库表结构，确保 schema 与 ORM 模型一致"""
    try:
        async with engine.begin() as conn:
            # 先删除所有表
            await conn.execute(text("PRAGMA foreign_keys = OFF"))
            for table in reversed(["UserItemShares", "Aliases", "ItemLinks", "FileLinks",
                                    "UserData", "Files", "MediaItems", "Users"]):
                try:
                    await conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
                except Exception:
                    pass
            await conn.execute(text("PRAGMA foreign_keys = ON"))

            # 重新创建所有表
            await conn.run_sync(Base.metadata.create_all)

        # 确保 admin 用户存在
        from app.services.auth_service import AuthService
        from database.core import AsyncSessionLocal

        async with AsyncSessionLocal() as db:
            admin = await AuthService.get_user_by_username(db, "admin")
            if not admin:
                await AuthService.create_user(db, username="admin", password="admin123", is_admin=True)
                await db.commit()
    except Exception as e:
        pytest.fail(f"初始化数据库失败: {e}")
    yield


@pytest.fixture(scope="function")
async def db_session():
    """提供数据库会话用于验证查询"""
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def app_client(init_database):
    """提供 FastAPI TestClient（带超时控制）"""
    # 直接导入并使用 app，确保 lifespan 事件被执行

    transport = ASGITransport(app=app)
    # 10秒超时，防止服务器无响应时阻塞
    timeout = Timeout(10.0, connect=5.0)
    async with AsyncClient(transport=transport, base_url="http://test", timeout=timeout) as client:
        yield client


@pytest.fixture(scope="function")
async def admin_token(app_client):
    """获取管理员访问令牌"""
    try:
        # admin 用户应该通过 app lifespan 自动创建
        # 登录获取 token（带超时保护）
        response = await app_client.post(
            "/api/user/login",
            json={"username": "admin", "password": "admin123"}
        )

        if response.status_code != 200:
            pytest.fail(f"管理员登录失败: {response.status_code} - {response.text}")

        data = response.json()
        if "access_token" not in data:
            pytest.fail(f"登录响应缺少 access_token: {data}")

        return data["access_token"]
    except asyncio.TimeoutError:
        pytest.fail("获取 admin token 超时")
    except Exception as e:
        pytest.fail(f"获取 admin token 失败: {e}")


@pytest.fixture(scope="function")
async def auth_headers(admin_token):
    """提供认证请求头"""
    return {"Authorization": f"Bearer {admin_token}"}
