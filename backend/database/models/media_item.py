# coding: utf-8
"""
MediaItem Model - 媒体项核心表
===========================================

媒体项核心表，采用单表设计。
所有媒体实体（Movie、Series、Season、Episode、Person、Genre、Studio 等）
都存储在此表，通过 Type 字段区分不同类型。

关联关系通过 ItemLinks 表维护。
Series → Season → Episode 层级通过 ItemLinks 建立关联。

作者：白鸟青城
版本：15.0.0 (移除 Guid/ExternalId/Video3DFormat/ExtraType，添加软删除+审计字段)
"""

from datetime import datetime, timezone
from typing import Any, Optional, Set

from sqlalchemy import (
    BigInteger, Boolean, Column, DateTime, Enum as SQLEnum, Float, Index, Integer, String, Text, func
)
from sqlalchemy import event
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base
from .enums import ItemStatus, MediaType


class MediaItem(Base):
    """
    媒体项表 - 采用单表设计

    所有媒体实体（Movie、Series、Season、Episode、Person、Genre、Studio 等）
    都存储在此表，通过 Type 字段区分不同类型。

    关联关系通过 ItemLinks 表维护（Genre、Studio、Tag、Person 等）。
    层级关系通过 ItemLinks 维护（Series → Season → Episode）。
    """

    __tablename__ = "MediaItems"

    FOLDER_MEDIA_TYPES: Set[MediaType] = {
        MediaType.Source,
        MediaType.BoxSet,
        MediaType.Season,
        MediaType.Series,
        MediaType.Genre,
        MediaType.Studio,
        MediaType.Person,
    }

    Id = Column("Id", Integer, primary_key=True, autoincrement=True, comment="主键 - 自增整数 ID")
    Type = Column("Type", SQLEnum(MediaType, name="media_type_enum", create_type=False, values_callable=lambda x: [e.value for e in x]), nullable=False, comment="媒体项类型")
    Name = Column("Name", String(500), nullable=True, comment="名称 - 显示名称")

    Overview = Column("Overview", Text, nullable=True, comment="简介 - 内容描述")
    Tagline = Column("Tagline", Text, nullable=True, comment="标语 - 宣传标语")
    PremiereDate = Column("PremiereDate", DateTime(timezone=True), nullable=True, comment="首映日期 - UTC 时间")
    EndDate = Column("EndDate", DateTime(timezone=True), nullable=True, comment="结束日期 - UTC 时间")
    StartDate = Column("StartDate", DateTime(timezone=True), nullable=True, comment="开始日期 - UTC 时间")

    OfficialRating = Column("OfficialRating", String(255), nullable=True, comment="官方评级")
    CustomRating = Column("CustomRating", String(255), nullable=True, comment="自定义评级")
    CommunityRating = Column("CommunityRating", Float, nullable=True, comment="社区评分 - 0-10")
    CriticRating = Column("CriticRating", Float, nullable=True, comment="评论家评分 - 0-100")

    Status = Column("Status", SQLEnum(ItemStatus, name="item_status_enum", create_type=False), nullable=True, comment="状态")

    ChannelNumber = Column("ChannelNumber", String(50), nullable=True, comment="频道号")

    ProductionLocations = Column("ProductionLocations", Text, nullable=True, comment="制作地点 - JSON 数组")
    RemoteTrailers = Column("RemoteTrailers", Text, nullable=True, comment="远程预告片 - JSON 数组")

    DateCreated = Column(
        "DateCreated",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="创建日期 - UTC 时间"
    )
    DateModified = Column(
        "DateModified",
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
        comment="修改日期 - UTC 时间"
    )
    CreatedAt = Column("CreatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 创建时间")
    UpdatedAt = Column("UpdatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 更新时间")

    IsDeleted = Column("IsDeleted", Boolean, default=False, nullable=False, comment="软删除标记")

    PresentationUniqueKey = Column("PresentationUniqueKey", Text, nullable=True, comment="展示唯一键")
    PreferredMetadataLanguage = Column("PreferredMetadataLanguage", String(50), nullable=True, comment="首选元数据语言")
    PreferredMetadataCountryCode = Column("PreferredMetadataCountryCode", String(10), nullable=True, comment="首选元数据国家代码")
    LockedFields = Column("LockedFields", Text, nullable=True, comment="锁定字段 - JSON 数组")

    Links = relationship("ItemLinks", back_populates="Item", cascade="all, delete-orphan", foreign_keys="ItemLinks.ItemId")
    LinkedItems = relationship("ItemLinks", back_populates="LinkedItem", cascade="all", foreign_keys="ItemLinks.LinkedItemId")
    UserDataItems = relationship("UserData", back_populates="Item", cascade="all, delete-orphan", foreign_keys="UserData.ItemId")
    FileLinks = relationship("FileLink", back_populates="Item", cascade="all, delete-orphan", foreign_keys="FileLink.ItemId")
    Aliases = relationship("Alias", back_populates="Item", cascade="all, delete-orphan", foreign_keys="Alias.ItemId")

    __table_args__ = (
        Index("idx_media_items_type", "Type"),
        Index("idx_media_items_name", "Name"),
        Index("idx_media_items_premiere_date", "PremiereDate"),
        Index("idx_media_items_community_rating", "CommunityRating"),
        Index("idx_media_items_is_deleted", "IsDeleted"),
        Index("idx_media_items_type_is_deleted", "Type", "IsDeleted"),
        Index("idx_media_items_type_is_deleted_created", "Type", "IsDeleted", "DateCreated"),
        Index("idx_media_items_type_is_deleted_name", "Type", "IsDeleted", "Name"),
        Index("idx_media_items_type_is_deleted_rating", "Type", "IsDeleted", "CommunityRating"),
    )


@event.listens_for(MediaItem, "before_insert", propagate=True)
def receive_before_insert(mapper: Any, connection: Any, target: MediaItem):
    """插入前事件监听器 - 自动设置时间戳"""
    now = datetime.now(timezone.utc)
    if target.DateCreated is None:
        target.DateCreated = now
    target.DateModified = now
    if target.CreatedAt is None:
        target.CreatedAt = now
    target.UpdatedAt = now


@event.listens_for(MediaItem, "before_update", propagate=True)
def receive_before_update(mapper: Any, connection: Any, target: MediaItem):
    """更新前事件监听器 - 自动更新时间戳"""
    target.DateModified = datetime.now(timezone.utc)
    target.UpdatedAt = datetime.now(timezone.utc)
