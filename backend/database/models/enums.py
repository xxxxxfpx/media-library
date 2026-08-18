# coding: utf-8
"""
Enums - 枚举类型定义
====================

定义数据库中使用的所有枚举类型。
使用字符串枚举，与 Emby API 完全一致。

主要枚举类型：
- MediaType: 媒体项类型（Movie、Series、Season、Episode、Person 等）
- PersonType: 人物类型（Actor、Director、Writer 等）
- ItemLinkType: ItemLinks 链接类型（Genre、Studio、Tag、Person、Source 等）
- FileType: 文件类型（Image、Video、Subtitle 等）
- ImageType: 图片类型（Primary、Backdrop、Logo 等）
- ItemStatus: 媒体项状态（Continuing、Ended、Cancelled）

作者: 白鸟青城
版本: 7.0.0 (精简枚举)
"""

from enum import Enum


class MediaType(str, Enum):
    """
    媒体项类型枚举（视频化精简版）

    对应 media_items 表的 type 字段
    使用字符串值与 Emby API 一致
    type_code 对应原生 Emby SQLite 数据库的整数值
    """
    Source = "Source"  # 4 - 媒体来源
    Movie = "Movie"  # 6 - 电影
    Series = "Series"  # 9 - 系列
    Season = "Season"  # 8 - 季数
    Episode = "Episode"  # 5 - 电视剧集
    BoxSet = "BoxSet"  # 15 - 合集
    Genre = "Genre"  # 34 - 类型
    Person = "Person"  # 23 - 人物
    Studio = "Studio"  # 29 - 工作室
    Tag = "Tag"  # 21 - 标签

    @property
    def type_code(self) -> int:
        """
        获取原生 Emby SQLite 数据库的 type 整数值

        Returns:
            int: 原生 Emby 的 type 值
        """
        type_code_map = {
            MediaType.Source: 4,
            MediaType.Episode: 5,
            MediaType.Movie: 6,
            MediaType.Season: 8,
            MediaType.Series: 9,
            MediaType.BoxSet: 15,
            MediaType.Tag: 21,
            MediaType.Person: 23,
            MediaType.Studio: 29,
            MediaType.Genre: 34,
        }
        return type_code_map.get(self, 0)

    @classmethod
    def from_type_code(cls, code: int) -> "MediaType":
        """
        从原生 Emby type 整数值获取 MediaType 枚举

        Args:
            code: 原生 Emby 的 type 值

        Returns:
            MediaType: 对应的 MediaType 枚举值
        """
        code_to_type = {
            4: cls.Source,
            5: cls.Episode,
            6: cls.Movie,
            8: cls.Season,
            9: cls.Series,
            15: cls.BoxSet,
            21: cls.Tag,
            23: cls.Person,
            29: cls.Studio,
            34: cls.Genre,
        }
        return code_to_type.get(code, cls.Movie)


class PersonType(str, Enum):
    """
    人物类型枚举

    对应 item_links 表的 people_type 字段
    """
    Actor = "Actor"
    Director = "Director"
    Writer = "Writer"
    Producer = "Producer"
    Composer = "Composer"
    Conductor = "Conductor"
    Lyricist = "Lyricist"
    GuestStar = "GuestStar"


class FileType(str, Enum):
    """
    文件类型枚举（视频化精简版）

    对应 files 表的 type 字段
    """
    Image = "Image"
    Video = "Video"
    Subtitle = "Subtitle"
    EmbeddedImage = "EmbeddedImage"
    Attachment = "Attachment"
    Data = "Data"
    Other = "Other"


class ImageType(str, Enum):
    """
    图片类型枚举

    对应 file_links 表的 image_type 字段
    """
    Primary = "Primary"
    Art = "Art"
    Backdrop = "Backdrop"
    Banner = "Banner"
    Logo = "Logo"
    Thumb = "Thumb"
    Disc = "Disc"
    Box = "Box"
    BoxRear = "BoxRear"
    Profile = "Profile"
    Chapter = "Chapter"
    Screenshot = "Screenshot"
    Menu = "Menu"


class ItemStatus(str, Enum):
    """
    状态枚举

    对应 media_items 表的 status 字段
    """
    Continuing = "Continuing"
    Ended = "Ended"
    Cancelled = "Cancelled"


class FileLinkType(str, Enum):
    """
    文件关联类型枚举

    对应 FileLinks 表的 link_type 字段，显式区分三种关联语义：
    - MediaSource: 视频/音频/字幕源文件
    - Image: 图片（海报/头像/截图等）
    - Chapter: 章节图片/标记
    """
    MediaSource = "MediaSource"
    Image = "Image"
    Chapter = "Chapter"


class ChapterMarkerType(str, Enum):
    """
    章节标记类型枚举

    对应 FileLinks 表的 marker_type 字段（章节图片使用）
    """
    Chapter = "Chapter"
    IntroStart = "IntroStart"
    IntroEnd = "IntroEnd"
    CreditsStart = "CreditsStart"


class ShareLevel(str, Enum):
    """
    分享级别枚举

    对应 user_item_shares 表的 share_level 字段
    """
    Read = "Read"
    Write = "Write"
    Admin = "Admin"