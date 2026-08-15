import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../core/constants.dart';
import '../data/api/api_client.dart';
import '../data/api/user_api.dart';

import '../providers/settings_provider.dart';
import '../services/sync_service.dart';

class MediaPlaySettingsPage extends ConsumerStatefulWidget {
  const MediaPlaySettingsPage({super.key});

  @override
  ConsumerState<MediaPlaySettingsPage> createState() => _MediaPlaySettingsPageState();
}

class _MediaPlaySettingsPageState extends ConsumerState<MediaPlaySettingsPage> {
  // 本地设置（仅存本地 SharedPreferences）
  bool _autoPlay = true;
  bool _muted = false;
  double _watchedThreshold = 0.9;

  // 云端设置（读取后从 Provider 获取默认值，修改后自动同步云端）
  bool _isLoading = true;
  String? _themeMode;
  String? _primaryColor;
  int? _autoSyncInterval;
  int? _mediaRetryInterval;
  String? _cacheMode;
  int? _forwardCacheSizeMb;
  int? _backwardCacheSizeMb;
  bool? _enableHardwareAcceleration;
  double? _defaultPlaybackRate;
  bool? _resumePlayback;

  @override
  void initState() {
    super.initState();
    SyncService().stop();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    setState(() => _isLoading = true);
    try {
      // 加载本地设置
      final prefs = await SharedPreferences.getInstance();
      if (!mounted) return;
      setState(() {
        _autoPlay = prefs.getBool(AppConstants.storageKeyAutoPlay) ?? true;
        _muted = prefs.getBool(AppConstants.storageKeyMuted) ?? false;
        _watchedThreshold = prefs.getDouble(AppConstants.storageKeyWatchedThreshold) ?? 0.9;
      });
      
      // 加载云端设置
      final client = ApiClient(prefs);
      final userApi = UserApi(client);
      final settings = await userApi.getSetting();
      if (!mounted) return;
      setState(() {
        _themeMode = settings.themeMode;
        _primaryColor = settings.primaryColor;
        _autoSyncInterval = settings.autoSyncInterval ?? 60;
        _mediaRetryInterval = settings.mediaRetryInterval ?? 5;
        _cacheMode = settings.cacheMode ?? 'memory';
        _forwardCacheSizeMb = settings.forwardCacheSizeMb ?? 32;
        _backwardCacheSizeMb = settings.backwardCacheSizeMb ?? 32;
        _enableHardwareAcceleration = settings.enableHardwareAcceleration ?? true;
        _defaultPlaybackRate = settings.defaultPlaybackRate ?? 1.0;
        _resumePlayback = settings.resumePlayback ?? true;
        _isLoading = false;
      });
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('加载设置失败：$e')),
        );
      }
    }
  }

  Future<void> _saveLocalSettings() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(AppConstants.storageKeyAutoPlay, _autoPlay);
    await prefs.setBool(AppConstants.storageKeyMuted, _muted);
    await prefs.setDouble(AppConstants.storageKeyWatchedThreshold, _watchedThreshold);
  }

  @override
  void dispose() {
    SyncService().start(ref);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Scaffold(
      backgroundColor: cs.surface,
      appBar: AppBar(
        title: const Text('播放设置'),
        backgroundColor: cs.surface,
        elevation: 0,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                _buildLocalSettingsCard(),
                const SizedBox(height: 16),
                _buildSyncSettingsCard(),
                const SizedBox(height: 16),
                _buildThemeSettingsCard(),
                const SizedBox(height: 16),
                _buildCacheSettingsCard(),
                const SizedBox(height: 16),
                _buildPlaybackSettingsCard(),
              ],
            ),
    );
  }

  Widget _buildLocalSettingsCard() {
    return _buildCard(
      title: '本地设置',
      icon: Icons.storage,
      children: [
        _buildSwitchTile(
          icon: Icons.play_circle_outline,
          title: '自动播放',
          subtitle: '进入媒体详情后自动播放',
          value: _autoPlay,
          onChanged: (v) async {
            setState(() => _autoPlay = v);
            await _saveLocalSettings();
          },
        ),
        const Divider(height: 1, indent: 56),
        _buildSwitchTile(
          icon: Icons.volume_off_outlined,
          title: '默认静音',
          subtitle: '播放时默认静音',
          value: _muted,
          onChanged: (v) async {
            setState(() => _muted = v);
            await _saveLocalSettings();
          },
        ),
        const Divider(height: 1, indent: 56),
        _buildSliderTile(
          icon: Icons.check_circle_outline,
          title: '标记已观看进度',
          subtitle: '播放到此进度时自动标记为已观看',
          value: _watchedThreshold,
          min: 0.5,
          max: 1.0,
          divisions: 10,
          displayFormat: (v) => '${(v * 100).round()}%',
          onChanged: (v) async {
            setState(() => _watchedThreshold = v);
            await _saveLocalSettings();
          },
        ),
      ],
    );
  }

  Widget _buildSyncSettingsCard() {
    final cs = Theme.of(context).colorScheme;
    return _buildCard(
      title: '同步设置',
      icon: Icons.sync,
      children: [
        _buildSliderTile(
          icon: Icons.update,
          title: '自动同步间隔',
          subtitle: '定时从云端同步设置的时间间隔（秒）',
          value: _autoSyncInterval?.toDouble() ?? 60,
          min: 1,
          max: 600,
          divisions: 60,
          displayFormat: (v) => '${v.round()}秒',
          onChanged: (v) {
            setState(() => _autoSyncInterval = v.round());
          },
          onChangeEnd: (v) {
            ref.read(settingsProvider.notifier).autoSyncInterval = v.round();
          },
        ),
        const Divider(height: 1, indent: 56),
        ListTile(
          leading: Icon(Icons.info_outline, color: cs.onSurfaceVariant),
          title: Text(
            '在设置页面时停止自动同步',
            style: TextStyle(fontSize: 12, color: cs.onSurfaceVariant),
          ),
        ),
      ],
    );
  }

  static const List<Color> _presetColors = [
    Colors.red,
    Colors.pink,
    Colors.purple,
    Colors.deepPurple,
    Colors.indigo,
    Colors.blue,
    Colors.lightBlue,
    Colors.cyan,
    Colors.teal,
    Colors.green,
    Colors.lightGreen,
    Colors.lime,
    Colors.yellow,
    Colors.amber,
    Colors.orange,
    Colors.deepOrange,
    Colors.brown,
    Colors.blueGrey,
  ];

  static String _colorToHex(Color color) {
    return '#${color.toARGB32().toRadixString(16).substring(2).toUpperCase()}';
  }

  Widget _buildThemeSettingsCard() {
    final cs = Theme.of(context).colorScheme;
    return _buildCard(
      title: '主题设置',
      icon: Icons.palette,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          child: Row(
            children: [
              Padding(
                padding: const EdgeInsets.only(right: 16),
                child: Icon(Icons.brightness_medium, color: cs.primary),
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '主题模式',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500, color: cs.onSurface),
                    ),
                    const SizedBox(height: 8),
                    SegmentedButton<String>(
                      segments: const [
                        ButtonSegment(value: 'system', label: Text('跟随系统')),
                        ButtonSegment(value: 'light', label: Text('浅色')),
                        ButtonSegment(value: 'dark', label: Text('深色')),
                      ],
                      selected: {_themeMode ?? 'system'},
                      onSelectionChanged: (Set<String> selected) {
                        setState(() => _themeMode = selected.first);
                        ref.read(settingsProvider.notifier).themeMode = selected.first;
                      },
                      showSelectedIcon: false,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        const Divider(height: 1, indent: 56),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          child: Row(
            children: [
              Padding(
                padding: const EdgeInsets.only(right: 16),
                child: Icon(Icons.colorize, color: cs.primary),
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '主题色',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500, color: cs.onSurface),
                    ),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: _presetColors.map((color) {
                        final hex = _colorToHex(color);
                        final isSelected = _primaryColor?.toUpperCase() == hex;
                        return GestureDetector(
                          onTap: () {
                            setState(() => _primaryColor = hex);
                            ref.read(settingsProvider.notifier).primaryColor = hex;
                          },
                          child: Container(
                            width: 36,
                            height: 36,
                            decoration: BoxDecoration(
                              color: color,
                              shape: BoxShape.circle,
                              border: isSelected
                                  ? Border.all(color: cs.onSurface, width: 3)
                                  : null,
                              boxShadow: isSelected
                                  ? [BoxShadow(color: color.withValues(alpha: 0.5), blurRadius: 8, spreadRadius: 1)]
                                  : null,
                            ),
                            child: isSelected
                                ? Icon(Icons.check, color: color.computeLuminance() > 0.5 ? Colors.black : Colors.white, size: 18)
                                : null,
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildCacheSettingsCard() {
    final cs = Theme.of(context).colorScheme;
    return _buildCard(
      title: '缓存设置',
      icon: Icons.folder,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          child: Row(
            children: [
              Padding(
                padding: const EdgeInsets.only(right: 16),
                child: Icon(Icons.storage, color: cs.primary),
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '缓存模式',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500, color: cs.onSurface),
                    ),
                    const SizedBox(height: 8),
                    SegmentedButton<String>(
                      segments: const [
                        ButtonSegment(value: 'memory', label: Text('内存缓存')),
                        ButtonSegment(value: 'disk', label: Text('磁盘缓存')),
                      ],
                      selected: {_cacheMode ?? 'memory'},
                      onSelectionChanged: (Set<String> selected) {
                        setState(() => _cacheMode = selected.first);
                        ref.read(settingsProvider.notifier).cacheMode = selected.first;
                      },
                      showSelectedIcon: false,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        const Divider(height: 1, indent: 56),
        _buildCacheSizeSlider(
          icon: Icons.forward,
          title: '前置缓存大小',
          subtitle: '用于预加载后续数据',
          value: _forwardCacheSizeMb ?? 32,
          onChanged: (v) {
            setState(() => _forwardCacheSizeMb = v);
          },
          onChangeEnd: (v) {
            ref.read(settingsProvider.notifier).forwardCacheSizeMb = v;
          },
        ),
        const Divider(height: 1, indent: 56),
        _buildCacheSizeSlider(
          icon: Icons.replay,
          title: '后置缓存大小',
          subtitle: '用于回退 seek 时的缓存',
          value: _backwardCacheSizeMb ?? 32,
          onChanged: (v) {
            setState(() => _backwardCacheSizeMb = v);
          },
          onChangeEnd: (v) {
            ref.read(settingsProvider.notifier).backwardCacheSizeMb = v;
          },
        ),
      ],
    );
  }

  Widget _buildCacheSizeSlider({
    required IconData icon,
    required String title,
    required String subtitle,
    required int value,
    required ValueChanged<int> onChanged,
    ValueChanged<int>? onChangeEnd,
  }) {
    final cs = Theme.of(context).colorScheme;
    final cacheSizes = [16, 32, 64, 128, 256, 512, 1024];
    
    // 找到最接近的缓存大小索引
    int currentIndex = cacheSizes.indexOf(value);
    if (currentIndex == -1) {
      // 如果值不在数组中，找到最接近的
      currentIndex = 1; // 默认 32MB
      for (int i = 0; i < cacheSizes.length; i++) {
        if (cacheSizes[i] >= value) {
          currentIndex = i;
          break;
        }
      }
      // 如果所有值都小于当前值，使用最大值
      if (value > cacheSizes.last) {
        currentIndex = cacheSizes.length - 1;
      }
    }
    
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Padding(
                padding: const EdgeInsets.only(right: 16),
                child: Icon(icon, color: cs.primary),
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500, color: cs.onSurface)),
                    const SizedBox(height: 2),
                    Text(subtitle, style: TextStyle(fontSize: 12, color: cs.onSurfaceVariant)),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: Slider(
                  value: currentIndex.toDouble(),
                  min: 0,
                  max: (cacheSizes.length - 1).toDouble(),
                  divisions: cacheSizes.length - 1,
                  activeColor: cs.primary,
                  inactiveColor: cs.surfaceContainerHighest,
                  onChanged: (v) {
                    onChanged(cacheSizes[v.toInt()]);
                  },
                  onChangeEnd: onChangeEnd != null ? (v) {
                    onChangeEnd(cacheSizes[v.toInt()]);
                  } : null,
                ),
              ),
              SizedBox(
                width: 60,
                child: Text(
                  '${cacheSizes[currentIndex]}MB',
                  style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: cs.primary),
                  textAlign: TextAlign.right,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildPlaybackSettingsCard() {
    return _buildCard(
      title: '播放设置',
      icon: Icons.movie,
      children: [
        _buildSliderTile(
          icon: Icons.speed,
          title: '默认播放速率',
          value: _defaultPlaybackRate?.toDouble() ?? 1.0,
          min: 0.5,
          max: 3.0,
          divisions: 10,
          displayFormat: (v) => '${v.toStringAsFixed(1)}x',
          onChanged: (v) {
            setState(() => _defaultPlaybackRate = v);
          },
          onChangeEnd: (v) {
            ref.read(settingsProvider.notifier).defaultPlaybackRate = v;
          },
        ),
        const Divider(height: 1, indent: 56),
        _buildSwitchTile(
          icon: Icons.history,
          title: '恢复播放位置',
          subtitle: '继续上次播放的位置',
          value: _resumePlayback ?? true,
          onChanged: (v) {
            setState(() => _resumePlayback = v);
            ref.read(settingsProvider.notifier).resumePlayback = v;
          },
        ),
        const Divider(height: 1, indent: 56),
        _buildSwitchTile(
          icon: Icons.memory,
          title: '硬件加速',
          subtitle: '启用硬件解码提升性能',
          value: _enableHardwareAcceleration ?? true,
          onChanged: (v) {
            setState(() => _enableHardwareAcceleration = v);
            ref.read(settingsProvider.notifier).enableHardwareAcceleration = v;
          },
        ),
        const Divider(height: 1, indent: 56),
        _buildSliderTile(
          icon: Icons.refresh,
          title: '媒体重试间隔',
          subtitle: '加载失败时自动重试的间隔',
          value: _mediaRetryInterval?.toDouble() ?? 5,
          min: 1,
          max: 60,
          divisions: 59,
          displayFormat: (v) => '${v.round()}秒',
          onChanged: (v) {
            setState(() => _mediaRetryInterval = v.round());
          },
          onChangeEnd: (v) {
            ref.read(settingsProvider.notifier).mediaRetryInterval = v.round();
          },
        ),
      ],
    );
  }

  Widget _buildCard({
    required String title,
    required IconData icon,
    required List<Widget> children,
  }) {
    final cs = Theme.of(context).colorScheme;
    return Container(
      decoration: BoxDecoration(
        color: cs.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Theme.of(context).shadowColor.withValues(alpha: 0.08),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Icon(icon, color: cs.primary, size: 24),
                const SizedBox(width: 12),
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: cs.onSurface,
                  ),
                ),
              ],
            ),
          ),
          ...children,
        ],
      ),
    );
  }

  Widget _buildSwitchTile({
    required IconData icon,
    required String title,
    required String subtitle,
    required bool value,
    required ValueChanged<bool> onChanged,
  }) {
    final cs = Theme.of(context).colorScheme;
    return ListTile(
      leading: Icon(icon, color: cs.primary),
      title: Text(title, style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500, color: cs.onSurface)),
      subtitle: Text(subtitle, style: TextStyle(fontSize: 12, color: cs.onSurfaceVariant)),
      trailing: Switch(
        value: value,
        onChanged: onChanged,
        activeTrackColor: cs.primary,
      ),
    );
  }

  Widget _buildSliderTile({
    required IconData icon,
    required String title,
    String? subtitle,
    required double value,
    required double min,
    required double max,
    int? divisions,
    required String Function(double) displayFormat,
    required ValueChanged<double> onChanged,
    ValueChanged<double>? onChangeEnd,
  }) {
    final cs = Theme.of(context).colorScheme;
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          Padding(
            padding: const EdgeInsets.only(right: 16),
            child: Icon(icon, color: cs.primary),
          ),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500, color: cs.onSurface)),
                if (subtitle != null) ...[
                  const SizedBox(height: 2),
                  Text(subtitle, style: TextStyle(fontSize: 12, color: cs.onSurfaceVariant)),
                ],
                Row(
                  children: [
                    Expanded(
                      child: Slider(
                        value: value,
                        min: min,
                        max: max,
                        divisions: divisions,
                        activeColor: cs.primary,
                        inactiveColor: cs.surfaceContainerHighest,
                        onChanged: onChanged,
                        onChangeEnd: onChangeEnd,
                      ),
                    ),
                    SizedBox(
                      width: 60,
                      child: Text(
                        displayFormat(value),
                        style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: cs.primary),
                        textAlign: TextAlign.right,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
