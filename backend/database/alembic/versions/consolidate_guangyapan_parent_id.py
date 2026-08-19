"""consolidate GuangYaPan parent-id columns into a single DefaultParentId

The original ``add_guangyapan_config`` migration created two columns
(``DefaultOfflineParentId`` / ``DefaultUploadParentId``) that were always
written with the same value, making the offline/upload distinction dead code.
This migration collapses them into one ``DefaultParentId`` column.

Idempotent: on a fresh database the column already exists and the legacy
columns never existed, so every step is skipped.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "consolidate_guangyapan_parent_id"
down_revision: str | Sequence[str] | None = "merge_filelink_guangyapan_heads"
branch_labels = None
depends_on = None


def _has_column(bind, table: str, column: str) -> bool:
    inspector = sa.inspect(bind)
    return any(c["name"] == column for c in inspector.get_columns(table))


def upgrade() -> None:
    bind = op.get_bind()
    if not _has_column(bind, "GuangYaPanConfig", "DefaultParentId"):
        op.add_column(
            "GuangYaPanConfig",
            sa.Column("DefaultParentId", sa.String(255), nullable=False, server_default=""),
        )
        op.execute(
            "UPDATE GuangYaPanConfig "
            "SET DefaultParentId = COALESCE("
            "NULLIF(DefaultOfflineParentId, ''), "
            "NULLIF(DefaultUploadParentId, ''), '')"
        )
    if _has_column(bind, "GuangYaPanConfig", "DefaultOfflineParentId"):
        op.drop_column("GuangYaPanConfig", "DefaultOfflineParentId")
    if _has_column(bind, "GuangYaPanConfig", "DefaultUploadParentId"):
        op.drop_column("GuangYaPanConfig", "DefaultUploadParentId")


def downgrade() -> None:
    bind = op.get_bind()
    if not _has_column(bind, "GuangYaPanConfig", "DefaultOfflineParentId"):
        op.add_column(
            "GuangYaPanConfig",
            sa.Column("DefaultOfflineParentId", sa.String(255), nullable=False, server_default=""),
        )
    if not _has_column(bind, "GuangYaPanConfig", "DefaultUploadParentId"):
        op.add_column(
            "GuangYaPanConfig",
            sa.Column("DefaultUploadParentId", sa.String(255), nullable=False, server_default=""),
        )
    if _has_column(bind, "GuangYaPanConfig", "DefaultParentId"):
        op.drop_column("GuangYaPanConfig", "DefaultParentId")
