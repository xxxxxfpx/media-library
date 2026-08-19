import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../core/app_logger.dart';
import '../../data/api/api_client.dart';
import '../../data/api/guangyapan_api.dart';

class GuangYaPanSettingsPage extends StatefulWidget {
  const GuangYaPanSettingsPage({super.key});

  @override
  State<GuangYaPanSettingsPage> createState() => _GuangYaPanSettingsPageState();
}

class _GuangYaPanSettingsPageState extends State<GuangYaPanSettingsPage> {
  final _accessTokenController = TextEditingController();
  final _refreshTokenController = TextEditingController();
  final _clientIdController = TextEditingController();
  final _deviceIdController = TextEditingController();
  final _parentIdController = TextEditingController();

  bool _loading = true;
  bool _saving = false;
  bool _configured = false;

  @override
  void initState() {
    super.initState();
    _loadConfig();
  }

  @override
  void dispose() {
    _accessTokenController.dispose();
    _refreshTokenController.dispose();
    _clientIdController.dispose();
    _deviceIdController.dispose();
    _parentIdController.dispose();
    super.dispose();
  }

  Future<GuangYaPanApi> _api() async {
    final prefs = await SharedPreferences.getInstance();
    return GuangYaPanApi(ApiClient(prefs));
  }

  Future<void> _loadConfig() async {
    try {
      final config = await (await _api()).getConfig();
      _configured = config['configured'] == true;
      _clientIdController.text = config['client_id'] as String? ?? '';
      _deviceIdController.text = config['device_id'] as String? ?? '';
      _parentIdController.text = config['default_parent_id'] as String? ?? '';
    } catch (error, stackTrace) {
      AppLogger.error(
        'guangyapan_config_load_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'settings',
      );
      if (mounted) {
        _showMessage('光芽云盘设置加载失败');
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _saveConfig() async {
    setState(() => _saving = true);
    try {
      final payload = <String, dynamic>{
        'client_id': _clientIdController.text.trim().isEmpty
            ? null
            : _clientIdController.text.trim(),
        'device_id': _deviceIdController.text.trim().isEmpty
            ? null
            : _deviceIdController.text.trim(),
        'default_parent_id': _parentIdController.text.trim(),
      };
      if (_accessTokenController.text.trim().isNotEmpty) {
        payload['access_token'] = _accessTokenController.text.trim();
      }
      if (_refreshTokenController.text.trim().isNotEmpty) {
        payload['refresh_token'] = _refreshTokenController.text.trim();
      }

      final config = await (await _api()).updateConfig(payload);
      _configured = config['configured'] == true;
      _accessTokenController.clear();
      _refreshTokenController.clear();
      if (mounted) _showMessage('光芽云盘设置已保存');
    } catch (error, stackTrace) {
      AppLogger.error(
        'guangyapan_config_save_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'settings',
      );
      if (mounted) _showMessage('光芽云盘设置保存失败');
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  void _showMessage(String message) {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(SnackBar(content: Text(message)));
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final cs = theme.colorScheme;
    return Scaffold(
      appBar: AppBar(title: const Text('光芽云盘设置')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.cloud_outlined, color: cs.primary),
                            const SizedBox(width: 10),
                            Text(
                              _configured ? '已配置' : '未配置',
                              style: theme.textTheme.titleMedium,
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Token 留空表示保持原值。上传和离线下载共用下面的目录 ID，文件名由源 URL 的 SHA-256 自动生成。',
                          style: theme.textTheme.bodySmall?.copyWith(
                            color: cs.onSurfaceVariant,
                          ),
                        ),
                        const SizedBox(height: 20),
                        _passwordField(
                          controller: _accessTokenController,
                          label: 'Access Token',
                          hint: '留空表示保持当前 Token',
                        ),
                        const SizedBox(height: 16),
                        _passwordField(
                          controller: _refreshTokenController,
                          label: 'Refresh Token',
                          hint: '留空表示保持当前 Refresh Token',
                        ),
                        const SizedBox(height: 16),
                        TextField(
                          controller: _clientIdController,
                          decoration: const InputDecoration(
                            labelText: 'Client ID',
                            border: OutlineInputBorder(),
                          ),
                        ),
                        const SizedBox(height: 16),
                        TextField(
                          controller: _deviceIdController,
                          decoration: const InputDecoration(
                            labelText: 'Device ID',
                            border: OutlineInputBorder(),
                          ),
                        ),
                        const SizedBox(height: 16),
                        TextField(
                          controller: _parentIdController,
                          decoration: const InputDecoration(
                            labelText: '默认网盘目录 ID',
                            helperText: '上传和离线下载共用此目录',
                            border: OutlineInputBorder(),
                          ),
                        ),
                        const SizedBox(height: 20),
                        SizedBox(
                          width: double.infinity,
                          child: FilledButton.icon(
                            onPressed: _saving ? null : _saveConfig,
                            icon: _saving
                                ? const SizedBox(
                                    width: 18,
                                    height: 18,
                                    child: CircularProgressIndicator(strokeWidth: 2),
                                  )
                                : const Icon(Icons.save_outlined),
                            label: Text(_saving ? '保存中...' : '保存设置'),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
    );
  }

  Widget _passwordField({
    required TextEditingController controller,
    required String label,
    required String hint,
  }) {
    return TextField(
      controller: controller,
      obscureText: true,
      decoration: InputDecoration(
        labelText: label,
        hintText: hint,
        border: const OutlineInputBorder(),
      ),
    );
  }
}
