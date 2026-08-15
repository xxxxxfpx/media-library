import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_lucide/flutter_lucide.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../component/horizontal_media_section.dart';
import '../../core/constants.dart';
import '../../data/api/api_client.dart';
import '../../data/api/media_api.dart';
import '../../data/models/media.dart';
import '../grid_view.dart';

class HomeTabMedia extends StatefulWidget {
  const HomeTabMedia({super.key});

  @override
  State<HomeTabMedia> createState() => _HomeTabMediaState();
}

class _HomeTabMediaState extends State<HomeTabMedia> {
  final TextEditingController _searchController = TextEditingController();
  final Completer<void> _apiReady = Completer<void>();
  MediaApi? _mediaApi;
  int _refreshKey = 0;

  @override
  void initState() {
    super.initState();
    _initApi();
  }

  Future<void> _initApi() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);
      _mediaApi = MediaApi(client);
    } catch (_) {
    }
    _apiReady.complete();
    if (mounted) setState(() {});
  }

  Future<void> _onRefresh() async {
    setState(() => _refreshKey++);
    // 等待各 section 完成数据重新加载
    await Future.delayed(const Duration(milliseconds: 300));
  }

  Future<MediaListResponse> _fetch(Future<MediaListResponse> Function(MediaApi) call, int offset, int limit) async {
    await _apiReady.future;
    return call(_mediaApi!);
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: _onRefresh,
      color: Theme.of(context).colorScheme.primary,
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: const EdgeInsets.only(top: 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: _buildSearchBar(),
            ),
            const SizedBox(height: 24),
            HorizontalMediaSection(
              key: ValueKey('recent_$_refreshKey'),
              title: '最近添加',
              contentPadding: const EdgeInsets.symmetric(horizontal: 16),
              request: const MediaListRequest(),
              fetchData: (offset, limit) => _fetch((api) => api.getList(const MediaListRequest(), limit: limit, offset: offset), offset, limit),
              onViewAll: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const MediaGridPage(initialRequest: MediaListRequest())),
              ),
            ),
            const SizedBox(height: 24),
            HorizontalMediaSection(
              key: ValueKey('library_$_refreshKey'),
              title: '我的媒体库',
              contentPadding: const EdgeInsets.symmetric(horizontal: 16),
              request: const MediaListRequest(types: {MediaType.Source}),
              fetchData: (offset, limit) => _fetch((api) => api.getList(const MediaListRequest(types: {MediaType.Source}), limit: limit, offset: offset), offset, limit),
              onViewAll: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => MediaGridPage(initialRequest: const MediaListRequest(types: {MediaType.Source}))),
              ),
            ),
            const SizedBox(height: 24),
            HorizontalMediaSection(
              key: ValueKey('favorite_$_refreshKey'),
              title: '我的收藏',
              contentPadding: const EdgeInsets.symmetric(horizontal: 16),
              request: const MediaListRequest(favorite: true, sortBy: 'favorited_at'),
              fetchData: (offset, limit) => _fetch((api) => api.getList(const MediaListRequest(favorite: true, sortBy: 'favorited_at'), limit: limit, offset: offset), offset, limit),
              onViewAll: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => MediaGridPage(initialRequest: const MediaListRequest(favorite: true, sortBy: 'favorited_at'))),
              ),
            ),
            const SizedBox(height: 24),
            HorizontalMediaSection(
              key: ValueKey('history_$_refreshKey'),
              title: '观看记录',
              contentPadding: const EdgeInsets.symmetric(horizontal: 16),
              request: const MediaListRequest(hasPlayback: true, sortBy: 'last_played'),
              fetchData: (offset, limit) => _fetch((api) => api.getList(const MediaListRequest(hasPlayback: true, sortBy: 'last_played'), limit: limit, offset: offset), offset, limit),
              onViewAll: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => MediaGridPage(initialRequest: const MediaListRequest(hasPlayback: true, sortBy: 'last_played'))),
              ),
            ),
            const SizedBox(height: 24),
            HorizontalMediaSection(
              key: ValueKey('user_rating_$_refreshKey'),
              title: '我的评分',
              contentPadding: const EdgeInsets.symmetric(horizontal: 16),
              request: const MediaListRequest(hasRating: true, sortBy: 'user_rating'),
              fetchData: (offset, limit) => _fetch((api) => api.getList(const MediaListRequest(hasRating: true, sortBy: 'user_rating'), limit: limit, offset: offset), offset, limit),
              onViewAll: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => MediaGridPage(initialRequest: const MediaListRequest(hasRating: true, sortBy: 'user_rating'))),
              ),
            ),
            const SizedBox(height: 80),
          ],
        ),
      ),
    );
  }

  Widget _buildSearchBar() {
    final cs = Theme.of(context).colorScheme;
    return Material(
      color: Colors.transparent,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: cs.surfaceContainerHighest.withValues(alpha: 0.5),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: cs.outlineVariant.withValues(alpha: 0.5)),
        ),
        child: Row(
          children: [
            const Padding(
              padding: EdgeInsets.only(left: 4),
              child: Icon(LucideIcons.search, size: 20),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: TextField(
                controller: _searchController,
                style: const TextStyle(fontSize: 14),
                decoration: const InputDecoration(
                  hintText: '搜索媒体...',
                  border: InputBorder.none,
                  isDense: true,
                  contentPadding: EdgeInsets.zero,
                ),
                onSubmitted: (value) {
                  if (value.isNotEmpty) {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => MediaGridPage(
                          initialRequest: MediaListRequest(search: value),
                        ),
                      ),
                    );
                  }
                },
                onChanged: (_) => setState(() {}),
              ),
            ),
            if (_searchController.text.isNotEmpty)
              GestureDetector(
                onTap: () {
                  _searchController.clear();
                  setState(() {});
                },
                child: const Padding(
                  padding: EdgeInsets.only(right: 4),
                  child: Icon(LucideIcons.x, size: 16),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
