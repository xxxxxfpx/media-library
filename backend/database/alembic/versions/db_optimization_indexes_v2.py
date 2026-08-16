"""db_optimization_indexes_v2

Revision ID: db_optimization_indexes_v2
Revises: video_only_schema
Create Date: 2026-08-16 00:00:00.000000

补充缺失的复合索引，覆盖收藏/历史/去重/主图查询热路径。
"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'db_optimization_indexes_v2'
down_revision: Union[str, Sequence[str], None] = 'video_only_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 收藏排序/过滤：WHERE UserId=.. AND FavoritedAt IS NOT NULL ORDER BY FavoritedAt
    op.create_index(
        "idx_user_data_user_favorited", "UserData", ["UserId", "FavoritedAt"]
    )
    # 历史排序/过滤：WHERE UserId=.. AND LastPlayedAt IS NOT NULL ORDER BY LastPlayedAt
    op.create_index(
        "idx_user_data_user_last_played", "UserData", ["UserId", "LastPlayedAt"]
    )
    # batch 去重查询：LinkedItemId=.. AND SourceId=..
    op.create_index(
        "idx_item_links_linked_source", "ItemLinks", ["LinkedItemId", "SourceId"]
    )
    # 主图查询：ItemId IN (..) AND ImageType IS NOT NULL
    op.create_index(
        "idx_file_links_item_image_type", "FileLinks", ["ItemId", "ImageType"]
    )


def downgrade() -> None:
    op.drop_index("idx_file_links_item_image_type", table_name="FileLinks")
    op.drop_index("idx_item_links_linked_source", table_name="ItemLinks")
    op.drop_index("idx_user_data_user_last_played", table_name="UserData")
    op.drop_index("idx_user_data_user_favorited", table_name="UserData")
