<template>
  <div class="history-container">
    <MediaGrid
      :params="{ has_playback: true, sort_by: 'last_played' }"
      empty-text="暂无观看记录"
    />
  </div>
</template>

<script setup>
import MediaGrid from '@/components/MediaGrid.vue'
</script>

<style scoped lang="scss">
.history-container {
  padding: 14px 16px 20px;

  @media (max-width: 768px) {
    padding: 10px 12px 16px;
  }
}
</style>
