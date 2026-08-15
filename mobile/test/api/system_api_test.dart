import 'package:flutter_test/flutter_test.dart';

import 'package:media_app/data/api/system_api.dart';
import 'package:media_app/data/models/system.dart';
import 'mock_helper.dart';

void main() {
  late MockApiClient mockClient;

  setUp(() async {
    final prefs = await createMockPrefs();
    mockClient = MockApiClient(prefs);
  });

  group('SystemApi', () {
    test('getInfo returns SystemInfo', () async {
      mockClient.on('/api/system/info', () => mockResponse({
            'hostname': 'media-server',
            'cpu_percent': 45.2,
            'memory_percent': 62.8,
            'disk_percent': 71.5,
            'platform': 'Linux',
            'python_version': '3.12',
            'uptime_seconds': 86400,
            'load_average_1m': 1.5,
            'memory_used': '8.5 GB',
            'memory_total': '16 GB',
            'disk_used': '450 GB',
            'disk_total': '1 TB',
          }));

      final api = SystemApi(mockClient);
      final result = await api.getInfo();

      expect(result.hostname, 'media-server');
      expect(result.cpuPercent, 45.2);
      expect(result.memoryPercent, 62.8);
      expect(result.diskPercent, 71.5);
      expect(result.platform, 'Linux');
      expect(result.pythonVersion, '3.12');
      expect(result.uptimeSeconds, 86400);
      expect(result.loadAverage1m, 1.5);
      expect(result.memoryUsed, '8.5 GB');
      expect(result.memoryTotal, '16 GB');
    });

    test('getInfo handles null fields', () async {
      mockClient.on('/api/system/info', () => mockResponse({
            'hostname': 'server',
          }));

      final api = SystemApi(mockClient);
      final result = await api.getInfo();

      expect(result.hostname, 'server');
      expect(result.cpuPercent, isNull);
      expect(result.memoryPercent, isNull);
    });

    test('getSetting returns SystemSetting with defaults', () async {
      mockClient.on('/api/system/setting', () => mockResponse({
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
          }));

      final api = SystemApi(mockClient);
      final result = await api.getSetting();

      expect(result.syncIntervalSeconds, 120);
      expect(result.heroMediaCard.disableClick, true);
      expect(result.listMediaCard.disableClick, false);
    });

    test('getSetting returns defaults when empty', () async {
      mockClient.on('/api/system/setting', () => mockResponse({}));

      final api = SystemApi(mockClient);
      final result = await api.getSetting();

      // Should use default values
      expect(result.syncIntervalSeconds, 60);
      expect(result.heroMediaCard.disableClick, true);
      expect(result.listMediaCard.disableClick, false);
    });

    test('updateSetting sends setting', () async {
      mockClient.on('/api/system/setting', () => mockResponse({}, statusCode: 204));

      final api = SystemApi(mockClient);
      await api.updateSetting(SystemSetting(
        syncIntervalSeconds: 30,
        heroMediaCard: MediaCardConfig.defaultHero,
        listMediaCard: MediaCardConfig.defaultList,
      ));
    });
  });
}
