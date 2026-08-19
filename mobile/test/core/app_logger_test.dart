import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:media_app/core/app_logger.dart';

void main() {
  setUp(() async {
    SharedPreferences.setMockInitialValues({});
    final prefs = await SharedPreferences.getInstance();
    await AppLogger.initialize(prefs);
    await AppLogger.clear();
  });

  test('persists structured non-debug logs in the local ring', () async {
    final prefs = await SharedPreferences.getInstance();

    AppLogger.info(
      'login_succeeded',
      category: 'auth',
      fields: {'username': 'admin', 'access_token': 'secret-token'},
    );
    await Future<void>.delayed(const Duration(milliseconds: 350));

    final logs = prefs.getStringList('app_log_ring')!;
    expect(logs.single, contains('login_succeeded'));
    expect(logs.single, contains('[REDACTED]'));
    expect(logs.single, isNot(contains('secret-token')));
  });

  test('does not persist debug logs', () async {
    final prefs = await SharedPreferences.getInstance();

    AppLogger.debug('cache_hit', category: 'cache');
    await Future<void>.delayed(const Duration(milliseconds: 350));

    expect(prefs.getStringList('app_log_ring'), isNull);
  });
}
