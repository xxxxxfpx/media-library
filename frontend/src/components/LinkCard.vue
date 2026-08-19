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
  padding: 16px;
  background: var(--imm-hover);
  border: 1px solid var(--imm-divider);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: var(--imm-hover-strong);
    border-color: var(--imm-accent);
    transform: translateY(-2px);
  }
}

.link-icon { margin-bottom: 8px; color: var(--imm-accent); }
.link-name { font-size: 0.9375rem; font-weight: 600; margin-bottom: 4px; }
.link-type { font-size: 0.8125rem; color: var(--imm-text-tertiary); }
</style>