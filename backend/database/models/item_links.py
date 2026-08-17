# coding: utf-8
"""
ItemLinks Model - 媒体项关联表
==============================

多对多关联表，用于维护 MediaItems 之间的所有关联关系。
连接不同类型的实体（Genre、Studio、Tag、Person、Source 等），
以及层级关系（Series → Season → Episode）。

支持类型：
- Genre、Studio、Tag、Keyword、BoxSet：将实体与元数据标签关联
- Person：将媒体项与人物关联（含 PeopleType 和 PeopleRole）
- Source：将媒体项与来源关联（含 SourceId 和 SourceLink）
- 层级关系：Series ↔ Season ↔ Episode 通过不同的 Type 区分

作者：白鸟青城
版本：4.0.0 (Role→PeopleRole，添加 SourceId/SourceLink，修复复合主键，添加审计字段)
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, Enum as SQLEnum, ForeignKey, Index, Integer, String, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship

from .base import Base
from .enums import MediaType, PersonType


class ItemLinks(Base):
    """
    媒体项关联表 - 连接 MediaItems 之间的所有关联关系

    设计说明：
    - 使用自增 Id 作为主键，通过 UniqueConstraint 确保同一对 (ItemId, LinkedItemId) 不重复
    - PeopleType 仅在 Person 关联时使用
    - PeopleRole 仅在 Person 关联时使用，描述人物在该媒体项中的角色
    - Order 用于子项在父项中的排序（如季号、集号）
    - Source 关联已迁移至 MediaItem.SourceId / SourceItemId / SourceLink
    """

    __tablename__ = "ItemLinks"

    Id = Column("Id", Integer, primary_key=True, autoincrement=True, comment="主键 - 自增整数 ID")
    ItemId = Column("ItemId", Integer, ForeignKey("MediaItems.Id", ondelete="CASCADE"), nullable=False, comment="源媒体项 ID")
    LinkedItemId = Column("LinkedItemId", Integer, ForeignKey("MediaItems.Id", ondelete="CASCADE"), nullable=False, comment="关联到的媒体项 ID")
    PeopleType = Column("PeopleType", SQLEnum(PersonType, name="person_type_enum", create_type=False), nullable=True, comment="人物类型")
    PeopleRole = Column("PeopleRole", Text, nullable=True, comment="角色 - 人物在媒体项中的角色名称")
    Order = Column("Order", Integer, nullable=True, comment="排序序号 - 子项在父项中的位置（如季号、集号）")

    CreatedAt = Column("CreatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 创建时间")
    UpdatedAt = Column("UpdatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 更新时间")

    Item = relationship("MediaItem", back_populates="Links", foreign_keys=[ItemId])
    LinkedItem = relationship("MediaItem", back_populates="LinkedItems", foreign_keys=[LinkedItemId])

    __table_args__ = (
        Index("idx_item_links_people_type", "PeopleType"),
        Index("idx_item_links_linked_item_item", "LinkedItemId", "ItemId"),
        Index("idx_item_links_linked_item_order", "LinkedItemId", "Order"),
        Index("idx_item_links_item_people_type", "ItemId", "PeopleType"),
        UniqueConstraint("ItemId", "LinkedItemId", name="uq_item_links_item_linked"),
    )
