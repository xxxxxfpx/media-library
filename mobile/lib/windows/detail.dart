import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';
import '../core/constants.dart';
import '../core/app_logger.dart';
import '../core/token_cache.dart';
import '../data/api/api_client.dart';
import '../data/api/media_api.dart';
import '../data/models/media.dart';
import '../component/media_card.dart';
import '../component/media_tag.dart';
import '../design_system/app_color_tokens.dart';
import '../phone/video_play.dart';

class DetailPageWindows extends StatefulWidget {
  final int mediaId;

  const DetailPageWindows({super.key, required this.mediaId});

  @override
  State<DetailPageWindows> createState() => _DetailPageWindowsState();
}

class _DetailPageWindowsState extends State<DetailPageWindows> {
  bool _isFavorite = false;
  bool _isLoading = true;
  MediaItem? _media;
  int _selectedVideoIndex = 0;

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
    _initApi();
  }

  Future<void> _initApi() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final api = MediaApi(ApiClient(prefs));
      final data = await api.getInfo(widget.mediaId);
      if (mounted) {
        setState(() {
          _media = data;
          _isFavorite = data.userdata?.favoritedAt != null;
          _isLoading = false;
        });
      }
    } catch (error, stackTrace) {
      AppLogger.error(
        'windows_media_detail_load_failed',
        error: error,
        stackTrace: stackTrace,
        category: 'media',
        fields: {'media_id': widget.mediaId},
      );
      if (mounted) setState(() => _isLoading = false);
    }
  }

  void _toggleFavorite() {
    setState(() {
      _isFavorite = !_isFavorite;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.surface,
      body: _isLoading
          ? Center(child: CircularProgressIndicator(color: Theme.of(context).colorScheme.onSurface))
          : _media == null
          ? Center(
              child: Text('加载失败', style: TextStyle(color: Theme.of(context).colorScheme.onSurfaceVariant)),
            )
          : SafeArea(
              top: false,
              child: SingleChildScrollView(
                child: Column(
                  children: [
                    _buildMediaInfoSection(),
                    if (_videoFiles.isNotEmpty) ...[
                      Divider(color: Theme.of(context).colorScheme.outlineVariant, height: 1),
                      _buildPlaySection(),
                    ],
                    Divider(color: Theme.of(context).colorScheme.outlineVariant, height: 1),
                    SizedBox(height: 48, child: _buildUserMediaData()),
                    Divider(color: Theme.of(context).colorScheme.outlineVariant, height: 1),
                    _buildLinksSection(),
                    if (_media!.files.isNotEmpty) ...[
                      Divider(color: Theme.of(context).colorScheme.outlineVariant, height: 1),
                      _buildFilesSection(),
                    ],
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildMediaInfoSection() {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildImageSection(),
        Expanded(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: _buildBasicInfo(),
          ),
        ),
      ],
    );
  }

  Widget _buildImageSection() {
    return Padding(
      padding: const EdgeInsets.only(left: 12, top: 12),
      child: MediaCard(
        media: _media!,
        config: const CardConfig(
          showProgress: false,
          showScore: true,
          showTitle: false,
        ),
      ),
    );
  }

  Widget _buildBasicInfo() {
    final m = _media!;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          crossAxisAlignment: CrossAxisAlignment.baseline,
          textBaseline: TextBaseline.alphabetic,
          children: [
            Flexible(
              child: Text(
                m.name ?? '未知标题',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Theme.of(context).colorScheme.onSurface,
                ),
              ),
            ),
            const SizedBox(width: 8),
            if (_sourceUrl != null)
              GestureDetector(
                onTap: () async {
                  final uri = Uri.tryParse(_sourceUrl!);
                  if (uri != null && await canLaunchUrl(uri)) {
                    launchUrl(uri, mode: LaunchMode.externalApplication);
                  }
                },
                child: Container(
                  padding: const EdgeInsets.all(4),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: Theme.of(context).colorScheme.onSurfaceVariant, width: 1),
                  ),
                  child: Icon(
                    Icons.language,
                    size: 16,
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                ),
              ),
            const SizedBox(width: 6),
            GestureDetector(
              onTap: () {
                _toggleFavorite();
              },
              child: Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  color: _isFavorite
                      ? Theme.of(context).extension<AppSemanticColors>()!.favorite.withValues(alpha: 0.8)
                      : Colors.transparent,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(
                    color: _isFavorite ? Theme.of(context).extension<AppSemanticColors>()!.favorite : Theme.of(context).colorScheme.onSurfaceVariant,
                    width: 1,
                  ),
                ),
                child: Icon(
                  _isFavorite ? Icons.favorite : Icons.favorite_border,
                  size: 16,
                  color: _isFavorite ? Theme.of(context).colorScheme.onSurface : Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
            ),
          ],
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
                      color: Theme.of(context).colorScheme.outlineVariant,
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Text(
                      a.name ?? '',
                      style: TextStyle(
                        fontSize: 11,
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
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
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
        ],
        const SizedBox(height: 12),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          alignment: WrapAlignment.start,
          children: [
            if (m.officialRating != null)
              _buildTag(m.officialRating!, Theme.of(context).extension<AppSemanticColors>()!.warning),
            if (m.productionYear != null)
              _buildTag('${m.productionYear}', Theme.of(context).extension<AppSemanticColors>()!.info),
            if (m.runTimeTicks != null)
              _buildTag(
                '${(m.runTimeTicks! / 600000000).round()} 分钟',
                Theme.of(context).extension<AppSemanticColors>()!.success,
              ),
            if (m.type != null) _buildTag(m.type!, Theme.of(context).colorScheme.primary),
          ],
        ),
        if (m.overview != null && m.overview!.isNotEmpty) ...[
          const SizedBox(height: 16),
          Text(
            '简介',
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            m.overview!,
            style: TextStyle(
              fontSize: 13,
              color: Theme.of(context).colorScheme.onSurfaceVariant,
              height: 1.5,
            ),
            maxLines: 5,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ],
    );
  }

  String _formatTicks(int? ticks) {
    if (ticks == null || ticks <= 0) return '--:--:--';
    final seconds = ticks ~/ 10000000;
    final h = seconds ~/ 3600;
    final m = (seconds % 3600) ~/ 60;
    final s = seconds % 60;
    return '${h.toString().padLeft(2, '0')}:${m.toString().padLeft(2, '0')}:${s.toString().padLeft(2, '0')}';
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

  Widget _buildUserMediaData() {
    final userdata = _media!.userdata;
    if (userdata == null) return const SizedBox.shrink();

    final runtimeSeconds = _media!.runTimeTicks != null
        ? _media!.runTimeTicks! ~/ 10000000
        : 0;
    final playedSeconds = userdata.playbackPositionTicks != null
        ? userdata.playbackPositionTicks! ~/ 10000000
        : 0;
    final progress = runtimeSeconds > 0 ? playedSeconds / runtimeSeconds : 0.0;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              if (userdata.favoritedAt != null)
                _buildInfoChip(Icons.favorite, '已收藏', Theme.of(context).extension<AppSemanticColors>()!.favorite),
              if (userdata.favoritedAt != null) const SizedBox(width: 12),
              if (userdata.rating != null)
                _buildInfoChip(
                  Icons.star,
                  userdata.rating!.toStringAsFixed(1),
                  Theme.of(context).extension<AppSemanticColors>()!.rating,
                ),
              if (userdata.rating != null) const SizedBox(width: 12),
              _buildInfoChip(
                Icons.play_arrow,
                '播放 ${userdata.playCount ?? 0} 次',
                Theme.of(context).extension<AppSemanticColors>()!.success,
              ),
              const SizedBox(width: 12),
              _buildInfoChip(
                Icons.history,
                userdata.lastPlayedDisplay ?? '未播放',
                Theme.of(context).extension<AppSemanticColors>()!.info,
              ),
            ],
          ),
          if (runtimeSeconds > 0 || playedSeconds > 0) ...[
            const SizedBox(height: 10),
            Row(
              children: [
                Text(
                  _formatTicks(userdata.playbackPositionTicks),
                  style: TextStyle(fontSize: 12, color: Theme.of(context).colorScheme.primary),
                ),
                if (runtimeSeconds > 0) ...[
                  Text(
                    ' / ',
                    style: TextStyle(fontSize: 12, color: Theme.of(context).colorScheme.onSurfaceVariant.withValues(alpha: 0.4)),
                  ),
                  Text(
                    _formatTicks(_media!.runTimeTicks),
                    style: TextStyle(fontSize: 12, color: Theme.of(context).colorScheme.primary),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(4),
                      child: LinearProgressIndicator(
                        value: progress,
                        backgroundColor: Theme.of(context).colorScheme.outlineVariant,
                        valueColor: AlwaysStoppedAnimation(Theme.of(context).colorScheme.primary),
                        minHeight: 6,
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    '${(progress * 100).toStringAsFixed(0)}%',
                    style: TextStyle(fontSize: 12, color: Theme.of(context).colorScheme.primary),
                  ),
                ],
              ],
            ),
          ],
        ],
      ),
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
    final groupedLinks = <String, List<LinkInfo>>{};
    for (final link in _media!.links) {
      final key =
          link.peopleType ??
          link.peopleRole ??
          link.linkedItem?.type ??
          'Other';
      final label = _linkTypeNames[key] ?? key;
      groupedLinks.putIfAbsent(label, () => []).add(link);
    }
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '关联内容',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.onSurface,
            ),
          ),
          const SizedBox(height: 12),
          ...groupedLinks.entries.map(
            (entry) => _buildLinkGroup(entry.key, entry.value),
          ),
        ],
      ),
    );
  }

  Widget _buildLinkGroup(String label, List<LinkInfo> links) {
    final tagItems = <LinkInfo>[];
    final cardItems = <LinkInfo>[];
    for (final link in links) {
      if (link.linkedItem?.primaryImage != null) {
        cardItems.add(link);
      } else {
        tagItems.add(link);
      }
    }
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(bottom: 8),
          child: Text(
            label,
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: Theme.of(context).colorScheme.primary,
            ),
          ),
        ),
        if (tagItems.isNotEmpty)
          Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Wrap(
              spacing: 8,
              runSpacing: 6,
              alignment: WrapAlignment.start,
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
              scrollDirection: Axis.horizontal,
              physics: const BouncingScrollPhysics(),
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
        const SizedBox(height: 12),
      ],
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
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '播放',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.onSurface,
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
                      color: Theme.of(context).colorScheme.outlineVariant,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: DropdownButtonHideUnderline(
                      child: DropdownButton<int>(
                        value: _selectedVideoIndex,
                        isExpanded: true,
                        dropdownColor: Theme.of(context).colorScheme.surfaceContainerHighest,
                        style: TextStyle(
                          color: Theme.of(context).colorScheme.onSurface,
                          fontSize: 13,
                        ),
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
                          if (v != null) {
                            setState(() => _selectedVideoIndex = v);
                          }
                        },
                      ),
                    ),
                  ),
                )
              else
                Expanded(
                  child: Text(
                    _videoLabel(_videoFiles.first),
                    style: TextStyle(fontSize: 13, color: Theme.of(context).colorScheme.onSurfaceVariant),
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
                icon: Icon(Icons.play_arrow, size: 20),
                label: Text('播放'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Theme.of(context).colorScheme.primary,
                  foregroundColor: Theme.of(context).colorScheme.onSurface,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildFilesSection() {
    final files = _media!.files;
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '文件',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.onSurface,
            ),
          ),
          const SizedBox(height: 12),
          SizedBox(
            height: 180,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              physics: const BouncingScrollPhysics(),
              itemCount: files.length,
              itemBuilder: (context, index) => _buildFileCard(files[index]),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFileCard(FileInfo file) {
    final sizeStr = file.size != null ? _formatFileSize(file.size!) : '未知大小';
    final codec = file.ffmpeg != null ? (file.ffmpeg!['codec'] ?? '') : '';
    final fileUrl = TokenCache.withToken(
      '${AppConstants.defaultBaseUrl}/api/file/data?file_id=${file.id}',
    );
    return Container(
      width: 180,
      margin: const EdgeInsets.only(right: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.outlineVariant,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Theme.of(context).colorScheme.outlineVariant.withValues(alpha: 0.5)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            file.name ?? '未知文件',
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.onSurface,
              height: 1.3,
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 6),
          if (file.type != null)
            Text(
              file.type!,
              style: TextStyle(fontSize: 11, color: Theme.of(context).colorScheme.onSurfaceVariant),
            ),
          if (sizeStr.isNotEmpty)
            Text(
              sizeStr,
              style: TextStyle(fontSize: 11, color: Theme.of(context).colorScheme.onSurfaceVariant),
            ),
          if (codec.isNotEmpty)
            Text(
              codec,
              style: TextStyle(fontSize: 11, color: Theme.of(context).colorScheme.primary),
            ),
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
    return SizedBox(
      width: 32,
      height: 32,
      child: IconButton(
        padding: EdgeInsets.zero,
        icon: Icon(icon, size: 16, color: Theme.of(context).colorScheme.onSurfaceVariant),
        tooltip: tooltip,
        onPressed: onPressed,
        style: IconButton.styleFrom(
          backgroundColor: Theme.of(context).colorScheme.surfaceContainerHighest.withValues(alpha: 0.3),
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