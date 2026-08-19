// 登录表单 UI 组件
import 'package:flutter/material.dart';
import '../../core/auth_service.dart';
import '../../core/app_logger.dart';
import '../home/home_shell.dart';

Widget buildGlowIcon(BuildContext context) {
  final primary = Theme.of(context).colorScheme.primary;
  return Container(
    decoration: BoxDecoration(
      shape: BoxShape.circle,
      boxShadow: [
        BoxShadow(
          color: primary.withValues(alpha: 0.5),
          blurRadius: 40,
          spreadRadius: 10,
        ),
        BoxShadow(
          color: primary.withValues(alpha: 0.3),
          blurRadius: 80,
          spreadRadius: 20,
        ),
      ],
    ),
    child: Icon(Icons.video_library_rounded, size: 100, color: primary),
  );
}

Widget buildLoginForm({
  required BuildContext context,
  TextAlign textAlign = TextAlign.start,
  VoidCallback? onLoginSuccess,
}) {
  final usernameCtrl = TextEditingController();
  final passwordCtrl = TextEditingController();
  final cs = Theme.of(context).colorScheme;
  final primary = cs.primary;

  return Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      Text(
        '欢迎回来',
        style: TextStyle(
          fontSize: 28,
          fontWeight: FontWeight.bold,
          color: cs.onSurface,
        ),
        textAlign: textAlign,
      ),
      const SizedBox(height: 8),
      Text(
        '请登录您的账号',
        style: TextStyle(fontSize: 14, color: cs.onSurfaceVariant),
        textAlign: textAlign,
      ),
      const SizedBox(height: 40),
      TextField(
        controller: usernameCtrl,
        style: TextStyle(color: cs.onSurface),
        decoration: InputDecoration(
          labelText: '用户名',
          labelStyle: TextStyle(color: cs.onSurfaceVariant),
          prefixIcon: Icon(Icons.person, color: cs.onSurfaceVariant),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: cs.outlineVariant),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: primary),
          ),
        ),
      ),
      const SizedBox(height: 20),
      TextField(
        controller: passwordCtrl,
        obscureText: true,
        style: TextStyle(color: cs.onSurface),
        decoration: InputDecoration(
          labelText: '密码',
          labelStyle: TextStyle(color: cs.onSurfaceVariant),
          prefixIcon: Icon(Icons.lock, color: cs.onSurfaceVariant),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: cs.outlineVariant),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: primary),
          ),
        ),
      ),
      const SizedBox(height: 32),
      FilledButton(
        onPressed: () async {
          final username = usernameCtrl.text;
          final password = passwordCtrl.text;

          if (username.isEmpty || password.isEmpty) {
            if (context.mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('请输入用户名和密码'), backgroundColor: cs.error),
              );
            }
            return;
          }

          try {
            AppLogger.info('login_submitted', category: 'ui');
            await AuthService().login(username: username, password: password);
            if (context.mounted) {
              onLoginSuccess?.call();
              if (context.mounted) {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (_) => const HomeShell()),
                );
              }
            }
          } catch (_) {
            if (context.mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: const Text('登录失败，请检查账号或服务器连接'),
                  backgroundColor: cs.error,
                ),
              );
            }
          }
        },
        style: FilledButton.styleFrom(
          minimumSize: const Size(double.infinity, 50),
        ),
        child: const Text(
          '登录',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
    ],
  );
}
