<template>
  <div class="home-content">
    <!-- 统计卡片 - 紧凑版 -->
    <div v-if="visibleStats.length" class="stats-section">
      <div
        v-for="stat in visibleStats"
        :key="stat.key"
        class="stat-card"
        :style="{ '--stat-color': stat.color }"
      >
        <div class="stat-icon-wrapper">
          <AppIcon :name="stat.icon" :size="16" />
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ formatNumber(stat.value) }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
        <div class="stat-glow"></div>
      </div>
    </div>

    <!-- 最近添加 - 去大圆角空心卡，直接沉浸式陈列 -->
    <div class="section">
      <div class="section-header">
        <div class="section-title">
          <AppIcon name="clock" :size="16" />
          <span>最近添加</span>
          <span class="section-count">精选</span>
        </div>
        <el-button
          type="primary"
          link
          class="view-all-btn"
          @click="$router.push('/library')"
        >
          查看全部 <AppIcon name="arrow-right" :size="13" />
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
import { ref, computed, onMounted } from 'vue'
import { mediaAPI } from '@/api'
import MediaGrid from '@/components/MediaGrid.vue'
import AppIcon from '@/components/ui/AppIcon.vue'

const stats = ref([
  { key: 'video', label: '视频', value: 0, icon: 'video', color: 'var(--color-stat-video)' },
  { key: 'audio', label: '音乐', value: 0, icon: 'headphones', color: 'var(--color-stat-audio)' },
  { key: 'image', label: '图片', value: 0, icon: 'image', color: 'var(--color-stat-image)' },
  { key: 'book', label: '电子书', value: 0, icon: 'book-open', color: 'var(--color-stat-book)' },
])

const visibleStats = computed(() => stats.value.filter(s => s.value > 0))

function formatNumber(num) {
  return num.toLocaleString('zh-CN')
}

async function fetchData() {
  try {
    const statsData = await mediaAPI.getStats()
    stats.value = [
      { key: 'video', label: '视频', value: statsData.video_count || 0, icon: 'video', color: 'var(--color-stat-video)' },
      { key: 'audio', label: '音乐', value: statsData.audio_count || 0, icon: 'headphones', color: 'var(--color-stat-audio)' },
      { key: 'image', label: '图片', value: statsData.image_count || 0, icon: 'image', color: 'var(--color-stat-image)' },
      { key: 'book', label: '电子书', value: statsData.book_count || 0, icon: 'book-open', color: 'var(--color-stat-book)' },
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
  padding: 16px 20px 24px;
  min-height: 100%;
}

// 统计卡片 - 紧凑，去大留白
.stats-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 18px;

  @media (max-width: 1200px) { grid-template-columns: repeat(2, 1fr); }

  @media (max-width: 768px) { grid-template-columns: repeat(2, 1fr); gap: 10px; }

  @media (max-width: 480px) { grid-template-columns: 1fr; }
}

.stat-card {
  position: relative;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-subtle);
  border-radius: 12px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 56px;
  overflow: hidden;
  transition: all var(--duration-base) var(--ease-standard);

  &:hover {
    background: var(--color-hover-strong);
    border-color: var(--color-border-default);
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);

    .stat-glow { opacity: 0.14; }
  }

  .stat-icon-wrapper {
    width: 32px; height: 32px; border-radius: 8px;
    background: var(--color-accent-soft);
    display: flex; align-items: center; justify-content: center;
    color: var(--stat-color); flex-shrink: 0;
  }

  .stat-info {
    flex: 1; min-width: 0;

    .stat-value {
      font-size: 1.15rem; font-weight: 750; color: var(--color-text-primary);
      line-height: 1.15; margin-bottom: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      letter-spacing: -0.02em;
    }

    .stat-label { font-size: 0.74rem; color: var(--color-text-tertiary); font-weight: 500; }
  }

  .stat-glow {
    position: absolute; top: -40%; right: -14%; width: 110px; height: 110px;
    background: var(--stat-color); filter: blur(42px); opacity: 0;
    transition: opacity var(--duration-base) var(--ease-standard); pointer-events: none;
  }
}

// 内容区域 - 去大圆角空心，去留白
.section {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-subtle);
  border-radius: 14px;
  padding: 14px 14px 12px;
}

.section-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 12px; padding: 0 2px;

  .section-title {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.9375rem; font-weight: 700; color: var(--color-text-primary);
    letter-spacing: -0.015em;

    .section-count {
      margin-left: 6px; padding: 2px 7px; border-radius: 999px;
      background: var(--video-chip-bg); border: 1px solid var(--video-chip-border);
      color: var(--color-accent); font-size: 0.68rem; font-weight: 700; letter-spacing: 0.02em;
    }
  }

  .view-all-btn {
    color: var(--color-text-tertiary) !important; font-weight: 600; font-size: 0.8125rem;

    &:hover { color: var(--color-accent) !important; }
    :deep(.app-icon) { margin-left: 4px; transition: transform var(--duration-fast) var(--ease-standard); }
    &:hover :deep(.app-icon) { transform: translateX(3px); }
  }
}
</style>
