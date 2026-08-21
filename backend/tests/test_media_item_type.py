"""MediaItem 类型字段契约测试。

STI 已移除，媒体类型由 MediaItem.Type 和 ItemLinks 表达。
"""

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MediaItem, MediaType


class TestMediaItemTypeField:
    async def test_query_returns_unified_model(self, db_session: AsyncSession):
        """测试查询返回统一模型"""
        # 先清理现有数据
        await db_session.execute(delete(MediaItem))
        await db_session.flush()

        movie = MediaItem(
            Name="Test Movie",
            Type=MediaType.Movie,
            StartDate=None,
            RunTimeTicks=72_000_000_000,
        )
        series = MediaItem(Name="Test Series", Type=MediaType.Series)
        db_session.add_all([movie, series])
        await db_session.flush()

        result = await db_session.execute(select(MediaItem).order_by(MediaItem.Id))
        items = result.scalars().all()

        assert all(type(item) is MediaItem for item in items)
        assert len(items) == 2
        assert items[0].Type == MediaType.Movie
        assert items[1].Type == MediaType.Series
        assert items[0].RunTimeTicks == 72_000_000_000

    async def test_type_specific_fields_are_available_on_unified_model(self, db_session: AsyncSession):
        """测试类型特有字段在统一模型上可用"""
        item = MediaItem(
            Type=MediaType.Person,
            BirthPlace="New York",
        )
        db_session.add(item)
        await db_session.flush()

        assert item.Type is MediaType.Person
        assert item.BirthPlace == "New York"
