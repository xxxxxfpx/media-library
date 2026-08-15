import 'dart:convert';
import '../../core/constants.dart';

class MediaItem {
  final int id;
  final String? name;
  final String? type;
  final String? overview;
  final String? tagline;
  final String? premiereDate;
  final String? endDate;
  final String? officialRating;
  final double? communityRating;
  final double? criticRating;
  final int? productionYear;
  final int? runTimeTicks;
  final String? dateCreated;
  final String? dateModified;
  final bool? hasChildren;
  final String? album;
  final String? artist;
  final String? author;
  final String? publisher;
  final String? publisherYear;
  final List<FileInfo> files;
  final List<LinkInfo> links;
  final UserData? userdata;
  final List<AliasInfo> alias;

  MediaItem({
    required this.id,
    this.name,
    this.type,
    this.overview,
    this.tagline,
    this.premiereDate,
    this.endDate,
    this.officialRating,
    this.communityRating,
    this.criticRating,
    this.productionYear,
    this.runTimeTicks,
    this.dateCreated,
    this.dateModified,
    this.hasChildren,
    this.album,
    this.artist,
    this.author,
    this.publisher,
    this.publisherYear,
    this.files = const [],
    this.links = const [],
    this.userdata,
    this.alias = const [],
  });

  String? getPrimaryImageUrl({String? token}) {
    String withToken(String url) {
      if (token == null || token.isEmpty) return url;
      return '$url&token=${Uri.encodeComponent(token)}';
    }

    for (final f in files) {
      if (f.imageType == 'Primary') {
        return withToken('/api/file/data?file_id=${f.id}');
      }
    }
    if (files.isNotEmpty) {
      final firstImage = files.firstWhere(
        (f) => f.type == 'Image',
        orElse: () => files.first,
      );
      return withToken('/api/file/data?file_id=${firstImage.id}');
    }
    return null;
  }

  MediaType get mediaType {
    if (type == null){
      return MediaType.unknown;
    }else{
      return MediaType.values.firstWhere((e) => e.name == type, orElse: () => MediaType.unknown);
    }
  }

  factory MediaItem.fromJson(Map<String, dynamic> json) {
    return MediaItem(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String?,
      type: json['type'] as String?,
      overview: json['overview'] as String?,
      tagline: json['tagline'] as String?,
      premiereDate: json['premiere_date'] as String?,
      endDate: json['end_date'] as String?,
      officialRating: json['official_rating'] as String?,
      communityRating: (json['community_rating'] as num?)?.toDouble(),
      criticRating: (json['critic_rating'] as num?)?.toDouble(),
      productionYear: (json['production_year'] as num?)?.toInt(),
      runTimeTicks: (json['run_time_ticks'] as num?)?.toInt(),
      dateCreated: json['date_created'] as String?,
      dateModified: json['date_modified'] as String?,
      hasChildren: json['has_children'] as bool?,
      album: json['album'] as String?,
      artist: json['artist'] as String?,
      author: json['author'] as String?,
      publisher: json['publisher'] as String?,
      publisherYear: json['publisher_year'] as String?,
      files: (json['files'] as List<dynamic>?)
              ?.map((e) => FileInfo.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      links: (json['links'] as List<dynamic>?)
              ?.map((e) => LinkInfo.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      userdata: json['userdata'] != null
          ? UserData.fromJson(json['userdata'] as Map<String, dynamic>)
          : null,
      alias: (json['alias'] as List<dynamic>?)
              ?.map((e) => AliasInfo.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }
}

class MediaListResponse {
  final List<MediaItem> items;
  final int total;
  final int limit;
  final int offset;

  MediaListResponse({
    required this.items,
    required this.total,
    required this.limit,
    required this.offset,
  });

  factory MediaListResponse.fromJson(Map<String, dynamic> json) {
    return MediaListResponse(
      items: (json['items'] as List<dynamic>)
          .map((e) => MediaItem.fromJson(e as Map<String, dynamic>))
          .toList(),
      total: (json['total'] as num?)?.toInt() ?? 0,
      limit: (json['limit'] as num?)?.toInt() ?? 50,
      offset: (json['offset'] as num?)?.toInt() ?? 0,
    );
  }
}

class MediaStats {
  final int videoCount;
  final int audioCount;
  final int imageCount;
  final int ebookCount;

  MediaStats({
    required this.videoCount,
    required this.audioCount,
    required this.imageCount,
    required this.ebookCount,
  });

  factory MediaStats.fromJson(Map<String, dynamic> json) {
    return MediaStats(
      videoCount: (json['video_count'] as num?)?.toInt() ?? 0,
      audioCount: (json['audio_count'] as num?)?.toInt() ?? 0,
      imageCount: (json['image_count'] as num?)?.toInt() ?? 0,
      ebookCount: (json['ebook_count'] as num?)?.toInt() ?? 0,
    );
  }
}

class FileInfo {
  final int id;
  final String? name;
  final String? path;
  final String? type;
  final String? imageType;
  final int? imageIndex;
  final int? size;
  final String? etag;
  final Map<String, dynamic>? ffmpeg;

  FileInfo({
    required this.id,
    this.name,
    this.path,
    this.type,
    this.imageType,
    this.imageIndex,
    this.size,
    this.etag,
    this.ffmpeg,
  });

  factory FileInfo.fromJson(Map<String, dynamic> json) {
    return FileInfo(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String?,
      path: json['path'] as String?,
      type: json['type'] as String?,
      imageType: json['image_type'] as String?,
      imageIndex: (json['image_index'] as num?)?.toInt(),
      size: (json['size'] as num?)?.toInt(),
      etag: json['etag'] as String?,
      ffmpeg: _parseFfmpeg(json['ffmpeg']),
    );
  }

  static Map<String, dynamic>? _parseFfmpeg(dynamic value) {
    if (value == null) return null;
    if (value is Map<String, dynamic>) return value;
    if (value is String) {
      try {
        final decoded = jsonDecode(value);
        if (decoded is Map<String, dynamic>) return decoded;
      } catch (_) {}
    }
    return null;
  }
}

class LinkInfo {
  final String? peopleType;
  final String? peopleRole;
  final String? sourceLink;
  final LinkedItem? linkedItem;

  LinkInfo({this.peopleType, this.peopleRole, this.sourceLink, this.linkedItem});

  factory LinkInfo.fromJson(Map<String, dynamic> json) {
    return LinkInfo(
      peopleType: json['people_type'] as String?,
      peopleRole: json['people_role'] as String?,
      sourceLink: json['source_link'] as String?,
      linkedItem: json['linked_item'] != null
          ? LinkedItem.fromJson(json['linked_item'] as Map<String, dynamic>)
          : null,
    );
  }
}

class LinkedItem {
  final int id;
  final String? name;
  final String? type;
  final String? overview;
  final String? tagline;
  final String? premiereDate;
  final String? officialRating;
  final double? communityRating;
  final String? primaryImage;
  final String? sourceLink;

  LinkedItem({
    required this.id,
    this.name,
    this.type,
    this.overview,
    this.tagline,
    this.premiereDate,
    this.officialRating,
    this.communityRating,
    this.primaryImage,
    this.sourceLink,
  });

  factory LinkedItem.fromJson(Map<String, dynamic> json) {
    return LinkedItem(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String?,
      type: json['type'] as String?,
      overview: json['overview'] as String?,
      tagline: json['tagline'] as String?,
      premiereDate: json['premiere_date'] as String?,
      officialRating: json['official_rating'] as String?,
      communityRating: (json['community_rating'] as num?)?.toDouble(),
      primaryImage: json['primary_image'] as String?,
      sourceLink: json['source_link'] as String?,
    );
  }
}

class UserData {
  final int? playbackPositionTicks;
  final double? playbackRate;
  final int? playCount;
  final bool? isPlayed;
  final double? rating;
  final DateTime? lastPlayedDate;
  final DateTime? favoritedAt;
  final bool? favorite;

  UserData({
    this.playbackPositionTicks,
    this.playbackRate,
    this.playCount,
    this.isPlayed,
    this.rating,
    this.lastPlayedDate,
    this.favoritedAt,
    this.favorite,
  });

  bool get isFavorite => favorite ?? (favoritedAt != null);

  String? get lastPlayedDisplay {
    if (lastPlayedDate != null) {
      final diff = DateTime.now().difference(lastPlayedDate!);
      if (diff.inMinutes < 1) return '刚刚';
      if (diff.inMinutes < 60) return '${diff.inMinutes} 分钟前';
      if (diff.inHours < 24) return '${diff.inHours} 小时前';
      if (diff.inDays < 30) return '${diff.inDays} 天前';
      return '${lastPlayedDate!.year}-${lastPlayedDate!.month.toString().padLeft(2, '0')}-${lastPlayedDate!.day.toString().padLeft(2, '0')}';
    }
    if (isPlayed == true) return '已观看';
    return null;
  }

  factory UserData.fromJson(Map<String, dynamic> json) {
    DateTime? lastPlayed;
    final lastPlayedStr = json['last_played_date'] as String?;
    if (lastPlayedStr != null) {
      lastPlayed = DateTime.tryParse(lastPlayedStr);
    }
    DateTime? favoritedAt;
    final favoritedAtStr = json['favorited_at'] as String?;
    if (favoritedAtStr != null) {
      favoritedAt = DateTime.tryParse(favoritedAtStr);
    }
    return UserData(
      playbackPositionTicks: (json['playback_position_ticks'] as num?)?.toInt(),
      playbackRate: (json['playback_rate'] as num?)?.toDouble(),
      playCount: (json['play_count'] as num?)?.toInt(),
      isPlayed: json['is_played'] as bool?,
      rating: (json['rating'] as num?)?.toDouble(),
      lastPlayedDate: lastPlayed,
      favoritedAt: favoritedAt,
      favorite: json['is_favorite'] as bool?,
    );
  }
}

class AliasInfo {
  final String? name;
  final String? source;

  AliasInfo({this.name, this.source});

  factory AliasInfo.fromJson(Map<String, dynamic> json) {
    return AliasInfo(
      name: json['name'] as String?,
      source: json['source'] as String?,
    );
  }
}

class UpdateUserDataRequest {
  final int itemId;
  final double? playbackPosition;
  final double? playbackRate;
  final bool? isFavorite;
  final bool? isPlayed;
  final int? playCount;
  final double? rating;
  final bool clearRating;

  UpdateUserDataRequest({
    required this.itemId,
    this.playbackPosition,
    this.playbackRate,
    this.isFavorite,
    this.isPlayed,
    this.playCount,
    this.rating,
    this.clearRating = false,
  });

  Map<String, dynamic> toJson() => {
        'item_id': itemId,
        if (playbackPosition != null) 'playback_position': playbackPosition,
        if (playbackRate != null) 'playback_rate': playbackRate,
        if (isFavorite != null) 'is_favorite': isFavorite,
        if (isPlayed != null) 'is_played': isPlayed,
        if (playCount != null) 'play_count': playCount,
        if (clearRating) 'rating': null else if (rating != null) 'rating': rating,
      };
}

/// 媒体列表请求参数
///
/// 封装 /api/media/list 的查询参数，用于横向媒体列表和网格页面之间传递筛选上下文。
class MediaListRequest {
  final Set<MediaType>? types;
  final bool favorite;
  final bool hasPlayback;
  final bool hasRating;
  final String? sortBy;
  final String? itemIds;
  final String? linkedItemIds;
  final String? search;

  const MediaListRequest({
    this.types,
    this.favorite = false,
    this.hasPlayback = false,
    this.hasRating = false,
    this.sortBy,
    this.itemIds,
    this.linkedItemIds,
    this.search,
  });

  /// 序列化为 API 查询参数（仅筛选字段，不含分页参数）
  Map<String, dynamic> toQueryParams() => {
        if (types != null && types!.isNotEmpty)
          'types': types!.map((t) => t.name).join(','),
        if (favorite) 'favorite': true,
        if (hasPlayback) 'has_playback': true,
        if (hasRating) 'has_rating': true,
        if (sortBy != null) 'sort_by': sortBy,
        if (itemIds != null) 'item_ids': itemIds,
        if (linkedItemIds != null) 'linked_item_ids': linkedItemIds,
        if (search != null) 'search': search,
      };

  MediaListRequest copyWith({
    Set<MediaType>? types,
    bool? favorite,
    bool? hasPlayback,
    bool? hasRating,
    String? sortBy,
    String? itemIds,
    String? linkedItemIds,
    String? search,
    bool clearTypes = false,
    bool clearItemIds = false,
    bool clearLinkedItemIds = false,
    bool clearSearch = false,
  }) =>
      MediaListRequest(
        types: clearTypes ? null : (types ?? this.types),
        favorite: favorite ?? this.favorite,
        hasPlayback: hasPlayback ?? this.hasPlayback,
        hasRating: hasRating ?? this.hasRating,
        sortBy: sortBy ?? this.sortBy,
        itemIds: clearItemIds ? null : (itemIds ?? this.itemIds),
        linkedItemIds:
            clearLinkedItemIds ? null : (linkedItemIds ?? this.linkedItemIds),
        search: clearSearch ? null : (search ?? this.search),
      );
}
