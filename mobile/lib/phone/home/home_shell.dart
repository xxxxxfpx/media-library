import 'package:flutter/material.dart';
import '../../design_system/app_breakpoints.dart';
import '../../design_system/app_icons.dart';
import '../../design_system/app_spacing.dart';
import 'home.dart';
import 'media.dart';
import 'my.dart';

enum HomeTab {
  home('首页', AppIcons.home),
  media('媒体', AppIcons.media),
  my('我的', AppIcons.my);

  final String label;
  final IconData icon;
  const HomeTab(this.label, this.icon);
}

/// 自适应首页壳 — 手机使用 NavigationBar，>=600dp 使用 NavigationRail
class HomeShell extends StatefulWidget {
  const HomeShell({super.key});

  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> {
  HomeTab _current = HomeTab.home;

  @override
  Widget build(BuildContext context) {
    final breakpoint = AppBreakpoints.of(context);
    final isLarge = breakpoint == AppBreakpoint.medium ||
        breakpoint == AppBreakpoint.expanded ||
        breakpoint == AppBreakpoint.large;

    final content = IndexedStack(
      index: _current.index,
      children: const [
        HomeTabHome(),
        HomeTabMedia(),
        HomeTabMy(),
      ],
    );

    if (isLarge) {
      return Scaffold(
        body: Row(
          children: [
            NavigationRail(
              selectedIndex: _current.index,
              onDestinationSelected: (i) =>
                  setState(() => _current = HomeTab.values[i]),
              labelType: NavigationRailLabelType.all,
              destinations: HomeTab.values
                  .map(
                    (t) => NavigationRailDestination(
                      icon: Icon(t.icon),
                      selectedIcon: Icon(t.icon),
                      label: Text(t.label),
                    ),
                  )
                  .toList(),
            ),
            const VerticalDivider(width: 1),
            Expanded(
              child: Center(
                child: ConstrainedBox(
                  constraints: const BoxConstraints(
                    maxWidth: AppSpacing.contentMaxWidth,
                  ),
                  child: content,
                ),
              ),
            ),
          ],
        ),
      );
    }

    // Compact — 复用原有底部导航逻辑的简化版本
    return Scaffold(
      body: SafeArea(child: content),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _current.index,
        onDestinationSelected: (i) =>
            setState(() => _current = HomeTab.values[i]),
        destinations: HomeTab.values
            .map(
              (t) => NavigationDestination(
                icon: Icon(t.icon),
                label: t.label,
              ),
            )
            .toList(),
      ),
    );
  }
}
