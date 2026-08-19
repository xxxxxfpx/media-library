import 'package:flutter/material.dart';

/// 统一 Material 图标映射 — 禁止页面直接散落 Icons.* / Lucide
abstract class AppIcons {
  // 媒体类型
  static const IconData movie = Icons.movie_outlined;
  static const IconData series = Icons.tv_outlined;
  static const IconData season = Icons.calendar_today_outlined;
  static const IconData episode = Icons.list_outlined;
  static const IconData audio = Icons.music_note_outlined;
  static const IconData photo = Icons.image_outlined;
  static const IconData book = Icons.book_outlined;
  static const IconData person = Icons.person_outline;
  static const IconData source = Icons.public_outlined;
  static const IconData studio = Icons.business_outlined;
  static const IconData genre = Icons.category_outlined;
  static const IconData tag = Icons.label_outline;
  static const IconData boxSet = Icons.inventory_2_outlined;
  static const IconData unknown = Icons.help_outline;

  // 文件类型
  static const IconData fileImage = Icons.image_outlined;
  static const IconData fileVideo = Icons.videocam_outlined;
  static const IconData fileAudio = Icons.audio_file_outlined;
  static const IconData fileSubtitle = Icons.subtitles_outlined;
  static const IconData fileNfo = Icons.description_outlined;
  static const IconData fileData = Icons.insert_drive_file_outlined;
  static const IconData fileAttachment = Icons.attach_file_outlined;

  // 导航
  static const IconData home = Icons.home_outlined;
  static const IconData homeFilled = Icons.home;
  static const IconData media = Icons.movie_outlined;
  static const IconData my = Icons.person_outline;
  static const IconData search = Icons.search;
  static const IconData filter = Icons.tune;
  static const IconData sort = Icons.sort;
  static const IconData grid = Icons.grid_view;
  static const IconData list = Icons.view_list_outlined;

  // 操作
  static const IconData favorite = Icons.favorite;
  static const IconData favoriteBorder = Icons.favorite_border;
  static const IconData play = Icons.play_arrow;
  static const IconData star = Icons.star;
  static const IconData starBorder = Icons.star_border;
  static const IconData share = Icons.share_outlined;
  static const IconData download = Icons.download_outlined;
  static const IconData copy = Icons.content_copy_outlined;
  static const IconData more = Icons.more_horiz;
  static const IconData chevronRight = Icons.chevron_right;
  static const IconData arrowBack = Icons.arrow_back;
  static const IconData close = Icons.close;
  static const IconData check = Icons.check;
  static const IconData refresh = Icons.refresh;
  static const IconData sync = Icons.sync;
  static const IconData settings = Icons.settings_outlined;
  static const IconData palette = Icons.palette_outlined;
  static const IconData brightness = Icons.brightness_medium_outlined;
  static const IconData logout = Icons.logout;
  static const IconData login = Icons.login;

  // 状态
  static const IconData error = Icons.error_outline;
  static const IconData empty = Icons.inbox_outlined;
  static const IconData loading = Icons.hourglass_empty;
}
