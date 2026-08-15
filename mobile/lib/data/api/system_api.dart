import 'api_client.dart';
import '../models/system.dart';

class SystemApi {
  final ApiClient _client;
  SystemApi(this._client);

  Future<SystemInfo> getInfo() async {
    final response = await _client.get('/api/system/info');
    return SystemInfo.fromJson(response.data);
  }

  Future<SystemSetting> getSetting() async {
    final response = await _client.get('/api/system/setting');
    return SystemSetting.fromJson(response.data);
  }

  Future<void> updateSetting(SystemSetting setting) async {
    await _client.post('/api/system/setting', data: {'data': setting.toJson()});
  }
}
