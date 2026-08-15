import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:media_app/data/api/api_client.dart';

/// A [MockApiClient] that extends [ApiClient] and overrides HTTP methods
/// to return canned responses without making real network calls.
class MockApiClient extends ApiClient {
  final Map<String, Response Function()> _handlers = {};

  /// Create a [MockApiClient] with empty SharedPreferences.
  MockApiClient(super.prefs);

  /// Register a handler for requests whose path contains [pathPattern].
  void on(String pathPattern, Response Function() handler) {
    _handlers[pathPattern] = handler;
  }

  @override
  Future<Response> get(String path,
      {Map<String, dynamic>? queryParameters}) async {
    return _handle(path);
  }

  @override
  Future<Response> post(String path, {dynamic data}) async {
    return _handle(path);
  }

  @override
  Future<Response> put(String path, {dynamic data}) async {
    return _handle(path);
  }

  @override
  Future<Response> delete(String path, {dynamic data}) async {
    return _handle(path);
  }

  Future<Response> _handle(String path) async {
    for (final entry in _handlers.entries) {
      if (path.contains(entry.key)) {
        return entry.value();
      }
    }
    throw Exception('MockApiClient: no handler for $path');
  }
}

/// Creates a [SharedPreferences] instance with mock initial values.
Future<SharedPreferences> createMockPrefs() async {
  SharedPreferences.setMockInitialValues({});
  return SharedPreferences.getInstance();
}

/// Helper to create a mock [Response].
Response mockResponse(Map<String, dynamic> data,
    {int statusCode = 200}) {
  return Response(
    requestOptions: RequestOptions(path: ''),
    data: data,
    statusCode: statusCode,
  );
}

/// Helper to create a mock [Response] with a List data.
Response mockListResponse(List<dynamic> data, {int statusCode = 200}) {
  return Response(
    requestOptions: RequestOptions(path: ''),
    data: data,
    statusCode: statusCode,
  );
}
