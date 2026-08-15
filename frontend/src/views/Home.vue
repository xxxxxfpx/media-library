<template>
  <div class="home-content">
    <!-- 统计卡片 -->
    <div class="stats-section">
      <div
        v-for="stat in stats"
        :key="stat.key"
        class="stat-card"
        :style="{ '--stat-color': stat.color }"
      >
        <div class="stat-icon-wrapper">
          <el-icon :size="18">
            <component :is="stat.icon" />
          </el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ formatNumber(stat.value) }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
        <div class="stat-glow"></div>
      </div>
    </div>

    <!-- 最近添加 -->
    <div class="section">
      <div class="section-header">
        <div class="section-title">
          <el-icon><Clock /></el-icon>
          <span>最近添加</span>
        </div>
        <el-button
          type="primary"
          link
          class="view-all-btn"
          @click="$router.push('/library')"
        >
          查看全部 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>

      <MediaGrid
        :params="{ limit: 12 }"
        :pagination="{ pageSize: 12, pageSizes: [], layout: '' }"
        empty-text="暂无媒体内容"
      >
        <template #empty-action>
          <el-button type="primary" @click="$router.push('/library')">
            浏览媒体库
          </el-button>
        </template>
      </MediaGrid>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { mediaAPI } from '@/api'
import MediaGrid from '@/components/MediaGrid.vue'
import {
  VideoCamera, Headset, Picture, Document, Clock, ArrowRight
} from '@element-plus/icons-vue'

const stats = ref([
  { key: 'video', label: '视频', value: 0, icon: 'VideoCamera', color: '#2196F3' },
  { key: 'audio', label: '音乐', value: 0, icon: 'Headset', color: '#4CAF50' },
  { key: 'image', label: '图片', value: 0, icon: 'Picture', color: '#FF9800' },
  { key: 'book', label: '电子书', value: 0, icon: 'Document', color: '#9C27B0' },
])

function formatNumber(num) {
  return num.toLocaleString('zh-CN')
}

async function fetchData() {
  try {
    const statsData = await mediaAPI.getStats()
    stats.value = [
      { key: 'video', label: '视频', value: statsData.video_count || 0, icon: 'VideoCamera', color: '#2196F3' },
      { key: 'audio', label: '音乐', value: statsData.audio_count || 0, icon: 'Headset', color: '#4CAF50' },
      { key: 'image', label: '图片', value: statsData.image_count || 0, icon: 'Picture', color: '#FF9800' },
      { key: 'book', label: '电子书', value: statsData.book_count || 0, icon: 'Document', color: '#9C27B0' },
    ]
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.home-content {
  padding: 32px;
  min-height: 100%;
}

// 统计卡片
.stats-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 40px;

  @media (max-width: 1200px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  position: relative;
  background: var(--imm-hover);
  border: 1px solid var(--imm-divider);
  border-radius: 16px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 64px;
  overflow: hidden;
  transition: all 0.3s ease;

  &:hover {
    background: var(--imm-hover-strong);
    border-color: var(--imm-border);
    transform: translateY(-2px);

    .stat-glow {
      opacity: 0.15;
    }
  }

  .stat-icon-wrapper {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: var(--imm-accent-bg);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--stat-color, #2196F3);
    flex-shrink: 0;
  }

  .stat-info {
    flex: 1;
    min-width: 0;

    .stat-value {
      font-size: clamp(1rem, 2.5vw, 1.5rem);
      font-weight: 700;
      color: var(--imm-text-primary);
      line-height: 1.2;
      margin-bottom: 2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .stat-label {
      font-size: clamp(0.75rem, 1.5vw, 0.875rem);
      color: var(--imm-text-tertiary);
    }
  }

  .stat-glow {
    position: absolute;
    top: -50%;
    right: -20%;
    width: 150px;
    height: 150px;
    background: var(--stat-color, #2196F3);
    filter: blur(60px);
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
  }
}

// 内容区域
.section {
  background: var(--imm-hover);
  border: 1px solid var(--imm-divider);
  border-radius: 20px;
  padding: 28px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;

  .section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--imm-text-primary);

    .el-icon {
      color: var(--imm-accent);
    }
  }

  .view-all-btn {
    color: var(--imm-text-tertiary) !important;
    font-weight: 500;

    &:hover {
      color: var(--imm-accent) !important;
    }

    .el-icon {
      margin-left: 4px;
      transition: transform 0.3s ease;
    }

    &:hover .el-icon {
      transform: translateX(4px);
    }
  }
}

// 媒体网格
.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 20px;

  .empty-state {
    grid-column: 1 / -1;
    padding: 60px 0;

    :deep(.el-empty__description) {
      color: var(--imm-text-tertiary);
      font-size: 0.9375rem;
    }
  }
}
</style>
