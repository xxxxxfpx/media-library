import 'package:flutter/material.dart';

/// 统一动效 Token — 遵循 Material Motion
abstract class AppMotion {
  static const Duration fast = Duration(milliseconds: 140);
  static const Duration normal = Duration(milliseconds: 220);
  static const Duration slow = Duration(milliseconds: 340);
  static const Duration extraSlow = Duration(milliseconds: 480);

  static const Curve emphasized = Curves.easeOutCubic;
  static const Curve emphasizedDecelerate = Cubic(0.05, 0.7, 0.1, 1.0);
  static const Curve emphasizedAccelerate = Cubic(0.3, 0.0, 0.8, 0.15);
  static const Curve standard = Curves.easeInOutCubic;
  static const Curve entrance = Curves.easeOut;

  /// 是否应减少动画
  static bool shouldReduceMotion(BuildContext context) {
    return MediaQuery.of(context).disableAnimations;
  }

  static Duration effective(
    BuildContext context,
    Duration duration,
  ) {
    return shouldReduceMotion(context) ? Duration.zero : duration;
  }
}
