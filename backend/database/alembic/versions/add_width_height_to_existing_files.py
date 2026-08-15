"""add width height to existing files table

Revision ID: add_width_height_v2
Revises: c9914bb18e7e
Create Date: 2026-04-25 14:56:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_width_height_v2'
down_revision: Union[str, Sequence[str], None] = 'c9914bb18e7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 添加 Width 列
    try:
        op.add_column('Files', sa.Column('Width', sa.Integer(), nullable=True, comment='图片/视频宽度 - 像素'))
    except Exception:
        pass  # 列可能已存在
    
    # 添加 Height 列
    try:
        op.add_column('Files', sa.Column('Height', sa.Integer(), nullable=True, comment='图片/视频高度 - 像素'))
    except Exception:
        pass  # 列可能已存在


def downgrade() -> None:
    """Downgrade schema."""
    try:
        op.drop_column('Files', 'Height')
    except Exception:
        pass
    
    try:
        op.drop_column('Files', 'Width')
    except Exception:
        pass
