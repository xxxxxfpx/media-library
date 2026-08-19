<script setup>
/**
 * 主题切换器：色板预览式选择 6 套主题。
 * 使用 lucide 图标（AppIcon）与语义令牌，全程无硬编码颜色、无 Unicode 图标。
 */
import { computed } from 'vue'
import { useAppStore } from '@/store'
import AppIcon from '@/components/ui/AppIcon.vue'

const store = useAppStore()
const themes = store.themes
const current = computed(() => themes.find((t) => t.id === store.theme) || themes[0])

function onSelect(id) {
  store.setTheme(id)
}
</script>

<template>
  <el-dropdown trigger="click" popper-class="theme-dropdown" @command="onSelect">
    <button class="trigger" type="button" :aria-label="`当前主题：${current.name}`">
      <AppIcon name="palette" :size="18" />
    </button>
    <template #dropdown>
      <div class="theme-grid">
        <div
          v-for="t in themes"
          :key="t.id"
          class="theme-card"
          :class="{ active: t.id === current.id }"
          @click="onSelect(t.id)"
        >
          <div class="swatches">
            <span class="sw" :style="{ background: t.swatch.page }" />
            <span class="sw" :style="{ background: t.swatch.surface }" />
            <span class="sw" :style="{ background: t.swatch.accent }" />
          </div>
          <div class="meta">
            <span class="name">{{ t.name }}</span>
            <AppIcon v-if="t.id === current.id" name="check" :size="14" class="tick" />
          </div>
        </div>
      </div>
    </template>
  </el-dropdown>
</template>

<style scoped lang="scss">
.trigger {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  background: var(--color-hover);
  border: 1px solid var(--color-border-default);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition:
    background var(--duration-fast) var(--ease-standard),
    color var(--duration-fast) var(--ease-standard),
    border-color var(--duration-fast) var(--ease-standard);

  &:hover {
    background: var(--color-hover-strong);
    color: var(--color-text-primary);
    border-color: var(--color-accent);
  }
}

:deep(.theme-dropdown) {
  background: var(--color-bg-elevated) !important;
  border: 1px solid var(--color-border-default) !important;
  border-radius: var(--radius-lg) !important;
  box-shadow: var(--shadow-lg) !important;
  padding: 10px !important;
}

.theme-grid {
  display: grid;
  grid-template-columns: repeat(2, 132px);
  gap: 8px;
}

.theme-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 10px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-subtle);
  cursor: pointer;
  transition:
    border-color var(--duration-fast) var(--ease-standard),
    background var(--duration-fast) var(--ease-standard),
    transform var(--duration-fast) var(--ease-standard);

  &:hover {
    border-color: var(--color-accent);
    transform: translateY(-2px);
  }

  &.active {
    border-color: var(--color-accent);
    background: var(--color-selected);
  }

  .swatches {
    display: flex;
    gap: 4px;
  }

  .sw {
    flex: 1;
    height: 22px;
    border-radius: 4px;
    border: 1px solid var(--color-border-subtle);
  }

  .meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .name {
    font-size: 0.8125rem;
    color: var(--color-text-primary);
    font-weight: 500;
  }

  .tick {
    color: var(--color-accent);
  }
}
</style>
