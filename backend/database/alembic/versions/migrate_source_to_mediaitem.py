"""migrate_source_to_mediaitem

Revision ID: source_to_mediaitem
Revises: db_index_cleanup
Create Date: 2026-08-17 00:00:00.000000

将 Source 关联从 ItemLinks 迁移至 MediaItem 直接字段（一对一绑定）：
- MediaItems 新增 SourceId / SourceLink / SourceItemId 列
- ItemLinks 删除 SourceId / SourceLink 列
- 数据迁移：将 ItemLinks 中的 SourceId/SourceLink 同步到 MediaItem
- 添加 MediaItem 上的 source 相关索引，优化去重查询
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'source_to_mediaitem'
down_revision: Union[str, Sequence[str], None] = 'db_index_cleanup'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. MediaItems 添加 Source 相关列
    with op.batch_alter_table("MediaItems", recreate="auto") as batch_op:
        batch_op.add_column(sa.Column("SourceId", sa.String(255), nullable=True, comment="来源标识"))
        batch_op.add_column(sa.Column("SourceLink", sa.Text(), nullable=True, comment="来源链接"))
        batch_op.add_column(sa.Column(
            "SourceItemId", sa.Integer(), ForeignKey("MediaItems.Id", ondelete="SET NULL"),
            nullable=True, comment="指向 Source 类型 MediaItem 的 ID"
        ))

    # 2. 数据迁移：从 ItemLinks 同步 Source 信息到 MediaItems
    op.execute(sa.text("""
        UPDATE MediaItems SET
            SourceId = (
                SELECT il.SourceId FROM ItemLinks il
                WHERE il.ItemId = MediaItems.Id AND il.SourceId IS NOT NULL
                LIMIT 1
            ),
            SourceLink = (
                SELECT il.SourceLink FROM ItemLinks il
                WHERE il.ItemId = MediaItems.Id AND il.SourceId IS NOT NULL
                LIMIT 1
            ),
            SourceItemId = (
                SELECT il.LinkedItemId FROM ItemLinks il
                WHERE il.ItemId = MediaItems.Id AND il.SourceId IS NOT NULL
                LIMIT 1
            )
        WHERE EXISTS (
            SELECT 1 FROM ItemLinks il
            WHERE il.ItemId = MediaItems.Id AND il.SourceId IS NOT NULL
        )
    """))

    # 3. 添加 MediaItems 索引
    op.create_index("idx_media_items_source_item", "MediaItems", ["SourceItemId"])
    op.create_index("idx_media_items_source_id", "MediaItems", ["SourceId"])
    op.create_index("idx_media_items_source_item_type", "MediaItems", ["SourceItemId", "SourceId", "Type"])

    # 4. ItemLinks 删除 SourceId / SourceLink 列及对应索引
    op.drop_index("idx_item_links_source_id", table_name="ItemLinks")
    op.drop_index("idx_item_links_linked_source", table_name="ItemLinks")
    with op.batch_alter_table("ItemLinks", recreate="auto") as batch_op:
        batch_op.drop_column("SourceId")
        batch_op.drop_column("SourceLink")


def downgrade() -> None:
    # 1. ItemLinks 恢复 SourceId / SourceLink 列
    with op.batch_alter_table("ItemLinks", recreate="auto") as batch_op:
        batch_op.add_column(sa.Column("SourceLink", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("SourceId", sa.Text(), nullable=True))

    op.create_index("idx_item_links_source_id", "ItemLinks", ["SourceId"])
    op.create_index("idx_item_links_linked_source", "ItemLinks", ["LinkedItemId", "SourceId"])

    # 2. 数据回迁：从 MediaItems 同步回 ItemLinks
    op.execute(sa.text("""
        INSERT INTO ItemLinks (ItemId, LinkedItemId, SourceId, SourceLink, CreatedAt, UpdatedAt)
        SELECT
            MediaItems.Id,
            MediaItems.SourceItemId,
            MediaItems.SourceId,
            MediaItems.SourceLink,
            MediaItems.UpdatedAt,
            MediaItems.UpdatedAt
        FROM MediaItems
        WHERE MediaItems.SourceId IS NOT NULL
    """))

    # 3. MediaItems 删除 Source 列及索引
    op.drop_index("idx_media_items_source_item_type", table_name="MediaItems")
    op.drop_index("idx_media_items_source_id", table_name="MediaItems")
    op.drop_index("idx_media_items_source_item", table_name="MediaItems")
    with op.batch_alter_table("MediaItems", recreate="auto") as batch_op:
        batch_op.drop_column("SourceItemId")
        batch_op.drop_column("SourceLink")
        batch_op.drop_column("SourceId")