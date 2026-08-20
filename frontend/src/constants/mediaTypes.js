/**
 * 媒体类型常量 - 统一维护类型标签和图标映射
 *
 * 图标统一为 lucide 图标名（字符串），由 AppIcon 渲染；
 * 新增类型只需在 TYPE_ICONS 登记图标名，并在 icons/registry.js 注册对应图标。
 */

export const TYPE_LABELS = {
  'Movie': '电影',
  'Series': '剧集',
  'Season': '季度',
  'Episode': '单集',
  'Person': '人物',
  'Source': '媒体源',
  'Studio': '工作室',
  'Genre': '类型',
  'Tag': '标签',
  'BoxSet': '合集',
}

export const TYPE_ICONS = {
  'Movie': 'film',
  'Series': 'tv',
  'Season': 'layers',
  'Episode': 'play-circle',
  'Person': 'user',
  'Source': 'folder-open',
  'Studio': 'clapperboard',
  'Genre': 'tag',
  'Tag': 'bookmark',
  'BoxSet': 'package',
}

export const TYPE_OPTIONS = Object.entries(TYPE_LABELS).map(([value, label]) => ({
  value,
  label,
}))

export function getTypeLabel(type) {
  return TYPE_LABELS[type] || type || '未知'
}

export function getTypeIconName(type) {
  return TYPE_ICONS[type] || 'clapperboard'
}

// 兼容旧调用方：返回 lucide 图标名（字符串），配合 <AppIcon :name="..."> 使用
export function getTypeIcon(type) {
  return getTypeIconName(type)
}
