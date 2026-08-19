import 'package:flutter/material.dart';

/// 主题预设枚举 — 必备 3 个 + 扩展 2 个
enum ThemePresetId {
  modernBlack('modernBlack', '现代黑'),
  modernWhite('modernWhite', '现代白'),
  currentPurple('currentPurple', '韵味紫'),
  ocean('ocean', '海洋蓝'),
  forest('forest', '森林绿');

  final String id;
  final String label;
  const ThemePresetId(this.id, this.label);

  static ThemePresetId fromId(String? id) {
    if (id == null) return currentPurple;
    return values.firstWhere(
      (e) => e.id == id,
      orElse: () => currentPurple,
    );
  }
}

/// 语义扩展色 — 超出 ColorScheme 的业务色
@immutable
class AppSemanticColors extends ThemeExtension<AppSemanticColors> {
  final Color success;
  final Color warning;
  final Color info;
  final Color rating;
  final Color favorite;
  final Color playerOverlay;
  final Color playerOverlayText;

  const AppSemanticColors({
    required this.success,
    required this.warning,
    required this.info,
    required this.rating,
    required this.favorite,
    required this.playerOverlay,
    required this.playerOverlayText,
  });

  @override
  AppSemanticColors copyWith({
    Color? success,
    Color? warning,
    Color? info,
    Color? rating,
    Color? favorite,
    Color? playerOverlay,
    Color? playerOverlayText,
  }) {
    return AppSemanticColors(
      success: success ?? this.success,
      warning: warning ?? this.warning,
      info: info ?? this.info,
      rating: rating ?? this.rating,
      favorite: favorite ?? this.favorite,
      playerOverlay: playerOverlay ?? this.playerOverlay,
      playerOverlayText: playerOverlayText ?? this.playerOverlayText,
    );
  }

  @override
  AppSemanticColors lerp(ThemeExtension<AppSemanticColors>? other, double t) {
    if (other is! AppSemanticColors) return this;
    return AppSemanticColors(
      success: Color.lerp(success, other.success, t)!,
      warning: Color.lerp(warning, other.warning, t)!,
      info: Color.lerp(info, other.info, t)!,
      rating: Color.lerp(rating, other.rating, t)!,
      favorite: Color.lerp(favorite, other.favorite, t)!,
      playerOverlay: Color.lerp(playerOverlay, other.playerOverlay, t)!,
      playerOverlayText:
          Color.lerp(playerOverlayText, other.playerOverlayText, t)!,
    );
  }
}

/// 完整主题定义
class AppThemePreset {
  final ThemePresetId id;
  final ColorScheme lightScheme;
  final ColorScheme darkScheme;
  final AppSemanticColors lightSemantic;
  final AppSemanticColors darkSemantic;

  const AppThemePreset({
    required this.id,
    required this.lightScheme,
    required this.darkScheme,
    required this.lightSemantic,
    required this.darkSemantic,
  });
}

abstract class AppThemePresets {
  // ── 现代黑：深邃黑底 + 冷灰蓝强调 ──
  static const modernBlack = AppThemePreset(
    id: ThemePresetId.modernBlack,
    lightScheme: ColorScheme(
      brightness: Brightness.light,
      primary: Color(0xFF2B2F45),
      onPrimary: Color(0xFFFFFFFF),
      primaryContainer: Color(0xFFDDDFFF),
      onPrimaryContainer: Color(0xFF14182B),
      secondary: Color(0xFF54576B),
      onSecondary: Color(0xFFFFFFFF),
      secondaryContainer: Color(0xFFD8DAF0),
      onSecondaryContainer: Color(0xFF111326),
      tertiary: Color(0xFF77536D),
      onTertiary: Color(0xFFFFFFFF),
      tertiaryContainer: Color(0xFFFFD8EE),
      onTertiaryContainer: Color(0xFF2E1127),
      error: Color(0xFFBA1A1A),
      onError: Color(0xFFFFFFFF),
      errorContainer: Color(0xFFFFDAD6),
      onErrorContainer: Color(0xFF410002),
      surface: Color(0xFFFBF9FF),
      onSurface: Color(0xFF1A1B21),
      surfaceContainerHighest: Color(0xFFE3E1E9),
      onSurfaceVariant: Color(0xFF46464F),
      outline: Color(0xFF777680),
      outlineVariant: Color(0xFFC7C5D0),
      scrim: Color(0xFF000000),
      inverseSurface: Color(0xFF2F3036),
      onInverseSurface: Color(0xFFF2F0F7),
      inversePrimary: Color(0xFFB9C4FF),
      surfaceTint: Color(0xFF2B2F45),
    ),
    darkScheme: ColorScheme(
      brightness: Brightness.dark,
      primary: Color(0xFFB9C4FF),
      onPrimary: Color(0xFF12215F),
      primaryContainer: Color(0xFF293978),
      onPrimaryContainer: Color(0xFFDDDFFF),
      secondary: Color(0xFFBDC0D9),
      onSecondary: Color(0xFF262A42),
      secondaryContainer: Color(0xFF3C4059),
      onSecondaryContainer: Color(0xFFD8DAF0),
      tertiary: Color(0xFFEAB8CF),
      onTertiary: Color(0xFF46263E),
      tertiaryContainer: Color(0xFF5E3C55),
      onTertiaryContainer: Color(0xFFFFD8EE),
      error: Color(0xFFFFB4AB),
      onError: Color(0xFF690005),
      errorContainer: Color(0xFF93000A),
      onErrorContainer: Color(0xFFFFDAD6),
      surface: Color(0xFF0D0E12),
      onSurface: Color(0xFFE5E1E9),
      surfaceContainerHighest: Color(0xFF2A2B32),
      onSurfaceVariant: Color(0xFFC5C6D0),
      outline: Color(0xFF8F909A),
      outlineVariant: Color(0xFF46464F),
      scrim: Color(0xFF000000),
      inverseSurface: Color(0xFFE5E1E9),
      onInverseSurface: Color(0xFF2F3036),
      inversePrimary: Color(0xFF404A78),
      surfaceTint: Color(0xFFB9C4FF),
    ),
    lightSemantic: AppSemanticColors(
      success: Color(0xFF2E7D32),
      warning: Color(0xFFED6C02),
      info: Color(0xFF0288D1),
      rating: Color(0xFFF59F0A),
      favorite: Color(0xFFE53935),
      playerOverlay: Color(0xCC000000),
      playerOverlayText: Color(0xFFFFFFFF),
    ),
    darkSemantic: AppSemanticColors(
      success: Color(0xFF81C784),
      warning: Color(0xFFFFB74D),
      info: Color(0xFF4FC3F7),
      rating: Color(0xFFFFC94A),
      favorite: Color(0xFFEF5350),
      playerOverlay: Color(0xCC000000),
      playerOverlayText: Color(0xFFFFFFFF),
    ),
  );

  // ── 现代白：纯净白底 + 中性灰阶 ──
  static const modernWhite = AppThemePreset(
    id: ThemePresetId.modernWhite,
    lightScheme: ColorScheme(
      brightness: Brightness.light,
      primary: Color(0xFF4E5EBA),
      onPrimary: Color(0xFFFFFFFF),
      primaryContainer: Color(0xFFDDE1FF),
      onPrimaryContainer: Color(0xFF001257),
      secondary: Color(0xFF5D5F72),
      onSecondary: Color(0xFFFFFFFF),
      secondaryContainer: Color(0xFFE2E1F9),
      onSecondaryContainer: Color(0xFF1A1B2C),
      tertiary: Color(0xFF7A4E86),
      onTertiary: Color(0xFFFFFFFF),
      tertiaryContainer: Color(0xFFFDD7FF),
      onTertiaryContainer: Color(0xFF2E0A38),
      error: Color(0xFFBA1A1A),
      onError: Color(0xFFFFFFFF),
      errorContainer: Color(0xFFFFDAD6),
      onErrorContainer: Color(0xFF410002),
      surface: Color(0xFFFFFFFF),
      onSurface: Color(0xFF1A1B21),
      surfaceContainerHighest: Color(0xFFE4E1EC),
      onSurfaceVariant: Color(0xFF46464F),
      outline: Color(0xFF777680),
      outlineVariant: Color(0xFFC7C5D0),
      scrim: Color(0xFF000000),
      inverseSurface: Color(0xFF2F3036),
      onInverseSurface: Color(0xFFF2F0F7),
      inversePrimary: Color(0xFFBAC3FF),
      surfaceTint: Color(0xFF4E5EBA),
    ),
    darkScheme: ColorScheme(
      brightness: Brightness.dark,
      primary: Color(0xFFBAC3FF),
      onPrimary: Color(0xFF1B2B8A),
      primaryContainer: Color(0xFF3646A1),
      onPrimaryContainer: Color(0xFFDDE1FF),
      secondary: Color(0xFFC5C4DD),
      onSecondary: Color(0xFF2F3042),
      secondaryContainer: Color(0xFF454659),
      onSecondaryContainer: Color(0xFFE2E1F9),
      tertiary: Color(0xFFE8B9F1),
      onTertiary: Color(0xFF482254),
      tertiaryContainer: Color(0xFF60376C),
      onTertiaryContainer: Color(0xFFFDD7FF),
      error: Color(0xFFFFB4AB),
      onError: Color(0xFF690005),
      errorContainer: Color(0xFF93000A),
      onErrorContainer: Color(0xFFFFDAD6),
      surface: Color(0xFF121318),
      onSurface: Color(0xFFE4E1EC),
      surfaceContainerHighest: Color(0xFF2F3036),
      onSurfaceVariant: Color(0xFFC7C5D0),
      outline: Color(0xFF91909A),
      outlineVariant: Color(0xFF46464F),
      scrim: Color(0xFF000000),
      inverseSurface: Color(0xFFE4E1EC),
      onInverseSurface: Color(0xFF2F3036),
      inversePrimary: Color(0xFF4E5EBA),
      surfaceTint: Color(0xFFBAC3FF),
    ),
    lightSemantic: AppSemanticColors(
      success: Color(0xFF2E7D32),
      warning: Color(0xFFEF6C00),
      info: Color(0xFF1565C0),
      rating: Color(0xFFF9A825),
      favorite: Color(0xFFD32F2F),
      playerOverlay: Color(0xCC000000),
      playerOverlayText: Color(0xFFFFFFFF),
    ),
    darkSemantic: AppSemanticColors(
      success: Color(0xFFA5D6A7),
      warning: Color(0xFFFFCC80),
      info: Color(0xFF90CAF9),
      rating: Color(0xFFFFE082),
      favorite: Color(0xFFEF9A9A),
      playerOverlay: Color(0xCC000000),
      playerOverlayText: Color(0xFFFFFFFF),
    ),
  );

  // ── 韵味紫：当前紫色 — 优雅紫调 ──
  static const currentPurple = AppThemePreset(
    id: ThemePresetId.currentPurple,
    lightScheme: ColorScheme(
      brightness: Brightness.light,
      primary: Color(0xFF7B4A9E),
      onPrimary: Color(0xFFFFFFFF),
      primaryContainer: Color(0xFFF0DBFF),
      onPrimaryContainer: Color(0xFF2D004E),
      secondary: Color(0xFF76527A),
      onSecondary: Color(0xFFFFFFFF),
      secondaryContainer: Color(0xFFFFD7F8),
      onSecondaryContainer: Color(0xFF2E1132),
      tertiary: Color(0xFF815252),
      onTertiary: Color(0xFFFFFFFF),
      tertiaryContainer: Color(0xFFFFDAD9),
      onTertiaryContainer: Color(0xFF331111),
      error: Color(0xFFBA1A1A),
      onError: Color(0xFFFFFFFF),
      errorContainer: Color(0xFFFFDAD6),
      onErrorContainer: Color(0xFF410002),
      surface: Color(0xFFFFF7FF),
      onSurface: Color(0xFF1F1A1F),
      surfaceContainerHighest: Color(0xFFEDE0EC),
      onSurfaceVariant: Color(0xFF4D444C),
      outline: Color(0xFF7E747E),
      outlineVariant: Color(0xFFD1C3D0),
      scrim: Color(0xFF000000),
      inverseSurface: Color(0xFF342F33),
      onInverseSurface: Color(0xFFF8EEF6),
      inversePrimary: Color(0xFFDCB8FF),
      surfaceTint: Color(0xFF7B4A9E),
    ),
    darkScheme: ColorScheme(
      brightness: Brightness.dark,
      primary: Color(0xFFDCB8FF),
      onPrimary: Color(0xFF461975),
      primaryContainer: Color(0xFF5F318E),
      onPrimaryContainer: Color(0xFFF0DBFF),
      secondary: Color(0xFFE0B4E3),
      onSecondary: Color(0xFF45264A),
      secondaryContainer: Color(0xFF5D3C61),
      onSecondaryContainer: Color(0xFFFFD7F8),
      tertiary: Color(0xFFF5B7B7),
      onTertiary: Color(0xFF4C2526),
      tertiaryContainer: Color(0xFF663B3C),
      onTertiaryContainer: Color(0xFFFFDAD9),
      error: Color(0xFFFFB4AB),
      onError: Color(0xFF690005),
      errorContainer: Color(0xFF93000A),
      onErrorContainer: Color(0xFFFFDAD6),
      surface: Color(0xFF17111A),
      onSurface: Color(0xFFF4EAF5),
      surfaceContainerHighest: Color(0xFF332F33),
      onSurfaceVariant: Color(0xFFCDBBCD),
      outline: Color(0xFF968790),
      outlineVariant: Color(0xFF4D444C),
      scrim: Color(0xFF000000),
      inverseSurface: Color(0xFFF4EAF5),
      onInverseSurface: Color(0xFF342F33),
      inversePrimary: Color(0xFF7B4A9E),
      surfaceTint: Color(0xFFDCB8FF),
    ),
    lightSemantic: AppSemanticColors(
      success: Color(0xFF2E7D32),
      warning: Color(0xFFE65100),
      info: Color(0xFF6A1B9A),
      rating: Color(0xFFFFB300),
      favorite: Color(0xFFAD1457),
      playerOverlay: Color(0xCC1A0E1F),
      playerOverlayText: Color(0xFFFFFFFF),
    ),
    darkSemantic: AppSemanticColors(
      success: Color(0xFF81C784),
      warning: Color(0xFFFFAB91),
      info: Color(0xFFCE93D8),
      rating: Color(0xFFFFD54F),
      favorite: Color(0xFFF48FB1),
      playerOverlay: Color(0xCC000000),
      playerOverlayText: Color(0xFFFFFFFF),
    ),
  );

  // ── 海洋蓝 ──
  static const ocean = AppThemePreset(
    id: ThemePresetId.ocean,
    lightScheme: ColorScheme(
      brightness: Brightness.light,
      primary: Color(0xFF006874),
      onPrimary: Color(0xFFFFFFFF),
      primaryContainer: Color(0xFF9EEFFD),
      onPrimaryContainer: Color(0xFF001F24),
      secondary: Color(0xFF4A6267),
      onSecondary: Color(0xFFFFFFFF),
      secondaryContainer: Color(0xFFCCE8ED),
      onSecondaryContainer: Color(0xFF051F23),
      tertiary: Color(0xFF525E7D),
      onTertiary: Color(0xFFFFFFFF),
      tertiaryContainer: Color(0xFFDAE2FF),
      onTertiaryContainer: Color(0xFF0E1B37),
      error: Color(0xFFBA1A1A),
      onError: Color(0xFFFFFFFF),
      errorContainer: Color(0xFFFFDAD6),
      onErrorContainer: Color(0xFF410002),
      surface: Color(0xFFF8FDFF),
      onSurface: Color(0xFF001F25),
      surfaceContainerHighest: Color(0xFFDEE3E6),
      onSurfaceVariant: Color(0xFF40484B),
      outline: Color(0xFF70787C),
      outlineVariant: Color(0xFFC0C8CB),
      scrim: Color(0xFF000000),
      inverseSurface: Color(0xFF2B3133),
      onInverseSurface: Color(0xFFEAF5F7),
      inversePrimary: Color(0xFF82D3E0),
      surfaceTint: Color(0xFF006874),
    ),
    darkScheme: ColorScheme(
      brightness: Brightness.dark,
      primary: Color(0xFF82D3E0),
      onPrimary: Color(0xFF00363D),
      primaryContainer: Color(0xFF004E58),
      onPrimaryContainer: Color(0xFF9EEFFD),
      secondary: Color(0xFFB0CCCF),
      onSecondary: Color(0xFF1B3438),
      secondaryContainer: Color(0xFF324A4E),
      onSecondaryContainer: Color(0xFFCCE8ED),
      tertiary: Color(0xFFBAC6EA),
      onTertiary: Color(0xFF24304D),
      tertiaryContainer: Color(0xFF3B4765),
      onTertiaryContainer: Color(0xFFDAE2FF),
      error: Color(0xFFFFB4AB),
      onError: Color(0xFF690005),
      errorContainer: Color(0xFF93000A),
      onErrorContainer: Color(0xFFFFDAD6),
      surface: Color(0xFF0A1F24),
      onSurface: Color(0xFFEAF5F7),
      surfaceContainerHighest: Color(0xFF2B3133),
      onSurfaceVariant: Color(0xFFC0C8CB),
      outline: Color(0xFF8A9295),
      outlineVariant: Color(0xFF40484B),
      scrim: Color(0xFF000000),
      inverseSurface: Color(0xFFEAF5F7),
      onInverseSurface: Color(0xFF2B3133),
      inversePrimary: Color(0xFF006874),
      surfaceTint: Color(0xFF82D3E0),
    ),
    lightSemantic: AppSemanticColors(
      success: Color(0xFF00695C),
      warning: Color(0xFFE65100),
      info: Color(0xFF0277BD),
      rating: Color(0xFFFF8F00),
      favorite: Color(0xFFC62828),
      playerOverlay: Color(0xCC001F24),
      playerOverlayText: Color(0xFFFFFFFF),
    ),
    darkSemantic: AppSemanticColors(
      success: Color(0xFF80CBC4),
      warning: Color(0xFFFFAB91),
      info: Color(0xFF81D4FA),
      rating: Color(0xFFFFCC02),
      favorite: Color(0xFFEF9A9A),
      playerOverlay: Color(0xCC000000),
      playerOverlayText: Color(0xFFFFFFFF),
    ),
  );

  // ── 森林绿 ──
  static const forest = AppThemePreset(
    id: ThemePresetId.forest,
    lightScheme: ColorScheme(
      brightness: Brightness.light,
      primary: Color(0xFF356859),
      onPrimary: Color(0xFFFFFFFF),
      primaryContainer: Color(0xFFB8F2DC),
      onPrimaryContainer: Color(0xFF002019),
      secondary: Color(0xFF4E6358),
      onSecondary: Color(0xFFFFFFFF),
      secondaryContainer: Color(0xFFD1E8DB),
      onSecondaryContainer: Color(0xFF0C1F16),
      tertiary: Color(0xFF3C6471),
      onTertiary: Color(0xFFFFFFFF),
      tertiaryContainer: Color(0xFFC0E9F8),
      onTertiaryContainer: Color(0xFF001F29),
      error: Color(0xFFBA1A1A),
      onError: Color(0xFFFFFFFF),
      errorContainer: Color(0xFFFFDAD6),
      onErrorContainer: Color(0xFF410002),
      surface: Color(0xFFFBFDF8),
      onSurface: Color(0xFF191C1A),
      surfaceContainerHighest: Color(0xFFDEE5DF),
      onSurfaceVariant: Color(0xFF404943),
      outline: Color(0xFF707973),
      outlineVariant: Color(0xFFC0C9C2),
      scrim: Color(0xFF000000),
      inverseSurface: Color(0xFF2E312F),
      onInverseSurface: Color(0xFFF0F1EC),
      inversePrimary: Color(0xFF9CD5C0),
      surfaceTint: Color(0xFF356859),
    ),
    darkScheme: ColorScheme(
      brightness: Brightness.dark,
      primary: Color(0xFF9CD5C0),
      onPrimary: Color(0xFF00382B),
      primaryContainer: Color(0xFF1D4F42),
      onPrimaryContainer: Color(0xFFB8F2DC),
      secondary: Color(0xFFB5CCBF),
      onSecondary: Color(0xFF21352B),
      secondaryContainer: Color(0xFF374B42),
      onSecondaryContainer: Color(0xFFD1E8DB),
      tertiary: Color(0xFFA4CCDB),
      onTertiary: Color(0xFF043542),
      tertiaryContainer: Color(0xFF234B59),
      onTertiaryContainer: Color(0xFFC0E9F8),
      error: Color(0xFFFFB4AB),
      onError: Color(0xFF690005),
      errorContainer: Color(0xFF93000A),
      onErrorContainer: Color(0xFFFFDAD6),
      surface: Color(0xFF0E1513),
      onSurface: Color(0xFFDEE5DF),
      surfaceContainerHighest: Color(0xFF2E312F),
      onSurfaceVariant: Color(0xFFC0C9C2),
      outline: Color(0xFF8A938D),
      outlineVariant: Color(0xFF404943),
      scrim: Color(0xFF000000),
      inverseSurface: Color(0xFFDEE5DF),
      onInverseSurface: Color(0xFF2E312F),
      inversePrimary: Color(0xFF356859),
      surfaceTint: Color(0xFF9CD5C0),
    ),
    lightSemantic: AppSemanticColors(
      success: Color(0xFF2E7D32),
      warning: Color(0xFFF57F17),
      info: Color(0xFF00695C),
      rating: Color(0xFFFF8F00),
      favorite: Color(0xFF6A1B1A),
      playerOverlay: Color(0xCC0E1513),
      playerOverlayText: Color(0xFFFFFFFF),
    ),
    darkSemantic: AppSemanticColors(
      success: Color(0xFFA5D6A7),
      warning: Color(0xFFFFE082),
      info: Color(0xFF80CBC4),
      rating: Color(0xFFFFCC02),
      favorite: Color(0xFFEF9A9A),
      playerOverlay: Color(0xCC000000),
      playerOverlayText: Color(0xFFFFFFFF),
    ),
  );

  static const List<AppThemePreset> all = [
    modernBlack,
    modernWhite,
    currentPurple,
    ocean,
    forest,
  ];

  static AppThemePreset byId(String? id) {
    return all.firstWhere(
      (e) => e.id.id == id,
      orElse: () => currentPurple,
    );
  }
}
