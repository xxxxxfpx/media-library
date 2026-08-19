// 登录认证业务逻辑
import 'package:shared_preferences/shared_preferences.dart';
import '../core/constants.dart';
import '../core/app_logger.dart';
import '../data/api/api_client.dart';
import '../data/api/auth_api.dart';
import '../data/models/auth.dart';

class AuthService {
  Future<LoginResponse> login({
    required String username,
    required String password,
  }) async {
    final stopwatch = Stopwatch()..start();
    try {
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);
      final authApi = AuthApi(client);
      final response = await authApi.login(username, password);
      await _saveTokens(response);
      AppLogger.info(
        'login_succeeded',
        category: 'auth',
        fields: {'duration_ms': stopwatch.elapsedMilliseconds},
      );
      return response;
    } catch (error, stackTrace) {
      AppLogger.error(
        'login_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'auth',
        fields: {'duration_ms': stopwatch.elapsedMilliseconds},
      );
      rethrow;
    }
  }

  Future<void> _saveTokens(LoginResponse response) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(
      AppConstants.storageKeyAccessToken,
      response.accessToken,
    );
    await prefs.setString(
      AppConstants.storageKeyRefreshToken,
      response.refreshToken,
    );
  }

  static Future<bool> hasValidToken() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(AppConstants.storageKeyAccessToken);
    return token != null && token.isNotEmpty;
  }

  static Future<void> clearTokens() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(AppConstants.storageKeyAccessToken);
    await prefs.remove(AppConstants.storageKeyRefreshToken);
  }
}
