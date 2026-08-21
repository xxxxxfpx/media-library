"""
CollectionSource Model - 采集源配置与日志
===========================================

管理苹果CMS V10协议采集源的配置、状态和采集日志。

CollectionSources: 采集源配置表
- 存储采集源的URL、轮询间隔、启停状态等配置
- 每个采集源对应一个 MediaType.Source 的 MediaItem

CollectionLogs: 采集日志表
- 记录每次采集的触发方式、结果、新增/更新数量等
"""

from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from .base import Base


class CollectionSource(Base):
    """采集源配置表"""

    __tablename__ = "CollectionSources"

    Id = Column("Id", Integer, primary_key=True, autoincrement=True, comment="主键")
    Name = Column("Name", String(100), nullable=False, comment="采集源名称")
    BaseUrl = Column("BaseUrl", String(500), nullable=False, comment="API基础URL")
    Enabled = Column("Enabled", Boolean, default=True, server_default="1", nullable=False, comment="是否启用")
    AutoCollect = Column("AutoCollect", Boolean, default=False, server_default="0", nullable=False, comment="自动轮询采集开关")
    IntervalMinutes = Column("IntervalMinutes", Integer, default=60, nullable=False, comment="轮询间隔(分钟)")
    LastCollectedAt = Column("LastCollectedAt", DateTime(timezone=True), nullable=True, comment="上次成功采集时间")
    LastStatus = Column("LastStatus", String(20), nullable=True, comment="上次采集状态: success/failed/running")
    LastError = Column("LastError", Text, nullable=True, comment="上次错误信息")
    CreatedAt = Column("CreatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, comment="创建时间")
    UpdatedAt = Column("UpdatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False, comment="更新时间")

    __table_args__ = (
        Index("idx_collection_sources_enabled", "Enabled"),
    )

    Logs = relationship("CollectionLog", back_populates="Source", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CollectionSource(Id={self.Id}, Name={self.Name!r}, Enabled={self.Enabled})>"


class CollectionLog(Base):
    """采集日志表"""

    __tablename__ = "CollectionLogs"

    Id = Column("Id", Integer, primary_key=True, autoincrement=True, comment="主键")
    SourceId = Column("SourceId", Integer, ForeignKey("CollectionSources.Id", ondelete="CASCADE"), nullable=False, comment="采集源ID")
    TriggerType = Column("TriggerType", String(20), nullable=False, comment="触发方式: auto/manual")
    StartedAt = Column("StartedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, comment="开始时间")
    FinishedAt = Column("FinishedAt", DateTime(timezone=True), nullable=True, comment="结束时间")
    Status = Column("Status", String(20), nullable=False, default="running", server_default="running", comment="状态: running/success/failed")
    NewCount = Column("NewCount", Integer, default=0, nullable=False, comment="新增视频数")
    UpdateCount = Column("UpdateCount", Integer, default=0, nullable=False, comment="更新视频数")
    ErrorCount = Column("ErrorCount", Integer, default=0, nullable=False, comment="失败条数")
    TotalFetched = Column("TotalFetched", Integer, default=0, nullable=False, comment="本次拉取总条数")
    ErrorMessage = Column("ErrorMessage", Text, nullable=True, comment="错误信息")
    Details = Column("Details", JSON, nullable=True, comment="详细信息(JSON)")

    CreatedAt = Column("CreatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, comment="创建时间")
    UpdatedAt = Column("UpdatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False, comment="更新时间")

    __table_args__ = (
        Index("idx_collection_logs_source", "SourceId"),
        Index("idx_collection_logs_status", "Status"),
        Index("idx_collection_logs_started", "StartedAt"),
    )

    Source = relationship("CollectionSource", back_populates="Logs")

    def __repr__(self):
        return f"<CollectionLog(Id={self.Id}, SourceId={self.SourceId}, Status={self.Status})>"
