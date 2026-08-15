import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:media_app/core/constants.dart';
import 'package:media_app/data/api/api_client.dart';

void main() {
  group('ApiClient baseUrl', () {
    test('uses default baseUrl when no stored value', () async {
      SharedPreferences.setMockInitialValues({});
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);
      expect(client.baseUrl, AppConstants.defaultBaseUrl);
    });

    test('reads stored baseUrl from preferences', () async {
      SharedPreferences.setMockInitialValues({
        AppConstants.storageKeyBaseUrl: 'http://custom.url:9000',
      });
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);
      expect(client.baseUrl, 'http://custom.url:9000');
    });

    test('updateBaseUrl persists and returns new URL', () async {
      SharedPreferences.setMockInitialValues({});
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);

      client.updateBaseUrl('http://new.url:8888');
      expect(client.baseUrl, 'http://new.url:8888');
      expect(
        prefs.getString(AppConstants.storageKeyBaseUrl),
        'http://new.url:8888',
      );
    });
  });
}
