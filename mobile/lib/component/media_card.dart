import 'package:cached_network_image/cached_network_image.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import '../data/models/media.dart';
import '../core/constants.dart';
import '../core/token_cache.dart';
import '../design_system/app_icons.dart';
import '../design_system/app_theme.dart';
import '../phone/detail.dart';

class CardConfig {
  /// 是否允许点击跳转详情页
  final bool enableClick;

  /// 是否显示播放进度条
  final bool showProgress;

  /// 是否显示评分
  final bool showScore;

  /// 是否显示标题
  final bool showTitle;

  /// 是否显示媒体类型标签
  final bool showType;

  const CardConfig({
    this.enableClick = true,
    this.showProgress = true,
    this.showScore = true,
    this.showTitle = true,
    this.showType = true,
  });
}

class MediaCard extends StatelessWidget {
  static final Map<MediaType, IconData> _mediaTypeIcons = {
    MediaType.Movie: AppIcons.movie,
    MediaType.Series: AppIcons.series,
    MediaType.Season: AppIcons.season,
    MediaType.Episode: AppIcons.episode,
    MediaType.Audio: AppIcons.audio,
    MediaType.Photo: AppIcons.photo,
    MediaType.Book: AppIcons.book,
    MediaType.Person: AppIcons.person,
    MediaType.Source: AppIcons.source,
    MediaType.Studio: AppIcons.studio,
    MediaType.Genre: AppIcons.genre,
    MediaType.Tag: AppIcons.tag,
    MediaType.BoxSet: AppIcons.boxSet,
    MediaType.unknown: AppIcons.unknown,
  };
  final MediaItem media;
  final CardConfig config;
  final String? imageBaseUrl;

  const MediaCard({
    super.key,
    required this.media,
    required this.config,
    this.imageBaseUrl,
  });

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return GestureDetector(
      onTap: config.enableClick
          ? () => Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => DetailPagePhone(mediaId: media.id),
                ),
              )
          : null,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(
            child: AspectRatio(
              aspectRatio: 0.65,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: Stack(
                  children: [
                    Positioned.fill(child: _buildImageStack(cs)),
                    Positioned.fill(child: _buildInfoOverlay(context, cs)),
                  ],
                ),
              ),
            ),
          ),
          if (config.showTitle) ...[
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 4),
              child: Text(
                media.name ?? '',
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.bold,
                  color: cs.onSurface,
                ),
                textAlign: TextAlign.center,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildNoImageFallback(ColorScheme cs) {
    final iconData = _mediaTypeIcons[media.mediaType] ?? Icons.help_outline;
    return Container(
      decoration: BoxDecoration(
        color: cs.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(iconData, size: 36, color: cs.onSurfaceVariant),
            const SizedBox(height: 4),
            Text(
              media.mediaType.labelZH,
              style: TextStyle(fontSize: 11, color: cs.onSurfaceVariant),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildImageStack(ColorScheme cs) {
    final relativeUrl = media.getPrimaryImageUrl(token: TokenCache.accessToken);
    final base = imageBaseUrl ?? AppConstants.defaultBaseUrl;
    final imageUrl = relativeUrl != null ? '$base$relativeUrl' : null;

    if (imageUrl == null || imageUrl.isEmpty) {
      return _buildNoImageFallback(cs);
    }

    final imageProvider = CachedNetworkImageProvider(imageUrl);

    return RepaintBoundary(
      child: Stack(
        children: [
          Positioned.fill(
            child: ImageFiltered(
              imageFilter: ImageFilter.blur(sigmaX: 11, sigmaY: 11),
              child: Image(
                image: imageProvider,
                fit: BoxFit.fill,
                errorBuilder: (_, _, _) => _buildNoImageFallback(cs),
              ),
            ),
          ),
          Positioned.fill(
            child: Container(
              color: cs.scrim.withValues(alpha: 0.2),
            ),
          ),
          Center(
            child: Image(
              image: imageProvider,
              fit: BoxFit.contain,
              errorBuilder: (_, _, _) => _buildNoImageFallback(cs),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoOverlay(BuildContext context, ColorScheme cs) {
    final semantic = context.semantic;
    return Stack(
      children: [
        // 显示媒体类型标签
        if (config.showType)
          Positioned(
            top: 4,
            left: 4,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 2),
              decoration: BoxDecoration(
                color: cs.primary.withValues(alpha: 0.8),
                borderRadius: BorderRadius.circular(5),
                border: Border.all(color: cs.onPrimary.withValues(alpha: 0.3), width: 1),
              ),
              child: Text(
                media.mediaType.labelZH,
                style: TextStyle(
                  color: cs.onPrimary,
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        // 显示评分
        if (config.showScore)
          Positioned(
            top: 4,
            right: 4,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
              decoration: BoxDecoration(
                color: cs.surfaceContainerHighest.withValues(alpha: 0.85),
                borderRadius: BorderRadius.circular(6),
              ),
              child: Text(
                (media.communityRating ?? 0).toStringAsFixed(1),
                style: TextStyle(
                  color: semantic.rating,
                  fontSize: 11,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
          // 显示播放进度条
        if (config.showProgress && media.userdata != null && media.runTimeTicks != null)
          Positioned(
            bottom: 8,
            left: 6,
            right: 6,
            child: ClipRRect(
              borderRadius: const BorderRadius.only(
                bottomLeft: Radius.circular(16),
                bottomRight: Radius.circular(16),
              ),
              child: LinearProgressIndicator(
                value: (media.userdata?.playbackPositionTicks ?? 0) / (media.runTimeTicks ?? 1),
                backgroundColor: cs.onSurface.withValues(alpha: 0.3),
                valueColor: AlwaysStoppedAnimation(cs.primary.withValues(alpha: 0.8)),
                minHeight: 3,
              ),
            ),
          ),
      ],
    );
  }
}