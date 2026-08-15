<template>
  <div class="history-container">

    <el-card>
      <MediaGrid
        :params="{ has_playback: true, sort_by: 'last_played' }"
        empty-text="暂无观看记录"
      />
    </el-card>
  </div>
</template>

<script setup>
import MediaGrid from '@/components/MediaGrid.vue'
</script>

<style scoped lang="scss">
.history-container {
  padding: 20px;
}
</style>
