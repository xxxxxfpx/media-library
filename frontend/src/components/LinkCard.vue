<template>
  <div class="link-card" @click="handleClick">
    <div class="link-icon">
      <AppIcon name="film" :size="20" />
    </div>
    <div class="link-name">{{ item.name }}</div>
    <div v-if="subType" class="link-type">{{ subType }}</div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import AppIcon from '@/components/ui/AppIcon.vue'

const props = defineProps({
  item: { type: Object, required: true },
  subType: { type: String, default: '' }
})

const router = useRouter()

function handleClick() {
  if (props.item.id) {
    router.push(`/media/${props.item.id}`)
  }
}
</script>

<style scoped lang="scss">
.link-card {
  padding: 12px 14px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-subtle);
  border-radius: 12px;
  cursor: pointer;
  transition: all var(--duration-base) var(--ease-standard);

  &:hover {
    background: var(--color-hover-strong);
    border-color: var(--video-card-border-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
  }
}

.link-icon { margin-bottom: 6px; color: var(--color-accent); }
.link-name { font-size: 0.875rem; font-weight: 650; margin-bottom: 2px; letter-spacing: -0.01em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.link-type { font-size: 0.72rem; color: var(--color-text-tertiary); font-weight: 500; }
</style>