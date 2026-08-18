"""媒体数据序列化 Schema"""

from typing import Optional
from pydantic import BaseModel


class LinkedItemSummary(BaseModel):
    """关联媒体摘要信息"""
    id: int
    name: str
    type: Optional[str] = None
    overview: Optional[str] = None
    tagline: Optional[str] = None
    premiere_date: Optional[str] = None
    official_rating: Optional[str] = None
    community_rating: Optional[float] = None
    primary_image: Optional[str] = None
    source_link: Optional[str] = None


class LinkItem(BaseModel):
    """媒体关联项（人物/角色）"""
    people_type: Optional[str] = None
    people_role: Optional[str] = None
    source_link: Optional[str] = None
    linked_item: LinkedItemSummary


class FileInfo(BaseModel):
    """文件信息"""
    id: int
    name: Optional[str] = None
    path: Optional[str] = None
    type: Optional[str] = None
    link_type: Optional[str] = None
    image_type: Optional[str] = None
    image_index: Optional[int] = None
    size: Optional[int] = None
    etag: Optional[str] = None
    ffmpeg: Optional[str] = None


class FileInfoDetail(BaseModel):
    """文件详情（含关联的 MediaItem ID）"""
    id: int
    name: str
    path: str
    type: Optional[str] = None
    link_type: Optional[str] = None
    item_id: int
    image_type: Optional[str] = None
    image_index: Optional[int] = None
    size: int
    etag: Optional[str] = None
    ffmpeg: Optional[str] = None


class AliasItem(BaseModel):
    """别名"""
    name: str
    source: Optional[str] = None


class UserDataInfo(BaseModel):
    """用户播放数据"""
    is_favorite: bool = False
    playback_position_ticks: int = 0
    playback_rate: float = 1.0
    play_count: int = 0
    is_played: bool = False
    rating: Optional[float] = None
    last_played_date: Optional[str] = None
    favorited_at: Optional[str] = None


class MediaItemSummary(BaseModel):
    """媒体项基本信息"""
    id: int
    name: str
    type: Optional[str] = None
    overview: Optional[str] = None
    tagline: Optional[str] = None
    premiere_date: Optional[str] = None
    end_date: Optional[str] = None
    official_rating: Optional[str] = None
    community_rating: Optional[float] = None
    critic_rating: Optional[float] = None
    date_created: Optional[str] = None
    date_modified: Optional[str] = None
    source_id: Optional[str] = None
    source_link: Optional[str] = None
    source_name: Optional[str] = None


class MediaItemResponse(MediaItemSummary):
    """媒体项完整响应（含关联数据）"""
    links: list[LinkItem] = []
    files: list[FileInfo] = []
    userdata: Optional[UserDataInfo] = None
    alias: list[AliasItem] = []
    has_children: bool = False


class MediaListResponse(BaseModel):
    """媒体列表响应"""
    items: list[MediaItemResponse]
    total: int
    limit: int
    offset: int
    next_cursor: Optional[str] = None


class MediaStatsResponse(BaseModel):
    """媒体统计响应"""
    video_count: int = 0
    audio_count: int = 0
    image_count: int = 0
    subtitle_count: int = 0
    movie_count: int = 0
    series_count: int = 0
    episode_count: int = 0
    book_count: int = 0
    source_count: int = 0


# ========== 序列化函数 ==========

def serialize_links(links_result, primary_images_map: dict[int, str] | None = None) -> list[LinkItem]:
    """序列化关联媒体链接"""
    links = []
    for link, linked_item in links_result:
        primary_image = primary_images_map.get(linked_item.Id) if primary_images_map else None
        links.append(LinkItem(
            people_type=link.PeopleType.value if link.PeopleType else None,
            people_role=link.PeopleRole,
            source_link=None,
            linked_item=LinkedItemSummary(
                id=linked_item.Id,
                name=linked_item.Name,
                type=linked_item.Type.value if linked_item.Type else None,
                overview=linked_item.Overview,
                tagline=linked_item.Tagline,
                premiere_date=linked_item.PremiereDate.isoformat() if linked_item.PremiereDate else None,
                official_rating=linked_item.OfficialRating,
                community_rating=linked_item.CommunityRating,
                primary_image=primary_image,
                source_link=None,
            )
        ))
    return links


def serialize_files(files_result) -> list[FileInfo]:
    """序列化文件列表"""
    files = []
    for file, file_link in files_result:
        fields = {
            'id': file.Id,
            'name': file.Name,
            'path': file.Path,
            'type': file.Type.value if file.Type else None,
            'link_type': file_link.LinkType.value if file_link.LinkType else None,
            'image_type': file_link.ImageType.value if file_link.ImageType else None,
            'image_index': file_link.ImageIndex,
            'etag': file.Etag,
            'ffmpeg': file.FFmpeg,
        }
        if file.Size is not None:
            fields['size'] = file.Size
        files.append(FileInfo(**fields))
    return files


def serialize_alias(alias_list) -> list[AliasItem]:
    """序列化别名列表"""
    return [AliasItem(name=a.Name, source=a.Source) for a in alias_list]


def serialize_userdata(ud) -> Optional[UserDataInfo]:
    """序列化用户播放数据"""
    if not ud:
        return None
    last_played = None
    if ud.LastPlayedAt:
        last_played = ud.LastPlayedAt.isoformat()
    favorited_at = None
    if ud.FavoritedAt:
        favorited_at = ud.FavoritedAt.isoformat()
    return UserDataInfo(
        is_favorite=ud.FavoritedAt is not None,
        playback_position_ticks=ud.PlaybackPositionTicks,
        playback_rate=ud.PlaybackRate,
        play_count=ud.PlayCount,
        is_played=ud.IsPlayed,
        rating=ud.Rating,
        last_played_date=last_played,
        favorited_at=favorited_at,
    )


def serialize_item(item) -> MediaItemSummary:
    """序列化媒体项基本信息"""
    return MediaItemSummary(
        id=item.Id,
        name=item.Name,
        type=item.Type.value if item.Type else None,
        overview=item.Overview,
        tagline=item.Tagline,
        premiere_date=item.PremiereDate.isoformat() if item.PremiereDate else None,
        end_date=item.EndDate.isoformat() if item.EndDate else None,
        official_rating=item.OfficialRating,
        community_rating=item.CommunityRating,
        critic_rating=item.CriticRating,
        date_created=item.DateCreated.isoformat() if item.DateCreated else None,
        date_modified=item.DateModified.isoformat() if item.DateModified else None,
        source_id=item.SourceId,
        source_link=item.SourceLink,
        source_name=None,
    )


def serialize_file_info(file, file_link) -> FileInfoDetail:
    """序列化文件详情"""
    return FileInfoDetail(
        id=file.Id,
        name=file.Name,
        path=file.Path,
        type=file.Type.value if file.Type else None,
        link_type=file_link.LinkType.value if file_link.LinkType else None,
        item_id=file_link.ItemId,
        image_type=file_link.ImageType.value if file_link.ImageType else None,
        image_index=file_link.ImageIndex,
        size=file.Size,
        etag=file.Etag,
        ffmpeg=file.FFmpeg,
    )
