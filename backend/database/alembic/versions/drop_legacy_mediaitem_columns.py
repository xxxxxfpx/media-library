"""drop legacy MediaItems columns

Revision ID: drop_legacy_mediaitem_columns
Revises: consolidate_guangyapan_parent_id
Create Date: 2026-08-19

The consolidated ``initial_schema`` baseline still declared five columns
(GenreName, LabelName, LockedFields, PresentationUniqueKey, StudioName) that
the refactored ``MediaItems`` model no longer maps. This migration drops them
so a fresh-DB build matches the ORM models. It is idempotent: columns that are
already absent are skipped, which keeps it safe on databases built via
``Base.metadata.create_all`` (which never had these columns).
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = "drop_legacy_mediaitem_columns"
down_revision: str = "consolidate_guangyapan_parent_id"
branch_labels: tuple[str, ...] | None = None
depends_on: tuple[str, ...] | None = None

LEGACY_COLUMNS = (
    "GenreName",
    "LabelName",
    "LockedFields",
    "PresentationUniqueKey",
    "StudioName",
)


def _existing_columns() -> set[str]:
    bind = op.get_bind()
    return {col["name"] for col in inspect(bind).get_columns("MediaItems")}


def upgrade() -> None:
    present = _existing_columns()
    for column in LEGACY_COLUMNS:
        if column in present:
            op.drop_column("MediaItems", column)


def downgrade() -> None:
    present = _existing_columns()
    if "GenreName" not in present:
        op.add_column("MediaItems", sa.Column("GenreName", sa.String(255), nullable=True))
    if "LabelName" not in present:
        op.add_column("MediaItems", sa.Column("LabelName", sa.String(255), nullable=True))
    if "LockedFields" not in present:
        op.add_column("MediaItems", sa.Column("LockedFields", sa.JSON(), nullable=True))
    if "PresentationUniqueKey" not in present:
        op.add_column("MediaItems", sa.Column("PresentationUniqueKey", sa.Text(), nullable=True))
    if "StudioName" not in present:
        op.add_column("MediaItems", sa.Column("StudioName", sa.String(255), nullable=True))
