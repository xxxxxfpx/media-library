"""
MediaItem Model - 媒体项核心表
===========================================

所有媒体实体都存储在此表，通过 Type 字段区分不同类型。

设计决策：
- 类型差异由 Type 字段和 ItemLinks 关系表达
- 所有可选媒体字段直接映射在同一模型上

优势：
- 查询简单，无需 JOIN
- 类型由 Type 字段明确表达
- 所有媒体字段集中在单一模型中
- 业务关系由 ItemLinks 维护

限制：
- 子类特有字段会增加表宽度
- 不适合子类特有字段非常多的情况

关联关系通过 ItemLinks 表维护。
Series → Season → Episode 层级通过 ItemLinks 建立关联。

作者：白鸟青城
版本：18.0.0 (移除无业务使用的 STI)
"""

from datetime import datetime, timezone
from math import isfinite
from typing import Any, ClassVar

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    and_,
    event,
    false,
    func,
)
from sqlalchemy import (
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.types import TypeDecorator

from .base import Base
from .enums import ItemStatus, MediaType

_TICKS_PER_SECOND = 10_000_000


class UTCDateTime(TypeDecorator):
    """跨 SQLite/PostgreSQL 保持 UTC 且带时区信息的日期时间类型。"""

    impl = DateTime
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(DateTime(timezone=True))

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if not isinstance(value, datetime):
            raise TypeError("datetime value required")
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        value = value.astimezone(timezone.utc)
        if dialect.name == "sqlite":
            return value.replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


def _validate_number(key: str, value: Any) -> Any:
    """校验有限数值，拒绝 bool、NaN 和无穷值。"""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ValueError(f"{key} must be a finite number")
    return value


def _validate_integer(key: str, value: Any) -> Any:
    """校验整数，bool 不能作为整数业务值。"""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be an integer")
    return value


def _format_runtime_ticks(ticks: int) -> str:
    """将 Ticks 转为小时/分钟，使用整数运算避免浮点精度损失。"""
    total_seconds, _ = divmod(ticks, _TICKS_PER_SECOND)
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


class MediaItem(Base):
    """
    媒体项表

    所有媒体类型共用此模型，类型由 Type 字段表达。

    关联关系通过 ItemLinks 表维护（Genre、Studio、Tag、Person 等）。
    层级关系通过 ItemLinks 维护（Series → Season → Episode）。
    """

    __tablename__ = "MediaItems"

    FOLDER_MEDIA_TYPES: ClassVar[frozenset[MediaType]] = frozenset({
        MediaType.Source,
        MediaType.BoxSet,
        MediaType.Season,
        MediaType.Series,
        MediaType.Genre,
        MediaType.Studio,
        MediaType.Person,
    })

    # ========== 公共字段 ==========
    Id = Column("Id", Integer, primary_key=True, autoincrement=True, comment="主键 - 自增整数 ID")
    Type = Column("Type", SQLEnum(MediaType, name="media_type_enum", create_type=False, values_callable=lambda x: [e.value for e in x]), nullable=False, comment="媒体项类型")
    Name = Column("Name", String(500), nullable=True, comment="名称 - 显示名称")

    Overview = Column("Overview", Text, nullable=True, comment="简介 - 内容描述")
    Tagline = Column("Tagline", Text, nullable=True, comment="标语 - 宣传标语")
    StartDate = Column("StartDate", UTCDateTime(), nullable=True, comment="开始日期 - 通用字段；Person 为出生日期，影视作品为首映/开始日期")
    EndDate = Column("EndDate", UTCDateTime(), nullable=True, comment="结束日期 - 通用字段；Person 为死亡日期，Series/Season 为结束日期")

    OfficialRating = Column("OfficialRating", String(255), nullable=True, comment="官方评级")
    CustomRating = Column("CustomRating", String(255), nullable=True, comment="自定义评级")
    CommunityRating = Column("CommunityRating", Float, nullable=True, comment="社区评分 - 0-10")
    CriticRating = Column("CriticRating", Float, nullable=True, comment="评论家评分 - 0-100")

    Status = Column("Status", SQLEnum(ItemStatus, name="item_status_enum", create_type=False), nullable=True, comment="状态")

    DateCreated = Column("DateCreated", UTCDateTime(), server_default=func.now(), nullable=False, comment="创建日期 - UTC 时间")
    DateModified = Column("DateModified", UTCDateTime(), server_default=func.now(), onupdate=func.now(), nullable=False, comment="修改日期 - UTC 时间")
    CreatedAt = Column("CreatedAt", UTCDateTime(), default=lambda: datetime.now(timezone.utc), server_default=func.now(), nullable=False, comment="审计字段 - 创建时间")
    UpdatedAt = Column("UpdatedAt", UTCDateTime(), default=lambda: datetime.now(timezone.utc), onupdate=func.now(), server_default=func.now(), nullable=False, comment="审计字段 - 更新时间")

    IsDeleted = Column("IsDeleted", Boolean, default=False, server_default=false(), nullable=False, comment="软删除标记")

    SourceId = Column("SourceId", String(255), nullable=True, comment="来源标识 - 关联来源的唯一 ID")
    SourceItemId = Column("SourceItemId", Integer, ForeignKey("MediaItems.Id", ondelete="SET NULL"), nullable=True, comment="来源或父级媒体项 ID")

    RunTimeTicks = Column("RunTimeTicks", BigInteger, nullable=True, comment="运行时长（Ticks）")
    BirthPlace = Column("BirthPlace", String(500), nullable=True, comment="出生地/地区")
    OriginalLanguage = Column("OriginalLanguage", String(100), nullable=True, comment="原始语言")
    # ========== 关联关系 ==========
    Links = relationship("ItemLinks", back_populates="Item", cascade="all, delete-orphan", foreign_keys="ItemLinks.ItemId")
    LinkedItems = relationship("ItemLinks", back_populates="LinkedItem", cascade="all", foreign_keys="ItemLinks.LinkedItemId")
    UserDataItems = relationship("UserData", back_populates="Item", cascade="all, delete-orphan", foreign_keys="UserData.ItemId")
    FileLinks = relationship("FileLink", back_populates="Item", cascade="all, delete-orphan", foreign_keys="FileLink.ItemId")
    Aliases = relationship("Alias", back_populates="Item", cascade="all, delete-orphan", foreign_keys="Alias.ItemId")
    ParentItem = relationship(
        "MediaItem",
        back_populates="ChildItems",
        foreign_keys=[SourceItemId],
        remote_side=[Id],
    )
    ChildItems = relationship(
        "MediaItem",
        back_populates="ParentItem",
        foreign_keys=[SourceItemId],
        passive_deletes=True,
    )

    # ========== 索引 ==========
    __table_args__ = (
        Index("idx_media_items_type", "Type"),
        Index("idx_media_items_name", "Name"),
        Index("idx_media_items_start_date", "StartDate"),
        Index("idx_media_items_community_rating", "CommunityRating"),
        Index("idx_media_items_is_deleted", "IsDeleted"),
        Index("idx_media_items_type_is_deleted", "Type", "IsDeleted"),
        Index("idx_media_items_type_is_deleted_created", "Type", "IsDeleted", "DateCreated"),
        Index("idx_media_items_type_is_deleted_name", "Type", "IsDeleted", "Name"),
        Index("idx_media_items_type_is_deleted_rating", "Type", "IsDeleted", "CommunityRating"),
        Index("idx_media_items_source_item", "SourceItemId"),
        Index("idx_media_items_source_id", "SourceId"),
        Index("idx_media_items_source_item_type", "SourceItemId", "SourceId", "Type"),
        Index(
            "idx_media_items_active_date_created",
            "DateCreated",
            "Id",
            sqlite_where=IsDeleted.is_(False),
            postgresql_where=IsDeleted.is_(False),
        ),
        Index(
            "idx_media_items_active_name",
            "Name",
            "Id",
            sqlite_where=IsDeleted.is_(False),
            postgresql_where=IsDeleted.is_(False),
        ),
        Index(
            "uq_media_items_source_key",
            "SourceItemId",
            "SourceId",
            "Type",
            unique=True,
            sqlite_where=and_(
                IsDeleted.is_(False),
                SourceItemId.isnot(None),
                SourceId.isnot(None),
            ),
            postgresql_where=and_(
                IsDeleted.is_(False),
                SourceItemId.isnot(None),
                SourceId.isnot(None),
            ),
        ),
        CheckConstraint(
            "CommunityRating IS NULL OR (CommunityRating >= 0 AND CommunityRating <= 10)",
            name="ck_media_items_community_rating_range",
        ),
        CheckConstraint(
            "CriticRating IS NULL OR (CriticRating >= 0 AND CriticRating <= 100)",
            name="ck_media_items_critic_rating_range",
        ),
        CheckConstraint(
            "RunTimeTicks IS NULL OR RunTimeTicks >= 0",
            name="ck_media_items_runtime_ticks_non_negative",
        ),
        CheckConstraint(
            "StartDate IS NULL OR EndDate IS NULL OR EndDate >= StartDate",
            name="ck_media_items_dates_order",
        ),
    )

    # ========== 公共方法 ==========
    def get_display_name(self) -> str:
        """获取显示名称。"""
        return self.Name or "Unknown"

    def get_duration_str(self) -> str | None:
        """获取运行时长字符串。"""
        runtime_ticks = getattr(self, "RunTimeTicks", None)
        if runtime_ticks is None:
            return None
        return _format_runtime_ticks(runtime_ticks)

    # ========== 公共字段验证器 ==========
    @validates('Name', 'Overview', 'Tagline', 'OfficialRating', 'CustomRating')
    def validate_string_fields(self, key, value):
        """验证字符串字段"""
        if value is not None and not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value

    @validates('CommunityRating')
    def validate_community_rating(self, key, value):
        """验证社区评分（0-10）"""
        if value is not None:
            _validate_number(key, value)
            if not (0 <= value <= 10):
                raise ValueError(f"{key} must be between 0 and 10")
        return value

    @validates('CriticRating')
    def validate_critic_rating(self, key, value):
        """验证评论家评分（0-100）"""
        if value is not None:
            _validate_number(key, value)
            if not (0 <= value <= 100):
                raise ValueError(f"{key} must be between 0 and 100")
        return value

    @validates('RunTimeTicks')
    def validate_runtime_ticks(self, key, value):
        if value is not None:
            _validate_integer(key, value)
            if value < 0:
                raise ValueError(f"{key} must be non-negative")
        return value

    @validates('StartDate', 'EndDate')
    def validate_dates(self, key, value):
        if value is not None and not isinstance(value, datetime):
            raise ValueError(f"{key} must be a datetime object")
        return value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(Id={self.Id}, Name={self.Name!r})>"


# ========== 事件监听器 ==========
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
    now = datetime.now(timezone.utc)
    target.DateModified = now
    target.UpdatedAt = now
