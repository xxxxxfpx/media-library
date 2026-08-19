"""
用户设置 Schema

用于 User.Setting JSON 字段的数据交互
"""

from pydantic import BaseModel, Field
from typing import Optional


class UserSettings(BaseModel):
    """用户设置模型"""
    
    # 主题设置
    theme_preset: Optional[str] = Field(None, description="主题预设：modernBlack/modernWhite/currentPurple/ocean/forest")
    theme_mode: Optional[str] = Field(None, description="主题模式：light/dark/system")
    primary_color: Optional[str] = Field(None, description="主题色（兼容旧版本，已废弃请使用 theme_preset）")
    
    # 播放设置
    default_playback_rate: Optional[float] = Field(None, description="默认播放速率")
    resume_playback: Optional[bool] = Field(None, description="恢复播放位置")
    
    # 通知设置
    enable_notifications: Optional[bool] = Field(None, description="启用通知")
    notification_sound: Optional[bool] = Field(None, description="通知声音")
    
    # 高级设置
    enable_hardware_acceleration: Optional[bool] = Field(None, description="启用硬件加速")
    cache_mode: Optional[str] = Field(None, description="缓存模式：memory/disk，使用内存缓存或磁盘缓存")
    forward_cache_size_mb: Optional[int] = Field(None, description="前置缓存大小 (MB)，用于预加载后续数据")
    backward_cache_size_mb: Optional[int] = Field(None, description="后置缓存大小 (MB)，用于回退 seek 时的缓存")
    media_retry_interval: Optional[int] = Field(None, description="媒体列表自动重试间隔 (秒)")
    
    # 通用设置
    auto_sync_interval: Optional[int] = Field(None, description="自动同步用户设置的时间间隔 (秒)，1-600 秒")
    
    def is_set(self, field: str) -> bool:
        """检查字段是否被设置"""
        return field in self.model_fields_set


class UpdateUserSettingsRequest(UserSettings):
    """更新用户设置请求
    
    继承自 UserSettings，支持 PATCH 语义
    """
    
    def to_dict(self) -> dict:
        """转换为字典，只包含被设置的字段（非 None）"""
        return {k: v for k, v in self.model_dump().items() if v is not None}