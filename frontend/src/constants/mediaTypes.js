/**
 * 媒体类型常量 - 统一维护类型标签和图标映射
 */

import {
  Film, VideoCamera, User, FolderOpened, Collection
} from '@element-plus/icons-vue'

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
  'Movie': 'Film',
  'Series': 'Film',
  'Season': 'Film',
  'Episode': 'Film',
  'Person': 'User',
  'Source': 'FolderOpened',
  'Studio': 'VideoCamera',
  'Genre': 'Collection',
  'Tag': 'Collection',
  'BoxSet': 'Collection',
}

// 图标名称 → 组件引用映射（唯一维护处，供各组件共用）
export const ICON_COMPONENT_MAP = {
  'Film': Film, 'VideoCamera': VideoCamera, 'User': User,
  'FolderOpened': FolderOpened, 'Collection': Collection,
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

export function getTypeIcon(type) {
  const iconName = TYPE_ICONS[type] || 'VideoCamera'
  return ICON_COMPONENT_MAP[iconName] || Film
}
