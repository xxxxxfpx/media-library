import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';

import '../component/horizontal_media_section.dart';
import '../component/media_tag.dart';
import '../data/api/api_client.dart';
import '../data/api/media_api.dart';
import '../data/api/user_api.dart';
import '../data/models/media.dart';
import '../core/constants.dart';
import '../core/app_logger.dart';
import '../core/token_cache.dart';
import '../component/media_card.dart';
import '../design_system/app_theme.dart';
import 'video_play.dart';
import 'grid_view.dart';

class DetailPagePhone extends StatefulWidget {
  final int mediaId;

  const DetailPagePhone({super.key, required this.mediaId});

  @override
  State<DetailPagePhone> createState() => _DetailPagePhoneState();
}

class _DetailPagePhoneState extends State<DetailPagePhone> {
  bool _isFavorite = false;
  bool _isLoading = true;
  final ValueNotifier<double> _appBarOpacity = ValueNotifier(0.0);
  final ScrollController _scrollController = ScrollController();
  final GlobalKey _imageKey = GlobalKey();
  MediaApi? _mediaApi;
  UserApi? _userApi;
  MediaItem? _media;
  int _selectedVideoIndex = 0;
  double? _ratingValue; // null 表示未评分

  List<FileInfo> get _videoFiles {
    final m = _media;
    if (m == null) return [];
    return m.files
        .where((f) => f.type == 'Video' || f.type == 'video')
        .toList();
  }

  String? get _sourceUrl {
    final m = _media;
    if (m == null) return null;
    for (final link in m.links) {
      if (link.sourceLink != null && link.sourceLink!.isNotEmpty) {
        return link.sourceLink;
      }
    }
    return null;
  }

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_updateAppBarOpacity);

    WidgetsBinding.instance.addPostFrameCallback((_) {
      _updateAppBarOpacity();
    });

    _initApi();
  }

  void _updateAppBarOpacity() {
    final renderBox =
        _imageKey.currentContext?.findRenderObject() as RenderBox?;
    if (renderBox == null || !renderBox.hasSize) {
      if (_appBarOpacity.value != 1.0) {
        _appBarOpacity.value = 1.0;
      }
      return;
    }

    final imageTop = renderBox.localToGlobal(Offset.zero).dy;
    final imageHeight = renderBox.size.height;
    final topPadding = MediaQuery.of(context).padding.top;
    final totalBarHeight = topPadding + kToolbarHeight;

    final startFadeY = -(imageHeight * 0.75 - totalBarHeight);
    final endFadeY = -(imageHeight - totalBarHeight);

    double opacity;
    if (imageTop > startFadeY) {
      opacity = 0.0;
    } else if (imageTop < endFadeY) {
      opacity = 1.0;
    } else {
      opacity = (startFadeY - imageTop) / (startFadeY - endFadeY);
    }

    if (opacity != _appBarOpacity.value) {
      _appBarOpacity.value = opacity;
    }
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _initApi() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final client = ApiClient(prefs);
      final api = MediaApi(client);
      final data = await api.getInfo(widget.mediaId);
      if (mounted) {
        setState(() {
          _mediaApi = api;
          _userApi = UserApi(client);
          _media = data;
          _isFavorite = data.userdata?.favoritedAt != null;
          _ratingValue = data.userdata?.rating; // null 表示未评分
          _isLoading = false;
        });
        WidgetsBinding.instance.addPostFrameCallback((_) {
          _updateAppBarOpacity();
        });
      }
    } catch (error, stackTrace) {
      AppLogger.error(
        'media_detail_load_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'media',
        fields: {'media_id': widget.mediaId},
      );
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(const SnackBar(content: Text('加载失败')));
        Navigator.pop(context);
      }
    }
  }

  Future<void> _toggleFavorite() async {
    final newValue = !_isFavorite;
    setState(() => _isFavorite = newValue);
    try {
      await _userApi?.updateUserData(
        UpdateUserDataRequest(itemId: widget.mediaId, isFavorite: newValue),
      );
    } catch (error, stackTrace) {
      AppLogger.error(
        'favorite_update_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'media',
        fields: {'media_id': widget.mediaId, 'favorite': newValue},
      );
      if (mounted) {
        setState(() => _isFavorite = !newValue);
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(const SnackBar(content: Text('操作失败，请稍后重试')));
      }
    }
  }

  Future<void> _saveRating(double? rating) async {
    final previousValue = _ratingValue;
    try {
      await _userApi?.updateUserData(
        UpdateUserDataRequest(
          itemId: widget.mediaId,
          rating: rating,
          clearRating: rating == null,
        ),
      );
    } catch (error, stackTrace) {
      AppLogger.error(
        'rating_update_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'media',
        fields: {'media_id': widget.mediaId, 'has_rating': rating != null},
      );
      if (mounted) {
        setState(() => _ratingValue = previousValue);
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(const SnackBar(content: Text('评分保存失败，请稍后重试')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final hasImage = _media?.getPrimaryImageUrl() != null;
    final cs = Theme.of(context).colorScheme;

    return Scaffold(
      extendBodyBehindAppBar: hasImage,
      backgroundColor: cs.surface,
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(kToolbarHeight),
        child: ListenableBuilder(
          listenable: _appBarOpacity,
          builder: (context, _) => AppBar(
            backgroundColor: hasImage
                ? cs.surface.withValues(alpha: _appBarOpacity.value)
                : cs.surface,
            surfaceTintColor: Colors.transparent,
            elevation: 0,
            leading: IconButton(
              icon: Icon(Icons.arrow_back, color: cs.onSurface),
              onPressed: () => Navigator.pop(context),
            ),
            actions: [
              if (_sourceUrl != null)
                IconButton(
                  icon: Icon(Icons.language, color: cs.onSurfaceVariant),
                  tooltip: '打开来源',
                  onPressed: () async {
                    final uri = Uri.tryParse(_sourceUrl!);
                    if (uri != null && await canLaunchUrl(uri)) {
                      launchUrl(uri, mode: LaunchMode.externalApplication);
                    }
                  },
                ),
              if (!_isLoading)
                IconButton(
                  icon: Icon(
                    _isFavorite ? Icons.favorite : Icons.favorite_border,
                    color: _isFavorite
                        ? context.semantic.favorite
                        : cs.onSurfaceVariant,
                  ),
                  onPressed: _toggleFavorite,
                ),
            ],
          ),
        ),
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator(color: cs.onSurface))
          : _media == null
          ? Center(
              child: Text('加载失败', style: TextStyle(color: cs.onSurfaceVariant)),
            )
          : SafeArea(
              top: !hasImage,
              bottom: false,
              child: SingleChildScrollView(
                controller: _scrollController,
                child: Column(
                  children: [
                    if (_media!.getPrimaryImageUrl() != null)
                      _buildImageSection(),
                    _buildActorsSection(),
                    _buildDetailSection(),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildImageSection() {
    return Center(
      key: _imageKey,
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxHeight: 350),
        child: MediaCard(
          media: _media!,
          config: const CardConfig(
            enableClick: false,
            showProgress: false,
            showScore: false,
            showTitle: false,
            showType: false,
          ),
        ),
      ),
    );
  }

  Widget _buildActorsSection() {
    final actors = _media!.links
        .where((l) => l.peopleType == 'Actor' || l.peopleRole == 'Actor')
        .toList();
    if (actors.isEmpty) return const SizedBox.shrink();

    final cs = Theme.of(context).colorScheme;

    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: Text(
              '演员',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: cs.onSurface,
              ),
            ),
          ),
          SizedBox(
            height: 110,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              physics: const BouncingScrollPhysics(),
              itemCount: actors.length,
              itemBuilder: (context, index) {
                final link = actors[index];
                final item = link.linkedItem;
                if (item == null) return const SizedBox.shrink();

                final baseUrl =
                    _mediaApi?.baseUrl ?? AppConstants.defaultBaseUrl;
                final imgUrl = item.primaryImage != null
                    ? TokenCache.withToken(
                        '$baseUrl/api/file/data?file_id=${item.primaryImage}',
                      )
                    : null;

                return Padding(
                  padding: const EdgeInsets.only(right: 16),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      ClipRRect(
                        borderRadius: BorderRadius.circular(35),
                        child: SizedBox(
                          width: 70,
                          height: 70,
                          child: imgUrl != null
                              ? Image.network(
                                  imgUrl,
                                  fit: BoxFit.cover,
                                  errorBuilder: (_, _, _) =>
                                      _buildActorPlaceholder(),
                                )
                              : _buildActorPlaceholder(),
                        ),
                      ),
                      const SizedBox(height: 6),
                      SizedBox(
                        width: 70,
                        child: Text(
                          item.name ?? '未知',
                          style: TextStyle(
                            fontSize: 12,
                            color: cs.onSurfaceVariant,
                          ),
                          textAlign: TextAlign.center,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActorPlaceholder() {
    final cs = Theme.of(context).colorScheme;
    return Container(
      decoration: BoxDecoration(
        color: cs.surfaceContainerHighest,
        shape: BoxShape.circle,
      ),
      child: Icon(Icons.person, color: cs.onSurfaceVariant, size: 32),
    );
  }

  Widget _buildDetailSection() {
    final cs = Theme.of(context).colorScheme;
    const sectionPadding = EdgeInsets.symmetric(horizontal: 16);
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(padding: sectionPadding, child: _buildDetailInfo()),
          if (_videoFiles.isNotEmpty) ...[
            Padding(
              padding: sectionPadding,
              child: Divider(color: cs.outlineVariant, height: 32),
            ),
            Padding(padding: sectionPadding, child: _buildPlaySection()),
          ],
          if (_media!.userdata != null) ...[
            Padding(
              padding: sectionPadding,
              child: Divider(color: cs.outlineVariant, height: 32),
            ),
            Padding(padding: sectionPadding, child: _buildUserMediaData()),
            Padding(
              padding: sectionPadding,
              child: Divider(color: cs.outlineVariant, height: 32),
            ),
          ],
          Padding(padding: sectionPadding, child: _buildLinksSection()),
          if (_media!.files.isNotEmpty) ...[
            Padding(
              padding: sectionPadding,
              child: Divider(color: cs.outlineVariant, height: 32),
            ),
            _buildFilesSection(),
          ],
          if (_mediaApi != null && _media!.hasChildren == true) ...[
            Padding(
              padding: sectionPadding,
              child: Divider(color: cs.outlineVariant, height: 32),
            ),
            HorizontalMediaSection(
              title: '包含的媒体',
              contentPadding: sectionPadding,
              onViewAll: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => MediaGridPage(
                      initialRequest: MediaListRequest(
                        linkedItemIds: _media!.id.toString(),
                        sortBy: _media!.type == 'BoxSet' ? 'order' : null,
                      ),
                    ),
                  ),
                );
              },
              fetchData: (offset, limit) => _mediaApi!.getList(
                MediaListRequest(
                  linkedItemIds: _media!.id.toString(),
                  sortBy: _media!.type == 'BoxSet' ? 'order' : null,
                ),
                limit: limit,
                offset: offset,
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildDetailInfo() {
    final m = _media!;
    final cs = Theme.of(context).colorScheme;

    String? formatDate(String? dateString) {
      if (dateString == null || dateString.isEmpty) return null;
      try {
        final date = DateTime.parse(dateString);
        return '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
      } catch (error) {
        AppLogger.debug(
          'media_date_parse_failed',
          category: 'media',
          fields: {'error_type': error.runtimeType.toString()},
        );
        return null;
      }
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          m.name ?? '未知标题',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: cs.onSurface,
          ),
        ),
        if (m.alias.isNotEmpty) ...[
          const SizedBox(height: 6),
          Wrap(
            spacing: 6,
            runSpacing: 6,
            alignment: WrapAlignment.start,
            children: m.alias
                .map(
                  (a) => Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 3,
                    ),
                    decoration: BoxDecoration(
                      color: cs.surfaceContainerHighest,
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Text(
                      a.name ?? '',
                      style: TextStyle(
                        fontSize: 11,
                        color: cs.onSurfaceVariant,
                      ),
                    ),
                  ),
                )
                .toList(),
          ),
        ],
        if (m.tagline != null) ...[
          const SizedBox(height: 4),
          Text(
            m.tagline!,
            style: TextStyle(
              fontSize: 14,
              fontStyle: FontStyle.italic,
              color: cs.onSurfaceVariant,
            ),
          ),
        ],
        const SizedBox(height: 12),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          alignment: WrapAlignment.start,
          children: [
            if (m.communityRating != null)
              _buildTag(
                m.communityRating!.toStringAsFixed(1),
                context.semantic.rating,
              ),
            _buildTag('#${_media!.id}', cs.outline),
            if (m.officialRating != null)
              _buildTag(m.officialRating!, context.semantic.warning),
            if (m.productionYear != null)
              _buildTag('${m.productionYear}', context.semantic.info),
            if (m.runTimeTicks != null)
              _buildTag(
                '${(m.runTimeTicks! / 600000000).round()} 分钟',
                context.semantic.success,
              ),
            _buildTag(_media!.mediaType.labelZH, cs.primary),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (m.premiereDate != null) ...[
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '发布日期',
                      style: TextStyle(
                        fontSize: 12,
                        color: cs.onSurfaceVariant,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      formatDate(m.premiereDate) ?? m.premiereDate!,
                      style: TextStyle(fontSize: 13, color: cs.onSurface),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 24),
            ],
            if (m.dateCreated != null) ...[
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '加入日期',
                      style: TextStyle(
                        fontSize: 12,
                        color: cs.onSurfaceVariant,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      formatDate(m.dateCreated) ?? m.dateCreated!,
                      style: TextStyle(fontSize: 13, color: cs.onSurface),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
        if (m.overview != null && m.overview!.isNotEmpty) ...[
          const SizedBox(height: 16),
          Text(
            '简介',
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: cs.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            m.overview!,
            style: TextStyle(
              fontSize: 13,
              color: cs.onSurfaceVariant,
              height: 1.5,
            ),
            maxLines: 5,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ],
    );
  }

  Widget _buildUserMediaData() {
    final userdata = _media!.userdata;
    if (userdata == null) return const SizedBox.shrink();
    final cs = Theme.of(context).colorScheme;

    String formatTicks(int? ticks) {
      if (ticks == null || ticks <= 0) return '--:--:--';
      final seconds = ticks ~/ 10000000;
      final h = seconds ~/ 3600;
      final m = (seconds % 3600) ~/ 60;
      final s = seconds % 60;
      return '${h.toString().padLeft(2, '0')}:${m.toString().padLeft(2, '0')}:${s.toString().padLeft(2, '0')}';
    }

    final runtimeSeconds = _media!.runTimeTicks != null
        ? _media!.runTimeTicks! ~/ 10000000
        : 0;
    final playedSeconds = userdata.playbackPositionTicks != null
        ? userdata.playbackPositionTicks! ~/ 10000000
        : 0;
    final progress = runtimeSeconds > 0 ? playedSeconds / runtimeSeconds : 0.0;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            if (userdata.favoritedAt != null)
              _buildInfoChip(
                Icons.favorite,
                '已收藏',
                context.semantic.favorite,
              ),
            if (userdata.favoritedAt != null) const SizedBox(width: 12),
            if (userdata.rating != null)
              _buildInfoChip(
                Icons.star,
                userdata.rating!.toStringAsFixed(1),
                context.semantic.rating,
              ),
            if (userdata.rating != null) const SizedBox(width: 12),
            _buildInfoChip(
              Icons.play_arrow,
              '播放 ${userdata.playCount ?? 0} 次',
              context.semantic.success,
            ),
            const SizedBox(width: 12),
            _buildInfoChip(
              Icons.history,
              userdata.lastPlayedDisplay ?? '未播放',
              cs.primary,
            ),
          ],
        ),
        const SizedBox(height: 16),
        _buildRatingSlider(),
        if (runtimeSeconds > 0 || playedSeconds > 0) ...[
          const SizedBox(height: 10),
          Row(
            children: [
              Text(
                formatTicks(userdata.playbackPositionTicks),
                style: TextStyle(fontSize: 12, color: cs.primary),
              ),
              if (runtimeSeconds > 0) ...[
                Text(
                  ' / ',
                  style: TextStyle(fontSize: 12, color: cs.onSurfaceVariant),
                ),
                Text(
                  formatTicks(_media!.runTimeTicks),
                  style: TextStyle(fontSize: 12, color: cs.primary),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(4),
                    child: LinearProgressIndicator(
                      value: progress,
                      backgroundColor: cs.surfaceContainerHighest,
                      valueColor: AlwaysStoppedAnimation(cs.primary),
                      minHeight: 6,
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                Text(
                  '${(progress * 100).toStringAsFixed(0)}%',
                  style: TextStyle(fontSize: 12, color: cs.primary),
                ),
              ],
            ],
          ),
        ],
      ],
    );
  }

  Widget _buildRatingSlider() {
    final cs = Theme.of(context).colorScheme;
    final hasRating = _ratingValue != null;
    const thumbRadius = 12.0;
    const nullZoneWidth = 30.0; // 左侧"未评分"区域宽度
    const trackHeight = 4.0;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(
              hasRating ? Icons.star : Icons.star_border,
              size: 18,
              color:
                  hasRating ? context.semantic.rating : cs.onSurfaceVariant,
            ),
            const SizedBox(width: 6),
            Text(
              '我的评分',
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: cs.onSurface,
              ),
            ),
            const Spacer(),
            AnimatedSwitcher(
              duration: const Duration(milliseconds: 200),
              child: Text(
                hasRating ? _ratingValue!.toStringAsFixed(1) : '未评分',
                key: ValueKey(hasRating),
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: hasRating
                      ? context.semantic.rating
                      : cs.onSurfaceVariant.withValues(alpha: 0.5),
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        LayoutBuilder(
          builder: (context, constraints) {
            final sliderWidth = constraints.maxWidth;
            // 滑块中心可移动范围：从 thumbRadius 到 sliderWidth - thumbRadius
            final trackStart = thumbRadius;
            final trackEnd = sliderWidth - thumbRadius;
            // 评分区域从 nullZoneWidth 开始
            final ratingZoneStart = nullZoneWidth;
            final ratingZoneLength = trackEnd - ratingZoneStart;

            // 计算滑块中心位置
            double thumbCenterX;
            if (_ratingValue == null) {
              thumbCenterX = trackStart;
            } else {
              final ratio = _ratingValue! / 10.0;
              thumbCenterX = ratingZoneStart + ratio * ratingZoneLength;
            }

            // 计算已激活的轨道长度
            double activeTrackLength = 0;
            if (hasRating) {
              activeTrackLength = thumbCenterX - ratingZoneStart;
            }

            return GestureDetector(
              behavior: HitTestBehavior.opaque,
              onHorizontalDragUpdate: (details) {
                final dx = details.localPosition.dx;
                if (dx <= ratingZoneStart) {
                  setState(() => _ratingValue = null);
                } else {
                  final ratio = ((dx - ratingZoneStart) / ratingZoneLength)
                      .clamp(0.0, 1.0);
                  final value = ratio * 10.0;
                  setState(() => _ratingValue = (value * 10).round() / 10.0);
                }
              },
              onHorizontalDragEnd: (details) {
                _saveRating(_ratingValue);
              },
              onTapDown: (details) {
                final dx = details.localPosition.dx;
                if (dx <= ratingZoneStart) {
                  setState(() => _ratingValue = null);
                } else {
                  final ratio = ((dx - ratingZoneStart) / ratingZoneLength)
                      .clamp(0.0, 1.0);
                  final value = ratio * 10.0;
                  setState(() => _ratingValue = (value * 10).round() / 10.0);
                }
                _saveRating(_ratingValue);
              },
              child: SizedBox(
                height: 48,
                child: Stack(
                  clipBehavior: Clip.none,
                  children: [
                    // 背景轨道
                    Positioned(
                      left: trackStart,
                      right: trackStart,
                      top: (48 - trackHeight) / 2,
                      child: Container(
                        height: trackHeight,
                        decoration: BoxDecoration(
                          color: cs.surfaceContainerHighest,
                          borderRadius: BorderRadius.circular(trackHeight / 2),
                        ),
                      ),
                    ),
                    // 已评分激活的轨道
                    if (hasRating && activeTrackLength > 0)
                      Positioned(
                        left: ratingZoneStart,
                        top: (48 - trackHeight) / 2,
                        child: Container(
                          width: activeTrackLength.clamp(0.0, ratingZoneLength),
                          height: trackHeight,
                          decoration: BoxDecoration(
                            color: context.semantic.rating,
                            borderRadius: BorderRadius.circular(
                              trackHeight / 2,
                            ),
                          ),
                        ),
                      ),
                    // 左侧"未评分"分隔线
                    Positioned(
                      left: ratingZoneStart,
                      top: 0,
                      bottom: 0,
                      child: Container(
                        width: 2,
                        color: cs.outlineVariant.withValues(alpha: 0.3),
                      ),
                    ),
                    // 刻度标记
                    Positioned(
                      left: ratingZoneStart,
                      right: 0,
                      bottom: 2,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          for (int i = 0; i <= 10; i += 2)
                            Text(
                              '$i',
                              style: TextStyle(
                                fontSize: 10,
                                color: cs.onSurfaceVariant.withValues(
                                  alpha: 0.5,
                                ),
                              ),
                            ),
                        ],
                      ),
                    ),
                    // 滑块
                    Positioned(
                      left: thumbCenterX - thumbRadius,
                      top: (48 - thumbRadius * 2) / 2,
                      child: Container(
                        width: thumbRadius * 2,
                        height: thumbRadius * 2,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: hasRating
                              ? context.semantic.rating
                              : cs.onSurfaceVariant,
                          border: Border.all(color: cs.surface, width: 2),
                          boxShadow: [
                            BoxShadow(
                              color: cs.scrim.withValues(alpha: 0.2),
                              blurRadius: 4,
                              offset: const Offset(0, 2),
                            ),
                          ],
                        ),
                        child: Icon(
                          hasRating ? Icons.star : Icons.block,
                          size: 12,
                          color: hasRating
                              ? context.semantic.playerOverlayText
                              : cs.surface,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ],
    );
  }

  Widget _buildInfoChip(IconData icon, String label, Color color) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 14, color: color),
        const SizedBox(width: 4),
        Text(label, style: TextStyle(fontSize: 12, color: color)),
      ],
    );
  }

  static const _linkTypeNames = {
    'Actor': '演员',
    'Director': '导演',
    'Writer': '编剧',
    'Producer': '制片',
    'Composer': '作曲家',
    'Conductor': '指挥',
    'Team': '团队',
    'Company': '公司',
    'Tag': '标签',
    'Genre': '类型',
    'Studio': '工作室',
    'Network': '网络',
    'Season': '季',
    'Series': '系列',
    'Source': '来源',
    'Part of Set': '合集',
    'Movie': '电影',
    'Episode': '集',
    'Audio': '音乐',
    'Photo': '图片',
    'Book': '电子书',
    'Person': '人物',
    'BoxSet': '集合',
    'Other': '其他',
  };

  Widget _buildLinksSection() {
    final cs = Theme.of(context).colorScheme;
    final groupedLinks = <String, List<LinkInfo>>{};
    for (final link in _media!.links) {
      if (link.peopleType == 'Actor' || link.peopleRole == 'Actor') continue;
      final key =
          link.peopleType ??
          link.peopleRole ??
          link.linkedItem?.type ??
          'Other';
      final label = _linkTypeNames[key] ?? key;
      groupedLinks.putIfAbsent(label, () => []).add(link);
    }
    if (groupedLinks.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '关联内容',
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: cs.onSurface,
          ),
        ),
        const SizedBox(height: 12),
        ...groupedLinks.entries.map(
          (entry) => _buildLinkGroup(entry.key, entry.value),
        ),
      ],
    );
  }

  Widget _buildLinkGroup(String label, List<LinkInfo> links) {
    final cs = Theme.of(context).colorScheme;
    final tagItems = <LinkInfo>[];
    final cardItems = <LinkInfo>[];
    for (final link in links) {
      if (link.linkedItem?.primaryImage != null) {
        cardItems.add(link);
      } else {
        tagItems.add(link);
      }
    }
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Text(
              label,
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: cs.primary,
              ),
            ),
          ),
          if (tagItems.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Wrap(
                spacing: 8,
                runSpacing: 6,
                alignment: WrapAlignment.spaceBetween,
                runAlignment: WrapAlignment.start,
                crossAxisAlignment: WrapCrossAlignment.center,
                children: tagItems.map((link) {
                  final item = link.linkedItem;
                  if (item == null) return const SizedBox.shrink();
                  return MediaTag(
                    media: MediaItem(
                      id: item.id,
                      name: item.name,
                      type: item.type,
                      overview: item.overview,
                      tagline: item.tagline,
                      premiereDate: item.premiereDate,
                      officialRating: item.officialRating,
                      communityRating: item.communityRating,
                    ),
                  );
                }).toList(),
              ),
            ),
          if (cardItems.isNotEmpty)
            SizedBox(
              height: 175,
              child: ListView.builder(
                physics: const BouncingScrollPhysics(),
                scrollDirection: Axis.horizontal,
                itemCount: cardItems.length,
                itemBuilder: (context, index) {
                  final item = cardItems[index].linkedItem;
                  if (item == null) return const SizedBox.shrink();
                  return Padding(
                    padding: const EdgeInsets.only(right: 10),
                    child: SizedBox(
                      width: 90,
                      child: MediaCard(
                        media: MediaItem(
                          id: item.id,
                          name: item.name,
                          type: item.type,
                          overview: item.overview,
                          tagline: item.tagline,
                          premiereDate: item.premiereDate,
                          officialRating: item.officialRating,
                          communityRating: item.communityRating,
                        ),
                        config: const CardConfig(
                          showProgress: false,
                          showScore: false,
                          showTitle: true,
                          showType: false,
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }

  String _videoLabel(FileInfo f) {
    final codec = f.ffmpeg?['codec'] ?? '';
    final w = f.ffmpeg?['width'];
    final h = f.ffmpeg?['height'];
    final resolution = w != null && h != null ? '${w}x$h' : '';
    final parts = [
      if (codec.isNotEmpty) codec,
      if (resolution.isNotEmpty) resolution,
    ];
    return parts.isNotEmpty
        ? '${f.name ?? ''} (${parts.join(', ')})'
        : (f.name ?? '未知');
  }

  Widget _buildPlaySection() {
    final cs = Theme.of(context).colorScheme;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '播放',
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: cs.onSurface,
          ),
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            if (_videoFiles.length > 1)
              Expanded(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12),
                  decoration: BoxDecoration(
                    color: cs.surfaceContainerHighest,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<int>(
                      value: _selectedVideoIndex,
                      isExpanded: true,
                      dropdownColor: cs.surfaceContainerHighest,
                      style: TextStyle(color: cs.onSurface, fontSize: 13),
                      items: List.generate(_videoFiles.length, (i) {
                        return DropdownMenuItem(
                          value: i,
                          child: Text(
                            _videoLabel(_videoFiles[i]),
                            overflow: TextOverflow.ellipsis,
                          ),
                        );
                      }),
                      onChanged: (v) {
                        if (v != null) setState(() => _selectedVideoIndex = v);
                      },
                    ),
                  ),
                ),
              )
            else
              Expanded(
                child: Text(
                  _videoLabel(_videoFiles.first),
                  style: TextStyle(fontSize: 13, color: cs.onSurfaceVariant),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            const SizedBox(width: 8),
            ElevatedButton.icon(
              onPressed: () {
                final file = _videoFiles[_selectedVideoIndex];
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => VideoPlayPage(
                      fileId: file.id,
                      itemId: widget.mediaId,
                      title: file.name ?? '',
                    ),
                  ),
                );
              },
              icon: const Icon(Icons.play_arrow, size: 20),
              label: const Text('播放'),
              style: ElevatedButton.styleFrom(
                backgroundColor: cs.primary,
                foregroundColor: cs.onPrimary,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildFilesSection() {
    final cs = Theme.of(context).colorScheme;
    final files = _media!.files;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: Text(
            '文件',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: cs.onSurface,
            ),
          ),
        ),
        const SizedBox(height: 12),
        SizedBox(
          height: 180,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            physics: const BouncingScrollPhysics(),
            padding: const EdgeInsets.symmetric(horizontal: 16),
            itemCount: files.length,
            itemBuilder: (context, index) => _buildFileCard(files[index]),
          ),
        ),
      ],
    );
  }

  Widget _buildFileCard(FileInfo file) {
    final cs = Theme.of(context).colorScheme;
    final sizeStr = file.size != null ? _formatFileSize(file.size!) : '未知大小';
    final codec = file.ffmpeg != null ? (file.ffmpeg!['codec'] ?? '') : '';
    final fileUrl = TokenCache.withToken(
      '${_mediaApi?.baseUrl ?? AppConstants.defaultBaseUrl}/api/file/data?file_id=${file.id}',
    );
    return Container(
      width: 180,
      margin: const EdgeInsets.only(right: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: cs.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: cs.outlineVariant),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            file.name ?? '未知文件',
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.bold,
              color: cs.onSurface,
              height: 1.3,
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 6),
          if (file.type != null)
            Text(
              file.type!,
              style: TextStyle(fontSize: 11, color: cs.onSurfaceVariant),
            ),
          if (sizeStr.isNotEmpty)
            Text(
              sizeStr,
              style: TextStyle(fontSize: 11, color: cs.onSurfaceVariant),
            ),
          if (codec.isNotEmpty)
            Text(codec, style: TextStyle(fontSize: 11, color: cs.primary)),
          const Spacer(),
          Row(
            children: [
              _buildFileAction(Icons.content_copy, '复制链接', () {
                Clipboard.setData(ClipboardData(text: fileUrl));
                ScaffoldMessenger.of(
                  context,
                ).showSnackBar(const SnackBar(content: Text('链接已复制')));
              }),
              const SizedBox(width: 8),
              _buildFileAction(Icons.download, '下载', () {
                final uri = Uri.tryParse(fileUrl);
                if (uri != null) {
                  launchUrl(uri, mode: LaunchMode.externalApplication);
                }
              }),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildFileAction(
    IconData icon,
    String tooltip,
    VoidCallback onPressed,
  ) {
    final cs = Theme.of(context).colorScheme;
    return SizedBox(
      width: 32,
      height: 32,
      child: IconButton(
        padding: EdgeInsets.zero,
        icon: Icon(icon, size: 16, color: cs.onSurfaceVariant),
        tooltip: tooltip,
        onPressed: onPressed,
        style: IconButton.styleFrom(
          backgroundColor: cs.surfaceContainerHighest,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
        ),
      ),
    );
  }

  String _formatFileSize(int bytes) {
    if (bytes < 1024) return '$bytes B';
    if (bytes < 1024 * 1024) return '${(bytes / 1024).toStringAsFixed(1)} KB';
    if (bytes < 1024 * 1024 * 1024) {
      return '${(bytes / (1024 * 1024)).toStringAsFixed(1)} MB';
    }
    return '${(bytes / (1024 * 1024 * 1024)).toStringAsFixed(1)} GB';
  }

  Widget _buildTag(String text, Color color) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
    decoration: BoxDecoration(
      color: color.withValues(alpha: 0.2),
      borderRadius: BorderRadius.circular(4),
      border: Border.all(color: color.withValues(alpha: 0.4)),
    ),
    child: Text(
      text,
      style: TextStyle(fontSize: 12, color: color, fontWeight: FontWeight.w500),
    ),
  );
}
