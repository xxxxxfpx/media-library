class SystemInfo {
  final String? hostname;
  final double? cpuPercent;
  final double? memoryPercent;
  final double? diskPercent;
  final String? platform;
  final String? pythonVersion;
  final double? uptimeSeconds;
  final double? loadAverage1m;
  final String? memoryUsed;
  final String? memoryTotal;
  final String? diskUsed;
  final String? diskTotal;

  SystemInfo({
    this.hostname,
    this.cpuPercent,
    this.memoryPercent,
    this.diskPercent,
    this.platform,
    this.pythonVersion,
    this.uptimeSeconds,
    this.loadAverage1m,
    this.memoryUsed,
    this.memoryTotal,
    this.diskUsed,
    this.diskTotal,
  });

  factory SystemInfo.fromJson(Map<String, dynamic> json) {
    return SystemInfo(
      hostname: json['hostname'] as String?,
      cpuPercent: (json['cpu_percent'] as num?)?.toDouble(),
      memoryPercent: (json['memory_percent'] as num?)?.toDouble(),
      diskPercent: (json['disk_percent'] as num?)?.toDouble(),
      platform: json['platform'] as String?,
      pythonVersion: json['python_version'] as String?,
      uptimeSeconds: (json['uptime_seconds'] as num?)?.toDouble(),
      loadAverage1m: (json['load_average_1m'] as num?)?.toDouble(),
      memoryUsed: json['memory_used'] as String?,
      memoryTotal: json['memory_total'] as String?,
      diskUsed: json['disk_used'] as String?,
      diskTotal: json['disk_total'] as String?,
    );
  }
}

class SystemSetting {
  final int syncIntervalSeconds;
  final MediaCardConfig heroMediaCard;
  final MediaCardConfig listMediaCard;

  SystemSetting({
    this.syncIntervalSeconds = 60,
    MediaCardConfig? heroMediaCard,
    MediaCardConfig? listMediaCard,
  })  : heroMediaCard = heroMediaCard ?? MediaCardConfig.defaultHero,
        listMediaCard = listMediaCard ?? MediaCardConfig.defaultList;

  factory SystemSetting.fromJson(Map<String, dynamic> json) {
    return SystemSetting(
      syncIntervalSeconds: (json['sync_interval_seconds'] as num?)?.toInt() ?? 60,
      heroMediaCard: json['hero_media_card'] != null
          ? MediaCardConfig.fromHeroJson(
              json['hero_media_card'] as Map<String, dynamic>)
          : MediaCardConfig.defaultHero,
      listMediaCard: json['list_media_card'] != null
          ? MediaCardConfig.fromListJson(
              json['list_media_card'] as Map<String, dynamic>)
          : MediaCardConfig.defaultList,
    );
  }

  Map<String, dynamic> toJson() => {
        'sync_interval_seconds': syncIntervalSeconds,
        'hero_media_card': heroMediaCard.toHeroJson(),
        'list_media_card': listMediaCard.toListJson(),
      };
}

class MediaCardConfig {
  final bool disableClick;
  final bool disableFavorite;
  final bool hideTypeBadge;
  final bool hideRatingBadge;
  final bool hideOverlay;
  final bool hideCardInfo;

  const MediaCardConfig({
    this.disableClick = false,
    this.disableFavorite = false,
    this.hideTypeBadge = false,
    this.hideRatingBadge = false,
    this.hideOverlay = false,
    this.hideCardInfo = false,
  });

  MediaCardConfig copyWith({
    bool? disableClick,
    bool? disableFavorite,
    bool? hideTypeBadge,
    bool? hideRatingBadge,
    bool? hideOverlay,
    bool? hideCardInfo,
  }) {
    return MediaCardConfig(
      disableClick: disableClick ?? this.disableClick,
      disableFavorite: disableFavorite ?? this.disableFavorite,
      hideTypeBadge: hideTypeBadge ?? this.hideTypeBadge,
      hideRatingBadge: hideRatingBadge ?? this.hideRatingBadge,
      hideOverlay: hideOverlay ?? this.hideOverlay,
      hideCardInfo: hideCardInfo ?? this.hideCardInfo,
    );
  }

  static const defaultHero = MediaCardConfig(
    disableClick: true,
    disableFavorite: true,
    hideTypeBadge: true,
    hideRatingBadge: true,
    hideOverlay: false,
    hideCardInfo: true,
  );

  static const defaultList = MediaCardConfig(
    disableClick: false,
    disableFavorite: false,
    hideTypeBadge: false,
    hideRatingBadge: false,
    hideOverlay: false,
    hideCardInfo: false,
  );

  factory MediaCardConfig.fromHeroJson(Map<String, dynamic> json) {
    return MediaCardConfig(
      disableClick: json['disable_click'] as bool? ?? true,
      disableFavorite: json['disable_favorite'] as bool? ?? true,
      hideTypeBadge: json['hide_type_badge'] as bool? ?? true,
      hideRatingBadge: json['hide_rating_badge'] as bool? ?? true,
      hideOverlay: json['hide_overlay'] as bool? ?? false,
      hideCardInfo: json['hide_card_info'] as bool? ?? true,
    );
  }

  factory MediaCardConfig.fromListJson(Map<String, dynamic> json) {
    return MediaCardConfig(
      disableClick: json['disable_click'] as bool? ?? false,
      disableFavorite: json['disable_favorite'] as bool? ?? false,
      hideTypeBadge: json['hide_type_badge'] as bool? ?? false,
      hideRatingBadge: json['hide_rating_badge'] as bool? ?? false,
      hideOverlay: json['hide_overlay'] as bool? ?? false,
      hideCardInfo: json['hide_card_info'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toHeroJson() => {
        'disable_click': disableClick,
        'disable_favorite': disableFavorite,
        'hide_type_badge': hideTypeBadge,
        'hide_rating_badge': hideRatingBadge,
        'hide_overlay': hideOverlay,
        'hide_card_info': hideCardInfo,
      };

  Map<String, dynamic> toListJson() => {
        'disable_click': disableClick,
        'disable_favorite': disableFavorite,
        'hide_type_badge': hideTypeBadge,
        'hide_rating_badge': hideRatingBadge,
        'hide_overlay': hideOverlay,
        'hide_card_info': hideCardInfo,
      };
}
