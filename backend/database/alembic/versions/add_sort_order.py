"""add sort_order to collection sources

Revision ID: add_sort_order
Revises: add_collection_tables
Create Date: 2026-08-21

为 CollectionSources 表添加 SortOrder 字段，支持采集源排序配置。
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "add_sort_order"
down_revision: str | Sequence[str] | None = "add_collection_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "CollectionSources" in inspector.get_table_names():
        columns = {c["name"] for c in inspector.get_columns("CollectionSources")}
        if "SortOrder" not in columns:
            op.add_column(
                "CollectionSources",
                sa.Column(
                    "SortOrder",
                    sa.String(20),
                    server_default=sa.text("'time'"),
                    nullable=False,
                    comment="排序方式: time/id/hits",
                ),
            )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "CollectionSources" in inspector.get_table_names():
        columns = {c["name"] for c in inspector.get_columns("CollectionSources")}
        if "SortOrder" in columns:
            op.drop_column("CollectionSources", "SortOrder")
