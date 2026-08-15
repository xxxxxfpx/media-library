// 登录流程页面：显示登录 UI + 加载遮罩
import 'package:flutter/material.dart';
import 'login_page.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Stack(
      children: [
        LoginPage(onLoginSuccess: () {}),
        if (_isLoading)
          Container(
            color: cs.surface.withValues(alpha: 0.3),
            child: Center(child: CircularProgressIndicator(color: cs.primary)),
          ),
      ],
    );
  }
}
