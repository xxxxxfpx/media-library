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
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from config import config

# 构建数据库URL
if config.database.type == "sqlite":
    DATABASE_URL = f"sqlite+aiosqlite:///{config.database.sqlite_path}"
else:
    DATABASE_URL = f"postgresql+asyncpg://{config.database.username}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.database}"

# ==================== SQL 日志配置 ====================
if config.app.debug:
    import logging
    import os
    from logging.handlers import RotatingFileHandler
    sql_logger = logging.getLogger("sqlalchemy.engine")
    sql_logger.setLevel(logging.INFO)
    sql_logger.propagate = False
    
    for handler in sql_logger.handlers[:]:
        sql_logger.removeHandler(handler)
    
    sql_log_dir = os.path.join(os.path.dirname(__file__), "..", "data", "log")
    os.makedirs(sql_log_dir, exist_ok=True)
    
    rotating_handler = RotatingFileHandler(
        os.path.join(sql_log_dir, "sql.log"),
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding="utf-8"
    )
    rotating_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    sql_logger.addHandler(rotating_handler)

# ==================== 引擎配置 ====================
engine = create_async_engine(
    DATABASE_URL,
    echo=config.app.debug,
    future=True,
    pool_size=32,
    max_overflow=0,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False},
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


async def init_db():
    """初始化数据库 - 异步方式创建表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
