// 手机端登录页面
import 'package:flutter/material.dart';
import 'login_form.dart';

class LoginPagePhone extends StatelessWidget {
  final VoidCallback? onLoginSuccess;

  const LoginPagePhone({super.key, this.onLoginSuccess});

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Scaffold(
      backgroundColor: cs.surface,
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 32),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const SizedBox(height: 60),
                buildGlowIcon(context),
                const SizedBox(height: 60),
                buildLoginForm(
                  context: context,
                  textAlign: TextAlign.center,
                  onLoginSuccess: onLoginSuccess,
                ),
                const SizedBox(height: 60),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
