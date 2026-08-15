"""
用户相关 Schema
"""

from pydantic import BaseModel, Field
from typing import Optional


class UserInfo(BaseModel):
    """用户信息"""
    id: int
    username: str
    email: Optional[str] = None
    is_admin: bool
    is_active: bool
    created_at: Optional[str] = None


class UpdateUserDataRequest(BaseModel):
    """更新用户数据请求 - PATCH 语义

    使用 model_fields_set 区分：
    - {"rating": null} -> rating=None, "rating" in model_fields_set=True -> 清除评分
    - {"is_favorite": true} -> rating=None, "rating" in model_fields_set=False -> 不修改
    """
    item_id: int = Field(..., description="媒体项 ID")
    playback_position: Optional[float] = Field(None, description="播放位置")
    playback_rate: Optional[float] = Field(None, description="播放速率")
    is_favorite: Optional[bool] = Field(None, description="是否收藏")
    is_played: Optional[bool] = Field(None, description="是否已播放完成")
    play_count: Optional[int] = Field(None, description="播放次数")
    rating: Optional[float] = Field(None, description="用户评分")

    def is_set(self, field: str) -> bool:
        return field in self.model_fields_set
