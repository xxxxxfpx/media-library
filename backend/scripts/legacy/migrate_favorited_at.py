# coding: utf-8
"""
数据迁移脚本 - 填充 FavoritedAt 字段
======================================

功能：为所有 IsFavorite=true 但 FavoritedAt=NULL 的记录填充 FavoritedAt
填充策略：使用 CreatedAt 或 UpdatedAt 作为 FavoritedAt

使用方法：
    python migrate_favorited_at.py

注意：
- 运行前先执行 alembic upgrade head 应用数据库迁移
- 此脚本只填充历史数据，不影响新数据
"""

import asyncio
import logging
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from database.models import UserData
from database.core import DATABASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def migrate_favorited_at():
    """迁移 FavoritedAt 字段"""
    # 创建异步引擎
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # 查询所有 IsFavorite=true 且 FavoritedAt=NULL 的记录
        stmt = select(UserData).where(
            UserData.IsFavorite == True,
            UserData.FavoritedAt == None
        )
        result = await session.execute(stmt)
        user_data_list = result.scalars().all()
        
        if not user_data_list:
            logger.info("没有需要迁移的记录")
            return
        
        logger.info(f"找到 {len(user_data_list)} 条需要迁移的记录")
        
        # 批量更新
        updated_count = 0
        for ud in user_data_list:
            # 优先使用 CreatedAt，如果没有则使用 UpdatedAt
            favorite_time = ud.CreatedAt or ud.UpdatedAt or datetime.now(timezone.utc)
            
            # 执行更新
            update_stmt = (
                update(UserData)
                .where(
                    UserData.UserId == ud.UserId,
                    UserData.ItemId == ud.ItemId
                )
                .values(FavoritedAt=favorite_time)
            )
            await session.execute(update_stmt)
            updated_count += 1
            
            if updated_count % 100 == 0:
                logger.info(f"已更新 {updated_count}/{len(user_data_list)} 条记录")
        
        # 提交事务
        await session.commit()
        
        logger.info(f"迁移完成！共更新 {updated_count} 条记录")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(migrate_favorited_at())
