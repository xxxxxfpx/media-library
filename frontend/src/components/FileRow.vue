<template>
  <div class="file-row">
    <div class="file-icon" :class="fileTypeClass">
      <AppIcon :name="fileIcon" :size="20" />
    </div>
    <div class="file-info">
      <span class="file-name">{{ file.name || file.path?.split('/').pop() }}</span>
      <span v-if="file.path" class="file-path">{{ file.path }}</span>
      <span v-if="file.size" class="file-size">{{ formatFileSize(file.size) }}</span>
    </div>
    <span v-if="file.image_type" class="file-badge">{{ file.image_type }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import AppIcon from '@/components/ui/AppIcon.vue'
import { formatFileSize } from '@/utils/format'

const props = defineProps({
  file: { type: Object, required: true }
})

// 根据文件类型返回对应的图标名（lucide），由 AppIcon 渲染
const fileIcon = computed(() => {
  const type = props.file?.type

  switch (type) {
    case 'Image':
    case 'EmbeddedImage':
      return 'image'
    case 'Video':
      return 'video'
    case 'Audio':
      return 'headphones'
    case 'Subtitle':
    case 'Lyrics':
      return 'message-square'
    case 'Nfo':
      return 'notebook'
    case 'Data':
      return 'chart-line'
    case 'Attachment':
      return 'folder'
    default:
      return 'file-text'
  }
})

// 根据文件类型返回对应的 CSS 类
const fileTypeClass = computed(() => {
  const type = props.file?.type
  return type ? `type-${type.toLowerCase()}` : 'type-other'
})
</script>

<style scoped lang="scss">
.file-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--imm-hover);
  border: 1px solid var(--imm-divider);
  border-radius: 10px;
}

.file-icon {
  color: var(--imm-text-tertiary);
  font-size: 1.25rem;
}

.file-icon.type-image,
.file-icon.type-embeddedimage {
  color: var(--color-success);
}

.file-icon.type-video {
  color: var(--color-accent);
}

.file-icon.type-audio {
  color: var(--color-warning);
}

.file-icon.type-subtitle,
.file-icon.type-lyrics {
  color: var(--color-info);
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-path {
  display: block;
  font-size: 0.6875rem;
  color: var(--imm-text-tertiary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-top: 2px;
  font-family: monospace;
}

.file-size {
  font-size: 0.75rem;
  color: var(--imm-text-tertiary);
}

.file-badge {
  padding: 3px 8px;
  background: var(--imm-accent-bg);
  border-radius: 4px;
  font-size: 0.6875rem;
  color: var(--imm-accent);
  font-weight: 600;
  flex-shrink: 0;
}
</style>
