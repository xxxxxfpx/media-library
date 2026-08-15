import 'api_client.dart';
import '../models/auth.dart';

class AuthApi {
  final ApiClient _client;
  AuthApi(this._client);

  Future<LoginResponse> login(String username, String password) async {
    final response = await _client.post('/api/user/login', data: {
      'username': username,
      'password': password,
    });
    return LoginResponse.fromJson(response.data);
  }

  Future<LoginResponse> refresh(String refreshToken) async {
    final response = await _client.post('/api/user/refresh', data: {
      'refresh_token': refreshToken,
    });
    return LoginResponse.fromJson(response.data);
  }

  Future<UserInfo> getInfo() async {
    final response = await _client.get('/api/user/info');
    return UserInfo.fromJson(response.data);
  }

  Future<void> logout() async {
    await _client.post('/api/user/logout');
  }
}
