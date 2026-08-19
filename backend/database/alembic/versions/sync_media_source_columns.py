"""sync source and runtime columns added to MediaItems

Idempotent: on a fresh database these columns/indexes are already part of
``initial_schema``, so this migration only adds them when they are missing.
This keeps ``alembic upgrade head`` safe to run from an empty database as
well as against a schema that was created by ``Base.metadata.create_all``.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "sync_media_source_columns"
down_revision: Union[str, Sequence[str], None] = "add_drive_files"
branch_labels = None
depends_on = None


def _has_column(bind, table: str, column: str) -> bool:
    inspector = sa.inspect(bind)
    return any(c["name"] == column for c in inspector.get_columns(table))


def _has_index(bind, table: str, index: str) -> bool:
    inspector = sa.inspect(bind)
    return any(i["name"] == index for i in inspector.get_indexes(table))


def upgrade() -> None:
    bind = op.get_bind()
    if not _has_column(bind, "MediaItems", "SourceId"):
        op.add_column("MediaItems", sa.Column("SourceId", sa.String(255), nullable=True))
    if not _has_column(bind, "MediaItems", "SourceItemId"):
        op.add_column("MediaItems", sa.Column("SourceItemId", sa.Integer(), nullable=True))
    if not _has_column(bind, "MediaItems", "RunTimeTicks"):
        op.add_column("MediaItems", sa.Column("RunTimeTicks", sa.BigInteger(), nullable=True))
    if not _has_column(bind, "MediaItems", "BirthPlace"):
        op.add_column("MediaItems", sa.Column("BirthPlace", sa.String(500), nullable=True))
    if not _has_index(bind, "MediaItems", "idx_media_items_source_id"):
        op.create_index("idx_media_items_source_id", "MediaItems", ["SourceId"])
    if not _has_index(bind, "MediaItems", "idx_media_items_source_item"):
        op.create_index("idx_media_items_source_item", "MediaItems", ["SourceItemId"])


def downgrade() -> None:
    bind = op.get_bind()
    if _has_index(bind, "MediaItems", "idx_media_items_source_item"):
        op.drop_index("idx_media_items_source_item", table_name="MediaItems")
    if _has_index(bind, "MediaItems", "idx_media_items_source_id"):
        op.drop_index("idx_media_items_source_id", table_name="MediaItems")
    if _has_column(bind, "MediaItems", "BirthPlace"):
        op.drop_column("MediaItems", "BirthPlace")
    if _has_column(bind, "MediaItems", "RunTimeTicks"):
        op.drop_column("MediaItems", "RunTimeTicks")
    if _has_column(bind, "MediaItems", "SourceItemId"):
        op.drop_column("MediaItems", "SourceItemId")
    if _has_column(bind, "MediaItems", "SourceId"):
        op.drop_column("MediaItems", "SourceId")
