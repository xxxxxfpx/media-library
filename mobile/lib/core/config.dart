import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:yaml/yaml.dart';

/// 应用配置读取类
///
/// 在 main() 启动时加载 config.yaml，之后通过 Config.instance 全局访问。
///
/// 使用方式：
/// ```dart
/// await Config.load();           // 启动时加载
/// Config.instance.landscapeThreshold  // 任意位置读取
/// ```
class Config {
  Config._();

  static Config? _instance;

  /// 配置单例
  static Config get instance {
    if (_instance == null) {
      throw StateError('Config 尚未加载，请先在 main() 中调用 await Config.load()');
    }
    return _instance!;
  }

  /// 从 assets/config.yaml 加载配置
  static Future<void> load() async {
    final yamlString = await rootBundle.loadString('assets/config.yaml');
    final yamlMap = loadYaml(yamlString) as YamlMap;
    _instance = Config._fromYaml(yamlMap);
  }

  static Config _fromYaml(YamlMap map) {
    final config = Config._();

    final layout = map['layout'] as YamlMap?;
    config._landscapeThreshold =
        (layout?['landscape_threshold'] as num?)?.toDouble() ?? 1.25;

    final api = map['api'] as YamlMap?;
    config._baseUrl = (api?['base_url'] as String?) ?? 'http://192.168.1.5:8000';
    config._connectTimeout =
        (api?['connect_timeout_seconds'] as num?)?.toInt() ?? 15;
    config._receiveTimeout =
        (api?['receive_timeout_seconds'] as num?)?.toInt() ?? 30;

    final cache = map['cache'] as YamlMap?;
    config._maxImageCacheMb =
        (cache?['max_image_cache_mb'] as num?)?.toInt() ?? 200;
    config._maxApiCacheMb =
        (cache?['max_api_cache_mb'] as num?)?.toInt() ?? 50;

    return config;
  }

  // ========== 布局配置 ==========

  late double _landscapeThreshold;
  double get landscapeThreshold => _landscapeThreshold;

  /// 根据 BuildContext 判断当前是否使用横屏布局
  bool isLandscape(BuildContext context) {
    return MediaQuery.of(context).size.aspectRatio > landscapeThreshold;
  }

  /// 根据 BuildContext 判断当前是否使用竖屏布局
  bool isPortrait(BuildContext context) {
    return MediaQuery.of(context).size.aspectRatio <= landscapeThreshold;
  }

  /// 根据宽高比直接判断是否横屏布局
  bool isLandscapeByRatio(double aspectRatio) {
    return aspectRatio > landscapeThreshold;
  }

  /// 获取当前屏幕宽高比
  double aspectRatioOf(BuildContext context) {
    return MediaQuery.of(context).size.aspectRatio;
  }

  // ========== API 配置 ==========

  late String _baseUrl;
  String get baseUrl => _baseUrl;

  late int _connectTimeout;
  int get connectTimeout => _connectTimeout;

  late int _receiveTimeout;
  int get receiveTimeout => _receiveTimeout;

  // ========== 缓存配置 ==========

  late int _maxImageCacheMb;
  int get maxImageCacheMb => _maxImageCacheMb;

  late int _maxApiCacheMb;
  int get maxApiCacheMb => _maxApiCacheMb;
}
