// 登录流程页面：显示登录 UI + 加载遮罩
import 'package:flutter/material.dart';
import 'login_page.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Stack(children: [LoginPage()]);
  }
}
