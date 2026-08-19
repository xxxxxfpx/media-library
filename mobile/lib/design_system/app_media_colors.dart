import 'package:flutter/material.dart';

/// 业务固定色 — 集中定义，仅此文件允许硬编码色值，页面禁止直接写 Color(0x...)
abstract class AppMediaColors {
  // 文件类型
  static const Color fileImage = Color(0xFF4CAF50);
  static const Color fileVideo = Color(0xFF2196F3);
  static const Color fileAudio = Color(0xFFFF9800);
  static const Color fileSubtitle = Color(0xFF00BCD4);
  static const Color fileNfo = Color(0xFF9E9E9E);
  static const Color fileData = Color(0xFF607D8B);
  static const Color fileAttachment = Color(0xFF795548);

  // 统计卡
  static const Color statVideo = Color(0xFF2196F3);
  static const Color statAudio = Color(0xFF4CAF50);
  static const Color statImage = Color(0xFFFF9800);
  static const Color statBook = Color(0xFF9C27B0);
}
