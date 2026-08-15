<template>
  <div class="season-card" @click="handleClick">
    <div class="season-poster">
      <AdaptiveImage :src="primaryImageUrl" :alt="item.name">
        <div class="season-placeholder"><el-icon :size="32"><Film /></el-icon></div>
      </AdaptiveImage>
    </div>
    <div class="season-info">
      <h3>{{ item.name }}</h3>
      <p v-if="item.overview" class="text-secondary">{{ item.overview }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Film } from '@element-plus/icons-vue'
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
.season-card {
  display: flex; gap: 16px; padding: 16px;
  background: var(--imm-hover); border: 1px solid var(--imm-divider);
  border-radius: 12px; cursor: pointer; transition: all 0.3s ease;

  &:hover {
    background: var(--imm-hover-strong); border-color: var(--imm-accent);
    transform: translateX(4px);
  }
}

.season-poster {
  width: 120px; aspect-ratio: 3/5; border-radius: 8px; overflow: hidden;
  flex-shrink: 0; background: var(--imm-bg-tertiary); position: relative;
}

.season-placeholder {
  width: 100%; height: 100%; display: flex; align-items: center;
  justify-content: center; color: var(--imm-text-disabled);
}

.season-info {
  flex: 1; min-width: 0;
  h3 { font-size: 1rem; font-weight: 600; margin: 0 0 4px; }
}

.text-secondary {
  font-size: 0.875rem; color: var(--imm-text-tertiary); line-height: 1.5;
  margin: 4px 0 0; display: -webkit-box; -webkit-line-clamp: 2;
  -webkit-box-orient: vertical; overflow: hidden;
}
</style>