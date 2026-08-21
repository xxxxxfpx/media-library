"""add collection source and log tables

Revision ID: add_collection_tables
Revises: drop_legacy_mediaitem_columns
Create Date: 2026-08-21

创建采集源配置表和采集日志表，支持苹果CMS V10协议采集源管理。
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "add_collection_tables"
down_revision: str | Sequence[str] | None = "drop_legacy_mediaitem_columns"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "CollectionSources" not in inspector.get_table_names():
        op.create_table(
            "CollectionSources",
            sa.Column("Id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
            sa.Column("Name", sa.String(100), nullable=False),
            sa.Column("BaseUrl", sa.String(500), nullable=False),
            sa.Column("Enabled", sa.Boolean(), server_default=sa.text("1"), nullable=False),
            sa.Column("AutoCollect", sa.Boolean(), server_default=sa.text("0"), nullable=False),
            sa.Column("IntervalMinutes", sa.Integer(), server_default=sa.text("60"), nullable=False),
            sa.Column("LastCollectedAt", sa.DateTime(timezone=True), nullable=True),
            sa.Column("LastStatus", sa.String(20), nullable=True),
            sa.Column("LastError", sa.Text(), nullable=True),
            sa.Column("CreatedAt", sa.DateTime(timezone=True), nullable=False),
            sa.Column("UpdatedAt", sa.DateTime(timezone=True), nullable=False),
        )
        op.create_index("idx_collection_sources_enabled", "CollectionSources", ["Enabled"])

    if "CollectionLogs" not in inspector.get_table_names():
        op.create_table(
            "CollectionLogs",
            sa.Column("Id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
            sa.Column("SourceId", sa.Integer(), nullable=False),
            sa.Column("TriggerType", sa.String(20), nullable=False),
            sa.Column("StartedAt", sa.DateTime(timezone=True), nullable=False),
            sa.Column("FinishedAt", sa.DateTime(timezone=True), nullable=True),
            sa.Column("Status", sa.String(20), server_default="running", nullable=False),
            sa.Column("NewCount", sa.Integer(), server_default=sa.text("0"), nullable=False),
            sa.Column("UpdateCount", sa.Integer(), server_default=sa.text("0"), nullable=False),
            sa.Column("ErrorCount", sa.Integer(), server_default=sa.text("0"), nullable=False),
            sa.Column("TotalFetched", sa.Integer(), server_default=sa.text("0"), nullable=False),
            sa.Column("ErrorMessage", sa.Text(), nullable=True),
            sa.Column("Details", sa.JSON(), nullable=True),
            sa.Column("CreatedAt", sa.DateTime(timezone=True), nullable=False),
            sa.Column("UpdatedAt", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["SourceId"], ["CollectionSources.Id"], ondelete="CASCADE"),
        )
        op.create_index("idx_collection_logs_source", "CollectionLogs", ["SourceId"])
        op.create_index("idx_collection_logs_status", "CollectionLogs", ["Status"])
        op.create_index("idx_collection_logs_started", "CollectionLogs", ["StartedAt"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "CollectionLogs" in inspector.get_table_names():
        op.drop_table("CollectionLogs")
    if "CollectionSources" in inspector.get_table_names():
        op.drop_table("CollectionSources")
