/// 全局访问令牌缓存。
///
/// 媒体 URL（图片/视频）由 `Image.network` / `CachedNetworkImageProvider` 等
/// 无法携带 Authorization 请求头的方式加载，需将令牌附加到 query 参数。
/// 该缓存由 `ApiClient` 在构造/刷新/登出时维护，供 URL 构造同步读取。
class TokenCache {
  TokenCache._();

  static String? _accessToken;

  static String? get accessToken => _accessToken;

  static void set(String? token) => _accessToken = token;

  static void clear() => _accessToken = null;

  /// 将访问令牌附加到已有 URL（若令牌存在）。
  static String withToken(String url) {
    final token = _accessToken;
    if (token == null || token.isEmpty) return url;
    return '$url&token=${Uri.encodeComponent(token)}';
  }
}
