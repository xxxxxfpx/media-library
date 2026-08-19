import 'dart:async';
import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:media_kit/media_kit.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'core/constants.dart';
import 'phone/home/view.dart';
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

    ThemeMode themeMode;
    switch (settings?.themeMode ?? 'system') {
      case 'light':
        themeMode = ThemeMode.light;
      case 'dark':
        themeMode = ThemeMode.dark;
      default:
        themeMode = ThemeMode.system;
    }

    final seedColor = _parseColor(settings?.primaryColor);

    return MaterialApp(
      title: '媒体库',
      debugShowCheckedModeBanner: false,
      themeMode: themeMode,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: seedColor),
        useMaterial3: true,
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: seedColor,
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
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

  static Color _parseColor(String? hex) {
    if (hex == null || hex.isEmpty) return Colors.purple;
    hex = hex.replaceFirst('#', '');
    if (hex.length != 6 && hex.length != 8) return Colors.purple;
    if (!RegExp(r'^[0-9a-fA-F]+$').hasMatch(hex)) return Colors.purple;
    final value = int.tryParse(hex, radix: 16);
    if (value == null) return Colors.purple;
    if (hex.length == 6) return Color(0xFF000000 | value);
    return Color(value);
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
      return const HomePagePhone();
    }
    return const LoginScreen();
  }
}
