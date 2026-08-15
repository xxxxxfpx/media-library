class LoginResponse {
  final String accessToken;
  final String refreshToken;
  final String tokenType;

  LoginResponse({
    required this.accessToken,
    required this.refreshToken,
    required this.tokenType,
  });

  factory LoginResponse.fromJson(Map<String, dynamic> json) {
    return LoginResponse(
      accessToken: json['access_token'] as String,
      refreshToken: json['refresh_token'] as String,
      tokenType: json['token_type'] as String? ?? 'bearer',
    );
  }
}

class UserInfo {
  final int id;
  final String username;
  final String? email;
  final bool isAdmin;
  final bool isActive;
  final String? createdAt;

  UserInfo({
    required this.id,
    required this.username,
    this.email,
    required this.isAdmin,
    required this.isActive,
    this.createdAt,
  });

  factory UserInfo.fromJson(Map<String, dynamic> json) {
    return UserInfo(
      id: (json['id'] as num).toInt(),
      username: json['username'] as String,
      email: json['email'] as String?,
      isAdmin: json['is_admin'] as bool? ?? false,
      isActive: json['is_active'] as bool? ?? true,
      createdAt: json['created_at'] as String?,
    );
  }
}

class UserSetting {
  // 主题设置
  final String? themeMode;
  final String? primaryColor;
  
  // 播放设置
  final double? defaultPlaybackRate;
  final bool? resumePlayback;
  
  // 通知设置
  final bool? enableNotifications;
  final bool? notificationSound;
  
  // 高级设置
  final bool? enableHardwareAcceleration;
  final String? cacheMode;
  final int? forwardCacheSizeMb;
  final int? backwardCacheSizeMb;
  final int? mediaRetryInterval;
  
  // 通用设置
  final int? autoSyncInterval;

  UserSetting({
    this.themeMode,
    this.primaryColor,
    this.defaultPlaybackRate,
    this.resumePlayback,
    this.enableNotifications,
    this.notificationSound,
    this.enableHardwareAcceleration,
    this.cacheMode,
    this.forwardCacheSizeMb,
    this.backwardCacheSizeMb,
    this.mediaRetryInterval,
    this.autoSyncInterval,
  });

  factory UserSetting.fromJson(Map<String, dynamic> json) {
    return UserSetting(
      themeMode: json['theme_mode'] as String?,
      primaryColor: json['primary_color'] as String?,
      defaultPlaybackRate: (json['default_playback_rate'] as num?)?.toDouble(),
      resumePlayback: json['resume_playback'] as bool?,
      enableNotifications: json['enable_notifications'] as bool?,
      notificationSound: json['notification_sound'] as bool?,
      enableHardwareAcceleration: json['enable_hardware_acceleration'] as bool?,
      cacheMode: json['cache_mode'] as String?,
      forwardCacheSizeMb: json['forward_cache_size_mb'] as int?,
      backwardCacheSizeMb: json['backward_cache_size_mb'] as int?,
      mediaRetryInterval: json['media_retry_interval'] as int?,
      autoSyncInterval: json['auto_sync_interval'] as int?,
    );
  }

  Map<String, dynamic> toJson() => {
        if (themeMode != null) 'theme_mode': themeMode,
        if (primaryColor != null) 'primary_color': primaryColor,
        if (defaultPlaybackRate != null) 'default_playback_rate': defaultPlaybackRate,
        if (resumePlayback != null) 'resume_playback': resumePlayback,
        if (enableNotifications != null) 'enable_notifications': enableNotifications,
        if (notificationSound != null) 'notification_sound': notificationSound,
        if (enableHardwareAcceleration != null) 'enable_hardware_acceleration': enableHardwareAcceleration,
        if (cacheMode != null) 'cache_mode': cacheMode,
        if (forwardCacheSizeMb != null) 'forward_cache_size_mb': forwardCacheSizeMb,
        if (backwardCacheSizeMb != null) 'backward_cache_size_mb': backwardCacheSizeMb,
        if (mediaRetryInterval != null) 'media_retry_interval': mediaRetryInterval,
        if (autoSyncInterval != null) 'auto_sync_interval': autoSyncInterval,
      };

  UserSetting copyWith({
    String? themeMode,
    String? primaryColor,
    double? defaultPlaybackRate,
    bool? resumePlayback,
    bool? enableNotifications,
    bool? notificationSound,
    bool? enableHardwareAcceleration,
    String? cacheMode,
    int? forwardCacheSizeMb,
    int? backwardCacheSizeMb,
    int? mediaRetryInterval,
    int? autoSyncInterval,
  }) {
    return UserSetting(
      themeMode: themeMode ?? this.themeMode,
      primaryColor: primaryColor ?? this.primaryColor,
      defaultPlaybackRate: defaultPlaybackRate ?? this.defaultPlaybackRate,
      resumePlayback: resumePlayback ?? this.resumePlayback,
      enableNotifications: enableNotifications ?? this.enableNotifications,
      notificationSound: notificationSound ?? this.notificationSound,
      enableHardwareAcceleration: enableHardwareAcceleration ?? this.enableHardwareAcceleration,
      cacheMode: cacheMode ?? this.cacheMode,
      forwardCacheSizeMb: forwardCacheSizeMb ?? this.forwardCacheSizeMb,
      backwardCacheSizeMb: backwardCacheSizeMb ?? this.backwardCacheSizeMb,
      mediaRetryInterval: mediaRetryInterval ?? this.mediaRetryInterval,
      autoSyncInterval: autoSyncInterval ?? this.autoSyncInterval,
    );
  }
}
