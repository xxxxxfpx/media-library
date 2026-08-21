"""add last_max_item_id for id-based cursor

Revision ID: add_last_max_item_id
Revises: add_sort_order
Create Date: 2026-08-21

为 CollectionSources 表添加 LastMaxItemId 字段，用于 ID 增量游标遍历。
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "add_last_max_item_id"
down_revision: str | Sequence[str] | None = "add_sort_order"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "CollectionSources" in inspector.get_table_names():
        columns = {c["name"] for c in inspector.get_columns("CollectionSources")}
        if "LastMaxItemId" not in columns:
            op.add_column(
                "CollectionSources",
                sa.Column(
                    "LastMaxItemId",
                    sa.Integer(),
                    server_default=sa.text("0"),
                    nullable=False,
                    comment="上次遍历到的最大item ID（用于ID增量游标）",
                ),
            )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "CollectionSources" in inspector.get_table_names():
        columns = {c["name"] for c in inspector.get_columns("CollectionSources")}
        if "LastMaxItemId" in columns:
            op.drop_column("CollectionSources", "LastMaxItemId")
