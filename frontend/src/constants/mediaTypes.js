/**
 * 媒体类型常量 - 统一维护类型标签和图标映射
 */

export const TYPE_LABELS = {
  'Movie': '电影',
  'Series': '剧集',
  'Season': '季度',
  'Episode': '单集',
  'Audio': '音乐',
  'Photo': '图片',
  'Book': '图书',
  'Person': '人物',
  'Source': '媒体源',
  'Studio': '工作室',
  'Genre': '类型',
  'Tag': '标签',
  'CollectionFolder': '合集',
  'BoxSet': '合集包',
}

export const TYPE_ICONS = {
  'Movie': 'Film',
  'Series': 'Film',
  'Season': 'Film',
  'Episode': 'Film',
  'Audio': 'Headset',
  'Photo': 'Picture',
  'Book': 'Document',
  'Person': 'User',
  'Source': 'FolderOpened',
  'Studio': 'VideoCamera',
  'Genre': 'Collection',
  'Tag': 'Collection',
  'CollectionFolder': 'Collection',
  'BoxSet': 'Collection',
}

export const TYPE_OPTIONS = Object.entries(TYPE_LABELS).map(([value, label]) => ({
  value,
  label,
}))

export function getTypeLabel(type) {
  return TYPE_LABELS[type] || type || '未知'
}

export function getTypeIconName(type) {
  return TYPE_ICONS[type] || 'VideoCamera'
}
