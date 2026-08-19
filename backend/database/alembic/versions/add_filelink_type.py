"""add explicit file link type

Idempotent: ``FileLinks.LinkType`` is already declared in ``initial_schema``,
so this migration only adds the column (and backfills existing rows) when it
is missing. This keeps ``alembic upgrade head`` safe to run from an empty
database as well as against a ``Base.metadata.create_all`` schema.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "add_filelink_type"
down_revision: str | Sequence[str] | None = "sync_media_source_columns"
branch_labels = None
depends_on = None


def _has_column(bind, table: str, column: str) -> bool:
    inspector = sa.inspect(bind)
    return any(c["name"] == column for c in inspector.get_columns(table))


def upgrade() -> None:
    bind = op.get_bind()
    if not _has_column(bind, "FileLinks", "LinkType"):
        op.add_column("FileLinks", sa.Column("LinkType", sa.String(32), nullable=True))
        op.execute("UPDATE FileLinks SET LinkType = 'MediaSource' WHERE LinkType IS NULL")


def downgrade() -> None:
    bind = op.get_bind()
    if _has_column(bind, "FileLinks", "LinkType"):
        op.drop_column("FileLinks", "LinkType")
