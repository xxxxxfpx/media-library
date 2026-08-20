<template>
  <div class="library-container">
    <MediaGrid empty-text="暂无媒体内容" />
  </div>
</template>

<script setup>
import MediaGrid from '@/components/MediaGrid.vue'
</script>

<style scoped lang="scss">
.library-container {
  padding: 14px 16px 20px;
  min-height: 100%;

  @media (max-width: 768px) {
    padding: 10px 12px 16px;
  }
}
</style>
