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
import logging
from collections.abc import AsyncGenerator

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import config
from database.fts_ddl import FTS5_CREATE_SQL

logger = logging.getLogger(__name__)

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


async def _ensure_collection_columns(conn) -> None:
    """确保 CollectionSources 表包含所有必需的列（兼容旧数据库）"""
    from sqlalchemy import inspect as sa_inspect

    try:
        inspector = sa_inspect(conn)
        if "CollectionSources" not in inspector.get_table_names():
            return

        columns = {c["name"] for c in inspector.get_columns("CollectionSources")}

        # 需要确保存在的列及其默认值
        missing_columns = {
            "SortOrder": "TEXT DEFAULT 'time'",
            "LastMaxItemId": "INTEGER DEFAULT 0",
        }

        for col_name, col_def in missing_columns.items():
            if col_name not in columns:
                await conn.execute(text(f"ALTER TABLE CollectionSources ADD COLUMN {col_name} {col_def}"))
                logger.info(f"自动添加缺失的列: CollectionSources.{col_name}")
    except Exception as e:
        logger.warning(f"检测/修复 CollectionSources 列失败（可忽略）: {e}")


async def init_db():
    """初始化数据库 - 异步方式创建表并自动修复缺失的列"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # FTS5 初始化失败不应阻止数据库正常工作
        try:
            await _ensure_fts5(conn)
        except Exception as e:
            logger.warning("FTS5 初始化失败（可忽略）: %s", e)
            # 尝试修复：删除损坏的 FTS5 表和触发器
            try:
                await conn.execute(text("DROP TRIGGER IF EXISTS media_item_fts_ai"))
                await conn.execute(text("DROP TRIGGER IF EXISTS media_item_fts_ad"))
                await conn.execute(text("DROP TRIGGER IF EXISTS media_item_fts_au"))
                await conn.execute(text("DROP TABLE IF EXISTS media_item_fts"))
                logger.info("已清理损坏的 FTS5 对象")
            except Exception as e2:
                logger.warning("清理 FTS5 失败: %s", e2)
        # 自动检测并添加迁移中新增的列（兼容旧数据库）
        await _ensure_collection_columns(conn)
