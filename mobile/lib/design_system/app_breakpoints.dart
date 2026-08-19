import 'package:flutter/widgets.dart';

/// 响应式断点
enum AppBreakpoint {
  compact,
  medium,
  expanded,
  large,
}

abstract class AppBreakpoints {
  static const double compactMax = 599;
  static const double mediumMin = 600;
  static const double mediumMax = 839;
  static const double expandedMin = 840;
  static const double expandedMax = 1199;
  static const double largeMin = 1200;

  static const double contentMaxWidth = 1200;
  static const double detailMaxWidth = 960;

  static AppBreakpoint of(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    return ofWidth(width);
  }

  static AppBreakpoint ofWidth(double width) {
    if (width >= largeMin) return AppBreakpoint.large;
    if (width >= expandedMin) return AppBreakpoint.expanded;
    if (width >= mediumMin) return AppBreakpoint.medium;
    return AppBreakpoint.compact;
  }

  static bool isCompact(BuildContext context) =>
      of(context) == AppBreakpoint.compact;
  static bool isMedium(BuildContext context) =>
      of(context) == AppBreakpoint.medium;
  static bool isExpanded(BuildContext context) =>
      of(context) == AppBreakpoint.expanded;
  static bool isLarge(BuildContext context) =>
      of(context) == AppBreakpoint.large;

  static bool isAtLeastMedium(BuildContext context) =>
      MediaQuery.of(context).size.width >= mediumMin;
  static bool isAtLeastExpanded(BuildContext context) =>
      MediaQuery.of(context).size.width >= expandedMin;
}
