import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/models/media.dart';
import '../core/app_logger.dart';
import '../providers/settings_provider.dart';
import 'media_card.dart';

/// 区块标题组件
class SectionHeader extends StatelessWidget {
  final String title;
  final VoidCallback? onViewAll;

  const SectionHeader({super.key, required this.title, this.onViewAll});

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return GestureDetector(
      onTap: onViewAll,
      child: Row(
        children: [
          Text(
            title,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const SizedBox(width: 4),
          Icon(
            Icons.chevron_right,
            size: 20,
            color: onViewAll != null ? cs.onSurface : cs.onSurfaceVariant,
          ),
        ],
      ),
    );
  }
}

/// 横向滚动媒体列表（带无限加载和自动重试）
class HorizontalMediaSection extends ConsumerStatefulWidget {
  final String title;
  final VoidCallback? onViewAll;
  final double itemWidth;
  final double itemHeight;
  final Future<MediaListResponse> Function(int offset, int limit) fetchData;
  final int pageSize;
  final EdgeInsetsGeometry? contentPadding;

  const HorizontalMediaSection({
    super.key,
    required this.title,
    required this.fetchData,
    this.onViewAll,
    this.itemWidth = 120,
    this.itemHeight = 220,
    this.pageSize = 30,
    this.contentPadding,
  });

  @override
  ConsumerState<HorizontalMediaSection> createState() =>
      _HorizontalMediaSectionState();
}

class _HorizontalMediaSectionState
    extends ConsumerState<HorizontalMediaSection> {
  final ScrollController _scrollController = ScrollController();
  List<MediaItem> _items = [];
  bool _isLoading = false;
  bool _hasMore = true;
  bool _isError = false;
  int _offset = 0;
  double _pullOffset = 0.0; // 当前拉动距离
  bool _willRefreshOnRelease = false; // 松手时是否刷新
  Timer? _retryTimer;
  int _retryCount = 0;
  // 无限重试模式

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
    _loadData(reset: true);
  }

  @override
  void dispose() {
    _retryTimer?.cancel();
    _scrollController.removeListener(_onScroll);
    _scrollController.dispose();
    super.dispose();
  }

  void _scheduleRetry() {
    // 从设置中获取重试间隔
    final retryInterval = ref.getMediaRetryInterval();

    _retryTimer?.cancel();
    _retryTimer = Timer(Duration(seconds: retryInterval), () {
      if (mounted && _isError) {
        _retryCount++;
        _loadData(reset: true);
      }
    });
  }

  Future<void> _loadData({required bool reset}) async {
    if (_isLoading) return;
    if (!reset && !_hasMore) return;

    setState(() {
      _isLoading = true;
      if (reset) {
        _isError = false;
        _retryCount = 0;
      }
    });

    try {
      final response = await widget.fetchData(
        reset ? 0 : _offset,
        widget.pageSize,
      );
      if (!mounted) return;
      setState(() {
        if (reset) {
          _items = response.items;
        } else {
          _items.addAll(response.items);
        }
        _offset = _items.length;
        _hasMore = _offset < response.total;
      });
    } catch (error, stackTrace) {
      final nextRetry = _retryCount + 1;
      if (nextRetry == 1 || nextRetry % 10 == 0) {
        AppLogger.warning(
          'media_section_load_failed',
          error: error,
          stackTrace: stackTrace,
          category: 'media',
          fields: {'section': widget.title, 'retry_count': nextRetry},
        );
      }
      if (!mounted) return;
      setState(() {
        _isError = true;
        if (reset) _items = [];
      });
      // 加载失败，安排自动重试
      _scheduleRetry();
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  bool _onPullRefreshNotification(ScrollNotification notification) {
    if (notification is ScrollUpdateNotification) {
      final pixels = notification.metrics.pixels;
      if (pixels < 0) {
        final currentPull = pixels.abs();
        setState(() {
          _pullOffset = currentPull;
          if (currentPull >= 50) {
            _willRefreshOnRelease = true;
          } else if (currentPull < 30) {
            _willRefreshOnRelease = false;
          }
        });
      }
      return false;
    }

    return false;
  }

  void _onScroll() {
    if (_isLoading || !_hasMore) return;
    if (!_scrollController.hasClients) return;

    final maxScroll = _scrollController.position.maxScrollExtent;
    final currentScroll = _scrollController.position.pixels;
    if (currentScroll >= maxScroll - 200) {
      _loadData(reset: false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: widget.contentPadding ?? EdgeInsets.zero,
          child: SectionHeader(
            title: widget.title,
            onViewAll: widget.onViewAll,
          ),
        ),
        const SizedBox(height: 12),
        _buildBody(),
      ],
    );
  }

  Widget _buildBody() {
    final cs = Theme.of(context).colorScheme;
    if (_items.isEmpty && _isError) {
      return GestureDetector(
        onTap: () {
          _retryTimer?.cancel();
          _retryCount = 0;
          _loadData(reset: true);
        },
        child: Container(
          height: widget.itemHeight,
          decoration: BoxDecoration(
            color: cs.surfaceContainerHighest.withValues(alpha: 0.3),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (_retryTimer != null) ...[
                SizedBox(
                  width: 24,
                  height: 24,
                  child: CircularProgressIndicator(strokeWidth: 2),
                ),
                const SizedBox(height: 8),
              ],
              Text(
                _retryTimer != null ? '加载失败，自动重试中...' : '加载失败，点击重试',
                style: TextStyle(color: cs.onSurfaceVariant),
              ),
              if (_retryCount > 0) ...[
                const SizedBox(height: 4),
                Text(
                  '已重试 $_retryCount 次',
                  style: TextStyle(color: cs.onSurfaceVariant, fontSize: 12),
                ),
              ],
            ],
          ),
        ),
      );
    }

    if (_items.isEmpty && _isLoading) {
      return SizedBox(
        height: widget.itemHeight,
        child: const Center(child: CircularProgressIndicator()),
      );
    }

    if (_items.isEmpty) {
      return GestureDetector(
        onTap: () => _loadData(reset: true),
        child: Container(
          height: widget.itemHeight,
          decoration: BoxDecoration(
            color: cs.surfaceContainerHighest.withValues(alpha: 0.3),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Center(
            child: Text(
              '暂无内容，点击刷新',
              style: TextStyle(color: cs.onSurfaceVariant),
            ),
          ),
        ),
      );
    }

    return SizedBox(
      height: widget.itemHeight,
      child: Listener(
        onPointerUp: (_) {
          // 触摸结束，检查是否应该刷新
          if (_willRefreshOnRelease) {
            _loadData(reset: true);
          }
          setState(() {
            _willRefreshOnRelease = false;
            _pullOffset = 0.0;
          });
        },
        child: NotificationListener<ScrollNotification>(
          onNotification: _onPullRefreshNotification,
          child: Stack(
            alignment: Alignment.centerLeft,
            children: [
              ListView.separated(
                controller: _scrollController,
                scrollDirection: Axis.horizontal,
                physics: const AlwaysScrollableScrollPhysics(
                  parent: BouncingScrollPhysics(),
                ),
                padding: widget.contentPadding,
                itemCount: _items.length + (_isLoading ? 1 : 0),
                separatorBuilder: (_, _) => const SizedBox(width: 12),
                itemBuilder: (context, index) {
                  if (index == _items.length) {
                    return const SizedBox(
                      width: 40,
                      child: Center(
                        child: SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        ),
                      ),
                    );
                  }
                  return SizedBox(
                    width: widget.itemWidth,
                    child: MediaCard(
                      media: _items[index],
                      config: const CardConfig(),
                    ),
                  );
                },
              ),
              // 右拉刷新指示器
              if (_willRefreshOnRelease || _pullOffset > 0)
                Positioned(
                  left: 8,
                  child: AnimatedOpacity(
                    opacity: (_pullOffset / 50).clamp(0.0, 1.0),
                    duration: const Duration(milliseconds: 200),
                    child: Container(
                      width: 40,
                      height: 40,
                      decoration: BoxDecoration(
                        color: cs.primary.withValues(alpha: 0.8),
                        shape: BoxShape.circle,
                      ),
                      child: Center(
                        child: _willRefreshOnRelease
                            ? SizedBox(
                                width: 20,
                                height: 20,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  color: cs.onPrimary,
                                ),
                              )
                            : Icon(
                                Icons.arrow_back,
                                color: cs.onPrimary,
                                size: 20,
                              ),
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
