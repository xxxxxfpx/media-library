<template>
  <div class="episode-item" @click="handleClick">
    <div class="episode-thumb">
      <AdaptiveImage :src="primaryImageUrl" :alt="item.name">
        <div class="episode-placeholder"><AppIcon name="video" :size="24" /></div>
      </AdaptiveImage>
    </div>
    <div class="episode-info">
      <div class="episode-header">
        <span class="episode-num">E{{ item.index_number || '?' }}</span>
        <h4>{{ item.name }}</h4>
      </div>
      <p v-if="item.overview" class="text-secondary">{{ item.overview }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import AppIcon from '@/components/ui/AppIcon.vue'
import AdaptiveImage from '@/components/AdaptiveImage.vue'
import { getPrimaryImageUrl } from '@/utils/url'

const props = defineProps({ item: { type: Object, required: true } })
const router = useRouter()

const primaryImageUrl = computed(() => getPrimaryImageUrl(props.item))

function handleClick() {
  router.push(`/media/${props.item.id}`)
}
</script>

<style scoped lang="scss">
.episode-item {
  display: flex; gap: 16px; padding: 12px 16px;
  background: var(--imm-hover); border: 1px solid var(--imm-divider);
  border-radius: 10px; cursor: pointer; transition: all 0.3s ease;

  &:hover {
    background: var(--imm-hover-strong); border-color: var(--color-border-subtle);
    transform: translateX(4px);
  }
}

.episode-thumb {
  width: 160px; aspect-ratio: 16/9; border-radius: 8px; overflow: hidden;
  flex-shrink: 0; background: var(--imm-bg-tertiary); position: relative;
}

.episode-placeholder {
  width: 100%; height: 100%; display: flex; align-items: center;
  justify-content: center; color: var(--imm-text-disabled);
}

.episode-info { flex: 1; min-width: 0; }

.episode-header {
  display: flex; align-items: center; gap: 8px; margin-bottom: 4px;
  h4 { font-size: 0.9375rem; font-weight: 600; margin: 0; }
}

.episode-num {
  font-size: 0.8125rem; font-weight: 700; color: var(--imm-accent);
  padding: 2px 8px; background: var(--imm-accent-bg);
  border-radius: 4px; flex-shrink: 0;
}

.text-secondary {
  font-size: 0.875rem; color: var(--imm-text-tertiary); line-height: 1.5;
  margin: 4px 0 0; display: -webkit-box; -webkit-line-clamp: 2;
  -webkit-box-orient: vertical; overflow: hidden;
}
</style>