// Enum values mirror backend API values and intentionally use PascalCase.
// ignore_for_file: constant_identifier_names

import 'package:flutter/material.dart';
import 'package:flutter_lucide/flutter_lucide.dart';

/// 应用配置的全局类
class AppConstants {
  AppConstants._();

  /// 本地存储键：访问令牌
  static const String storageKeyAccessToken = 'access_token';

  /// 本地存储键：刷新令牌
  static const String storageKeyRefreshToken = 'refresh_token';

  /// 本地存储键：基础 URL
  static const String storageKeyBaseUrl = 'base_url';

  /// 本地存储键：主题模式
  static const String storageKeyTheme = 'theme_mode';

  /// 本地存储键：自动播放
  static const String storageKeyAutoPlay = 'auto_play';

  /// 本地存储键：静音
  static const String storageKeyMuted = 'muted';

  /// 本地存储键：同步间隔
  static const String storageKeySyncInterval = 'sync_interval';

  /// 本地存储键：标记已观看阈值
  static const String storageKeyWatchedThreshold = 'watched_threshold';

  /// 默认后端 API 地址
  static const String defaultBaseUrl = 'http://192.168.1.5:8000';
}

/// 媒体类型枚举，定义所有支持的媒体类型
///
/// 枚举名称与后端 API 返回的 MediaType.value 完全一致
enum MediaType {
  Movie("电影"),
  Series("剧集"),
  Season("季"),
  Episode("集"),
  Audio("音乐"),
  Photo("图片"),
  Book("电子书"),
  Person("人物"),
  Source("来源"),
  Studio("工作室"),
  Genre("类型"),
  Tag("标签"),
  BoxSet("集合"),
  unknown("未知");

  const MediaType(this.labelZH);
  final String labelZH;
}

/// 视图模式：网格或列表
enum ViewMode { grid, list }

/// 文件类型枚举
enum FileType { image, video, audio, subtitle, nfo, data, attachment }

/// 文件类型信息类，存储图标和颜色
class FileTypeInfo {
  /// 文件类型对应的图标
  final IconData icon;

  /// 文件类型对应的颜色
  final Color color;
  const FileTypeInfo(this.icon, this.color);
}

/// 文件类型信息映射，包含图标和颜色
const Map<FileType, FileTypeInfo> fileTypeInfo = {
  FileType.image: FileTypeInfo(LucideIcons.image, Color(0xFF4CAF50)),
  FileType.video: FileTypeInfo(LucideIcons.video, Color(0xFF2196F3)),
  FileType.audio: FileTypeInfo(LucideIcons.music, Color(0xFFFF9800)),
  FileType.subtitle: FileTypeInfo(LucideIcons.captions, Color(0xFF00BCD4)),
  FileType.nfo: FileTypeInfo(LucideIcons.file_text, Color(0xFF9E9E9E)),
  FileType.data: FileTypeInfo(LucideIcons.file, Color(0xFF607D8B)),
  FileType.attachment: FileTypeInfo(LucideIcons.paperclip, Color(0xFF795548)),
};

/// 媒体数据类型枚举，用于统计数据卡片
enum MediaDataType { videoCount, audioCount, imageCount, ebookCount }

/// 统计数据卡片配置类
class StatCardConfig {
  /// 卡片图标
  final IconData icon;

  /// 卡片颜色
  final Color color;

  /// 卡片显示文本
  final String label;

  /// 对应的数据类型键
  final MediaDataType dataKey;

  const StatCardConfig({
    required this.icon,
    required this.color,
    required this.label,
    required this.dataKey,
  });
}

/// 统计数据卡片配置列表，定义首页显示的统计卡片
const List<StatCardConfig> statCards = [
  StatCardConfig(
    icon: LucideIcons.video,
    color: Color(0xFF2196F3),
    label: '视频',
    dataKey: MediaDataType.videoCount,
  ),
  StatCardConfig(
    icon: LucideIcons.music,
    color: Color(0xFF4CAF50),
    label: '音乐',
    dataKey: MediaDataType.audioCount,
  ),
  StatCardConfig(
    icon: LucideIcons.image,
    color: Color(0xFFFF9800),
    label: '图片',
    dataKey: MediaDataType.imageCount,
  ),
  StatCardConfig(
    icon: LucideIcons.book_open,
    color: Color(0xFF9C27B0),
    label: '电子书',
    dataKey: MediaDataType.ebookCount,
  ),
];
