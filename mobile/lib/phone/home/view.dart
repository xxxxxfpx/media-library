import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'home.dart';
import 'media.dart';
import 'my.dart';
import '../../services/sync_service.dart';

enum HomeTab {
  home('首页', Icons.home_outlined),
  media('媒体', Icons.movie_outlined),
  my('我的', Icons.person_outlined);

  final String name;
  final IconData icon;
  const HomeTab(this.name, this.icon);

  static const double itemWidth = 66;
}

class HomePagePhone extends ConsumerStatefulWidget {
  const HomePagePhone({super.key});

  @override
  ConsumerState<HomePagePhone> createState() => _HomePagePhoneState();
}

class _HomePagePhoneState extends ConsumerState<HomePagePhone> {
  HomeTab _currentTab = HomeTab.home;
  bool _isNavBarHidden = false;

  static const _navBarHideDuration = Duration(milliseconds: 300);
  static const _containerDuration = Duration(milliseconds: 200);
  static const _indicatorDuration = Duration(milliseconds: 130);
  static const _bottomBarHeight = 42.0;
  static final _tabCount = HomeTab.values.length;

  @override
  void initState() {
    super.initState();
    SyncService().start(ref);
  }

  bool _handleScrollNotification(ScrollNotification notification) {
    if (notification.metrics.axis != Axis.vertical) return false;
    
    if (notification is UserScrollNotification) {
      final direction = notification.direction;
      if (direction == ScrollDirection.reverse && !_isNavBarHidden) {
        setState(() => _isNavBarHidden = true);
      } else if (direction == ScrollDirection.forward && _isNavBarHidden) {
        setState(() => _isNavBarHidden = false);
      }
    } else if (notification is ScrollEndNotification) {
      final pixels = notification.metrics.pixels;
      final maxScroll = notification.metrics.maxScrollExtent;
      if (pixels >= maxScroll - 1 && _isNavBarHidden) {
        setState(() => _isNavBarHidden = false);
      }
    }
    return false;
  }

  @override
  Widget build(BuildContext context) {
    return ColoredBox(
      color: Theme.of(context).colorScheme.surface,
      child: Stack(
        children: [
          NotificationListener<ScrollNotification>(
            onNotification: _handleScrollNotification,
            child: SafeArea(
              top: true,
              bottom: false,
              child: IndexedStack(
                index: _currentTab.index,
                children: const [HomeTabHome(), HomeTabMedia(), HomeTabMy()],
              ),
            ),
          ),
          _buildBottomBar(),
        ],
      ),
    );
  }

  Widget _buildBottomBar() {
    final barWidth = HomeTab.itemWidth * _tabCount;
    final indicatorLeft = _currentTab.index * HomeTab.itemWidth;
    
    return Positioned(
      bottom: 0,
      left: 0,
      right: 0,
      child: AnimatedSlide(
        duration: _navBarHideDuration,
        offset: _isNavBarHidden ? const Offset(0, 1.5) : Offset.zero,
        child: AnimatedContainer(
          duration: _containerDuration,
          margin: const EdgeInsets.only(bottom: 32),
          child: Center(
            child: Stack(
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(44),
                  child: BackdropFilter(
                    filter: ImageFilter.blur(sigmaX: 8, sigmaY: 8),
                    child: Container(
                      height: _bottomBarHeight,
                      width: barWidth,
                      color: Colors.black.withValues(alpha: 0.25),
                    ),
                  ),
                ),
                AnimatedContainer(
                  duration: _indicatorDuration,
                  margin: EdgeInsets.only(left: indicatorLeft),
                  child: Container(
                    height: _bottomBarHeight,
                    width: HomeTab.itemWidth,
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.76),
                      borderRadius: BorderRadius.circular(44),
                    ),
                  ),
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  mainAxisSize: MainAxisSize.min,
                  children: HomeTab.values.map((tab) {
                    return _NavItem(
                      icon: tab.icon,
                      label: tab,
                      isSelected: _currentTab == tab,
                      onTap: () => setState(() {
                        _currentTab = tab;
                        _isNavBarHidden = false;
                      }),
                    );
                  }).toList(),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _NavItem extends StatelessWidget {
  final IconData icon;
  final HomeTab label;
  final bool isSelected;
  final VoidCallback onTap;

  const _NavItem({
    required this.icon,
    required this.label,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final navItemColor = Theme.of(context).colorScheme.onPrimary;
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: HomeTab.itemWidth,
        padding: const EdgeInsets.symmetric(vertical: 3),
        decoration: BoxDecoration(borderRadius: BorderRadius.circular(44)),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              color: isSelected
                  ? navItemColor
                  : navItemColor.withValues(alpha: 0.5),
              size: 22,
            ),
            Text(
              label.name,
              style: TextStyle(
                color: isSelected
                    ? navItemColor
                    : navItemColor.withValues(alpha: 0.5),
                fontSize: 11,
                height: 1,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
