import 'package:flutter_test/flutter_test.dart';

import 'package:media_app/data/api/user_api.dart';
import 'package:media_app/data/models/auth.dart';
import 'package:media_app/data/models/media.dart';
import 'mock_helper.dart';

void main() {
  late MockApiClient mockClient;

  setUp(() async {
    final prefs = await createMockPrefs();
    mockClient = MockApiClient(prefs);
  });

  group('UserApi', () {
    test('updateUserData sends request', () async {
      mockClient.on('/api/user/userdata', () => mockResponse({}, statusCode: 204));

      final api = UserApi(mockClient);
      final request = UpdateUserDataRequest(
        itemId: 1,
        isFavorite: true,
        playCount: 5,
      );

      // Should not throw
      await api.updateUserData(request);
    });

    test('getHistory returns MediaListResponse', () async {
      mockClient.on('/api/user/history', () => mockResponse({
            'items': [
              {
                'id': 10,
                'name': 'Watched Movie',
                'type': 'movie',
              },
            ],
            'total': 1,
            'limit': 60,
            'offset': 0,
          }));

      final api = UserApi(mockClient);
      final result = await api.getHistory();

      expect(result.total, 1);
      expect(result.items.length, 1);
      expect(result.items[0].name, 'Watched Movie');
    });

    test('getHistory with pagination', () async {
      mockClient.on('/api/user/history', () => mockResponse({
            'items': [],
            'total': 0,
            'limit': 20,
            'offset': 0,
          }));

      final api = UserApi(mockClient);
      final result = await api.getHistory(limit: 20, offset: 0);

      expect(result.total, 0);
      expect(result.limit, 20);
    });

    test('getSetting returns UserSetting', () async {
      mockClient.on('/api/user/setting', () => mockResponse({
            'theme_mode': 'dark',
          }));

      final api = UserApi(mockClient);
      final result = await api.getSetting();

      expect(result.themeMode, 'dark');
    });

    test('getSetting returns default when field missing', () async {
      mockClient.on('/api/user/setting', () => mockResponse({}));

      final api = UserApi(mockClient);
      final result = await api.getSetting();

      expect(result.themeMode, null);
    });

    test('updateSetting sends setting', () async {
      mockClient.on('/api/user/setting', () => mockResponse({}, statusCode: 204));

      final api = UserApi(mockClient);
      await api.updateSetting(UserSetting(themeMode: 'dark'));
    });
  });
}
