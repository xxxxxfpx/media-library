import 'dart:async';

import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../core/constants.dart';
import '../../core/token_cache.dart';

class ApiClient {
  late Dio _dio;
  final SharedPreferences _prefs;
  String? _baseUrl;

  bool _isRefreshing = false;
  final List<_PendingRequest> _pendingRequests = [];

  ApiClient(this._prefs) {
    _baseUrl = _prefs.getString(AppConstants.storageKeyBaseUrl) ??
        AppConstants.defaultBaseUrl;
    _dio = _createDio();
    TokenCache.set(_prefs.getString(AppConstants.storageKeyAccessToken));
  }

  /// Internal constructor for testing with a pre-configured [Dio] instance.
  /// Skips [_createDio] and [_baseUrl] initialization from SharedPreferences.
  ApiClient.withDio(this._dio, this._prefs) : _baseUrl = null;

  Dio _createDio() {
    final dio = Dio(BaseOptions(
      baseUrl: _baseUrl!,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
      headers: {'Content-Type': 'application/json'},
    ));

    dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) {
        final token =
            _prefs.getString(AppConstants.storageKeyAccessToken);
        if (token != null && !options.path.contains('/api/user/login')) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
      onError: (error, handler) async {
        if (error.response?.statusCode != 401) {
          return handler.next(error);
        }

        final request = error.requestOptions;

        // Replayed requests must not start a second refresh cycle if the new
        // access token is rejected. The original error is propagated instead.
        if (request.extra['_skipAuthRefresh'] == true) {
          return handler.next(error);
        }

        // Don't retry the refresh endpoint itself
        if (request.path.contains('/api/user/refresh')) {
          _clearTokens();
          return handler.next(error);
        }

        // Don't retry login
        if (request.path.contains('/api/user/login')) {
          return handler.next(error);
        }

        if (_isRefreshing) {
          final completer = Completer<Response>();
          _pendingRequests.add(_PendingRequest(completer, request));
          try {
            final result = await completer.future;
            return handler.resolve(result);
          } catch (_) {
            return handler.next(error);
          }
        }

        _isRefreshing = true;
        try {
          final refreshToken =
              _prefs.getString(AppConstants.storageKeyRefreshToken);
          if (refreshToken == null) {
            throw Exception('No refresh token');
          }

          final refreshDio = Dio(BaseOptions(baseUrl: _dio.options.baseUrl));
          final refreshResponse = await refreshDio.post(
            '/api/user/refresh',
            data: {'refresh_token': refreshToken},
          );

          final newAccess = refreshResponse.data['access_token'] as String?;
          final newRefresh = refreshResponse.data['refresh_token'] as String?;

          if (newAccess == null || newRefresh == null) {
            throw Exception('Invalid refresh response');
          }

          await _prefs.setString(
              AppConstants.storageKeyAccessToken, newAccess);
          await _prefs.setString(
              AppConstants.storageKeyRefreshToken, newRefresh);
          TokenCache.set(newAccess);

          // Replay all queued requests
          final pending = List<_PendingRequest>.from(_pendingRequests);
          _pendingRequests.clear();

           for (final p in pending) {
             p.request.headers['Authorization'] = 'Bearer $newAccess';
             p.request.extra['_skipAuthRefresh'] = true;
            try {
              final result = await _dio.fetch(p.request);
              p.completer.complete(result);
            } catch (e) {
              p.completer.completeError(e);
            }
          }

          // Retry original request
           request.headers['Authorization'] = 'Bearer $newAccess';
           request.extra['_skipAuthRefresh'] = true;
           final retryResponse = await _dio.fetch(request);
           return handler.resolve(retryResponse);
         } catch (refreshError) {
           for (final pendingRequest in _pendingRequests) {
             if (!pendingRequest.completer.isCompleted) {
               pendingRequest.completer.completeError(refreshError);
             }
           }
           _pendingRequests.clear();
           _clearTokens();
           return handler.next(error);
        } finally {
          _isRefreshing = false;
        }
      },
    ));

    return dio;
  }

  void _clearTokens() {
    TokenCache.clear();
    _prefs.remove(AppConstants.storageKeyAccessToken);
    _prefs.remove(AppConstants.storageKeyRefreshToken);
  }

  void updateBaseUrl(String url) {
    _baseUrl = url;
    _prefs.setString(AppConstants.storageKeyBaseUrl, url);
    _dio = _createDio();
  }

  String get baseUrl => _baseUrl!;

  String? get accessToken =>
      TokenCache.accessToken ??
          _prefs.getString(AppConstants.storageKeyAccessToken);

  Future<Response> get(String path,
      {Map<String, dynamic>? queryParameters}) async {
    return _dio.get(path, queryParameters: queryParameters);
  }

  /// 获取重定向 URL，不跟随重定向
  ///
  /// 用于文件流媒体地址获取，避免 Dio 跟随重定向下载整个文件。
  Future<String> getRedirectUrl(String path,
      {Map<String, dynamic>? queryParameters}) async {
    final response = await _dio.get(
      path,
      queryParameters: queryParameters,
      options: Options(
        followRedirects: false,
        validateStatus: (status) => status != null && status >= 200 && status < 400,
      ),
    );
    final location = response.headers.value('location');
    if (location == null || location.isEmpty) {
      throw Exception('未获取到重定向地址');
    }
    return location;
  }

  Future<Response> post(String path, {dynamic data}) async {
    return _dio.post(path, data: data);
  }

  Future<Response> put(String path, {dynamic data}) async {
    return _dio.put(path, data: data);
  }

  Future<Response> delete(String path, {dynamic data}) async {
    return _dio.delete(path, data: data);
  }
}

class _PendingRequest {
  final Completer<Response> completer;
  final RequestOptions request;

  _PendingRequest(this.completer, this.request);
}
