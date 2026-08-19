import 'dart:io';

import 'package:flutter/material.dart';
import 'package:device_info_plus/device_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../data/api/api_client.dart';
import '../../data/api/media_api.dart';
import '../../data/models/media.dart';
import '../../core/app_logger.dart';

class HomeTabHome extends StatefulWidget {
  const HomeTabHome({super.key});

  @override
  State<HomeTabHome> createState() => _HomeTabHomeState();
}

class _HomeTabHomeState extends State<HomeTabHome> {
  Map<String, String> _deviceData = {};
  bool _isLoading = true;
  MediaStats? _stats;
  bool _isStatsLoading = true;

  @override
  void initState() {
    super.initState();
    _loadDeviceInfo();
    _loadStats();
  }

  Future<void> _loadStats() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final api = MediaApi(ApiClient(prefs));
      final stats = await api.getStats();
      if (mounted) {
        setState(() {
          _stats = stats;
          _isStatsLoading = false;
        });
      }
    } catch (error, stackTrace) {
      AppLogger.error(
        'home_stats_load_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'home',
      );
      if (mounted) setState(() => _isStatsLoading = false);
    }
  }

  Future<void> _loadDeviceInfo() async {
    try {
      final info = await DeviceInfoPlugin().deviceInfo;

      String ip = '未知';
      try {
        final interfaces = await NetworkInterface.list();
        for (final iface in interfaces) {
          for (final addr in iface.addresses) {
            if (addr.type == InternetAddressType.IPv4 && !addr.isLoopback) {
              ip = addr.address;
              break;
            }
          }
          if (ip != '未知') break;
        }
      } catch (error, stackTrace) {
        AppLogger.debug(
          'network_interface_unavailable',
          category: 'device',
          fields: {'error_type': error.runtimeType.toString()},
        );
        AppLogger.debug('$stackTrace', category: 'device');
      }

      final memMb = (ProcessInfo.currentRss / 1024 / 1024).toStringAsFixed(1);

      String cpu = '未知';
      try {
        final stat = await File('/proc/stat').readAsString();
        final firstLine = stat.split('\n').first;
        final parts = firstLine
            .split(RegExp(r'\s+'))
            .skip(1)
            .map((e) => int.tryParse(e) ?? 0)
            .toList();
        if (parts.length >= 5) {
          final total = parts.fold(0, (a, b) => a + b);
          final idle = parts[3];
          cpu = total > 0
              ? '${((1 - idle / total) * 100).toStringAsFixed(1)}%'
              : '未知';
        }
      } catch (error) {
        AppLogger.debug(
          'cpu_usage_unavailable',
          category: 'device',
          fields: {'error_type': error.runtimeType.toString()},
        );
      }

      setState(() {
        final infoType = info.runtimeType.toString();
        if (infoType.contains('Android')) {
          final androidInfo = info as dynamic;
          _deviceData = {
            '平台': 'Android',
            '设备': androidInfo.device ?? '未知',
            '型号': androidInfo.model ?? '未知',
            '品牌': androidInfo.brand ?? '未知',
            '系统版本': 'Android ${androidInfo.version?.release ?? '未知'}',
            'SDK': androidInfo.version?.sdkInt?.toString() ?? '未知',
            'IP': ip,
            '内存': '$memMb MB',
            'CPU': cpu,
          };
        } else if (infoType.contains('Ios') ||
            infoType.contains('IOS') ||
            infoType.contains('Apple')) {
          final iosInfo = info as dynamic;
          _deviceData = {
            '平台': 'iOS',
            '名称': iosInfo.name ?? '未知',
            '系统': iosInfo.systemName ?? '未知',
            '版本': iosInfo.systemVersion ?? '未知',
            '型号': iosInfo.model ?? '未知',
            'IP': ip,
            '内存': '$memMb MB',
          };
        } else {
          _deviceData = {
            '平台': infoType,
            'IP': ip,
            '内存': '$memMb MB',
            'CPU': cpu,
          };
        }
        _isLoading = false;
      });
    } catch (error, stackTrace) {
      AppLogger.error(
        'device_info_load_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'device',
      );
      setState(() {
        _deviceData = {'错误': '设备信息加载失败'};
        _isLoading = false;
      });
    }
  }

  Future<void> _onRefresh() async {
    await Future.wait([_loadDeviceInfo(), _loadStats()]);
  }

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Container(
      color: cs.surface,
      child: RefreshIndicator(
        onRefresh: _onRefresh,
        color: cs.primary,
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildStatSection(),
              const SizedBox(height: 24),
              _buildSystemSection(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatSection() {
    final cs = Theme.of(context).colorScheme;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '媒体统计',
          style: TextStyle(
            fontSize: 15,
            fontWeight: FontWeight.bold,
            color: cs.onSurface,
          ),
        ),
        const SizedBox(height: 12),
        if (_isStatsLoading)
          const SizedBox(
            height: 80,
            child: Center(child: CircularProgressIndicator(strokeWidth: 2)),
          )
        else
          Row(
            children: [
              _buildStatCard(
                '视频',
                '${_stats?.videoCount ?? 0}',
                Icons.videocam,
                cs.primary,
              ),
              const SizedBox(width: 12),
              _buildStatCard(
                '音乐',
                '${_stats?.audioCount ?? 0}',
                Icons.music_note,
                cs.secondary,
              ),
              const SizedBox(width: 12),
              _buildStatCard(
                '图片',
                '${_stats?.imageCount ?? 0}',
                Icons.image,
                cs.tertiary,
              ),
            ],
          ),
      ],
    );
  }

  Widget _buildStatCard(
    String label,
    String count,
    IconData icon,
    Color color,
  ) {
    final cs = Theme.of(context).colorScheme;
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 8),
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
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 22, color: color),
            const SizedBox(height: 4),
            Text(
              count,
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: cs.onSurface,
              ),
            ),
            Text(
              label,
              style: TextStyle(fontSize: 11, color: cs.onSurfaceVariant),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSystemSection() {
    final cs = Theme.of(context).colorScheme;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '设备信息',
          style: TextStyle(
            fontSize: 15,
            fontWeight: FontWeight.bold,
            color: cs.onSurface,
          ),
        ),
        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.all(14),
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
          child: _isLoading
              ? const Center(child: CircularProgressIndicator())
              : Column(
                  children: _deviceData.entries
                      .map(
                        (e) => Padding(
                          padding: const EdgeInsets.symmetric(vertical: 3),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                e.key,
                                style: TextStyle(
                                  fontSize: 12,
                                  color: cs.onSurfaceVariant,
                                ),
                              ),
                              Flexible(
                                child: Text(
                                  e.value,
                                  style: TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.w500,
                                    color: cs.onSurface,
                                  ),
                                  textAlign: TextAlign.end,
                                ),
                              ),
                            ],
                          ),
                        ),
                      )
                      .toList(),
                ),
        ),
      ],
    );
  }
}
