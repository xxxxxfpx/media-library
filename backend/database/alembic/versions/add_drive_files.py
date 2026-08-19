"""add provider-backed drive file records"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_drive_files"
down_revision: Union[str, Sequence[str], None] = "initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("Files", sa.Column("Provider", sa.String(64), nullable=True))
    op.add_column("Files", sa.Column("ProviderFileId", sa.String(255), nullable=True))
    op.create_index("idx_files_provider_file", "Files", ["Provider", "ProviderFileId"], unique=True)
    op.create_table(
        "DriveFiles",
        sa.Column("Id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("Provider", sa.String(64), nullable=False),
        sa.Column("ProviderFileId", sa.String(255), nullable=False),
        sa.Column("SourceUrl", sa.Text(), nullable=False),
        sa.Column("PlaybackUrl", sa.Text(), nullable=True),
        sa.Column("Mode", sa.String(32), nullable=False),
        sa.Column("Name", sa.Text(), nullable=True),
        sa.Column("Size", sa.BigInteger(), nullable=True),
        sa.Column("Status", sa.String(32), nullable=False, server_default="ready"),
        sa.Column("TaskId", sa.String(255), nullable=True),
        sa.Column("ErrorMessage", sa.Text(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(timezone=True), nullable=False),
        sa.Column("UpdatedAt", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("uq_drive_files_provider_file", "DriveFiles", ["Provider", "ProviderFileId"], unique=True)
    op.create_index("idx_drive_files_source_url", "DriveFiles", ["SourceUrl"])
    op.create_index("idx_drive_files_status", "DriveFiles", ["Status"])


def downgrade() -> None:
    op.drop_index("idx_drive_files_status", table_name="DriveFiles")
    op.drop_index("idx_drive_files_source_url", table_name="DriveFiles")
    op.drop_index("uq_drive_files_provider_file", table_name="DriveFiles")
    op.drop_table("DriveFiles")
    op.drop_index("idx_files_provider_file", table_name="Files")
    op.drop_column("Files", "ProviderFileId")
    op.drop_column("Files", "Provider")
