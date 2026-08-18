# coding: utf-8
"""
File Models - 文件模型
============================

存储媒体文件信息，包括图片、视频、音频、字幕等。

表名：Files, FileLinks

File 表字段说明：
- Id: INT (主键 ID) - 自增，用于关联
- Etag: String (ETag) - 文件哈希值，用于缓存验证
- Size: BigInteger (文件大小) - 字节
- Name: Text (文件名)
- SortName: Text (排序名称) - 用于排序
- Path: Text (文件路径) - 唯一键，用于标识文件
- Type: ENUM (文件类型) - Image、Video、Audio、Subtitle 等
- FFmpeg: JSON (ffprobe 完整输出) - 前端自行解析流信息

FileLink 表字段说明（融合 ItemSource + LinkImageFile + ChapterImage）：
- ItemId: INT (媒体项 ID)
- FileId: INT (文件 ID)
- LinkType: ENUM (关联类型) - MediaSource/Image/Chapter，显式区分三种语义
- ImageType: ENUM (图片类型) - Primary、Backdrop、Logo 等（仅 Image/Chapter 使用）
- ImageIndex: INT (图片索引)
- ChapterIndex: INT (章节索引) - 章节图片使用，标记该图片属于哪个章节
- ChapterName: TEXT (章节名称) - 该图片对应的章节名称
- StartPositionTicks: BIGINT (章节开始位置) - ticks (1 tick = 100ns)
- MarkerType: ENUM (标记类型) - Chapter、IntroStart、CreditsStart 等

作者：白鸟青城
版本：11.0.0 (合并 Chapter 到 FileLink，添加章节相关字段)
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Column, Integer, BigInteger, String, Text, ForeignKey, Index,
    Enum as SQLEnum, DateTime, JSON
)
from sqlalchemy.orm import relationship

from .base import Base
from .enums import FileType, ImageType, ChapterMarkerType, FileLinkType


class File(Base):
    """
    文件表 - 存储媒体文件信息

    统一存储图片、视频、音频、字幕等文件信息。

    设计说明：
    - Id: 自增主键，用于关联
    - Path: 文件路径，唯一键，用于标识文件
    - CloudId: 云盘文件 ID，唯一键，可为空（后续客户端下载后更新）
    """

    __tablename__ = "Files"

    Id = Column("Id", Integer, primary_key=True, autoincrement=True, comment="主键 ID - 自增，用于关联")
    Etag = Column("Etag", String(64), nullable=True, comment="ETag - 文件哈希值，用于缓存验证")
    Size = Column("Size", BigInteger, nullable=True, comment="文件大小 - 字节")
    Name = Column("Name", Text, nullable=True, comment="文件名")
    SortName = Column("SortName", Text, nullable=True, comment="排序名称 - 用于排序的文件名")
    Path = Column("Path", Text, nullable=False, comment="文件路径 - 唯一键，用于标识文件")
    CloudId = Column("CloudId", String(255), nullable=True, comment="云盘文件 ID - 唯一键，可为空")
    Type = Column("Type", SQLEnum(FileType, name="file_type_enum", create_type=False, values_callable=lambda x: [e.value for e in x]), nullable=False, comment="文件类型")
    FFmpeg = Column("FFmpeg", JSON, nullable=True, comment="ffprobe 完整输出 - JSON 格式，前端自行解析流信息")

    CreatedAt = Column("CreatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 创建时间")
    UpdatedAt = Column("UpdatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 更新时间")

    __table_args__ = (
        Index("idx_files_etag", "Etag"),
        Index("idx_files_path", "Path", unique=True),
        Index("idx_files_cloud_id", "CloudId", unique=True),
    )
    FileLinks = relationship("FileLink", back_populates="File", cascade="all, delete")

    def __repr__(self):
        return f"<File(Id={self.Id}, Path='{self.Path}')>"


class FileLink(Base):
    """
    文件链接关联表 - 融合 ItemSource + LinkImageFile + ChapterImage

    存储 MediaItem 与 File 之间的关联关系，通过 LinkType 显式区分三种语义：
    - MediaSource: 视频/音频/字幕源文件
    - Image: 图片文件（海报/头像/截图等），同时指定 ImageType 和 ImageIndex
    - Chapter: 章节图片/标记，同时指定 ChapterIndex 及其他章节字段

    设计原则：
    - 一个文件对应一个 FileLink
    - 响应 MediaSource 时，id 字段使用 FileId
    - LinkType 由服务层根据 File.Type + 字段组合自动推断
    """

    __tablename__ = "FileLinks"

    Id = Column("Id", Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    ItemId = Column("ItemId", Integer, ForeignKey("MediaItems.Id", ondelete="CASCADE"), nullable=False, comment="媒体项 ID")
    FileId = Column("FileId", Integer, ForeignKey("Files.Id", ondelete="CASCADE"), nullable=False, comment="文件 ID")
    LinkType = Column(
        "LinkType",
        SQLEnum(
            FileLinkType,
            name="file_link_type_enum",
            create_type=False,
            values_callable=lambda x: [e.value for e in x]
        ),
        nullable=False,
        comment="关联类型 - MediaSource/Image/Chapter"
    )
    ImageType = Column("ImageType", SQLEnum(ImageType, name="image_type_enum", create_type=False, values_callable=lambda x: [e.value for e in x]), nullable=True, comment="图片类型 - Primary、Backdrop、Logo 等（仅图片使用）")
    ImageIndex = Column("ImageIndex", Integer, nullable=False, default=0, comment="图片索引")
    ChapterIndex = Column("ChapterIndex", Integer, nullable=True, comment="章节索引 - 章节图片使用，标记该图片属于哪个章节")
    ChapterName = Column("ChapterName", Text, nullable=True, comment="章节名称 - 该图片对应的章节名称")
    StartPositionTicks = Column("StartPositionTicks", BigInteger, nullable=True, comment="章节开始位置 - ticks (1 tick = 100ns)")
    MarkerType = Column(
        "MarkerType",
        SQLEnum(
            ChapterMarkerType,
            name="chapter_marker_type_enum",
            create_type=False,
            values_callable=lambda x: [e.value for e in x]
        ),
        nullable=True,
        comment="标记类型 - Chapter、IntroStart、CreditsStart 等"
    )

    CreatedAt = Column("CreatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 创建时间")
    UpdatedAt = Column("UpdatedAt", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False, comment="审计字段 - 更新时间")

    __table_args__ = (
        Index("idx_file_links_file", "FileId"),
        Index("idx_file_links_chapter", "ItemId", "ChapterIndex"),
        Index("idx_file_links_item_file", "ItemId", "FileId"),
        Index("idx_file_links_item_image_type", "ItemId", "ImageType"),
    )

    Item = relationship("MediaItem", back_populates="FileLinks")
    File = relationship("File", back_populates="FileLinks")

    @property
    def IsChapterImage(self) -> bool:
        return self.LinkType == FileLinkType.Chapter

    @property
    def StartPositionSeconds(self) -> float:
        if self.StartPositionTicks is None:
            return 0.0
        return self.StartPositionTicks / 10_000_000

    @property
    def StartPositionMinutes(self) -> float:
        return self.StartPositionSeconds / 60

    def __repr__(self):
        return f"<FileLink(Id={self.Id}, ItemId={self.ItemId}, FileId={self.FileId})>"
