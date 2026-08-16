"""video_only_schema

Revision ID: video_only_schema
Revises: db_optimization_indexes
Create Date: 2026-08-15 00:00:00.000000

视频化精简：
- 删除 MediaItems.AlbumId 列（音乐专辑关联，视频库不再需要）
- 清理遗留的 ProductionYear 索引（表列已移除）
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'video_only_schema'
down_revision: Union[str, Sequence[str], None] = 'db_optimization_indexes'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 清理遗留索引（可能不存在，忽略）
    try:
        op.drop_index("idx_media_items_production_year", table_name="MediaItems")
    except Exception:
        pass

    # 删除 MediaItems.AlbumId 列。
    # SQLite 下 DROP COLUMN 遇到自引用 FK 会失败，故用 batch_alter_table
    # 走"建新表 → 拷数据 → 删旧表 → 重命名"的完整重建流程。
    with op.batch_alter_table("MediaItems", recreate="auto") as batch_op:
        batch_op.drop_column("AlbumId")


def downgrade() -> None:
    with op.batch_alter_table("MediaItems", recreate="auto") as batch_op:
        batch_op.add_column(sa.Column(
            "AlbumId",
            sa.Integer(),
            sa.ForeignKey("MediaItems.Id", ondelete="CASCADE"),
            nullable=True,
            comment="专辑 ID",
        ))
