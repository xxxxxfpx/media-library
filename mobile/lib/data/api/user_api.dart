import 'api_client.dart';
import '../models/auth.dart';
import '../models/media.dart';

class UserApi {
  final ApiClient _client;
  UserApi(this._client);

  Future<void> updateUserData(UpdateUserDataRequest request) async {
    await _client.post('/api/user/userdata', data: request.toJson());
  }

  Future<MediaListResponse> getHistory({
    int limit = 60,
    int offset = 0,
  }) async {
    final response = await _client.get(
      '/api/user/history',
      queryParameters: {'limit': limit, 'offset': offset},
    );
    return MediaListResponse.fromJson(response.data);
  }

  Future<UserSetting> getSetting() async {
    final response = await _client.get('/api/user/setting');
    return UserSetting.fromJson(response.data);
  }

  Future<void> updateSetting(UserSetting setting) async {
    await _client.post('/api/user/setting', data: setting.toJson());
  }
}
