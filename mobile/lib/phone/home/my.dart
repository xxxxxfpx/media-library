import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../core/constants.dart';
import '../../data/api/api_client.dart';
import '../../data/api/auth_api.dart';
import '../../data/api/user_api.dart';
import '../media_play_settings.dart';
import 'guangyapan_settings.dart';
import '../login/view.dart';
import '../../providers/settings_provider.dart';
import '../../services/sync_service.dart';
import '../../core/app_logger.dart';

class HomeTabMy extends ConsumerStatefulWidget {
  const HomeTabMy({super.key});

  @override
  ConsumerState<HomeTabMy> createState() => _HomeTabMyState();
}

class _HomeTabMyState extends ConsumerState<HomeTabMy> {
  String _username = '';
  bool _isSyncing = false;
  String? _lastSyncTime;
  String _currentBaseUrl = AppConstants.defaultBaseUrl;

  @override
  void initState() {
    super.initState();
    _loadUserInfo();
    _loadLastSyncTime();
    _loadBaseUrl();
  }

  Future<void> _loadBaseUrl() async {
    final prefs = await SharedPreferences.getInstance();
    final url = prefs.getString(AppConstants.storageKeyBaseUrl) ??
        AppConstants.defaultBaseUrl;
    if (mounted) setState(() => _currentBaseUrl = url);
  }

  Future<void> _showEditBaseUrlDialog() async {
    final controller = TextEditingController(text: _currentBaseUrl);
    final result = await showDialog<String>(
      context: context,
      builder: (ctx) {
        final cs = Theme.of(ctx).colorScheme;
        return AlertDialog(
          title: const Text('后端 API 端点'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '仅 debug 模式可修改，用于测试不同后端。\n生产默认：${AppConstants.defaultBaseUrl}',
                style: TextStyle(fontSize: 12, color: cs.onSurfaceVariant),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: controller,
                autofocus: true,
                decoration: const InputDecoration(
                  labelText: 'Base URL',
                  hintText: 'https://media.mz727.top',
                  border: OutlineInputBorder(),
                  isDense: true,
                ),
                keyboardType: TextInputType.url,
                autocorrect: false,
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(ctx),
              child: const Text('取消'),
            ),
            TextButton(
              onPressed: () async {
                final prefs = await SharedPreferences.getInstance();
                await prefs.remove(AppConstants.storageKeyBaseUrl);
                if (ctx.mounted) Navigator.pop(ctx, AppConstants.defaultBaseUrl);
              },
              child: const Text('重置默认'),
            ),
            FilledButton(
              onPressed: () {
                var url = controller.text.trim();
                if (url.isEmpty) return;
                if (!url.startsWith('http://') && !url.startsWith('https://')) {
                  url = 'https://$url';
                }
                url = url.replaceAll(RegExp(r'/+$'), '');
                if (url.isEmpty) return;
                Navigator.pop(ctx, url);
              },
              child: const Text('保存'),
            ),
          ],
        );
      },
    );
    if (result != null && mounted) {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(AppConstants.storageKeyBaseUrl, result);
      setState(() => _currentBaseUrl = result);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('已切换至 $result，下次请求生效'),
            duration: const Duration(seconds: 2),
          ),
        );
      }
      AppLogger.info(
        'debug_base_url_changed',
        category: 'settings',
        fields: {'base_url': result},
      );
    }
  }

  Future<void> _loadLastSyncTime() async {
    final prefs = await SharedPreferences.getInstance();
    final timestamp = prefs.getInt('last_settings_sync_time');
    if (timestamp != null) {
      final dateTime = DateTime.fromMillisecondsSinceEpoch(timestamp);
      if (!mounted) return;
      setState(() {
        _lastSyncTime =
            '${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}';
      });
    }
  }

  Future<void> _handleSyncSettings() async {
    AppLogger.info('settings_sync_submitted', category: 'ui');
    setState(() => _isSyncing = true);
    try {
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);
      final userApi = UserApi(client);
      final settings = await userApi.getSetting();
      await prefs.setString(
        'user_settings_json',
        jsonEncode(settings.toJson()),
      );
      if (mounted) {
        ref.read(settingsProvider.notifier).updateLocal(settings);
      }
      await prefs.setInt(
        'last_settings_sync_time',
        DateTime.now().millisecondsSinceEpoch,
      );
      await _loadLastSyncTime();

      if (mounted) {
        AppLogger.info('settings_sync_succeeded', category: 'settings');
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('设置已同步'),
            duration: Duration(seconds: 2),
          ),
        );
      }
    } catch (error, stackTrace) {
      AppLogger.error(
        'settings_sync_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'settings',
      );
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('同步失败，请稍后重试'),
            duration: Duration(seconds: 2),
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isSyncing = false);
      }
    }
  }

  Future<void> _loadUserInfo() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);
      final authApi = AuthApi(client);
      final info = await authApi.getInfo();
      if (mounted) {
        setState(() => _username = info.username);
      }
    } catch (error, stackTrace) {
      AppLogger.warning(
        'user_info_load_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'account',
      );
      // 加载用户信息失败，保持默认
    }
  }

  Future<void> _handleLogout() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);
      final authApi = AuthApi(client);
      await authApi.logout();
    } catch (error, stackTrace) {
      AppLogger.warning(
        'logout_request_failed_continue_local_logout',
        error: error,
        stackTrace: stackTrace,
        category: 'auth',
      );
      // 即使服务端 logout 失败也清除本地 token
    }

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(AppConstants.storageKeyAccessToken);
    await prefs.remove(AppConstants.storageKeyRefreshToken);
    SyncService().stop();
    AppLogger.info('logout_succeeded', category: 'auth');

    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const LoginScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildUserSection(context),
          const SizedBox(height: 24),
          _buildSettingSection(context),
        ],
      ),
    );
  }

  Widget _buildUserSection(BuildContext context) {
    final theme = Theme.of(context);
    final cs = theme.colorScheme;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '账户',
          style: theme.textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 12),
        Container(
          decoration: BoxDecoration(
            color: theme.cardColor,
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: theme.shadowColor.withValues(alpha: 0.05),
                blurRadius: 8,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Column(
            children: [
              Material(
                color: Colors.transparent,
                child: ListTile(
                  leading: Icon(Icons.person_outline, color: cs.primary),
                  title: Text(
                    _username.isNotEmpty ? _username : '未登录',
                    style: TextStyle(fontSize: 16, color: cs.onSurface),
                  ),
                  subtitle: Text(
                    '点击退出登录',
                    style: TextStyle(fontSize: 12, color: cs.onSurfaceVariant),
                  ),
                  trailing: const Icon(Icons.logout, size: 20),
                  onTap: () async {
                    final confirm = await showDialog<bool>(
                      context: context,
                      builder: (ctx) => AlertDialog(
                        title: const Text('退出登录'),
                        content: const Text('确定要退出登录吗？'),
                        actions: [
                          TextButton(
                            onPressed: () => Navigator.pop(ctx, false),
                            child: const Text('取消'),
                          ),
                          TextButton(
                            onPressed: () => Navigator.pop(ctx, true),
                            child: const Text('确定'),
                          ),
                        ],
                      ),
                    );
                    if (confirm == true) {
                      _handleLogout();
                    }
                  },
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildSettingSection(BuildContext context) {
    final theme = Theme.of(context);
    final cs = theme.colorScheme;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              '设置',
              style: theme.textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            if (_lastSyncTime != null)
              Text(
                '上次同步：$_lastSyncTime',
                style: theme.textTheme.bodySmall?.copyWith(
                  color: cs.onSurfaceVariant,
                ),
              ),
          ],
        ),
        const SizedBox(height: 12),
        Container(
          decoration: BoxDecoration(
            color: theme.cardColor,
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: theme.shadowColor.withValues(alpha: 0.05),
                blurRadius: 8,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Column(
            children: [
              Material(
                color: Colors.transparent,
                child: ListTile(
                  leading: Icon(Icons.play_circle_outline, color: cs.primary),
                  title: Text(
                    '媒体播放设置',
                    style: TextStyle(fontSize: 16, color: cs.onSurface),
                  ),
                  subtitle: Text(
                    '自动播放、默认静音',
                    style: TextStyle(fontSize: 12, color: cs.onSurfaceVariant),
                  ),
                  trailing: const Icon(Icons.chevron_right, size: 20),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const MediaPlaySettingsPage(),
                      ),
                    );
                  },
                ),
              ),
              const Divider(height: 1, indent: 56),
              Material(
                color: Colors.transparent,
                child: ListTile(
                  leading: Icon(Icons.cloud_outlined, color: cs.primary),
                  title: Text(
                    '光芽云盘设置',
                    style: TextStyle(fontSize: 16, color: cs.onSurface),
                  ),
                  subtitle: Text(
                    '配置 Token 和默认上传目录',
                    style: TextStyle(fontSize: 12, color: cs.onSurfaceVariant),
                  ),
                  trailing: const Icon(Icons.chevron_right, size: 20),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const GuangYaPanSettingsPage(),
                      ),
                    );
                  },
                ),
              ),
              const Divider(height: 1, indent: 56),
              Material(
                color: Colors.transparent,
                child: ListTile(
                  leading: Icon(Icons.sync, color: cs.primary),
                  title: Text(
                    '同步云端设置',
                    style: TextStyle(fontSize: 16, color: cs.onSurface),
                  ),
                  subtitle: Text(
                    '从服务器获取最新设置',
                    style: TextStyle(fontSize: 12, color: cs.onSurfaceVariant),
                  ),
                  trailing: _isSyncing
                      ? SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: cs.primary,
                          ),
                        )
                      : const Icon(Icons.refresh, size: 20),
                  onTap: _isSyncing ? null : _handleSyncSettings,
                ),
              ),
              if (kDebugMode) ...[
                const Divider(height: 1, indent: 56),
                Material(
                  color: Colors.transparent,
                  child: ListTile(
                    leading: Icon(Icons.bug_report_outlined, color: cs.primary),
                    title: Text(
                      '后端 API 端点 (Debug)',
                      style: TextStyle(fontSize: 16, color: cs.onSurface),
                    ),
                    subtitle: Text(
                      _currentBaseUrl,
                      style: TextStyle(fontSize: 11, color: cs.onSurfaceVariant),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    trailing: const Icon(Icons.edit_outlined, size: 18),
                    onTap: _showEditBaseUrlDialog,
                  ),
                ),
              ],
            ],
          ),
        ),
      ],
    );
  }
}
