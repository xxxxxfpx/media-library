import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:media_app/core/constants.dart';
import 'package:media_app/data/api/file_api.dart';
import 'mock_helper.dart';

void main() {
  group('FileApi', () {
    Future<FileApi> buildApi() async {
      SharedPreferences.setMockInitialValues({
        AppConstants.storageKeyBaseUrl: 'http://localhost:8000',
      });
      final prefs = await SharedPreferences.getInstance();
      return FileApi(MockApiClient(prefs));
    }

    test('getFileDataUrl returns correct URL', () async {
      final api = await buildApi();

      final url = api.getFileDataUrl(42);
      expect(url, 'http://localhost:8000/api/file/data?file_id=42');
    });

    test('getFileDataUrl handles file id 1', () async {
      final api = await buildApi();

      final url = api.getFileDataUrl(1);
      expect(url, 'http://localhost:8000/api/file/data?file_id=1');
    });
  });
}
