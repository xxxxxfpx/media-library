"""remove_date_last_fields

Revision ID: remove_date_last_fields
Revises: db_index_cleanup
Create Date: 2026-08-17 00:00:00.000000

清理 MediaItems 表冗余时间戳字段：
- 删除 DateLastRefreshed（无任何业务代码使用）
- 删除 DateLastSaved（无任何业务代码使用）

CreatedAt/UpdatedAt 为统一审计字段，DateCreated/DateModified 为业务时间戳，均保留。
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'remove_date_last_fields'
down_revision: Union[str, Sequence[str], None] = 'db_index_cleanup'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # SQLite 下 DROP COLUMN 受限，用 batch_alter_table 走"建新表 → 拷数据 → 删旧表 → 重命名"
    with op.batch_alter_table("MediaItems", recreate="auto") as batch_op:
        batch_op.drop_column("DateLastRefreshed")
        batch_op.drop_column("DateLastSaved")


def downgrade() -> None:
    with op.batch_alter_table("MediaItems", recreate="auto") as batch_op:
        batch_op.add_column(sa.Column("DateLastRefreshed", sa.DateTime(timezone=True), nullable=True, comment="最后刷新日期"))
        batch_op.add_column(sa.Column("DateLastSaved", sa.DateTime(timezone=True), nullable=True, comment="最后保存日期"))