"""db_index_cleanup

Revision ID: db_index_cleanup
Revises: fts_search
Create Date: 2026-08-16 22:00:00.000000

数据库模型索引清理：
- 删除重复索引（Column index=True/unique=True 与 __table_args__ 显式 Index 重复创建）：
  ix_Files_Etag / ix_MediaItems_Type / ix_MediaItems_IsDeleted
- 删除被复合索引/主键左前缀覆盖的冗余单列索引：
  idx_user_data_user_id（被 UserData 复合主键覆盖）
  idx_user_data_item_id（被 idx_user_data_item_user 覆盖）
  idx_file_links_item（被 idx_file_links_item_file 覆盖）
  idx_item_links_linked_item_id（被 idx_item_links_linked_item_item 覆盖）
  idx_item_links_item_id（被唯一约束 uq_item_links_item_linked 覆盖）
  idx_aliases_item（被复合主键 pk_aliases 覆盖）
- 补充列表排序/过滤热路径缺失的复合索引：
  idx_media_items_type_is_deleted_name / idx_media_items_type_is_deleted_rating
  idx_user_data_user_rating / idx_item_links_item_people_type
"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'db_index_cleanup'
down_revision: Union[str, Sequence[str], None] = 'fts_search'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


_DROP_IF_EXISTS = [
    # 重复索引（来自 Column index=True，与显式 Index 并存）
    "DROP INDEX IF EXISTS ix_Files_Etag",
    "DROP INDEX IF EXISTS ix_MediaItems_Type",
    "DROP INDEX IF EXISTS ix_MediaItems_IsDeleted",
    # 冗余单列索引（被复合索引/主键左前缀覆盖）
    "DROP INDEX IF EXISTS idx_user_data_user_id",
    "DROP INDEX IF EXISTS idx_user_data_item_id",
    "DROP INDEX IF EXISTS idx_file_links_item",
    "DROP INDEX IF EXISTS idx_item_links_linked_item_id",
    "DROP INDEX IF EXISTS idx_item_links_item_id",
    "DROP INDEX IF EXISTS idx_aliases_item",
]

_CREATE_IF_NOT_EXISTS = [
    # 列表排序热路径：Type + 软删除 + 排序键
    'CREATE INDEX IF NOT EXISTS idx_media_items_type_is_deleted_name '
    'ON "MediaItems" ("Type", "IsDeleted", "Name")',
    'CREATE INDEX IF NOT EXISTS idx_media_items_type_is_deleted_rating '
    'ON "MediaItems" ("Type", "IsDeleted", "CommunityRating")',
    # 用户评分过滤热路径
    'CREATE INDEX IF NOT EXISTS idx_user_data_user_rating '
    'ON "UserData" ("UserId", "Rating")',
    # 演职人员查询热路径
    'CREATE INDEX IF NOT EXISTS idx_item_links_item_people_type '
    'ON "ItemLinks" ("ItemId", "PeopleType")',
]

# downgrade 时重建被删除的索引（含原表与原列）
_RESTORE = [
    'CREATE INDEX IF NOT EXISTS ix_Files_Etag ON "Files" ("Etag")',
    'CREATE INDEX IF NOT EXISTS ix_MediaItems_Type ON "MediaItems" ("Type")',
    'CREATE INDEX IF NOT EXISTS ix_MediaItems_IsDeleted ON "MediaItems" ("IsDeleted")',
    'CREATE INDEX IF NOT EXISTS idx_user_data_user_id ON "UserData" ("UserId")',
    'CREATE INDEX IF NOT EXISTS idx_user_data_item_id ON "UserData" ("ItemId")',
    'CREATE INDEX IF NOT EXISTS idx_file_links_item ON "FileLinks" ("ItemId")',
    'CREATE INDEX IF NOT EXISTS idx_item_links_linked_item_id ON "ItemLinks" ("LinkedItemId")',
    'CREATE INDEX IF NOT EXISTS idx_item_links_item_id ON "ItemLinks" ("ItemId")',
    'CREATE INDEX IF NOT EXISTS idx_aliases_item ON "Aliases" ("ItemId")',
]


def _drop(name: str) -> None:
    op.execute(f'DROP INDEX IF EXISTS {name}')


def upgrade() -> None:
    for stmt in _DROP_IF_EXISTS:
        op.execute(stmt)
    for stmt in _CREATE_IF_NOT_EXISTS:
        op.execute(stmt)


def downgrade() -> None:
    for stmt in reversed(_CREATE_IF_NOT_EXISTS):
        _drop(stmt.split()[3])
    for stmt in reversed(_RESTORE):
        op.execute(stmt)