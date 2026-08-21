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
  bool _testing = false;
  bool _configured = false;
  Map<String, dynamic>? _testResult;
  String _testError = '';

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
        _showMessage('光鸭云盘设置加载失败');
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _testConfig() async {
    setState(() {
      _testing = true;
      _testResult = null;
      _testError = '';
    });
    try {
      final payload = _buildPayload();
      final result = await (await _api()).testConfig(payload);
      if (mounted) {
        setState(() {
          _testResult = result;
        });
      }
    } catch (error, stackTrace) {
      AppLogger.error(
        'guangyapan_config_test_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'settings',
      );
      if (mounted) {
        setState(() {
          _testError = error.toString().contains('detail')
              ? error.toString().replaceAll('Exception: ', '')
              : '测试失败，请检查 Token 和目录 ID';
        });
      }
    } finally {
      if (mounted) setState(() => _testing = false);
    }
  }

  Map<String, dynamic> _buildPayload() {
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
    return payload;
  }

  Future<void> _saveConfig() async {
    if (_testing) return;
    setState(() => _saving = true);
    try {
      // 保存前先测试：确保凭据和目录可用
      final payload = _buildPayload();
      try {
        final testResult = await (await _api()).testConfig(payload);
        if (testResult['ok'] != true) {
          if (!mounted) return;
          setState(() {
            _testError = '测试未通过，请检查配置';
          });
          _showMessage('保存前测试未通过，无法保存');
          return;
        }
        if (mounted) {
          setState(() {
            _testResult = testResult;
          });
        }
      } catch (testError) {
        if (!mounted) return;
        setState(() {
          _testError = testError.toString().contains('detail')
              ? testError.toString().replaceAll('Exception: ', '')
              : '连接测试失败，请检查 Token 和目录 ID';
        });
        _showMessage('保存前连接测试失败，请检查 Token 和目录 ID');
        return;
      }

      final config = await (await _api()).updateConfig(payload);
      if (!mounted) return;
      setState(() {
        _configured = config['configured'] == true;
        _testError = '';
      });
      _accessTokenController.clear();
      _refreshTokenController.clear();
      _showMessage('光鸭云盘设置已保存');
    } catch (error, stackTrace) {
      AppLogger.error(
        'guangyapan_config_save_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'settings',
      );
      if (mounted) _showMessage('光鸭云盘设置保存失败');
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
      appBar: AppBar(title: const Text('光鸭云盘设置')),
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
                        const SizedBox(height: 16),
                        // 测试连接按钮与结果
                        Row(
                          children: [
                            OutlinedButton.icon(
                              onPressed: (_saving || _testing) ? null : _testConfig,
                              icon: const Icon(Icons.cloud_done_outlined, size: 18),
                              label: Text(_testing ? '测试中...' : '测试连接'),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: _testResult != null
                                  ? Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                                      decoration: BoxDecoration(
                                        color: Colors.green.shade50,
                                        borderRadius: BorderRadius.circular(6),
                                        border: Border.all(color: Colors.green.shade200),
                                      ),
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          Row(
                                            children: [
                                              Icon(Icons.check_circle, color: Colors.green.shade600, size: 16),
                                              const SizedBox(width: 4),
                                              Expanded(
                                                child: Text(
                                                  '目录可访问 · 共 ${_testResult!['total']} 项',
                                                  style: TextStyle(color: Colors.green.shade700, fontSize: 13),
                                                ),
                                              ),
                                            ],
                                          ),
                                          if (_testResult!['sample'] != null && (_testResult!['sample'] as List).isNotEmpty)
                                            Padding(
                                              padding: const EdgeInsets.only(top: 4),
                                              child: Text(
                                                '示例：${(_testResult!['sample'] as List).map((e) => e['name']).join('、')}',
                                                style: TextStyle(color: Colors.green.shade600, fontSize: 12),
                                                maxLines: 2,
                                                overflow: TextOverflow.ellipsis,
                                              ),
                                            ),
                                        ],
                                      ),
                                    )
                                  : _testError.isNotEmpty
                                      ? Container(
                                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                                          decoration: BoxDecoration(
                                            color: Colors.red.shade50,
                                            borderRadius: BorderRadius.circular(6),
                                            border: Border.all(color: Colors.red.shade200),
                                          ),
                                          child: Row(
                                            children: [
                                              Icon(Icons.error_outline, color: Colors.red.shade600, size: 16),
                                              const SizedBox(width: 4),
                                              Expanded(
                                                child: Text(
                                                  _testError,
                                                  style: TextStyle(color: Colors.red.shade700, fontSize: 13),
                                                ),
                                              ),
                                            ],
                                          ),
                                        )
                                      : Text(
                                          '点击「测试连接」验证目录 ID 是否有效',
                                          style: TextStyle(color: cs.onSurfaceVariant, fontSize: 13),
                                        ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 20),
                        SizedBox(
                          width: double.infinity,
                          child: FilledButton.icon(
                            onPressed: (_saving || _testing) ? null : _saveConfig,
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
