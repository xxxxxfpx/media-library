# 移动端主题系统

## 概述
本阶段已实现完整的主题预设系统，满足现代黑、现代白、韵味紫必选 + 扩展海洋蓝、森林绿。

## 设计系统位置
`mobile/lib/design_system/`:
- `app_color_tokens.dart` — `ThemePresetId` / `AppSemanticColors` / `AppThemePresets`（5套完整 ColorScheme）
- `app_theme.dart` — `AppTheme.light/dark/fromMode` 统一构建 `ThemeData`
- `app_spacing.dart` — 4dp基线间距
- `app_radius.dart` — 统一圆角
- `app_motion.dart` — 动效 Token，支持 `MediaQuery.disableAnimations`
- `app_breakpoints.dart` — 响应式断点
- `app_icons.dart` — Material 图标语义映射（已移除 Lucide 依赖）
- `app_semantics.dart` — 无障碍辅助

## 色彩系统
每个预设包含 `lightScheme` + `darkScheme` + `lightSemantic` + `darkSemantic`，覆盖：
- Material `ColorScheme` 全部角色
- 业务语义色：`success/warning/info/rating/favorite/playerOverlay`

必选主题：
- **现代黑** `#B9C4FF` — 深邃黑底
- **现代白** `#4E5EBA` — 纯净白底
- **韵味紫** `#7B4A9E/#DCB8FF` — 现有紫色兼容基准

## 主题切换实现
- 设置存储：`UserSetting.themePreset` + `themeMode`，通过 `SettingsNotifier` 持久化到 `SharedPreferences:user_settings_json` 并同步云端 `/api/user/setting`
- 应用层：`main.dart:MyApp` 监听 `settingsProvider`，通过 `ThemePresetId.fromId` 解析预设，`AppTheme.toThemeMode` 解析亮色模式，使用 `MaterialApp.theme/darkTheme`
- 兼容：旧数据无 `theme_preset` 时回退 `currentPurple`，并兼容 `primary_color` 映射
- 后端：`backend/app/schemas/setting.py:UserSettings.theme_preset` 新增，无需 DB 迁移（JSON字段）

## 颜色管理要求
- 页面禁止硬编码 `Colors.*` / `Color(0x...)`，仅允许在 `design_system/` 定义
- 已迁移：`component/media_card.dart` 使用 `context.semantic.rating` 和 `cs.scrim`，`core/constants.dart` 使用 `AppIcons`

## 验证
- `flutter analyze` 无新增错误
- `flutter test` 63/63 通过
- 后端 `pytest tests/test_user_api.py` 13/13 通过
