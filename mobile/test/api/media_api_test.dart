import 'package:flutter_test/flutter_test.dart';

import 'package:media_app/data/api/media_api.dart';
import 'package:media_app/data/models/media.dart';
import 'package:media_app/core/constants.dart';
import 'mock_helper.dart';

void main() {
  late MockApiClient mockClient;

  setUp(() async {
    final prefs = await createMockPrefs();
    mockClient = MockApiClient(prefs);
  });

  group('MediaApi', () {
    test('getList returns MediaListResponse', () async {
      mockClient.on('/api/media/list', () => mockResponse({
            'items': [
              {
                'id': 1,
                'name': 'Test Movie',
                'type': 'movie',
                'production_year': 2023,
              },
              {
                'id': 2,
                'name': 'Test Series',
                'type': 'series',
              },
            ],
            'total': 2,
            'limit': 60,
            'offset': 0,
          }));

      final api = MediaApi(mockClient);
      final result = await api.getList(const MediaListRequest());

      expect(result, isA<MediaListResponse>());
      expect(result.total, 2);
      expect(result.items.length, 2);
      expect(result.items[0].name, 'Test Movie');
      expect(result.items[0].type, 'movie');
      expect(result.items[1].name, 'Test Series');
    });

    test('getList with filters passes parameters', () async {
      mockClient.on('/api/media/list', () => mockResponse({
            'items': [],
            'total': 0,
            'limit': 10,
            'offset': 20,
          }));

      final api = MediaApi(mockClient);
      final result = await api.getList(
        const MediaListRequest(
          types: {MediaType.Movie, MediaType.Series},
          favorite: true,
          sortBy: 'name',
        ),
        limit: 10,
        offset: 20,
      );

      expect(result.total, 0);
      expect(result.limit, 10);
      expect(result.offset, 20);
    });

    test('getInfo returns MediaItem', () async {
      mockClient.on('/api/media/info', () => mockResponse({
            'id': 42,
            'name': 'Inception',
            'type': 'movie',
            'overview': 'A mind-bending thriller',
            'production_year': 2010,
            'community_rating': 8.8,
            'files': [
              {'id': 1, 'name': 'inception.mp4', 'type': 'video'},
            ],
          }));

      final api = MediaApi(mockClient);
      final result = await api.getInfo(42);

      expect(result.id, 42);
      expect(result.name, 'Inception');
      expect(result.type, 'movie');
      expect(result.productionYear, 2010);
      expect(result.communityRating, 8.8);
      expect(result.files.length, 1);
      expect(result.files[0].name, 'inception.mp4');
    });

    test('getInfo with minimal data', () async {
      mockClient.on('/api/media/info', () => mockResponse({
            'id': 99,
          }));

      final api = MediaApi(mockClient);
      final result = await api.getInfo(99);

      expect(result.id, 99);
      expect(result.name, isNull);
      expect(result.files, isEmpty);
      expect(result.links, isEmpty);
    });

    test('getStats returns MediaStats', () async {
      mockClient.on('/api/media/stats', () => mockResponse({
            'video_count': 100,
            'audio_count': 50,
            'image_count': 200,
            'ebook_count': 30,
          }));

      final api = MediaApi(mockClient);
      final result = await api.getStats();

      expect(result.videoCount, 100);
      expect(result.audioCount, 50);
      expect(result.imageCount, 200);
      expect(result.ebookCount, 30);
    });

    test('getStats with defaults', () async {
      mockClient.on('/api/media/stats', () => mockResponse({}));

      final api = MediaApi(mockClient);
      final result = await api.getStats();

      expect(result.videoCount, 0);
      expect(result.audioCount, 0);
    });
  });
}
