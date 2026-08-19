import 'package:flutter/material.dart';
import '../phone/home/home_shell.dart';

/// 桌面端首页 — 复用自适应 HomeShell，避免与手机端双重维护数据逻辑
class HomePageWindows extends StatelessWidget {
  const HomePageWindows({super.key});

  @override
  Widget build(BuildContext context) {
    return const HomeShell();
  }
}
