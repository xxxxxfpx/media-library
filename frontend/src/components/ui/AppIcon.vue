<script setup>
/**
 * 统一图标出口：所有图标只走 AppIcon / <i-lucide-*> 前缀。
 * 图标来自 lucide（unplugin-icons 构建时按需打包），随 currentColor 变色。
 * filled：将描边图标填充为实心（如收藏星标）。
 */
import { computed } from 'vue'
import { iconRegistry } from '@/icons/registry'

const props = defineProps({
  name: { type: String, required: true },
  size: { type: [Number, String], default: 18 },
  strokeWidth: { type: [Number, String], default: 2 },
  filled: { type: Boolean, default: false },
})

const comp = computed(() => iconRegistry[props.name] || null)
</script>

<template>
  <component
    :is="comp"
    v-if="comp"
    :size="size"
    :stroke-width="strokeWidth"
    class="app-icon"
    :class="{ 'app-icon--filled': filled }"
    aria-hidden="true"
  />
</template>

<style scoped>
.app-icon {
  display: inline-flex;
  flex-shrink: 0;
  color: inherit;
  vertical-align: middle;
}

/* 实心模式：填充描边图标（lucide 为 stroke 风格，CSS 可覆盖其 fill 属性） */
.app-icon--filled :deep(svg) {
  fill: currentColor;
  stroke: currentColor;
}
</style>
