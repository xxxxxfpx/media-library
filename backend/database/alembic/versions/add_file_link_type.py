"""add_file_link_type

Revision ID: add_file_link_type
Revises: source_to_mediaitem, remove_date_last_fields
Create Date: 2026-08-18 00:00:00.000000

FileLink 添加显式 LinkType 列：
- 新增 file_link_type_enum 枚举（MediaSource / Image / Chapter）
- 新增 LinkType 列（NOT NULL），根据已有数据自动推断填充
- 合并 source_to_mediaitem 和 remove_date_last_fields 两个并行分支
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_file_link_type'
down_revision: Union[str, Sequence[str], None] = ('source_to_mediaitem', 'remove_date_last_fields')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. 创建枚举类型（SQLite 不支持 CREATE TYPE，sa.Enum 会自动跳过）
    file_link_type_enum = sa.Enum(
        'MediaSource', 'Image', 'Chapter',
        name='file_link_type_enum',
    )
    file_link_type_enum.create(op.get_bind(), checkfirst=True)

    # 2. 添加 LinkType 列（先可空，填充后再改 NOT NULL）
    with op.batch_alter_table("FileLinks", recreate="auto") as batch_op:
        batch_op.add_column(
            sa.Column(
                "LinkType",
                sa.Enum(
                    'MediaSource', 'Image', 'Chapter',
                    name='file_link_type_enum',
                    create_type=False,
                ),
                nullable=True,
                comment="关联类型 - MediaSource/Image/Chapter",
            )
        )

    # 3. 根据已有数据推断并填充 LinkType
    op.execute("""
        UPDATE "FileLinks"
        SET "LinkType" = CASE
            WHEN "ChapterIndex" IS NOT NULL THEN 'Chapter'
            WHEN "ImageType" IS NOT NULL THEN 'Image'
            ELSE 'MediaSource'
        END
    """)

    # 4. 改为 NOT NULL
    with op.batch_alter_table("FileLinks", recreate="auto") as batch_op:
        batch_op.alter_column(
            "LinkType",
            existing_type=sa.Enum(
                'MediaSource', 'Image', 'Chapter',
                name='file_link_type_enum',
                create_type=False,
            ),
            nullable=False,
        )

    # 5. 添加索引
    op.create_index("idx_file_links_link_type", "FileLinks", ["LinkType"])


def downgrade() -> None:
    op.drop_index("idx_file_links_link_type", table_name="FileLinks")

    with op.batch_alter_table("FileLinks", recreate="auto") as batch_op:
        batch_op.drop_column("LinkType")

    sa.Enum(name='file_link_type_enum').drop(op.get_bind(), checkfirst=True)
