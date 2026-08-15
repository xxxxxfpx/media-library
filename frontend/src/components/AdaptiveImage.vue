<template>
  <div class="adaptive-image" :class="`mode-${mode}`" :style="cssVars">
    <img v-if="src" :src="src" :alt="alt" class="ai-bg" loading="lazy" aria-hidden="true" />
    <img v-if="src" :src="src" :alt="alt" class="ai-fg" loading="lazy" />
    <slot v-if="!src" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  src: { type: String, default: '' },
  alt: { type: String, default: '' },
  blur: { type: Number, default: 20 },
  feather: { type: Number, default: 4 },
  mode: { type: String, default: 'contain', validator: v => ['contain', 'cover'].includes(v) }
})

const cssVars = computed(() => ({
  '--ai-blur': props.blur + 'px',
  '--ai-feather': props.feather + '%'
}))
</script>

<style scoped lang="scss">
.adaptive-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.ai-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: fill;
  filter: blur(var(--ai-blur));
  pointer-events: none;
}

.ai-fg {
  position: relative;
  width: 100%;
  height: 100%;
  object-fit: contain;
  z-index: 1;
  pointer-events: none;
  -webkit-mask-image:
    linear-gradient(to right, transparent, black var(--ai-feather), black calc(100% - var(--ai-feather)), transparent),
    linear-gradient(to bottom, transparent, black var(--ai-feather), black calc(100% - var(--ai-feather)), transparent);
  mask-image:
    linear-gradient(to right, transparent, black var(--ai-feather), black calc(100% - var(--ai-feather)), transparent),
    linear-gradient(to bottom, transparent, black var(--ai-feather), black calc(100% - var(--ai-feather)), transparent);
  -webkit-mask-composite: source-in;
  mask-composite: intersect;
}

// Cover 模式 - 图片填满容器，无羽化
.mode-cover .ai-fg {
  object-fit: cover;
  -webkit-mask-image: none;
  mask-image: none;
}
</style>
