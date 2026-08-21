<template>
  <div class="home-content">
    <!-- 统计卡片 -->
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { mediaAPI } from '@/api'
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

.stats-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;

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
</style>
