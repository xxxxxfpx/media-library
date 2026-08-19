import 'package:flutter/material.dart';

/// 无障碍语义辅助
abstract class AppSemantics {
  static Widget iconButton({
    required String label,
    required VoidCallback? onPressed,
    required Widget icon,
    String? tooltip,
  }) {
    return Semantics(
      button: true,
      label: label,
      child: IconButton(
        onPressed: onPressed,
        icon: icon,
        tooltip: tooltip ?? label,
      ),
    );
  }

  static const double minTouchTarget = 44;
}
