<template>
  <div class="recent-container">
    <MediaGrid
      :params="{ sort_by: 'date_created', limit: 60 }"
      :pagination="{ pageSize: 24, pageSizes: [24, 48, 60], layout: 'total, prev, pager, next' }"
      empty-text="暂无最近添加内容"
      empty-action="去媒体库添加"
      empty-action-to="/library"
    />
  </div>
</template>

<script setup>
import MediaGrid from '@/components/MediaGrid.vue'
</script>

<style scoped lang="scss">
.recent-container {
  padding: 14px 16px 20px;

  @media (max-width: 768px) {
    padding: 10px 12px 16px;
  }
}
</style>
