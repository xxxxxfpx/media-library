// 登录页面入口，根据屏幕宽度自动切换手机/桌面布局
import 'package:flutter/material.dart';
import 'login_phone.dart';
import 'login_windows.dart';

class LoginPage extends StatelessWidget {
  final VoidCallback? onLoginSuccess;

  const LoginPage({super.key, this.onLoginSuccess});

  static const double _breakpoint = 600;

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth >= _breakpoint) {
          return LoginPageWindows(onLoginSuccess: onLoginSuccess);
        }
        return LoginPagePhone(onLoginSuccess: onLoginSuccess);
      },
    );
  }
}
