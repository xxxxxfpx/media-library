"""MediaItem 类型字段契约测试。

STI 已移除，媒体类型由 MediaItem.Type 和 ItemLinks 表达。
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MediaItem, MediaType


class TestMediaItemTypeField:
    async def test_query_returns_unified_model(self, db_session: AsyncSession):
        movie = MediaItem(
            Name="Test Movie",
            Type=MediaType.Movie,
            ProductionYear=2024,
            RunTimeTicks=72_000_000_000,
        )
        series = MediaItem(Name="Test Series", Type=MediaType.Series, SeasonCount=5)
        db_session.add_all([movie, series])
        await db_session.flush()

        result = await db_session.execute(select(MediaItem).order_by(MediaItem.Id))
        items = result.scalars().all()

        assert all(type(item) is MediaItem for item in items)
        assert [item.Type for item in items] == [MediaType.Movie, MediaType.Series]
        assert items[0].ProductionYear == 2024
        assert items[1].SeasonCount == 5

    async def test_type_specific_fields_are_available_on_unified_model(self, db_session: AsyncSession):
        item = MediaItem(
            Type=MediaType.Person,
            BirthPlace="New York",
            GenreName=None,
            StudioName=None,
        )
        db_session.add(item)
        await db_session.flush()

        assert item.Type is MediaType.Person
        assert item.BirthPlace == "New York"
