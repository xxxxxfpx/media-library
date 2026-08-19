import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from database.models import MediaItem, MediaType


class TestMediaItemHardening:
    def test_runtime_ticks_are_integral_and_format_without_float_rounding(self):
        movie = MediaItem(Type=MediaType.Movie, RunTimeTicks=3_661 * 10_000_000)

        assert movie.get_duration_str() == "1h 1m"

        with pytest.raises(ValueError):
            movie.RunTimeTicks = 1.5
        with pytest.raises(ValueError):
            movie.RunTimeTicks = True

    @pytest.mark.asyncio
    async def test_source_key_is_unique_for_active_items(self, init_database, db_session):
        source = MediaItem(Name="source", Type=MediaType.Source)
        db_session.add(source)
        await db_session.flush()

        first = MediaItem(Type=MediaType.Movie, SourceItemId=source.Id, SourceId="same-id")
        second = MediaItem(Type=MediaType.Movie, SourceItemId=source.Id, SourceId="same-id")
        db_session.add(first)
        await db_session.flush()
        db_session.add(second)

        with pytest.raises(IntegrityError):
            await db_session.flush()

    @pytest.mark.asyncio
    async def test_json_fields_round_trip_as_containers(self, init_database, db_session):
        movie = MediaItem(
            Type=MediaType.Movie,
            LockedFields=["Overview"],
        )
        db_session.add(movie)
        await db_session.flush()
        await db_session.refresh(movie)

        assert movie.LockedFields == ["Overview"]

    @pytest.mark.asyncio
    async def test_timestamps_are_returned_as_utc(self, init_database, db_session):
        movie = MediaItem(Type=MediaType.Movie)
        db_session.add(movie)
        await db_session.flush()
        await db_session.refresh(movie)

        assert movie.DateCreated.tzinfo is not None
        assert movie.DateCreated.utcoffset().total_seconds() == 0
        assert movie.CreatedAt.tzinfo is not None
        assert movie.UpdatedAt.tzinfo is not None

    @pytest.mark.asyncio
    async def test_database_check_constraints_reject_invalid_rating(self, init_database, db_session):
        with pytest.raises(IntegrityError):
            await db_session.execute(
                text(
                    "INSERT INTO MediaItems (Type, CommunityRating) "
                    "VALUES (:type, :rating)"
                ),
                {"type": MediaType.Movie.value, "rating": 11},
            )
