import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_lucide/flutter_lucide.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../data/api/api_client.dart';
import '../data/api/media_api.dart';
import '../data/models/media.dart';
import '../core/constants.dart';
import '../core/app_logger.dart';
import '../component/media_card.dart';

class MediaGridPage extends StatefulWidget {
  final MediaListRequest? initialRequest;

  const MediaGridPage({super.key, this.initialRequest});

  @override
  State<MediaGridPage> createState() => _MediaGridPageState();
}

class _MediaGridPageState extends State<MediaGridPage> {
  final Completer<void> _apiReady = Completer<void>();
  final ScrollController _scrollCtrl = ScrollController();
  final TextEditingController _searchCtrl = TextEditingController();
  final FocusNode _searchFocus = FocusNode();

  MediaApi? _mediaApi;

  final List<MediaItem> _items = [];
  int _totalCount = 0;
  int _offset = 0;
  bool _isLoading = false;
  bool _hasMore = true;
  bool _isInitialLoading = true;

  bool _showSearch = false;
  String _sortBy = 'date_created';
  final Set<MediaType> _selectedTypes = {};
  bool _showTypeSelector = false;

  bool _favorite = false;
  bool _hasPlayback = false;
  String? _itemIds;
  String? _linkedItemIds;
  bool _suppressSearchCallback = false;

  static const int _pageSize = 60;

  static const _sortOptions = <(String, String, IconData)>[
    ('date_created', '添加时间', LucideIcons.calendar),
    ('name', '名称', LucideIcons.arrow_up_a_z),
    ('production_year', '年份', LucideIcons.calendar_days),
    ('community_rating', '评分', LucideIcons.star),
    ('premiere_date', '发布日期', LucideIcons.calendar_check),
  ];

  static const _allTypes = [
    MediaType.Movie,
    MediaType.Series,
    MediaType.Season,
    MediaType.Episode,
    MediaType.Audio,
    MediaType.Photo,
    MediaType.Book,
    MediaType.Person,
    MediaType.Source,
    MediaType.Studio,
    MediaType.Genre,
    MediaType.Tag,
    MediaType.BoxSet,
  ];

  @override
  void initState() {
    super.initState();
    _scrollCtrl.addListener(_onScroll);
    _initFromRequest();
    _initApi();
  }

  void _initFromRequest() {
    final req = widget.initialRequest;
    if (req == null) return;
    if (req.types != null && req.types!.isNotEmpty) {
      _selectedTypes.addAll(req.types!);
    }
    if (req.sortBy != null) {
      _sortBy = req.sortBy!;
    }
    _suppressSearchCallback = true;
    if (req.search != null && req.search!.isNotEmpty) {
      _searchCtrl.text = req.search!;
    }
    _suppressSearchCallback = false;
    _favorite = req.favorite;
    _hasPlayback = req.hasPlayback;
    _itemIds = req.itemIds;
    _linkedItemIds = req.linkedItemIds;
  }

  Future<void> _initApi() async {
    final prefs = await SharedPreferences.getInstance();
    _mediaApi = MediaApi(ApiClient(prefs));
    _apiReady.complete();
    _loadData();
  }

  void _onScroll() {
    if (_isLoading || !_hasMore) return;
    final maxScroll = _scrollCtrl.position.maxScrollExtent;
    final currentScroll = _scrollCtrl.position.pixels;
    if (maxScroll - currentScroll < 300) {
      _loadData();
    }
  }

  Future<void> _loadData() async {
    if (_isLoading || !_hasMore) return;
    await _apiReady.future;
    setState(() => _isLoading = true);

    try {
      final request = MediaListRequest(
        types: _selectedTypes.isEmpty ? null : Set.from(_selectedTypes),
        favorite: _favorite,
        hasPlayback: _hasPlayback,
        sortBy: _sortBy,
        itemIds: _itemIds,
        linkedItemIds: _linkedItemIds,
        search: _searchCtrl.text.isNotEmpty ? _searchCtrl.text : null,
      );
      final response = await _mediaApi!.getList(
        request,
        limit: _pageSize,
        offset: _offset,
      );

      if (mounted) {
        setState(() {
          if (_offset == 0) {
            _items
              ..clear()
              ..addAll(response.items);
          } else {
            _items.addAll(response.items);
          }
          _totalCount = response.total;
          _offset += response.items.length;
          _hasMore = _items.length < _totalCount;
          _isLoading = false;
          _isInitialLoading = false;
        });
      }
    } catch (error, stackTrace) {
      AppLogger.error(
        'media_grid_load_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'media',
        fields: {'offset': _offset},
      );
      if (mounted) {
        setState(() {
          _isLoading = false;
          _isInitialLoading = false;
        });
      }
    }
  }

  void _resetAndLoad() {
    setState(() {
      _items.clear();
      _offset = 0;
      _hasMore = true;
    });
    _loadData();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollCtrl.hasClients) {
        _scrollCtrl.jumpTo(0);
      }
    });
  }

  void _refreshData() {
    setState(() {
      _offset = 0;
      _hasMore = true;
    });
    _loadData();
  }

  void _toggleType(MediaType type) {
    setState(() {
      if (_selectedTypes.contains(type)) {
        _selectedTypes.remove(type);
      } else {
        _selectedTypes.add(type);
      }
    });
    _refreshData();
  }

  @override
  void dispose() {
    _scrollCtrl.removeListener(_onScroll);
    _scrollCtrl.dispose();
    _searchCtrl.dispose();
    _searchFocus.dispose();
    _debounceTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;

    if (_isInitialLoading) {
      return Scaffold(
        backgroundColor: cs.surface,
        body: Center(child: CircularProgressIndicator(color: cs.primary)),
      );
    }

    return Scaffold(
      backgroundColor: cs.surface,
      body: Column(
        children: [
          _buildNavBar(),
          if (_showTypeSelector) _buildTypeSelector(),
          Expanded(
            child: Column(
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 8, 16, 4),
                  child: Row(
                    children: [
                      _buildSortDropdown(),
                      const SizedBox(width: 6),
                      _buildIconButton(
                        LucideIcons.list_filter,
                        () => setState(
                          () => _showTypeSelector = !_showTypeSelector,
                        ),
                        isActive: _selectedTypes.isNotEmpty,
                        narrow: true,
                      ),
                      const Spacer(),
                      if (_items.isNotEmpty)
                        Text(
                          '共 $_totalCount 项 · 显示 ${_items.length} 项',
                          style: TextStyle(
                            color: Theme.of(
                              context,
                            ).colorScheme.onSurfaceVariant,
                            fontSize: 12,
                          ),
                        ),
                    ],
                  ),
                ),
                Expanded(
                  child: ColoredBox(
                    color: Theme.of(context).colorScheme.surface,
                    child: RefreshIndicator(
                      onRefresh: () async {
                        _refreshData();
                        await _apiReady.future;
                        await Future.doWhile(() {
                          return Future.delayed(
                            const Duration(milliseconds: 50),
                            () => _isLoading,
                          );
                        });
                      },
                      displacement: 40,
                      child: CustomScrollView(
                        controller: _scrollCtrl,
                        slivers: [
                          if (_items.isEmpty)
                            SliverFillRemaining(
                              child: Center(
                                child: _isLoading
                                    ? const CircularProgressIndicator(
                                        strokeWidth: 2.5,
                                      )
                                    : Column(
                                        mainAxisAlignment:
                                            MainAxisAlignment.center,
                                        children: [
                                          Icon(
                                            LucideIcons.inbox,
                                            size: 48,
                                            color: Theme.of(
                                              context,
                                            ).colorScheme.onSurfaceVariant,
                                          ),
                                          const SizedBox(height: 12),
                                          Text(
                                            '暂无数据',
                                            style: TextStyle(
                                              color: Theme.of(
                                                context,
                                              ).colorScheme.onSurfaceVariant,
                                              fontSize: 16,
                                            ),
                                          ),
                                          const SizedBox(height: 4),
                                          TextButton(
                                            onPressed: _resetAndLoad,
                                            child: const Text('重置筛选条件'),
                                          ),
                                        ],
                                      ),
                              ),
                            )
                          else
                            SliverPadding(
                              padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                              sliver: SliverGrid(
                                gridDelegate:
                                    SliverGridDelegateWithMaxCrossAxisExtent(
                                      maxCrossAxisExtent: 140,
                                      mainAxisSpacing: 16,
                                      crossAxisSpacing: 8,
                                      childAspectRatio: 0.55,
                                    ),
                                delegate: SliverChildBuilderDelegate(
                                  (context, index) => MediaCard(
                                    media: _items[index],
                                    config: const CardConfig(),
                                  ),
                                  childCount: _items.length,
                                ),
                              ),
                            ),
                          if (_isLoading)
                            const SliverToBoxAdapter(
                              child: Padding(
                                padding: EdgeInsets.symmetric(vertical: 16),
                                child: Center(
                                  child: CircularProgressIndicator(
                                    strokeWidth: 2.5,
                                  ),
                                ),
                              ),
                            ),
                          if (!_hasMore && _items.isNotEmpty)
                            SliverToBoxAdapter(
                              child: Padding(
                                padding: const EdgeInsets.symmetric(
                                  vertical: 16,
                                ),
                                child: Center(
                                  child: Text(
                                    '已加载全部',
                                    style: TextStyle(
                                      color: Theme.of(
                                        context,
                                      ).colorScheme.onSurfaceVariant,
                                      fontSize: 13,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          const SliverToBoxAdapter(child: SizedBox(height: 80)),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNavBar() {
    return ColoredBox(
      color: Theme.of(context).colorScheme.surface,
      child: Material(
        type: MaterialType.transparency,
        child: SafeArea(
          bottom: false,
          top: true,
          maintainBottomViewPadding: false,
          child: Padding(
            padding: const EdgeInsets.fromLTRB(4, 4, 16, 4),
            child: Row(
              children: [
                const BackButton(),
                const SizedBox(width: 4),
                Expanded(
                  child: _showSearch
                      ? _buildSearchField()
                      : _buildSearchButton(),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildIconButton(
    IconData icon,
    VoidCallback onPressed, {
    bool isActive = false,
    bool narrow = true,
  }) {
    final cs = Theme.of(context).colorScheme;
    return Container(
      decoration: BoxDecoration(
        color: isActive
            ? cs.primary.withValues(alpha: 0.15)
            : cs.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(8),
      ),
      child: IconButton(
        icon: Icon(icon, size: 18),
        color: isActive ? cs.primary : cs.onSurfaceVariant,
        onPressed: onPressed,
        constraints: BoxConstraints(
          minWidth: narrow ? 24 : 24,
          minHeight: narrow ? 24 : 24,
        ),
        padding: EdgeInsets.zero,
        splashRadius: narrow ? 15 : 18,
        visualDensity: VisualDensity.compact,
      ),
    );
  }

  Widget _buildSearchField() {
    final cs = Theme.of(context).colorScheme;
    return Container(
      height: 40,
      padding: const EdgeInsets.symmetric(horizontal: 12),
      decoration: BoxDecoration(
        color: cs.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          Icon(LucideIcons.search, size: 18, color: cs.onSurfaceVariant),
          const SizedBox(width: 8),
          Expanded(
            child: TextField(
              controller: _searchCtrl,
              focusNode: _searchFocus,
              style: const TextStyle(fontSize: 14),
              decoration: const InputDecoration(
                hintText: '搜索媒体名称...',
                border: InputBorder.none,
                isDense: true,
                contentPadding: EdgeInsets.symmetric(vertical: 10),
              ),
              onSubmitted: (_) => _resetAndLoad(),
              onChanged: _onSearchChanged,
            ),
          ),
          GestureDetector(
            onTap: () {
              setState(() {
                _showSearch = false;
                _searchCtrl.clear();
              });
              _resetAndLoad();
            },
            child: Icon(LucideIcons.x, size: 18, color: cs.onSurfaceVariant),
          ),
        ],
      ),
    );
  }

  Timer? _debounceTimer;
  void _onSearchChanged(String _) {
    if (_suppressSearchCallback) return;
    _debounceTimer?.cancel();
    _debounceTimer = Timer(const Duration(milliseconds: 500), _resetAndLoad);
  }

  Widget _buildSearchButton() {
    final cs = Theme.of(context).colorScheme;
    return GestureDetector(
      onTap: () {
        setState(() => _showSearch = true);
        WidgetsBinding.instance.addPostFrameCallback((_) {
          _searchFocus.requestFocus();
        });
      },
      child: Container(
        height: 40,
        decoration: BoxDecoration(
          color: cs.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(10),
        ),
        padding: const EdgeInsets.symmetric(horizontal: 12),
        child: Row(
          children: [
            Icon(LucideIcons.search, size: 18, color: cs.onSurfaceVariant),
            const SizedBox(width: 8),
            Text(
              '搜索媒体名称...',
              style: TextStyle(fontSize: 13, color: cs.onSurfaceVariant),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSortDropdown() {
    final cs = Theme.of(context).colorScheme;
    return Material(
      type: MaterialType.transparency,
      child: PopupMenuButton<String>(
        onSelected: (v) {
          if (v != _sortBy) {
            setState(() => _sortBy = v);
            _resetAndLoad();
          }
        },
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        itemBuilder: (context) => _sortOptions.map((opt) {
          final isSelected = _sortBy == opt.$1;
          return PopupMenuItem<String>(
            value: opt.$1,
            child: Row(
              children: [
                Icon(
                  opt.$3,
                  size: 18,
                  color: isSelected ? cs.primary : cs.onSurfaceVariant,
                ),
                const SizedBox(width: 10),
                Text(
                  opt.$2,
                  style: TextStyle(
                    fontWeight: isSelected
                        ? FontWeight.w600
                        : FontWeight.normal,
                    color: isSelected ? cs.primary : null,
                  ),
                ),
                if (isSelected) ...[
                  const Spacer(),
                  Icon(Icons.check, size: 16, color: cs.primary),
                ],
              ],
            ),
          );
        }).toList(),
        child: Container(
          height: 40,
          padding: const EdgeInsets.symmetric(horizontal: 10),
          decoration: BoxDecoration(
            color: cs.surfaceContainerHighest,
            borderRadius: BorderRadius.circular(10),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                _sortOptions
                    .firstWhere(
                      (o) => o.$1 == _sortBy,
                      orElse: () => _sortOptions[0],
                    )
                    .$3,
                size: 14,
                color: cs.onSurfaceVariant,
              ),
              const SizedBox(width: 4),
              Text(
                _sortOptions
                    .firstWhere(
                      (o) => o.$1 == _sortBy,
                      orElse: () => _sortOptions[0],
                    )
                    .$2,
                style: const TextStyle(fontSize: 13),
              ),
              const SizedBox(width: 2),
              Icon(
                LucideIcons.chevron_down,
                size: 16,
                color: cs.onSurfaceVariant,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTypeSelector() {
    final cs = Theme.of(context).colorScheme;
    return ColoredBox(
      color: cs.surface,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 4, 16, 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Row(
                children: [
                  Text(
                    '媒体类型',
                    style: TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w500,
                      color: cs.onSurfaceVariant,
                    ),
                  ),
                  const Spacer(),
                  if (_selectedTypes.isNotEmpty)
                    GestureDetector(
                      onTap: () {
                        setState(() => _selectedTypes.clear());
                        _refreshData();
                      },
                      child: Text(
                        '清除筛选',
                        style: TextStyle(fontSize: 12, color: cs.primary),
                      ),
                    ),
                ],
              ),
            ),
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: _allTypes.map((type) {
                final selected = _selectedTypes.contains(type);
                return GestureDetector(
                  onTap: () => _toggleType(type),
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: selected ? cs.primary : cs.surfaceContainerHighest,
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(
                        color: selected
                            ? cs.primary.withValues(alpha: 0.7)
                            : cs.outlineVariant,
                        width: 0.5,
                      ),
                    ),
                    child: Text(
                      type.labelZH,
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: selected
                            ? FontWeight.w500
                            : FontWeight.normal,
                        color: selected ? cs.onPrimary : cs.onSurfaceVariant,
                      ),
                    ),
                  ),
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}
