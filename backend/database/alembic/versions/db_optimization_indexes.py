"""db_optimization_indexes

Revision ID: db_optimization_indexes
Revises: 06beeca3f0ea
Create Date: 2026-08-15 00:00:00.000000

添加视频库场景的组合索引。
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db_optimization_indexes'
down_revision: Union[str, Sequence[str], None] = '06beeca3f0ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 列表热路径：Type 过滤 + 软删除过滤
    op.create_index("idx_media_items_type_is_deleted", "MediaItems", ["Type", "IsDeleted"])
    # 常见排序：Type 过滤 + 创建时间排序
    op.create_index(
        "idx_media_items_type_is_deleted_created",
        "MediaItems",
        ["Type", "IsDeleted", "DateCreated"],
    )
    # 反向关联查询（has_children / children 列表）
    op.create_index(
        "idx_item_links_linked_item_item", "ItemLinks", ["LinkedItemId", "ItemId"]
    )
    # 层级排序（Series→Season→Episode 按 Order）
    op.create_index(
        "idx_item_links_linked_item_order", "ItemLinks", ["LinkedItemId", "Order"]
    )
    # 用户数据批量回填（按 ItemId 维度）
    op.create_index("idx_user_data_item_user", "UserData", ["ItemId", "UserId"])
    # FileLink 去重/存在性检查（create_media_batch 热路径）
    op.create_index("idx_file_links_item_file", "FileLinks", ["ItemId", "FileId"])


def downgrade() -> None:
    op.drop_index("idx_file_links_item_file", table_name="FileLinks")
    op.drop_index("idx_user_data_item_user", table_name="UserData")
    op.drop_index("idx_item_links_linked_item_order", table_name="ItemLinks")
    op.drop_index("idx_item_links_linked_item_item", table_name="ItemLinks")
    op.drop_index("idx_media_items_type_is_deleted_created", table_name="MediaItems")
    op.drop_index("idx_media_items_type_is_deleted", table_name="MediaItems")
