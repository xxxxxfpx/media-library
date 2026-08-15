# coding: utf-8
"""
Alias Model - 媒体别名表
=========================

存储媒体项的多种名称，用于记录不同来源或语言的名称。

表名：Aliases

字段说明：
- ItemId: INT (媒体项 ID) - 主键之一
- Name: TEXT (别名) - 主键之一
- Source: TEXT (来源) - 如 tmdb、imdb、tvdb、user 等

设计说明：
- 复合主键：(ItemId, Name)
- 一个媒体项可以有多个别名
- 来源字段标识别名的来源，便于追踪和管理

作者：白鸟青城
版本：1.1.0 (添加审计字段)
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Text, ForeignKey, Index, PrimaryKeyConstraint, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class Alias(Base):
    """
    媒体别名表 - 存储媒体项的多种名称

    用于记录媒体项在不同来源或语言下的名称。
    """

    __tablename__ = "Aliases"

    ItemId = Column("ItemId", Integer, ForeignKey("MediaItems.Id", ondelete="CASCADE"), nullable=False, comment="媒体项 ID")
    Name = Column("Name", Text, nullable=False, comment="别名名称")
    Source = Column("Source", Text, nullable=True, comment="来源 - 如 tmdb、imdb、tvdb、user 等")

    CreatedAt = Column("CreatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 创建时间")
    UpdatedAt = Column("UpdatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 更新时间")

    __table_args__ = (
        PrimaryKeyConstraint("ItemId", "Name", name="pk_aliases"),
        Index("idx_aliases_item", "ItemId"),
        Index("idx_aliases_name", "Name"),
        Index("idx_aliases_source", "Source", "ItemId"),
    )

    Item = relationship("MediaItem", back_populates="Aliases")

    def __repr__(self):
        return f"<Alias(ItemId={self.ItemId}, Name='{self.Name}', Source='{self.Source}')>"
