# coding: utf-8
"""
用户服务层 - 用户数据管理
=========================

提供用户数据（收藏、播放状态、设置）的业务逻辑。

作者：白鸟青城
版本：4.0.0 (从 API 层迁入业务逻辑)
"""

import datetime
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, UserData
from app.schemas.user import UpdateUserDataRequest
from app.schemas.setting import UserSettings, UpdateUserSettingsRequest

logger = logging.getLogger(__name__)


async def update_userdata(
    db: AsyncSession,
    user_id: int,
    request: UpdateUserDataRequest,
) -> dict:
    stmt = select(UserData).where(
        UserData.UserId == user_id,
        UserData.ItemId == request.item_id,
    )
    result = await db.execute(stmt)
    user_data = result.scalar_one_or_none()

    if not user_data:
        user_data = UserData(
            UserId=user_id,
            ItemId=request.item_id,
        )
        db.add(user_data)

    if request.is_set("playback_position"):
        user_data.PlaybackPositionTicks = request.playback_position
        user_data.LastPlayedAt = datetime.datetime.now(datetime.timezone.utc)
    if request.is_set("playback_rate"):
        user_data.PlaybackRate = request.playback_rate
    if request.is_set("is_favorite"):
        if request.is_favorite:
            user_data.FavoritedAt = datetime.datetime.now(datetime.timezone.utc)
        else:
            user_data.FavoritedAt = None
    if request.is_set("is_played"):
        if request.is_played and not user_data.IsPlayed:
            user_data.PlayCount = (user_data.PlayCount or 0) + 1
        user_data.IsPlayed = request.is_played
        if request.is_played:
            user_data.LastPlayedAt = datetime.datetime.now(datetime.timezone.utc)
    if request.is_set("play_count"):
        user_data.PlayCount = request.play_count
    if request.is_set("rating"):
        user_data.Rating = request.rating

    user_data.UpdatedAt = datetime.datetime.now(datetime.timezone.utc)
    await db.commit()

    return {"message": "更新成功", "item_id": request.item_id}


async def get_user_setting(db: AsyncSession, user: User) -> UserSettings:
    if not user.Setting:
        return UserSettings()
    return UserSettings(**user.Setting)


async def update_user_setting(db: AsyncSession, user_id: int, setting: UpdateUserSettingsRequest) -> UserSettings:
    user = await db.get(User, user_id)
    
    current_settings = user.Setting or {}
    update_dict = setting.to_dict()
    current_settings.update(update_dict)
    
    user.Setting = current_settings
    await db.commit()
    
    return UserSettings(**current_settings)
