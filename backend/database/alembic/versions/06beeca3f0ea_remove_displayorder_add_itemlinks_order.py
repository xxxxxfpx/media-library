"""remove_displayorder_add_itemlinks_order

Revision ID: 06beeca3f0ea
Revises: remove_likes
Create Date: 2026-05-26 02:31:35.010830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06beeca3f0ea'
down_revision: Union[str, Sequence[str], None] = 'remove_likes'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # SQLite 3.50 fully supports ALTER TABLE DROP COLUMN
    op.drop_column("MediaItems", "DisplayOrder")
    op.add_column("ItemLinks", sa.Column("Order", sa.Integer(), nullable=True))


def downgrade() -> None:
    # Re-add DisplayOrder to MediaItems
    op.add_column("MediaItems", sa.Column(
        "DisplayOrder",
        sa.Enum(name="display_order_enum"),
        nullable=True,
        comment="显示顺序",
    ))
    op.drop_column("ItemLinks", "Order")
