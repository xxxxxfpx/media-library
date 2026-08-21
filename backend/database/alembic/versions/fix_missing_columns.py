"""fix missing columns on existing databases

Revision ID: fix_missing_columns
Revises: 23cd4601dd39
Create Date: 2026-08-21

为 CollectionSources 表添加可能缺失的列（兼容旧数据库）。
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "fix_missing_columns"
down_revision: str | Sequence[str] | None = "23cd4601dd39"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # 修复 CollectionSources 表缺失的列
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
            # 为已有行设置默认值
            op.execute(sa.text("UPDATE CollectionSources SET SortOrder = 'time' WHERE SortOrder IS NULL"))

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
            op.execute(sa.text("UPDATE CollectionSources SET LastMaxItemId = 0 WHERE LastMaxItemId IS NULL"))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "CollectionSources" in inspector.get_table_names():
        columns = {c["name"] for c in inspector.get_columns("CollectionSources")}
        if "LastMaxItemId" in columns:
            op.drop_column("CollectionSources", "LastMaxItemId")
        if "SortOrder" in columns:
            op.drop_column("CollectionSources", "SortOrder")
