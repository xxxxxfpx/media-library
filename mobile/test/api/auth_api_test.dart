import 'package:flutter_test/flutter_test.dart';

import 'package:media_app/data/api/auth_api.dart';
import 'package:media_app/data/models/auth.dart';
import 'mock_helper.dart';

void main() {
  late MockApiClient mockClient;

  setUp(() async {
    final prefs = await createMockPrefs();
    mockClient = MockApiClient(prefs);
  });

  group('AuthApi', () {
    test('login returns LoginResponse', () async {
      mockClient.on('/api/user/login', () => mockResponse({
            'access_token': 'access-123',
            'refresh_token': 'refresh-456',
            'token_type': 'bearer',
          }));

      final api = AuthApi(mockClient);
      final result = await api.login('admin', 'admin123');

      expect(result, isA<LoginResponse>());
      expect(result.accessToken, 'access-123');
      expect(result.refreshToken, 'refresh-456');
      expect(result.tokenType, 'bearer');
    });

    test('refresh returns LoginResponse', () async {
      mockClient.on('/api/user/refresh', () => mockResponse({
            'access_token': 'new-access',
            'refresh_token': 'new-refresh',
            'token_type': 'bearer',
          }));

      final api = AuthApi(mockClient);
      final result = await api.refresh('old-refresh-token');

      expect(result.accessToken, 'new-access');
      expect(result.refreshToken, 'new-refresh');
    });

    test('getInfo returns UserInfo', () async {
      mockClient.on('/api/user/info', () => mockResponse({
            'id': 1,
            'username': 'admin',
            'email': 'admin@example.com',
            'is_admin': true,
            'is_active': true,
          }));

      final api = AuthApi(mockClient);
      final result = await api.getInfo();

      expect(result.id, 1);
      expect(result.username, 'admin');
      expect(result.email, 'admin@example.com');
      expect(result.isAdmin, true);
      expect(result.isActive, true);
    });

    test('logout calls logout endpoint', () async {
      mockClient.on('/api/user/logout', () => mockResponse({}, statusCode: 204));

      final api = AuthApi(mockClient);
      // Should not throw
      await api.logout();
    });

    test('login with minimal fields', () async {
      mockClient.on('/api/user/login', () => mockResponse({
            'access_token': 'tok',
            'refresh_token': 'ref',
          }));

      final api = AuthApi(mockClient);
      final result = await api.login('user', 'pass');

      expect(result.accessToken, 'tok');
      expect(result.refreshToken, 'ref');
      // token_type defaults to 'bearer'
      expect(result.tokenType, 'bearer');
    });
  });
}
