import 'api_client.dart';
import '../../core/token_cache.dart';

class FileApi {
  final ApiClient _client;
  FileApi(this._client);

  String getFileDataUrl(int fileId) {
    return TokenCache.withToken(
        '${_client.baseUrl}/api/file/data?file_id=$fileId');
  }
}
