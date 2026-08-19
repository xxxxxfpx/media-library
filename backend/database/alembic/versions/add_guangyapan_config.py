"""add singleton GuangYaPan configuration

Idempotent against a schema already created by ``Base.metadata.create_all``
(which may contain this table). Only creates the table when it does not exist.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_guangyapan_config"
down_revision: Union[str, Sequence[str], None] = "sync_media_source_columns"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "GuangYaPanConfig" not in inspector.get_table_names():
        op.create_table(
            "GuangYaPanConfig",
            sa.Column("Id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("AccessTokenEncrypted", sa.Text(), nullable=True),
            sa.Column("RefreshTokenEncrypted", sa.Text(), nullable=True),
            sa.Column("ClientId", sa.String(255), nullable=True),
            sa.Column("DeviceId", sa.String(255), nullable=True),
            sa.Column("DefaultParentId", sa.String(255), nullable=False, server_default=""),
            sa.Column("CreatedAt", sa.DateTime(timezone=True), nullable=False),
            sa.Column("UpdatedAt", sa.DateTime(timezone=True), nullable=False),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "GuangYaPanConfig" in inspector.get_table_names():
        op.drop_table("GuangYaPanConfig")
