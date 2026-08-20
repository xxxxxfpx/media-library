<template>
  <div class="recent-container">
    <!-- 页面标题横幅 -->
    <div class="page-header">
      <div class="page-title">
        <AppIcon name="clock" :size="18" />
        <span>最近添加</span>
      </div>
    </div>

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
import AppIcon from '@/components/ui/AppIcon.vue'
</script>

<style scoped lang="scss">
.recent-container {
  padding: 14px 16px 20px;

  @media (max-width: 768px) {
    padding: 10px 12px 16px;
  }
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 14px;
  padding: 0 2px;
  border-bottom: 2px solid var(--color-accent);
  padding-bottom: 10px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.015em;
}
</style>
