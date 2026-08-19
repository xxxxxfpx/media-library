import 'dart:async';
import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:media_kit/media_kit.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'core/constants.dart';
import 'design_system/app_color_tokens.dart';
import 'design_system/app_theme.dart';
import 'phone/home/home_shell.dart';
import 'phone/login/view.dart';
import 'services/sync_service.dart';
import 'providers/settings_provider.dart';
import 'core/app_logger.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  MediaKit.ensureInitialized();
  final prefs = await SharedPreferences.getInstance();
  await AppLogger.initialize(prefs);
  FlutterError.onError = (details) {
    FlutterError.presentError(details);
    AppLogger.error(
      'framework_error',
      error: details.exception,
      stackTrace: details.stack,
      category: 'flutter',
    );
  };
  PlatformDispatcher.instance.onError = (error, stackTrace) {
    AppLogger.error(
      'platform_error',
      error: error,
      stackTrace: stackTrace,
      category: 'platform',
    );
    return true;
  };

  runZonedGuarded(() => runApp(const ProviderScope(child: MyApp())), (
    error,
    stackTrace,
  ) {
    AppLogger.error(
      'unhandled_error',
      error: error,
      stackTrace: stackTrace,
      category: 'app',
    );
  });
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final settings = ref.watch(settingsProvider);
    final presetId = _resolvePreset(settings);
    final themeMode = AppTheme.toThemeMode(settings?.themeMode);

    return MaterialApp(
      title: '媒体库',
      debugShowCheckedModeBanner: false,
      themeMode: themeMode,
      theme: AppTheme.light(presetId),
      darkTheme: AppTheme.dark(presetId),
      home: const AuthGate(),
      builder: (context, child) {
        final textTheme = Theme.of(context).textTheme;
        return DefaultTextStyle(
          style: (textTheme.bodyMedium ?? const TextStyle()).copyWith(
            decoration: TextDecoration.none,
          ),
          child: child!,
        );
      },
    );
  }

  static ThemePresetId _resolvePreset(dynamic settings) {
    final presetId = settings?.themePreset as String?;
    if (presetId != null && presetId.isNotEmpty) {
      return ThemePresetId.fromId(presetId);
    }
    // 兼容旧版本：primary_color -> 推断预设
    final legacyHex = settings?.primaryColor as String?;
    if (legacyHex != null && legacyHex.isNotEmpty) {
      final hex = legacyHex.replaceFirst('#', '').toUpperCase();
      // 旧紫色系仍映射到韵味紫
      if (hex.contains('9C27B0') || hex.contains('9C27') || hex == 'FF9C27B0') {
        return ThemePresetId.currentPurple;
      }
    }
    return ThemePresetId.currentPurple;
  }
}

class AuthGate extends ConsumerStatefulWidget {
  const AuthGate({super.key});

  @override
  ConsumerState<AuthGate> createState() => _AuthGateState();
}

class _AuthGateState extends ConsumerState<AuthGate> {
  bool? _isLoggedIn;

  @override
  void initState() {
    super.initState();
    _checkAuth();
  }

  Future<void> _checkAuth() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(AppConstants.storageKeyAccessToken);
    if (mounted) {
      setState(() => _isLoggedIn = token != null && token.isNotEmpty);
      if (_isLoggedIn == true) {
        SyncService().start(ref);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoggedIn == null) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    if (_isLoggedIn!) {
      return const HomeShell();
    }
    return const LoginScreen();
  }
}
