"""媒体项创建 Schema - 拓扑结构重组

设计原则：
1. 先确定 source_name（用于组织拓扑结构）
2. 所有实体对象（items、files）先创建，通过 temp_id 标识
3. item_links 和 file_links 通过 temp_id 绑定实体
4. 媒体项 attrs 使用类型感知校验：通过 Annotated[Union[...], Field(discriminator="type")]
      按 type 字段值直接匹配到具体类型类，在 API 输入层拦截无效类型和多余字段。
"""

from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class SourceInfo(BaseModel):
    """来源信息 - 用于标识媒体的来源"""
    source_id: Optional[str] = None
    source_link: Optional[str] = None

    def is_set(self, field: str) -> bool:
        return field in self.model_fields_set


class ItemAttrsBase(BaseModel):
    """所有媒体项类型共用的公共属性 - 禁止额外字段"""

    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(None, max_length=500, description="名称")
    overview: Optional[str] = Field(None, description="简介")
    tagline: Optional[str] = Field(None, description="标语")
    premiere_date: Optional[str] = Field(None, description="首映日期 (ISO 8601)")
    end_date: Optional[str] = Field(None, description="结束日期 (ISO 8601)")
    official_rating: Optional[str] = Field(None, max_length=255, description="官方评级")
    community_rating: Optional[float] = Field(None, ge=0.0, le=10.0, description="社区评分 0-10")
    critic_rating: Optional[float] = Field(None, ge=0.0, le=100.0, description="评论家评分 0-100")
    status: Optional[str] = Field(None, description="状态 (Continuing/Ended/Cancelled)")

    def is_set(self, field: str) -> bool:
        return field in self.model_fields_set


# ========== 按 MediaType 定义具体类型类 ==========

class MovieAttrs(ItemAttrsBase):
    """电影属性"""
    type: Literal["Movie"]


class SeriesAttrs(ItemAttrsBase):
    """系列属性"""
    type: Literal["Series"]


class SeasonAttrs(ItemAttrsBase):
    """季属性"""
    type: Literal["Season"]


class EpisodeAttrs(ItemAttrsBase):
    """剧集属性"""
    type: Literal["Episode"]


class BoxSetAttrs(ItemAttrsBase):
    """合集属性"""
    type: Literal["BoxSet"]


class GenreAttrs(ItemAttrsBase):
    """类型属性"""
    type: Literal["Genre"]


class PersonAttrs(ItemAttrsBase):
    """人物属性"""
    type: Literal["Person"]


class StudioAttrs(ItemAttrsBase):
    """工作室属性"""
    type: Literal["Studio"]


class SourceAttrs(ItemAttrsBase):
    """来源属性"""
    type: Literal["Source"]


class TagAttrs(ItemAttrsBase):
    """标签属性"""
    type: Literal["Tag"]


# Union 类型：使用 discriminator="type" 加速分发，按 type 字段值直接匹配到对应具体类做全量校验
ItemAttrs = Annotated[
    Union[
        MovieAttrs,
        SeriesAttrs,
        SeasonAttrs,
        EpisodeAttrs,
        BoxSetAttrs,
        GenreAttrs,
        PersonAttrs,
        StudioAttrs,
        SourceAttrs,
        TagAttrs,
    ],
    Field(discriminator="type"),
]


class FileBaseAttrs(BaseModel):
    """文件基本属性"""
    name: str
    path: Optional[str] = None
    url: Optional[str] = None
    provider: Optional[str] = None
    provider_file_id: Optional[str] = None
    type: str  # 文件类型必填
    size: Optional[int] = None
    etag: Optional[str] = None
    ffmpeg: Optional[dict] = None

    def is_set(self, field: str) -> bool:
        return field in self.model_fields_set


# ========== 实体创建模型 ==========

class ItemCreate(BaseModel):
    """媒体项创建 - 包含基本属性和来源信息"""
    temp_id: str = Field(..., min_length=1, description="客户端生成的临时唯一ID")
    source_info: SourceInfo = SourceInfo()
    attrs: ItemAttrs


class SingleItemCreate(BaseModel):
    """单个媒体项创建，供局部修正使用。"""
    source_name: str = Field(..., min_length=1)
    source_info: SourceInfo = SourceInfo()
    attrs: ItemAttrs


class FileCreate(BaseModel):
    """文件创建"""
    temp_id: str  # 客户端生成的临时唯一ID，用于关联
    attrs: FileBaseAttrs


# ========== 关联模型 ==========

class ItemLinkCreate(BaseModel):
    """媒体项关联 - 通过 temp_id 绑定源项和目标项"""
    people_type: Optional[str] = None
    people_role: Optional[str] = None
    link: str  # 源项的 temp_id
    linked: str  # 目标项的 temp_id

    def is_set(self, field: str) -> bool:
        return field in self.model_fields_set


class SingleItemLinkCreate(BaseModel):
    """已有媒体项之间的单条关联。"""
    linked_item_id: int = Field(..., gt=0)
    people_type: Optional[str] = None
    people_role: Optional[str] = None


class FileLinkBase(BaseModel):
    """文件关联的公共字段。"""

    model_config = ConfigDict(extra="forbid")

    item: str
    file: str
    image_index: Optional[int] = 0
    start_position_ticks: Optional[int] = None

    def is_set(self, field: str) -> bool:
        return field in self.model_fields_set


class MediaSourceFileLink(FileLinkBase):
    """媒体源文件关联。"""

    link_type: Literal["MediaSource"]


class ImageFileLink(FileLinkBase):
    """图片文件关联。"""

    link_type: Literal["Image"]
    image_type: str


class ChapterFileLink(FileLinkBase):
    """章节文件关联。"""

    link_type: Literal["Chapter"]
    chapter_index: int
    chapter_name: Optional[str] = None
    marker_type: Optional[str] = None


FileLinkCreate = Annotated[
    Union[MediaSourceFileLink, ImageFileLink, ChapterFileLink],
    Field(discriminator="link_type"),
]


# ========== 顶层创建模型 ==========

class MediaBatchCreate(BaseModel):
    """批量创建媒体项 - 顶层入口

    结构说明：
    - source_name: 来源名称，用于组织拓扑结构
    - items: 媒体项列表（先创建所有实体）
    - files: 文件列表（先创建所有实体）
    - item_links: 媒体项关联列表（通过 temp_id 绑定）
    - file_links: 文件关联列表（通过 temp_id 绑定）
    """
    source_name: str
    items: list[ItemCreate] = []
    files: list[FileCreate] = []
    item_links: list[ItemLinkCreate] = []
    file_links: list[FileLinkCreate] = []
