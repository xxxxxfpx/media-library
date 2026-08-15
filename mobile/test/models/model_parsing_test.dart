import 'package:flutter_test/flutter_test.dart';
import 'package:media_app/core/constants.dart';
import 'package:media_app/data/models/auth.dart';
import 'package:media_app/data/models/media.dart';
import 'package:media_app/data/models/system.dart';

void main() {
  group('Auth model parsing', () {
    test('LoginResponse parses valid backend response', () {
      final json = {
        'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9',
        'refresh_token': 'refresh_abc123',
        'token_type': 'bearer',
      };

      final result = LoginResponse.fromJson(json);

      expect(result.accessToken, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9');
      expect(result.refreshToken, 'refresh_abc123');
      expect(result.tokenType, 'bearer');
    });

    test('LoginResponse handles missing token_type', () {
      final json = {
        'access_token': 'access',
        'refresh_token': 'refresh',
      };

      final result = LoginResponse.fromJson(json);

      expect(result.tokenType, 'bearer'); // default value
    });

    test('UserInfo parses valid backend response', () {
      final json = {
        'id': 42,
        'username': 'admin',
        'email': 'admin@example.com',
        'is_admin': true,
        'is_active': true,
        'created_at': '2024-01-15T10:30:00Z',
      };

      final result = UserInfo.fromJson(json);

      expect(result.id, 42);
      expect(result.username, 'admin');
      expect(result.email, 'admin@example.com');
      expect(result.isAdmin, true);
      expect(result.isActive, true);
      expect(result.createdAt, '2024-01-15T10:30:00Z');
    });

    test('UserInfo handles missing optional fields', () {
      final json = {
        'id': 1,
        'username': 'testuser',
      };

      final result = UserInfo.fromJson(json);

      expect(result.id, 1);
      expect(result.username, 'testuser');
      expect(result.email, isNull);
      expect(result.isAdmin, false); // default
      expect(result.isActive, true); // default
    });

    test('UserSetting parses valid backend response', () {
      final json = {'theme_mode': 'dark'};

      final result = UserSetting.fromJson(json);

      expect(result.themeMode, 'dark');
    });
  });

  group('Media model parsing', () {
    test('MediaItem parses movie response', () {
      final json = {
        'id': 100,
        'name': 'Inception',
        'type': 'Movie',
        'overview': 'A thief who steals corporate secrets through dream-sharing technology.',
        'tagline': 'Your mind is the scene of the crime.',
        'premiere_date': '2010-07-16',
        'official_rating': 'PG-13',
        'community_rating': 8.8,
        'critic_rating': 74.0,
        'production_year': 2010,
        'run_time_ticks': 828000000000,
        'has_children': false,
        'files': <Map<String, dynamic>>[],
        'links': <Map<String, dynamic>>[],
        'userdata': null,
        'alias': <Map<String, dynamic>>[],
      };

      final result = MediaItem.fromJson(json);

      expect(result.id, 100);
      expect(result.name, 'Inception');
      expect(result.type, 'Movie');
      expect(result.overview, contains('dream-sharing'));
      expect(result.communityRating, 8.8);
      expect(result.productionYear, 2010);
      expect(result.mediaType, MediaType.Movie);
    });

    test('MediaItem handles series response', () {
      final json = {
        'id': 200,
        'name': 'Breaking Bad',
        'type': 'Series',
        'premiere_date': '2008-01-20',
        'production_year': 2008,
        'has_children': true,
        'files': <Map<String, dynamic>>[],
        'links': <Map<String, dynamic>>[],
        'userdata': {
          'is_favorite': true,
          'playback_position_ticks': 180000000000,
          'play_count': 3,
        },
        'alias': <Map<String, dynamic>>[],
      };

      final result = MediaItem.fromJson(json);

      expect(result.id, 200);
      expect(result.name, 'Breaking Bad');
      expect(result.mediaType, MediaType.Series);
      expect(result.hasChildren, true);
      expect(result.userdata?.isFavorite, true);
      expect(result.userdata?.playCount, 3);
    });

    test('MediaItem handles null numeric fields', () {
      final json = {
        'id': 300,
        'name': 'Test Movie',
        'type': 'Movie',
        'community_rating': null,
        'critic_rating': null,
        'production_year': null,
        'files': <Map<String, dynamic>>[],
        'links': <Map<String, dynamic>>[],
        'alias': <Map<String, dynamic>>[],
      };

      final result = MediaItem.fromJson(json);

      expect(result.communityRating, isNull);
      expect(result.criticRating, isNull);
      expect(result.productionYear, isNull);
    });

    test('MediaListResponse parses pagination fields', () {
      final json = {
        'items': <Map<String, dynamic>>[],
        'total': 150,
        'limit': 50,
        'offset': 100,
      };

      final result = MediaListResponse.fromJson(json);

      expect(result.total, 150);
      expect(result.limit, 50);
      expect(result.offset, 100);
    });

    test('MediaStats parses counts', () {
      final json = {
        'video_count': 120,
        'audio_count': 45,
        'image_count': 300,
        'ebook_count': 25,
      };

      final result = MediaStats.fromJson(json);

      expect(result.videoCount, 120);
      expect(result.audioCount, 45);
      expect(result.imageCount, 300);
      expect(result.ebookCount, 25);
    });

    test('UserData parses playback info', () {
      final json = {
        'is_favorite': true,
        'playback_position_ticks': 36000000000,
        'playback_rate': 1.5,
        'play_count': 2,
        'is_played': false,
        'rating': 9.0,
        'last_played_date': DateTime.now().subtract(const Duration(days: 10)).toIso8601String(),
      };

      final result = UserData.fromJson(json);

      expect(result.isFavorite, true);
      expect(result.playbackPositionTicks, 36000000000);
      expect(result.playbackRate, 1.5);
      expect(result.playCount, 2);
      expect(result.isPlayed, false);
      expect(result.rating, 9.0);
      expect(result.lastPlayedDisplay, '10 天前');
    });

    test('UserData lastPlayedDisplay formats correctly', () {
      // Recent playback (less than 1 minute)
      final recentJson = {
        'last_played_date': DateTime.now().subtract(const Duration(seconds: 30)).toIso8601String(),
      };
      expect(UserData.fromJson(recentJson).lastPlayedDisplay, '刚刚');

      // Minutes ago
      final minutesJson = {
        'last_played_date': DateTime.now().subtract(const Duration(minutes: 5)).toIso8601String(),
      };
      expect(UserData.fromJson(minutesJson).lastPlayedDisplay, '5 分钟前');

      // Hours ago
      final hoursJson = {
        'last_played_date': DateTime.now().subtract(const Duration(hours: 3)).toIso8601String(),
      };
      expect(UserData.fromJson(hoursJson).lastPlayedDisplay, '3 小时前');
    });
  });

  group('File model parsing', () {
    test('FileInfo parses basic file', () {
      final json = {
        'id': 1001,
        'name': 'movie.mkv',
        'path': '/mnt/media/movies/movie.mkv',
        'type': 'Video',
        'size': 15000000000,
        'etag': 'abc123',
      };

      final result = FileInfo.fromJson(json);

      expect(result.id, 1001);
      expect(result.name, 'movie.mkv');
      expect(result.path, '/mnt/media/movies/movie.mkv');
      expect(result.type, 'Video');
      expect(result.size, 15000000000);
    });

    test('FileInfo parses image file with imageType', () {
      final json = {
        'id': 1002,
        'name': 'poster.jpg',
        'type': 'Image',
        'image_type': 'Primary',
        'image_index': 0,
      };

      final result = FileInfo.fromJson(json);

      expect(result.imageType, 'Primary');
      expect(result.imageIndex, 0);
    });

    test('FileInfo parses ffmpeg probe data', () {
      final json = {
        'id': 1003,
        'name': 'video.mp4',
        'type': 'Video',
        'ffmpeg': {
          'duration': '7200.5',
          'width': 1920,
          'height': 1080,
          'codec': 'h264',
        },
      };

      final result = FileInfo.fromJson(json);

      expect(result.ffmpeg, isNotNull);
      expect(result.ffmpeg?['duration'], '7200.5');
      expect(result.ffmpeg?['width'], 1920);
    });

    test('FileInfo handles ffmpeg as JSON string', () {
      final json = {
        'id': 1004,
        'name': 'video.mp4',
        'type': 'Video',
        'ffmpeg': '{"duration": "3600", "codec": "hevc"}', // JSON string
      };

      final result = FileInfo.fromJson(json);

      expect(result.ffmpeg, isNotNull);
      expect(result.ffmpeg?['duration'], '3600');
    });

    test('FileInfo handles null ffmpeg', () {
      final json = {
        'id': 1005,
        'name': 'video.mp4',
        'type': 'Video',
        'ffmpeg': null,
      };

      final result = FileInfo.fromJson(json);

      expect(result.ffmpeg, isNull);
    });
  });

  group('System model parsing', () {
    test('SystemInfo parses valid response', () {
      final json = {
        'hostname': 'media-server',
        'cpu_percent': 45.5,
        'memory_percent': 62.3,
        'disk_percent': 78.0,
        'platform': 'Linux',
        'python_version': '3.11.0',
        'uptime_seconds': 86400.0,
        'load_average_1m': 1.5,
        'memory_used': '16 GB',
        'memory_total': '32 GB',
        'disk_used': '780 GB',
        'disk_total': '1 TB',
      };

      final result = SystemInfo.fromJson(json);

      expect(result.hostname, 'media-server');
      expect(result.cpuPercent, 45.5);
      expect(result.memoryPercent, 62.3);
      expect(result.diskPercent, 78.0);
      expect(result.uptimeSeconds, 86400.0);
    });

    test('SystemInfo handles null numeric fields', () {
      final json = {
        'hostname': 'test',
        'cpu_percent': null,
        'memory_percent': null,
      };

      final result = SystemInfo.fromJson(json);

      expect(result.cpuPercent, isNull);
      expect(result.memoryPercent, isNull);
    });

    test('SystemSetting parses with defaults', () {
      final json = {
        'sync_interval_seconds': 120,
        'hero_media_card': {
          'disable_click': true,
          'disable_favorite': true,
          'hide_type_badge': true,
          'hide_rating_badge': true,
          'hide_overlay': false,
          'hide_card_info': true,
        },
        'list_media_card': {
          'disable_click': false,
          'disable_favorite': false,
          'hide_type_badge': false,
          'hide_rating_badge': false,
          'hide_overlay': false,
          'hide_card_info': false,
        },
      };

      final result = SystemSetting.fromJson(json);

      expect(result.syncIntervalSeconds, 120);
      expect(result.heroMediaCard.disableClick, true);
      expect(result.listMediaCard.disableClick, false);
    });

    test('SystemSetting uses default values for missing fields', () {
      final json = <String, dynamic>{};

      final result = SystemSetting.fromJson(json);

      expect(result.syncIntervalSeconds, 60); // default
      expect(result.heroMediaCard.disableClick, true); // default
    });

    test('MediaCardConfig parses hero config', () {
      final json = {
        'disable_click': true,
        'disable_favorite': true,
        'hide_type_badge': true,
        'hide_rating_badge': true,
        'hide_overlay': false,
        'hide_card_info': true,
      };

      final result = MediaCardConfig.fromHeroJson(json);

      expect(result.disableClick, true);
      expect(result.hideTypeBadge, true);
    });

    test('MediaCardConfig parses list config', () {
      final json = {
        'disable_click': false,
        'disable_favorite': false,
        'hide_type_badge': false,
        'hide_rating_badge': false,
        'hide_overlay': false,
        'hide_card_info': false,
      };

      final result = MediaCardConfig.fromListJson(json);

      expect(result.disableClick, false);
      expect(result.hideCardInfo, false);
    });
  });

  group('Edge cases', () {
    test('MediaType maps correctly from backend string', () {
      expect(MediaType.values.firstWhere((e) => e.name == 'Movie'), MediaType.Movie);
      expect(MediaType.values.firstWhere((e) => e.name == 'Series'), MediaType.Series);
      expect(MediaType.values.firstWhere((e) => e.name == 'Audio'), MediaType.Audio);
      expect(MediaType.values.firstWhere((e) => e.name == 'Photo'), MediaType.Photo);
      expect(MediaType.values.firstWhere((e) => e.name == 'Book'), MediaType.Book);
      expect(MediaType.values.firstWhere((e) => e.name == 'Episode'), MediaType.Episode);
      expect(MediaType.values.firstWhere((e) => e.name == 'unknown'), MediaType.unknown);
    });

    test('MediaItem.getPrimaryImageUrl returns correct format', () {
      final json = {
        'id': 1,
        'name': 'Test',
        'type': 'Movie',
        'files': [
          {'id': 100, 'type': 'Image', 'image_type': 'Primary'},
          {'id': 101, 'type': 'Image', 'image_type': 'Banner'},
        ],
        'links': <Map<String, dynamic>>[],
        'alias': <Map<String, dynamic>>[],
      };

      final item = MediaItem.fromJson(json);
      expect(item.getPrimaryImageUrl(), '/api/file/data?file_id=100');
    });

    test('MediaItem.getPrimaryImageUrl falls back to first file', () {
      final json = {
        'id': 1,
        'name': 'Test',
        'type': 'Movie',
        'files': [
          {'id': 200, 'type': 'Video'},
          {'id': 201, 'type': 'Image'},
        ],
        'links': <Map<String, dynamic>>[],
        'alias': <Map<String, dynamic>>[],
      };

      final item = MediaItem.fromJson(json);
      expect(item.getPrimaryImageUrl(), '/api/file/data?file_id=201'); // first image
    });

    test('MediaItem.getPrimaryImageUrl returns null when no files', () {
      final json = {
        'id': 1,
        'name': 'Test',
        'type': 'Movie',
        'files': <Map<String, dynamic>>[],
        'links': <Map<String, dynamic>>[],
        'alias': <Map<String, dynamic>>[],
      };

      final item = MediaItem.fromJson(json);
      expect(item.getPrimaryImageUrl(), isNull);
    });
  });
}