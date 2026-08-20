<template>
  <div class="favorites-container">
    <MediaGrid
      :params="{ favorite: true, sort_by: 'name' }"
      empty-text="暂无收藏内容"
      empty-action="去媒体库逛逛"
      empty-action-to="/library"
    />
  </div>
</template>

<script setup>
import MediaGrid from '@/components/MediaGrid.vue'
</script>

<style scoped lang="scss">
.favorites-container {
  padding: 14px 16px 20px;

  @media (max-width: 768px) {
    padding: 10px 12px 16px;
  }
}
</style>
