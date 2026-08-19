import 'api_client.dart';

class GuangYaPanApi {
  final ApiClient _client;

  GuangYaPanApi(this._client);

  Future<Map<String, dynamic>> getConfig() async {
    final response = await _client.get('/api/drives/guangyapan/config');
    return Map<String, dynamic>.from(response.data as Map);
  }

  Future<Map<String, dynamic>> updateConfig(Map<String, dynamic> config) async {
    final response = await _client.put(
      '/api/drives/guangyapan/config',
      data: config,
    );
    return Map<String, dynamic>.from(response.data as Map);
  }
}
