# coding: utf-8
"""
User Model - 用户模型
==================================

定义用户表、用户数据表（收藏/播放状态）。

作者：白鸟青城
版本：3.0.0
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean, Column, DateTime, Enum as SQLEnum, Float, ForeignKey, Index, Integer, String, Text, JSON,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .base import Base
from .enums import ShareLevel

if TYPE_CHECKING:
    from .media_item import MediaItem
    from .file import File


class User(Base):
    """
    用户表

    存储用户账户信息和认证数据
    """

    __tablename__ = "Users"

    Id = Column("Id", Integer, primary_key=True, autoincrement=True, comment="主键 - 自增整数 ID")
    Name = Column("Name", String(255), nullable=False, comment="用户名 - 登录名称")
    PasswordHash = Column("PasswordHash", String(255), nullable=False, comment="密码哈希 - PBKDF2-SHA256")
    Salt = Column("Salt", String(255), nullable=False, comment="密码盐值 - 随机生成")
    Email = Column("Email", String(255), nullable=True, comment="电子邮箱")
    IsAdmin = Column("IsAdmin", Boolean, default=False, nullable=False, comment="是否为管理员")
    IsActive = Column("IsActive", Boolean, default=True, nullable=False, comment="是否激活")
    Setting = Column("Setting", JSON, nullable=True, comment="用户设置 - JSON 格式，如深色模式配置")

    CreatedAt = Column("CreatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 创建时间")
    UpdatedAt = Column("UpdatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 更新时间")

    UserDataItems = relationship("UserData", back_populates="User", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_users_name", "Name"),
        Index("idx_users_email", "Email"),
    )

    @staticmethod
    def generate_salt(length: int = 32) -> str:
        """生成随机盐值"""
        return secrets.token_hex(length)

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """使用 PBKDF2-SHA256 哈希密码"""
        iterations = 100000
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations)
        return dk.hex()

    def set_password(self, password: str) -> None:
        """设置密码（自动生成盐值并哈希）"""
        self.Salt = self.generate_salt()
        self.PasswordHash = self.hash_password(password, self.Salt)

    def verify_password(self, password: str) -> bool:
        """验证密码"""
        if not self.Salt or not self.PasswordHash:
            return False
        return self.PasswordHash == self.hash_password(password, self.Salt)


class UserData(Base):
    """
    用户数据表

    存储用户对媒体项的个人数据（播放状态、收藏状态等）
    主键为 (UserId, ItemId) 复合主键
    """

    __tablename__ = "UserData"

    UserId = Column("UserId", Integer, ForeignKey("Users.Id", ondelete="CASCADE"), primary_key=True, comment="用户 ID")
    ItemId = Column("ItemId", Integer, ForeignKey("MediaItems.Id", ondelete="CASCADE"), primary_key=True, comment="媒体项 ID")
    PlaybackPositionTicks = Column("PlaybackPositionTicks", Float, default=0, nullable=False, comment="播放位置 - 以 ticks 为单位")
    PlayCount = Column("PlayCount", Integer, default=0, nullable=False, comment="播放次数")
    IsPlayed = Column("IsPlayed", Boolean, default=False, nullable=False, comment="是否已播放完成")
    Rating = Column("Rating", Float, nullable=True, comment="用户评分 - 0-10")
    PlaybackRate = Column("PlaybackRate", Float, default=1.0, nullable=False, comment="播放速率 - 如 0.5, 1.0, 2.0")
    LastPlayedAt = Column("LastPlayedAt", DateTime(timezone=True), nullable=True, comment="最后播放时间")
    FavoritedAt = Column("FavoritedAt", DateTime(timezone=True), nullable=True, comment="收藏时间 - NULL 表示从未收藏")

    CreatedAt = Column("CreatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 创建时间")
    UpdatedAt = Column("UpdatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 更新时间")

    User = relationship("User", back_populates="UserDataItems")
    Item = relationship("MediaItem", back_populates="UserDataItems")

    __table_args__ = (
        Index("idx_user_data_favorited_at", "FavoritedAt"),
        Index("idx_user_data_item_user", "ItemId", "UserId"),
        Index("idx_user_data_user_favorited", "UserId", "FavoritedAt"),
        Index("idx_user_data_user_last_played", "UserId", "LastPlayedAt"),
        Index("idx_user_data_user_rating", "UserId", "Rating"),
    )
