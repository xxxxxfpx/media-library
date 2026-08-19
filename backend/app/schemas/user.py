"""
用户相关 Schema
"""


from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    """用户信息"""
    id: int
    username: str
    email: str | None = None
    is_admin: bool
    is_active: bool
    created_at: str | None = None


class UpdateUserDataRequest(BaseModel):
    """更新用户数据请求 - PATCH 语义

    使用 model_fields_set 区分：
    - {"rating": null} -> rating=None, "rating" in model_fields_set=True -> 清除评分
    - {"is_favorite": true} -> rating=None, "rating" in model_fields_set=False -> 不修改
    """
    item_id: int = Field(..., description="媒体项 ID")
    playback_position: float | None = Field(None, description="播放位置")
    playback_rate: float | None = Field(None, description="播放速率")
    is_favorite: bool | None = Field(None, description="是否收藏")
    is_played: bool | None = Field(None, description="是否已播放完成")
    play_count: int | None = Field(None, description="播放次数")
    rating: float | None = Field(None, description="用户评分")

    def is_set(self, field: str) -> bool:
        return field in self.model_fields_set


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码（至少 6 位）")
