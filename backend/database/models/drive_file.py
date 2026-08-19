# coding: utf-8
"""Provider-backed file records used by external drive integrations."""

from datetime import datetime, timezone

from sqlalchemy import BigInteger, Column, DateTime, Index, Integer, String, Text

from .base import Base


class DriveFile(Base):
    __tablename__ = "DriveFiles"

    Id = Column("Id", Integer, primary_key=True, autoincrement=True)
    Provider = Column("Provider", String(64), nullable=False)
    ProviderFileId = Column("ProviderFileId", String(255), nullable=False)
    SourceUrl = Column("SourceUrl", Text, nullable=False)
    PlaybackUrl = Column("PlaybackUrl", Text, nullable=True)
    Mode = Column("Mode", String(32), nullable=False)
    Name = Column("Name", Text, nullable=True)
    Size = Column("Size", BigInteger, nullable=True)
    Status = Column("Status", String(32), nullable=False, default="ready")
    TaskId = Column("TaskId", String(255), nullable=True)
    ErrorMessage = Column("ErrorMessage", Text, nullable=True)
    CreatedAt = Column("CreatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    UpdatedAt = Column("UpdatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        Index("uq_drive_files_provider_file", "Provider", "ProviderFileId", unique=True),
        Index("idx_drive_files_source_url", "SourceUrl"),
        Index("idx_drive_files_status", "Status"),
    )
