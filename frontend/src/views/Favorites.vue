<template>
  <div class="favorites-container">

    <el-card>
      <MediaGrid
        :params="{ favorite: true, sort_by: 'name' }"
        empty-text="暂无收藏内容"
        empty-action="去媒体库逛逛"
        empty-action-to="/library"
      />
    </el-card>
  </div>
</template>

<script setup>
import MediaGrid from '@/components/MediaGrid.vue'
</script>

<style scoped lang="scss">
.favorites-container {
  padding: 20px;
}
</style>
