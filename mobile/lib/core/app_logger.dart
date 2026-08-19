import 'dart:convert';
import 'dart:developer' as developer;

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Structured application logger with console output and a bounded local ring.
class AppLogger {
  AppLogger._();

  static const _storageKey = 'app_log_ring';
  static const _maxEntries = 300;
  static const _maxFieldLength = 500;

  static SharedPreferences? _prefs;
  static final List<String> _ring = <String>[];
  static bool _persistScheduled = false;

  static Future<void> initialize(SharedPreferences prefs) async {
    _prefs = prefs;
    _ring
      ..clear()
      ..addAll(prefs.getStringList(_storageKey) ?? const <String>[]);
    if (_ring.length > _maxEntries) {
      _ring.removeRange(0, _ring.length - _maxEntries);
    }
  }

  static void debug(
    String action, {
    String category = 'app',
    Map<String, Object?> fields = const <String, Object?>{},
  }) {
    _write('DEBUG', action, category: category, fields: fields, persist: false);
  }

  static void info(
    String action, {
    String category = 'app',
    Map<String, Object?> fields = const <String, Object?>{},
  }) {
    _write('INFO', action, category: category, fields: fields);
  }

  static void warning(
    String action, {
    Object? error,
    StackTrace? stackTrace,
    String category = 'app',
    Map<String, Object?> fields = const <String, Object?>{},
  }) {
    _write(
      'WARNING',
      action,
      category: category,
      fields: fields,
      error: error,
      stackTrace: stackTrace,
    );
  }

  static void error(
    String action, {
    Object? error,
    StackTrace? stackTrace,
    String category = 'app',
    Map<String, Object?> fields = const <String, Object?>{},
  }) {
    _write(
      'ERROR',
      action,
      category: category,
      fields: fields,
      error: error,
      stackTrace: stackTrace,
    );
  }

  static List<String> get recentLogs => List.unmodifiable(_ring);

  static Future<void> clear() async {
    _ring.clear();
    await _prefs?.remove(_storageKey);
  }

  static void _write(
    String level,
    String action, {
    required String category,
    required Map<String, Object?> fields,
    Object? error,
    StackTrace? stackTrace,
    bool persist = true,
  }) {
    final record = <String, Object?>{
      'time': DateTime.now().toUtc().toIso8601String(),
      'level': level,
      'category': category,
      'action': action,
      if (fields.isNotEmpty) 'fields': _sanitizeMap(fields),
      if (error != null) 'error': _redact(error.toString()),
    };
    final message = jsonEncode(record);
    developer.log(
      message,
      name: 'media_app.$category',
      level: _developerLevel(level),
      error: error == null ? null : _redact(error.toString()),
      stackTrace: stackTrace,
    );

    if (persist && level != 'DEBUG') {
      _ring.add(message);
      if (_ring.length > _maxEntries) {
        _ring.removeAt(0);
      }
      _schedulePersist();
    }
  }

  static int _developerLevel(String level) {
    switch (level) {
      case 'DEBUG':
        return 500;
      case 'INFO':
        return 800;
      case 'WARNING':
        return 900;
      default:
        return 1000;
    }
  }

  static Map<String, Object?> _sanitizeMap(Map<String, Object?> fields) {
    return fields.map(
      (key, value) => MapEntry(key, _sanitizeValue(key, value)),
    );
  }

  static Object? _sanitizeValue(String key, Object? value) {
    final sensitive = RegExp(
      r'token|password|secret|authorization|cookie',
      caseSensitive: false,
    );
    if (sensitive.hasMatch(key)) return '[REDACTED]';
    if (value is Map<String, Object?>) return _sanitizeMap(value);
    if (value is Iterable) {
      return value.map((item) => _sanitizeValue(key, item)).toList();
    }
    return _redact(value?.toString());
  }

  static String? _redact(String? value) {
    if (value == null) return null;
    final redacted = value
        .replaceAllMapped(
          RegExp(
            r'(authorization|token|password|secret)=([^&\s]+)',
            caseSensitive: false,
          ),
          (match) => '${match.group(1)}=[REDACTED]',
        )
        .replaceAll(
          RegExp(r'bearer\s+[A-Za-z0-9._-]+', caseSensitive: false),
          'Bearer [REDACTED]',
        );
    return redacted.length > _maxFieldLength
        ? '${redacted.substring(0, _maxFieldLength)}…'
        : redacted;
  }

  static void _schedulePersist() {
    if (_persistScheduled || _prefs == null) return;
    _persistScheduled = true;
    Future<void>.delayed(const Duration(milliseconds: 250), () async {
      _persistScheduled = false;
      try {
        await _prefs?.setStringList(_storageKey, List<String>.from(_ring));
      } catch (error, stackTrace) {
        if (kDebugMode) {
          developer.log(
            'Failed to persist local log ring',
            error: error,
            stackTrace: stackTrace,
          );
        }
      }
    });
  }
}
