import 'package:flutter/material.dart';
import '../data/models/media.dart';
import '../phone/detail.dart';

/// 媒体标签组件，展示媒体名称，点击跳转详情页
class MediaTag extends StatelessWidget {
  final MediaItem media;

  const MediaTag({super.key, required this.media});

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return GestureDetector(
      onTap: () => Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => DetailPagePhone(mediaId: media.id)),
      ),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: cs.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(6),
          border: Border.all(color: cs.outlineVariant),
        ),
        child: Text(
          media.name ?? '',
          style: TextStyle(fontSize: 12, color: cs.onSurfaceVariant),
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
        ),
      ),
    );
  }
}
