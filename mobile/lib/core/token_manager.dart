import 'package:shared_preferences/shared_preferences.dart';
import 'constants.dart';

class TokenManager {
  static Future<String?> getAccessToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(AppConstants.storageKeyAccessToken);
  }

  static Future<String?> getRefreshToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(AppConstants.storageKeyRefreshToken);
  }

  static Future<void> setTokens(String access, String refresh) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(AppConstants.storageKeyAccessToken, access);
    await prefs.setString(AppConstants.storageKeyRefreshToken, refresh);
  }

  static Future<void> clearTokens() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(AppConstants.storageKeyAccessToken);
    await prefs.remove(AppConstants.storageKeyRefreshToken);
  }
}
