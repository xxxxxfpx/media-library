# coding: utf-8
"""
Database Core - 数据库核心配置
================================

提供 SQLAlchemy 异步引擎、会话工厂和依赖注入配置。

使用方式:
    from database.core import SessionManager

    # 上下文管理器方式
    async with SessionManager() as session:
        stmt = select(User).where(User.Username == username)
        result = await session.execute(stmt)

作者：数据库架构团队
版本：3.0.0 (移除循环导入，统一会话管理)
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import event, text
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from config import config

# 构建数据库URL
if config.database.type == "sqlite":
    DATABASE_URL = f"sqlite+aiosqlite:///{config.database.sqlite_path}"
else:
    DATABASE_URL = f"postgresql+asyncpg://{config.database.username}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.database}"

# ==================== 引擎配置 ====================
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
    )

# ==================== 会话工厂 ====================
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

@asynccontextmanager
async def SessionManager(auto_commit: bool = True) -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话（上下文管理器方式）

    Yields:
        AsyncSession: 异步数据库会话
    """
    async with AsyncSessionLocal() as db:
        try:
            yield db
            if auto_commit:
                await db.commit()
        except Exception:
            await db.rollback()
            raise


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
    """SQLite 下创建 FTS5 trigram 虚拟表与同步触发器（幂等，与 alembic fts_search 迁移一致）"""
    if config.database.type != "sqlite":
        return
    await conn.execute(text("""
        CREATE VIRTUAL TABLE IF NOT EXISTS media_item_fts USING fts5(
            Name, Overview, Tagline,
            content='MediaItems', content_rowid='Id',
            tokenize='trigram'
        )
    """))
    await conn.execute(text("""
        CREATE TRIGGER IF NOT EXISTS media_item_fts_ai AFTER INSERT ON MediaItems BEGIN
            INSERT INTO media_item_fts(rowid, Name, Overview, Tagline)
            VALUES (new.Id, new.Name, new.Overview, new.Tagline);
        END
    """))
    await conn.execute(text("""
        CREATE TRIGGER IF NOT EXISTS media_item_fts_ad AFTER DELETE ON MediaItems BEGIN
            INSERT INTO media_item_fts(media_item_fts, rowid, Name, Overview, Tagline)
            VALUES ('delete', old.Id, old.Name, old.Overview, old.Tagline);
        END
    """))
    await conn.execute(text("""
        CREATE TRIGGER IF NOT EXISTS media_item_fts_au AFTER UPDATE ON MediaItems BEGIN
            INSERT INTO media_item_fts(media_item_fts, rowid, Name, Overview, Tagline)
            VALUES ('delete', old.Id, old.Name, old.Overview, old.Tagline);
            INSERT INTO media_item_fts(rowid, Name, Overview, Tagline)
            VALUES (new.Id, new.Name, new.Overview, new.Tagline);
        END
    """))
    await conn.execute(text("INSERT INTO media_item_fts(media_item_fts) VALUES('rebuild')"))


async def init_db():
    """初始化数据库 - 异步方式创建表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _ensure_fts5(conn)
