<template>
  <div class="media-detail">
    <div v-if="loading" class="loading-state">
      <AppIcon name="loader-circle" :size="48" class="loading-icon" />
      <p>加载中...</p>
    </div>

    <template v-else-if="item">
      <!-- ====== 英雄区域 ====== -->
      <div class="hero-section" :class="`type-${itemTypeClass}`" :style="heroBgStyle">
        <div class="hero-gradient"></div>
        <div class="hero-content">
          <button class="back-btn" @click="goBack">
            <AppIcon name="arrow-left" :size="16" />
            <span>返回</span>
          </button>

          <div class="hero-layout">
            <MediaCard
              :item="item"
              class="hero-media-card"
              :setting="heroConfig"
            />

            <div class="hero-info">
              <div class="info-badges">
                <span class="badge type-badge">{{ typeLabel }}</span>
                <span v-if="item.production_year" class="badge year-badge">{{ item.production_year }}</span>
                <span v-if="item.official_rating" class="badge rating-badge-official">{{ item.official_rating }}</span>
                <span v-if="item.community_rating" class="badge rating-badge">
                  <AppIcon name="star" :size="14" :filled="true" /> {{ item.community_rating.toFixed(1) }}
                </span>
                <span v-if="runTimeText" class="badge runtime-badge">{{ runTimeText }}</span>
              </div>

              <div class="hero-title-row">
                <h1 class="hero-title">{{ item.name || '未知' }}</h1>
                <button
                  class="detail-favorite-btn"
                  :class="{ active: isFavorite }"
                  :disabled="favLoading"
                  :title="isFavorite ? '取消收藏' : '加入收藏'"
                  @click="toggleFavorite"
                >
                  <AppIcon :name="'star'" :size="18" :filled="isFavorite" />
                </button>
              </div>

              <p v-if="item.tagline" class="hero-tagline">{{ item.tagline }}</p>

              <div v-if="item.premiere_date || item.end_date" class="hero-dates">
                <span v-if="item.premiere_date">首映: {{ formatDate(item.premiere_date) }}</span>
                <span v-if="item.end_date"> ~ {{ formatDate(item.end_date) }}</span>
              </div>

              <p v-if="item.overview" class="hero-overview">{{ item.overview }}</p>

              <div v-if="castList.length" class="hero-cast">
                <span class="meta-label">演员</span>
                <div class="cast-scroll">
                  <div v-for="actor in castList.slice(0, 10)" :key="actor.id" class="cast-chip" @click="navigateTo(actor.id)">
                    <div class="cast-avatar">{{ actor.name.charAt(0) }}</div>
                    <div class="cast-name">{{ actor.name }}</div>
                    <div v-if="actor.role" class="cast-role">{{ actor.role }}</div>
                  </div>
                </div>
              </div>

              <!-- 视频选择和播放区域 -->
              <div v-if="videoFiles.length" class="hero-video-section">
                <el-select
                  v-model="selectedVideo"
                  value-key="id"
                  placeholder="选择视频版本"
                  class="video-select"
                  size="large"
                >
                  <el-option
                    v-for="video in videoFiles"
                    :key="video.id"
                    :label="video.name || `视频 ${video.id}`"
                    :value="video"
                  />
                </el-select>

                <!-- 视频详情信息 -->
                <div v-if="selectedVideoInfo" class="video-info-grid">
                  <div v-if="selectedVideoInfo.resolution" class="video-info-item">
                    <span class="info-label">分辨率</span>
                    <span class="info-value">{{ selectedVideoInfo.resolution }}</span>
                  </div>
                  <div v-if="selectedVideoInfo.codec" class="video-info-item">
                    <span class="info-label">编码</span>
                    <span class="info-value">{{ selectedVideoInfo.codec }}</span>
                  </div>
                  <div v-if="selectedVideoInfo.bitrate" class="video-info-item">
                    <span class="info-label">码率</span>
                    <span class="info-value">{{ selectedVideoInfo.bitrate }}</span>
                  </div>
                  <div v-if="selectedVideoInfo.duration" class="video-info-item">
                    <span class="info-label">时长</span>
                    <span class="info-value">{{ selectedVideoInfo.duration }}</span>
                  </div>
                  <div v-if="selectedVideoInfo.size" class="video-info-item">
                    <span class="info-label">大小</span>
                    <span class="info-value">{{ selectedVideoInfo.size }}</span>
                  </div>
                </div>

                <button
                  class="imm-play-btn"
                  :disabled="!selectedVideo"
                  @click="playVideo(selectedVideo)"
                >
                  <AppIcon name="play" :size="18" />
                  <span>播放</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ====== 内容主体 ====== -->
      <div class="body-section">

        <!-- 包含的媒体 -->
        <div v-if="item?.has_children" ref="childrenSectionRef" class="content-section">
          <h2 class="section-title">包含的媒体</h2>
          <MediaGrid :params="{ linked_item_ids: String(item.id), limit: 100 }" />
        </div>

        <!-- 合集 -->
        <div v-if="boxSetLinks.length" class="content-section">
          <h2 class="section-title">合集</h2>
          <div class="links-grid">
            <LinkCard v-for="l in boxSetLinks" :key="l.id" :item="{ id: l.id, name: l.name }" sub-type="合集" />
          </div>
        </div>

        <!-- 来源 -->
        <div v-if="sourceLinks.length" class="content-section">
          <h2 class="section-title">来源</h2>
          <div class="links-grid">
            <LinkCard v-for="l in sourceLinks" :key="l.id" :item="{ id: l.id, name: l.name }" sub-type="来源" />
          </div>
        </div>

        <!-- 类型 -->
        <div v-if="genreLinks.length" class="content-section">
          <h2 class="section-title">类型</h2>
          <div class="links-grid">
            <LinkCard v-for="l in genreLinks" :key="l.id" :item="{ id: l.id, name: l.name }" sub-type="类型" />
          </div>
        </div>

        <!-- 标签 -->
        <div v-if="tagLinks.length" class="content-section">
          <h2 class="section-title">标签</h2>
          <div class="links-grid">
            <LinkCard v-for="l in tagLinks" :key="l.id" :item="{ id: l.id, name: l.name }" sub-type="标签" />
          </div>
        </div>

        <!-- 工作室 -->
        <div v-if="studioLinks.length" class="content-section">
          <h2 class="section-title">工作室</h2>
          <div class="links-grid">
            <LinkCard v-for="l in studioLinks" :key="l.id" :item="{ id: l.id, name: l.name }" sub-type="工作室" />
          </div>
        </div>


        <!-- 单集类型 -->
        <template v-if="item.type === 'Episode'">
          <!-- 所属季 -->
          <div v-if="seasonLinks.length" class="content-section">
            <h2 class="section-title">所属季</h2>
            <div class="links-grid">
              <LinkCard v-for="l in seasonLinks" :key="l.id" :item="{ id: l.id, name: l.name }" sub-type="季" />
            </div>
          </div>
          <div class="content-section">
            <h2 class="section-title">详情</h2>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">时长</span>
                <span class="detail-value">{{ runTimeText || '未知' }}</span>
              </div>
              <div v-if="item.premiere_date" class="detail-item">
                <span class="detail-label">播出日期</span>
                <span class="detail-value">{{ formatDate(item.premiere_date) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">评分</span>
                <span class="detail-value">{{ item.community_rating ? item.community_rating.toFixed(1) : '暂无' }}</span>
              </div>
            </div>
          </div>
        </template>

        <!-- 音频类型 -->
        <template v-if="item.type === 'Audio'">
          <div class="content-section audio-section">
            <h2 class="section-title">音频信息</h2>
            <div class="detail-grid">
              <div v-if="item.album" class="detail-item">
                <span class="detail-label">专辑</span>
                <span class="detail-value">{{ item.album }}</span>
              </div>
              <div v-if="item.artist" class="detail-item">
                <span class="detail-label">艺术家</span>
                <span class="detail-value">{{ item.artist }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">时长</span>
                <span class="detail-value">{{ runTimeText || '未知' }}</span>
              </div>
              <div v-if="item.community_rating" class="detail-item">
                <span class="detail-label">评分</span>
                <span class="detail-value">{{ item.community_rating.toFixed(1) }}</span>
              </div>
            </div>
          </div>
        </template>

        <!-- 图书类型 -->
        <template v-if="item.type === 'Book'">
          <div class="content-section">
            <h2 class="section-title">图书信息</h2>
            <div class="detail-grid">
              <div v-if="item.author" class="detail-item">
                <span class="detail-label">作者</span>
                <span class="detail-value">{{ item.author }}</span>
              </div>
              <div v-if="item.production_year" class="detail-item">
                <span class="detail-label">出版年份</span>
                <span class="detail-value">{{ item.production_year }}</span>
              </div>
              <div v-if="item.community_rating" class="detail-item">
                <span class="detail-label">评分</span>
                <span class="detail-value">{{ item.community_rating.toFixed(1) }}</span>
              </div>
            </div>
          </div>
        </template>

        <!-- 文件列表 -->
        <div v-if="item.files && item.files.length" class="content-section">
          <h2 class="section-title">文件</h2>
          <div class="file-list">
            <FileRow v-for="file in item.files" :key="file.id" :file="file" />
          </div>
        </div>
      </div>
    </template>

    <el-empty v-else description="未找到媒体信息" class="empty-state" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { mediaAPI, userAPI } from '@/api'
import MediaGrid from '@/components/MediaGrid.vue'
import MediaCard from '@/components/MediaCard.vue'
import LinkCard from '@/components/LinkCard.vue'
import FileRow from '@/components/FileRow.vue'
import { getTypeLabel } from '@/constants/mediaTypes'
import AppIcon from '@/components/ui/AppIcon.vue'
import { formatDate, parseFFmpegInfo } from '@/utils/format'

const heroConfig = {
  disableClick: true,
  disableFavorite: true,
  hideTypeBadge: true,
  hideRatingBadge: true,
  hideOverlay: false,
  hideCardInfo: true
}

const route = useRoute()
const router = useRouter()

const item = ref(null)
const loading = ref(true)
const childrenSectionRef = ref(null)

const isFavorite = ref(false)
const favLoading = ref(false)

// 选中的视频
const selectedVideo = ref(null)

// 图片 URL 缓存
const backdropUrl = ref(null)

const itemTypeClass = computed(() => (item.value?.type || '').toLowerCase())

const typeLabel = computed(() => getTypeLabel(item.value?.type))

const heroBgStyle = computed(() => {
  if (backdropUrl.value) {
    return { backgroundImage: `url(${backdropUrl.value})` }
  }
  return {}
})

const castList = computed(() => getPeopleByType('Actor'))

// 视频文件列表
const videoFiles = computed(() => {
  if (!item.value?.files) return []
  return item.value.files.filter(f => f.type === 'Video')
})

// 选中的视频信息解析
const selectedVideoInfo = computed(() => {
  if (!selectedVideo.value) return null
  const video = selectedVideo.value
  const parsed = parseFFmpegInfo(video.ffmpeg, video.size)
  return {
    ...parsed,
    duration: parsed.duration || null,
    resolution: parsed.resolution || null,
    bitrate: parsed.bitrate || null,
    size: parsed.size || null,
    codec: parsed.codec || null,
  }
})

const sourceLinks = computed(() => {
  if (!item.value?.links) return []
  return item.value.links
    .filter(l => l.linked_item?.type === 'Source' && l.linked_item?.type !== 'BoxSet')
    .map(l => ({ id: l.linked_item?.id, name: l.linked_item?.name }))
})

const boxSetLinks = computed(() => {
  if (!item.value?.links) return []
  return item.value.links
    .filter(l => l.linked_item?.type === 'BoxSet')
    .map(l => ({ id: l.linked_item?.id, name: l.linked_item?.name }))
})

const genreLinks = computed(() => getLinksByType('Genre'))
const tagLinks = computed(() => getLinksByType('Tag'))
const studioLinks = computed(() => getLinksByType('Studio'))
const seasonLinks = computed(() => {
  if (!item.value?.links) return []
  return item.value.links
    .filter(l => l.linked_item?.type === 'Season')
    .map(l => ({ id: l.linked_item?.id, name: l.linked_item?.name }))
})

const runTimeText = computed(() => {
  if (!item.value?.run_time_ticks) return null
  const totalSeconds = Math.floor(item.value.run_time_ticks / 10000000)
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  if (hours > 0) return `${hours}小时${minutes}分钟`
  return `${minutes}分钟`
})


function getLinksByType(type) {
  if (!item.value?.links) return []
  return item.value.links
    .filter(l => l.linked_item?.type === type)
    .map(l => ({
      id: l.linked_item?.id,
      name: l.linked_item?.name,
      type: l.linked_item?.type,
      people_type: l.people_type,
      role: l.people_role
    }))
}

function getPeopleByType(personType) {
  if (!item.value?.links) return []
  return item.value.links
    .filter(l => l.linked_item?.type === 'Person' && l.people_type === personType)
    .map(l => ({
      id: l.linked_item?.id,
      name: l.linked_item?.name,
      type: l.linked_item?.type,
      role: l.role
    }))
}

function playVideo(video) {
  if (!video) {
    ElMessage.warning('视频文件不存在')
    return
  }
  const videoId = video.id || video.Id
  if (!videoId) {
    ElMessage.warning('视频文件ID不存在')
    return
  }
  router.push({
    name: 'Player',
    query: { file_id: videoId, item_id: item.value.id || item.value.Id }
  })
}

function navigateTo(id) {
  if (id) router.push(`/media/${id}`)
}

async function fetchItem() {
  const id = route.params.id
  if (!id) {
    loading.value = false
    return
  }
  try {
    const response = await mediaAPI.getInfo(id)
    item.value = response

    // 初始化收藏状态
    isFavorite.value = response.userdata?.is_favorite ?? false

    // 初始化选中的视频（按 id 排序，选择第一个）
    const videos = (item.value.files || []).filter(f => f.type === 'Video')
    if (videos.length > 0) {
      videos.sort((a, b) => (a.id || 0) - (b.id || 0))
      selectedVideo.value = videos[0]
    } else {
      selectedVideo.value = null
    }
  } catch (error) {
    ElMessage.error('获取媒体详情失败')
  } finally {
    loading.value = false
  }

  // 加载完成后，如果包含子媒体则滚动到"包含的媒体"区域
  // 必须放在 loading=false 之后，否则 DOM 还未渲染，childrenSectionRef 为 null
  if (item.value?.has_children) {
    await nextTick()
    childrenSectionRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

async function toggleFavorite() {
  if (favLoading.value || !item.value) return
  favLoading.value = true
  try {
    const newValue = !isFavorite.value
    await userAPI.updateUserData({ item_id: item.value.id || item.value.Id, is_favorite: newValue })
    isFavorite.value = newValue
    ElMessage.success(isFavorite.value ? '已添加到收藏' : '已取消收藏')
  } catch {
    ElMessage.warning('操作失败，请稍后重试')
  } finally {
    favLoading.value = false
  }
}


function goBack() {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}

onMounted(() => {
  fetchItem()
})

watch(() => route.params.id, (newId, oldId) => {
  if (newId && newId !== oldId) {
    fetchItem()
  }
})
</script>

<style scoped lang="scss">
.media-detail {
  min-height: 100%;
  color: var(--imm-text-primary);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120px 0;
  gap: 16px;
  color: var(--imm-text-tertiary);

  .loading-icon {
    animation: spin 1s linear infinite;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

// ====== 英雄区域 - 密度收紧，去留白 ======
.hero-section {
  position: relative;
  background-size: cover;
  background-position: center;
  background-color: var(--color-bg-surface);
  min-height: 420px;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--color-bg-page);
    opacity: 0.68;
  }
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    color-mix(in oklch, black 12%, transparent) 0%,
    color-mix(in oklch, black 44%, transparent) 48%,
    var(--color-bg-page) 100%
  );
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 16px 16px 28px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  background: color-mix(in oklch, var(--color-bg-elevated) 88%, transparent);
  border: 1px solid var(--color-border-subtle);
  border-radius: 999px;
  color: var(--color-text-secondary);
  cursor: pointer;
  font-size: 0.8125rem;
  font-weight: 600;
  transition: all var(--duration-fast) var(--ease-standard);
  margin-bottom: 18px;
  backdrop-filter: blur(8px);

  &:hover {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
  }
}

.hero-layout {
  display: flex;
  gap: 24px;
  align-items: flex-start;

  @media (max-width: 768px) {
    flex-direction: column;
    align-items: center;
  }
}

.hero-media-card {
  flex-shrink: 0;
  width: 260px;

  @media (max-width: 768px) { width: 200px; }
}

.hero-info {
  flex: 1;
  min-width: 0;
  padding-top: 8px;
}

.info-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.badge {
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 600;

  &.type-badge {
    background: var(--imm-accent-bg);
    color: var(--imm-accent);
    border: 1px solid var(--imm-accent);
  }

  &.year-badge { background: var(--color-hover); color: var(--color-text-secondary); }
  &.rating-badge-official { background: var(--color-hover); color: var(--color-text-secondary); }

  &.rating-badge {
    background: color-mix(in oklch, var(--color-warning) 15%, transparent);
    color: var(--color-warning);
    display: flex;
    align-items: center;
    gap: 4px;
  }

  &.runtime-badge {
    background: color-mix(in oklch, var(--color-info) 15%, transparent);
    color: var(--color-info);
  }
}

.hero-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.hero-title {
  font-size: 1.75rem;
  font-weight: 800;
  margin: 0;
  line-height: 1.2;
  letter-spacing: -0.02em;

  @media (max-width: 768px) { font-size: 1.4rem; }
}

.detail-favorite-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid var(--imm-border);
  background: transparent;
  color: var(--imm-text-tertiary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;

  &:hover:not(:disabled) {
    background: var(--imm-hover);
    border-color: var(--imm-warning);
    color: var(--imm-warning);
    transform: scale(1.05);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &.active {
    color: var(--color-warning);
    background: color-mix(in oklch, var(--color-warning) 10%, transparent);
    border-color: color-mix(in oklch, var(--color-warning) 30%, transparent);

    &:hover:not(:disabled) {
      background: color-mix(in oklch, var(--color-warning) 15%, transparent);
      border-color: var(--color-warning);
    }
  }

  &:active .app-icon {
    transform: scale(0.9);
  }
}

.hero-tagline {
  font-size: 1rem;
  color: var(--imm-text-tertiary);
  margin: 0 0 12px;
  font-style: italic;
}

.hero-dates {
  font-size: 0.875rem;
  color: var(--imm-text-tertiary);
  margin-bottom: 16px;
}

.hero-overview {
  font-size: 0.9375rem;
  line-height: 1.7;
  color: var(--imm-text-secondary);
  margin: 0 0 20px;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.hero-cast {
  margin-top: 16px;
}

.meta-label {
  font-size: 0.8125rem;
  color: var(--imm-text-tertiary);
  font-weight: 600;
  margin-right: 4px;
}

.cast-scroll {
  display: flex;
  gap: 12px;
  margin-top: 8px;
  overflow-x: auto;
  padding-bottom: 8px;

  &::-webkit-scrollbar { height: 4px; }
  &::-webkit-scrollbar-track { background: transparent; }
  &::-webkit-scrollbar-thumb { background: var(--color-border-subtle); border-radius: 4px; }
}

.cast-chip {
  flex-shrink: 0;
  text-align: center;
  width: 72px;
  cursor: pointer;

  &:hover .cast-avatar {
    background: var(--imm-accent);
  }
}

.cast-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--imm-hover-strong);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 6px;
  font-weight: 700;
  font-size: 1.125rem;
  color: var(--imm-text-secondary);
  transition: background 0.3s ease;
}

.cast-name {
  font-size: 0.75rem;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cast-role {
  font-size: 0.6875rem;
  color: var(--imm-text-tertiary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

// ====== 视频选择和播放区域 ======
.hero-video-section {
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid var(--color-border-subtle);
}

.hero-video-section .video-select {
  width: 100%;
  max-width: 400px;

  :deep(.el-select__wrapper) {
    background: var(--imm-bg-elevated) !important;
    border: 1px solid var(--imm-border) !important;
    border-radius: 10px;
    box-shadow: none !important;

    &:hover, &.is-focus {
      border-color: var(--imm-accent) !important;
      box-shadow: 0 0 0 2px var(--imm-accent-bg) !important;
    }
  }

  :deep(.el-select__selection) {
    color: var(--imm-text-primary) !important;
  }

  :deep(.el-select__selected-item) {
    color: var(--imm-text-primary) !important;
  }
}

.imm-play-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 28px;
  margin-top: 16px;
  background: var(--imm-hover);
  border: 1px solid var(--imm-border);
  border-radius: 10px;
  color: var(--imm-text-secondary);
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(8px);

  &:hover:not(:disabled) {
    background: var(--imm-hover-strong);
    border-color: var(--imm-accent);
    color: var(--imm-accent);
    transform: translateY(-1px);
  }

  &:disabled {
    opacity: 0.35;
    cursor: not-allowed;
  }

  .el-icon {
    font-size: 1.125rem;
  }
}

.video-info-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 12px 0;
}

.video-info-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 10px 12px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-subtle);
  border-radius: 8px;
  min-width: 76px;
  transition: all var(--duration-fast) var(--ease-standard);

  &:hover {
    background: var(--color-hover);
    border-color: var(--color-border-default);
  }
}

.info-label {
  font-size: 0.6875rem;
  color: var(--imm-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--imm-text-primary);
}

// ====== 主体区域 - 密度提升 ======
.body-section {
  max-width: 1280px;
  margin: 0 auto;
  padding: 18px 16px 32px;
}

.content-section {
  margin-bottom: 22px;
}

.section-title {
  font-size: 1rem;
  font-weight: 700;
  margin: 0 0 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  letter-spacing: -0.01em;

  &::before {
    content: '';
    width: 3px; height: 16px; border-radius: 999px;
    background: var(--color-accent);
  }
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 10px;

  @media (max-width: 480px) { grid-template-columns: repeat(2, 1fr); }
}

.season-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.episode-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 10px;
}

.detail-item {
  padding: 12px 14px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-subtle);
  border-radius: 10px;
}

.detail-label {
  display: block;
  font-size: 0.75rem;
  color: var(--imm-text-tertiary);
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 1rem;
  font-weight: 600;
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(168px, 1fr));
  gap: var(--video-grid-gap);
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.empty-state {
  padding: 80px 0;
}

.audio-section .detail-grid {
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
}
</style>
