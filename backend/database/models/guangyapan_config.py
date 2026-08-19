"""Singleton configuration for the GuangYaPan integration."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from .base import Base


class GuangYaPanConfig(Base):
    __tablename__ = "GuangYaPanConfig"

    # This table intentionally contains one row only (Id=1).
    Id = Column("Id", Integer, primary_key=True, default=1)
    AccessTokenEncrypted = Column("AccessTokenEncrypted", Text, nullable=True)
    RefreshTokenEncrypted = Column("RefreshTokenEncrypted", Text, nullable=True)
    ClientId = Column("ClientId", String(255), nullable=True)
    DeviceId = Column("DeviceId", String(255), nullable=True)
    # Single default parent directory used for offline tasks and uploads.
    DefaultParentId = Column("DefaultParentId", String(255), nullable=False, default="")
    CreatedAt = Column(
        "CreatedAt",
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    UpdatedAt = Column(
        "UpdatedAt",
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
