import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../data/api/api_client.dart';
import '../data/api/user_api.dart';
import '../data/models/auth.dart';

/// 设置提供者 - 管理全局用户设置
class SettingsNotifier extends StateNotifier<UserSetting?> {
  SettingsNotifier() : super(null) {
    _loadFromPrefs();
  }

  /// 从本地缓存加载设置
  Future<void> _loadFromPrefs() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final data = prefs.getString('user_settings_json');
      if (data != null) {
        final json = jsonDecode(data) as Map<String, dynamic>;
        state = UserSetting.fromJson(json);
      }
    } catch (e) {
      // 加载失败，使用默认值
    }
  }

  /// 保存到本地缓存
  Future<void> _saveToPrefs() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      if (state != null) {
        final json = jsonEncode(state!.toJson());
        await prefs.setString('user_settings_json', json);
      }
    } catch (e) {
      // 保存失败
    }
  }

  /// 基础设置方法 - 更新单个属性后自动提交云端
  Future<void> _setProperty(UserSetting updated) async {
    state = updated;
    await _saveToPrefs();
    try {
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);
      final userApi = UserApi(client);
      await userApi.updateSetting(updated);
    } catch (_) {
      // 云端同步失败，本地已保存
    }
  }

  // ──────────────────────────────
  // 主题设置 getter/setter
  // ──────────────────────────────

  String get themeMode => state?.themeMode ?? 'system';
  set themeMode(String value) => _setProperty((state ?? UserSetting()).copyWith(themeMode: value));

  String? get primaryColor => state?.primaryColor;
  set primaryColor(String? value) => _setProperty((state ?? UserSetting()).copyWith(primaryColor: value));

  // ──────────────────────────────
  // 播放设置 getter/setter
  // ──────────────────────────────

  double get defaultPlaybackRate => state?.defaultPlaybackRate ?? 1.0;
  set defaultPlaybackRate(double value) => _setProperty((state ?? UserSetting()).copyWith(defaultPlaybackRate: value));

  bool get resumePlayback => state?.resumePlayback ?? true;
  set resumePlayback(bool value) => _setProperty((state ?? UserSetting()).copyWith(resumePlayback: value));

  // ──────────────────────────────
  // 高级设置 getter/setter
  // ──────────────────────────────

  bool get enableHardwareAcceleration => state?.enableHardwareAcceleration ?? true;
  set enableHardwareAcceleration(bool value) => _setProperty((state ?? UserSetting()).copyWith(enableHardwareAcceleration: value));

  String get cacheMode => state?.cacheMode ?? 'memory';
  set cacheMode(String value) => _setProperty((state ?? UserSetting()).copyWith(cacheMode: value));

  int get forwardCacheSizeMb => state?.forwardCacheSizeMb ?? 32;
  set forwardCacheSizeMb(int value) => _setProperty((state ?? UserSetting()).copyWith(forwardCacheSizeMb: value));

  int get backwardCacheSizeMb => state?.backwardCacheSizeMb ?? 32;
  set backwardCacheSizeMb(int value) => _setProperty((state ?? UserSetting()).copyWith(backwardCacheSizeMb: value));

  int get mediaRetryInterval => state?.mediaRetryInterval ?? 5;
  set mediaRetryInterval(int value) => _setProperty((state ?? UserSetting()).copyWith(mediaRetryInterval: value));

  // ──────────────────────────────
  // 通用设置 getter/setter
  // ──────────────────────────────

  int get autoSyncInterval => state?.autoSyncInterval ?? 60;
  set autoSyncInterval(int value) => _setProperty((state ?? UserSetting()).copyWith(autoSyncInterval: value));

  /// 获取自动同步间隔（秒），用于 SyncService 定时器
  int getAutoSyncInterval() => autoSyncInterval;

  /// 从云端加载设置
  Future<void> loadFromCloud() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);
      final userApi = UserApi(client);
      final settings = await userApi.getSetting();
      state = settings;
      await _saveToPrefs();
    } catch (e) {
      rethrow;
    }
  }

  /// 仅更新本地状态（来自云端同步，不推送到云端）
  void updateLocal(UserSetting settings) {
    state = settings;
    _saveToPrefs();
  }

  /// 更新设置（完整替换 + 推送到云端）
  Future<void> updateSettings(UserSetting settings) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);
      final userApi = UserApi(client);
      await userApi.updateSetting(settings);
      state = settings;
      await _saveToPrefs();
    } catch (e) {
      rethrow;
    }
  }

  /// 清除设置
  void clear() {
    state = null;
  }
}

/// Riverpod 提供者
final settingsProvider = StateNotifierProvider<SettingsNotifier, UserSetting?>((ref) {
  return SettingsNotifier();
});

/// 辅助扩展：方便获取设置值（带默认值）
extension SettingsExtension on WidgetRef {
  String getCacheMode() {
    return watch(settingsProvider)?.cacheMode ?? 'memory';
  }

  int getForwardCacheSize() {
    return watch(settingsProvider)?.forwardCacheSizeMb ?? 32;
  }

  int getBackwardCacheSize() {
    return watch(settingsProvider)?.backwardCacheSizeMb ?? 32;
  }

  int getAutoSyncInterval() {
    return watch(settingsProvider)?.autoSyncInterval ?? 60;
  }

  int getMediaRetryInterval() {
    return watch(settingsProvider)?.mediaRetryInterval ?? 5;
  }

  bool getHardwareAcceleration() {
    return watch(settingsProvider)?.enableHardwareAcceleration ?? true;
  }

  double getDefaultPlaybackRate() {
    return watch(settingsProvider)?.defaultPlaybackRate ?? 1.0;
  }

  bool getResumePlayback() {
    return watch(settingsProvider)?.resumePlayback ?? true;
  }

  String getThemeMode() {
    return watch(settingsProvider)?.themeMode ?? 'system';
  }

  String? getPrimaryColor() {
    return watch(settingsProvider)?.primaryColor;
  }
}
