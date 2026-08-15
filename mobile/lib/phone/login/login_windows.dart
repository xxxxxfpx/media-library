// 桌面端登录页面
import 'package:flutter/material.dart';
import 'login_form.dart';

class LoginPageWindows extends StatelessWidget {
  final VoidCallback? onLoginSuccess;

  const LoginPageWindows({super.key, this.onLoginSuccess});

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Scaffold(
      backgroundColor: cs.surface,
      body: Row(
        children: [
          Expanded(
            flex: 3,
            child: Center(child: buildGlowIcon(context)),
          ),
          Expanded(
            flex: 2,
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 24),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  buildLoginForm(context: context, onLoginSuccess: onLoginSuccess),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
