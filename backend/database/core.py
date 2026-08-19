"""
Database Core - 数据库核心配置
================================

提供 SQLAlchemy 异步引擎、会话工厂和依赖注入配置。

使用方式:
    from database.core import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.Username == username)
        result = await session.execute(stmt)

作者：数据库架构团队
版本：3.1.0 (移除未使用的 SessionManager，统一 get_db_session)
"""

import json
from collections.abc import AsyncGenerator

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import config
from database.fts_ddl import FTS5_CREATE_SQL

# 构建数据库URL
if config.database.type == "sqlite":
    DATABASE_URL = f"sqlite+aiosqlite:///{config.database.sqlite_path}"
else:
    DATABASE_URL = f"postgresql+asyncpg://{config.database.username}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.database}"

# ==================== 引擎配置 ====================
def _json_serializer(value):
    """统一 JSON 存储格式，保留非 ASCII 字符以兼容现有 SQLite 数据。"""
    return json.dumps(value, ensure_ascii=False)


if config.database.type == "sqlite":
    # SQLite 单写者模型：小连接池即可，WAL 支持多读并发
    engine = create_async_engine(
        DATABASE_URL,
        echo=config.app.debug,
        future=True,
        pool_size=5,
        max_overflow=5,
        pool_timeout=30,
        connect_args={"check_same_thread": False},
        json_serializer=_json_serializer,
    )

    @event.listens_for(engine.sync_engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        """SQLite 连接级 PRAGMA：WAL 提升读写并发，busy_timeout 避免锁冲突"""
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA busy_timeout=5000")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    engine = create_async_engine(
        DATABASE_URL,
        echo=config.app.debug,
        future=True,
        pool_size=32,
        max_overflow=0,
        pool_timeout=30,
        pool_recycle=3600,
        pool_pre_ping=True,
        json_serializer=_json_serializer,
    )

# ==================== 会话工厂 ====================
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话（FastAPI 依赖注入方式）

    用于 FastAPI 的 Depends() 注入。

    Yields:
        AsyncSession: 异步数据库会话
    """
    async with AsyncSessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise


# ==================== Base 声明 ====================
from database.models.base import Base


async def _ensure_fts5(conn) -> None:
    """SQLite 下创建 FTS5 trigram 虚拟表与同步触发器（幂等，DDL 与 alembic fts_search 迁移共用单一来源）"""
    if config.database.type != "sqlite":
        return
    for statement in FTS5_CREATE_SQL:
        await conn.execute(text(statement))


async def init_db():
    """初始化数据库 - 异步方式创建表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _ensure_fts5(conn)
