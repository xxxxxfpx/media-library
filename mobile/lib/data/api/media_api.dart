import 'api_client.dart';
import '../models/media.dart';

class MediaApi {
  final ApiClient _client;
  MediaApi(this._client);

  String get baseUrl => _client.baseUrl;

  /// 获取媒体列表
  ///
  /// [request] 包含筛选参数，[limit]/[offset] 为分页参数。
  Future<MediaListResponse> getList(
    MediaListRequest request, {
    int limit = 60,
    int offset = 0,
  }) async {
    final params = request.toQueryParams()
      ..['limit'] = limit
      ..['offset'] = offset;
    final response =
        await _client.get('/api/media/list', queryParameters: params);
    return MediaListResponse.fromJson(response.data);
  }

  Future<MediaItem> getInfo(int id) async {
    final response =
        await _client.get('/api/media/info', queryParameters: {'id': id});
    return MediaItem.fromJson(response.data);
  }

  Future<MediaStats> getStats() async {
    final response = await _client.get('/api/media/stats');
    return MediaStats.fromJson(response.data);
  }
}
