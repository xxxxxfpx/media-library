<template>
  <div class="library-container">
    <el-card>
      <MediaGrid empty-text="暂无媒体内容" />
    </el-card>
  </div>
</template>

<script setup>
import MediaGrid from '@/components/MediaGrid.vue'
</script>

<style scoped lang="scss">
.library-container {
  padding: 20px;
}
</style>
