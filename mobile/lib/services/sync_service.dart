import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../data/api/api_client.dart';
import '../data/api/user_api.dart';
import '../providers/settings_provider.dart';
import '../core/app_logger.dart';

class SyncService {
  static final SyncService _instance = SyncService._();
  factory SyncService() => _instance;
  SyncService._();

  Timer? _timer;
  bool _isRunning = false;

  void start(WidgetRef ref) {
    stop();

    final interval = ref.read(settingsProvider.notifier).getAutoSyncInterval();

    _timer = Timer.periodic(Duration(seconds: interval), (_) async {
      try {
        final prefs = await SharedPreferences.getInstance();
        final client = ApiClient(prefs);
        final userApi = UserApi(client);
        final settings = await userApi.getSetting();
        ref.read(settingsProvider.notifier).updateLocal(settings);
      } catch (error, stackTrace) {
        AppLogger.error(
          'settings_sync_failed',
          error: error,
          stackTrace: stackTrace,
          category: 'sync',
        );
      }
    });

    _isRunning = true;
    AppLogger.info(
      'background_sync_started',
      category: 'sync',
      fields: {'interval_seconds': interval},
    );
  }

  void stop() {
    if (_isRunning) {
      AppLogger.info('background_sync_stopped', category: 'sync');
    }
    _timer?.cancel();
    _timer = null;
    _isRunning = false;
  }

  bool get isRunning => _isRunning;
}
