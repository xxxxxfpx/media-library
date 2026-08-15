"""媒体项创建 Schema - 拓扑结构重组

设计原则：
1. 先确定 source_name（用于组织拓扑结构）
2. 所有实体对象（items、files）先创建，通过 temp_id 标识
3. item_links 和 file_links 通过 temp_id 绑定实体
"""

from typing import Optional
from pydantic import BaseModel


class SourceInfo(BaseModel):
    """来源信息 - 用于标识媒体的来源"""
    source_id: Optional[str] = None
    source_link: Optional[str] = None

    def is_set(self, field: str) -> bool:
        return field in self.model_fields_set


class ItemBaseAttrs(BaseModel):
    """媒体项基本属性"""
    type: str
    name: Optional[str] = None
    overview: Optional[str] = None
    tagline: Optional[str] = None
    premiere_date: Optional[str] = None
    end_date: Optional[str] = None
    official_rating: Optional[str] = None
    community_rating: Optional[float] = None
    critic_rating: Optional[float] = None
    status: Optional[str] = None
    display_order: Optional[str] = None
    production_locations: Optional[list] = None
    remote_trailers: Optional[list] = None
    preferred_metadata_language: Optional[str] = None
    preferred_metadata_country_code: Optional[str] = None

    def is_set(self, field: str) -> bool:
        return field in self.model_fields_set


class FileBaseAttrs(BaseModel):
    """文件基本属性"""
    name: str
    path: Optional[str] = None
    type: str  # 文件类型必填
    size: Optional[int] = None
    etag: Optional[str] = None
    ffmpeg: Optional[dict] = None

    def is_set(self, field: str) -> bool:
        return field in self.model_fields_set


# ========== 实体创建模型 ==========

class ItemCreate(BaseModel):
    """媒体项创建 - 包含基本属性和来源信息"""
    temp_id: str  # 客户端生成的临时唯一ID，用于关联
    source_info: SourceInfo = SourceInfo()
    attrs: ItemBaseAttrs


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


class FileLinkCreate(BaseModel):
    """文件关联 - 通过 temp_id 绑定媒体项和文件"""
    item: str  # 媒体项的 temp_id
    file: str  # 文件的 temp_id
    image_type: Optional[str] = None
    image_index: Optional[int] = 0
    chapter_index: Optional[int] = None
    chapter_name: Optional[str] = None
    start_position_ticks: Optional[int] = None
    marker_type: Optional[str] = None

    def is_set(self, field: str) -> bool:
        return field in self.model_fields_set


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
