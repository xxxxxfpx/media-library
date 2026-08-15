import 'package:yaml/yaml.dart';

/// 系统全局静态配置
///
/// 通过解析 assets/config.yaml 初始化，用于指导访问后端的哪个 URL
class SystemConfig {
  SystemConfig._();

  static final SystemConfig _instance = SystemConfig._();

  static SystemConfig get instance => _instance;

  late String _baseUrl;
  String get baseUrl => _baseUrl;

  /// 从 YAML 字符串加载配置
  void loadFromYaml(String yamlString) {
    final yamlMap = loadYaml(yamlString) as YamlMap;
    _applyYaml(yamlMap);
  }

  void _applyYaml(YamlMap map) {
    final api = map['api'] as YamlMap?;
    _baseUrl = (api?['base_url'] as String?) ?? 'https://xmedia.iepose.cn';
  }
}
