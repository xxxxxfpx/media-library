/**
 * 媒体详情抽屉组件
 * 
 * 全局媒体详情展示容器，通过 useMediaNavigation 控制显示
 * 支持从右侧滑出，展示媒体详细信息
 */
<template>
  <el-drawer
    v-model="visible"
    :size="drawerWidth"
    :with-header="false"
    :destroy-on-close="false"
    class="media-detail-drawer"
    @closed="handleClosed"
  >
    <div v-if="loading" class="drawer-loading">
      <el-icon class="loading-icon" :size="32"><Loading /></el-icon>
      <p>加载中...</p>
    </div>

    <template v-else-if="item">
      <!-- 头部海报区 -->
      <div class="drawer-hero" :class="`type-${itemTypeClass}`">
        <div class="hero-backdrop" :style="heroBgStyle">
          <div class="backdrop-overlay"></div>
        </div>

        <div class="hero-content">
          <button class="close-btn" @click="close">
            <el-icon><Close /></el-icon>
          </button>

          <div class="poster-wrapper">
            <img v-if="currentImageUrl" :src="currentImageUrl" :alt="item.name" class="poster-img" />
            <div v-else class="poster-placeholder">
              <el-icon :size="48"><component :is="typeIcon" /></el-icon>
            </div>
          </div>

          <div class="hero-info">
            <div class="info-badges">
              <span class="badge type-badge">{{ typeLabel }}</span>
              <span v-if="item.production_year" class="badge year-badge">{{ item.production_year }}</span>
              <span v-if="item.community_rating" class="badge rating-badge">
                <el-icon><StarFilled /></el-icon> {{ item.community_rating.toFixed(1) }}
              </span>
            </div>

            <h1 class="hero-title">{{ item.name || '未知' }}</h1>
            <p v-if="item.tagline" class="hero-tagline">{{ item.tagline }}</p>
            <p v-if="item.overview" class="hero-overview">{{ item.overview }}</p>
          </div>
        </div>
      </div>

      <!-- 详情内容区 -->
      <div class="drawer-body">
        <!-- 元信息 -->
        <div v-if="metaItems.length" class="detail-section">
          <h3 class="section-title">基本信息</h3>
          <div class="meta-grid">
            <div v-for="meta in metaItems" :key="meta.label" class="meta-item">
              <span class="meta-label">{{ meta.label }}</span>
              <span class="meta-value">{{ meta.value }}</span>
            </div>
          </div>
        </div>

        <!-- 所属合集 -->
        <div v-if="boxSetLinks.length" class="detail-section">
          <h3 class="section-title">所属合集</h3>
          <div class="link-grid">
            <div
              v-for="link in boxSetLinks"
              :key="link.id"
              class="link-card-mini"
              @click="openLink(link)"
            >
              <span class="link-name">{{ link.name }}</span>
              <span class="link-sub">合集</span>
            </div>
          </div>
        </div>

        <!-- 关联内容 -->
        <div v-if="linkItems.length" class="detail-section">
          <h3 class="section-title">关联内容</h3>
          <div class="link-grid">
            <div
              v-for="link in linkItems"
              :key="link.id"
              class="link-card-mini"
              @click="openLink(link)"
            >
              <span class="link-name">{{ link.name }}</span>
              <span v-if="link.subType" class="link-sub">{{ link.subType }}</span>
            </div>
          </div>
        </div>

        <!-- 包含的媒体 -->
        <div v-if="item?.has_children" ref="childrenSectionRef" class="detail-section">
          <h3 class="section-title">包含的媒体</h3>
          <div v-if="childrenLoading" class="drawer-loading" style="padding: 20px 0;">
            <el-icon class="loading-icon" :size="24"><Loading /></el-icon>
            <p style="margin-top: 8px;">加载子媒体...</p>
          </div>
          <div v-else-if="childrenItems.length" class="link-grid">
            <div
              v-for="child in childrenItems"
              :key="child.id"
              class="link-card-mini"
              @click="openLink(child)"
            >
              <span class="link-name">{{ child.name }}</span>
              <span v-if="child.type" class="link-sub">{{ getTypeLabel(child.type) }}</span>
            </div>
          </div>
          <p v-else class="empty-hint">暂无子媒体</p>
        </div>
      </div>

      <!-- 底部操作栏 -->
      <div class="drawer-footer">
        <el-button type="primary" class="action-btn" @click="goToDetailPage">
          <el-icon><Document /></el-icon>
          <span>查看完整详情</span>
        </el-button>
      </div>
    </template>

    <el-empty v-else description="未找到媒体信息" />
  </el-drawer>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { mediaAPI, fileAPI } from '@/api'
import { useMediaNavigation, closeMediaDetail } from '@/composables/useMediaNavigation'
import { getTypeLabel, getTypeIcon } from '@/constants/mediaTypes'
import { formatDate, formatFileSize } from '@/utils/format'
import { getFileDataUrl, getPrimaryImageUrl } from '@/utils/url'
import {
  Loading, Close, StarFilled
} from '@element-plus/icons-vue'

const router = useRouter()
const { state } = useMediaNavigation()

const visible = computed({
  get: () => state.visible,
  set: (val) => {
    if (!val) closeMediaDetail()
  }
})

const loading = computed(() => state.loading)
const item = computed(() => state.itemData)
const itemId = computed(() => state.itemId)
const childrenSectionRef = ref(null)
const childrenItems = ref([])
const childrenLoading = ref(false)

const drawerWidth = computed(() => {
  return window.innerWidth > 768 ? '560px' : '90%'
})

const itemTypeClass = computed(() => (item.value?.type || '').toLowerCase())

const typeLabel = computed(() => getTypeLabel(item.value?.type))

const typeIcon = computed(() => getTypeIcon(item.value?.type))

const heroBgStyle = computed(() => {
  const backdrop = item.value?.files?.find(f => f.image_type === 'Backdrop')
  if (backdrop?.id) {
    return { backgroundImage: `url(${fileAPI.getDataUrl(backdrop.id)})` }
  }
  return {}
})

const currentImageUrl = computed(() => {
  return getPrimaryImageUrl(item.value) || item.value?.poster_url || null
})

const metaItems = computed(() => {
  if (!item.value) return []
  const items = []
  if (item.value.premiere_date) {
    items.push({ label: '首映日期', value: formatDate(item.value.premiere_date) })
  }
  if (item.value.official_rating) {
    items.push({ label: '分级', value: item.value.official_rating })
  }
  if (item.value.run_time_ticks) {
    const seconds = Math.floor(item.value.run_time_ticks / 10000000)
    const hours = Math.floor(seconds / 3600)
    const mins = Math.floor((seconds % 3600) / 60)
    items.push({ label: '时长', value: hours > 0 ? `${hours}小时${mins}分钟` : `${mins}分钟` })
  }
  if (item.value.production_year) {
    items.push({ label: '年份', value: item.value.production_year })
  }
  // 文件信息：只显示非图片文件的数量和总大小
  const dataFiles = item.value.files?.filter(f => f.type !== 'Image' && f.type !== 'Backdrop') || []
  if (dataFiles.length > 0) {
    const totalSize = dataFiles.reduce((sum, f) => sum + (f.size || 0), 0)
    items.push({ label: '文件数量', value: `${dataFiles.length} 个` })
    if (totalSize > 0) {
      items.push({ label: '总大小', value: formatFileSize(totalSize) })
    }
  }
  return items
})

const linkItems = computed(() => {
  if (!item.value?.links) return []
  return item.value.links
    .filter(l => (l.linked_item?.id || l.linked_item?.Id) && l.linked_item?.type !== 'BoxSet')
    .map(l => ({
      id: l.linked_item?.id || l.linked_item?.Id,
      name: l.linked_item?.name || l.linked_item?.Name,
      subType: l.type || l.subType || ''
    }))
})

const boxSetLinks = computed(() => {
  if (!item.value?.links) return []
  return item.value.links
    .filter(l => l.linked_item?.type === 'BoxSet')
    .map(l => ({
      id: l.linked_item?.id,
      name: l.linked_item?.name,
    }))
})

function openMedia(id) {
  closeMediaDetail()
  router.push(`/media/${id}`)
}

function handleClosed() {
  // 抽屉关闭后的清理
}

function goToDetailPage() {
  const id = itemId.value
  closeMediaDetail()
  if (id) {
    router.push(`/media/${id}`)
  }
}

function openLink(link) {
  if (link.id) {
    const linkId = link.id
    closeMediaDetail()
    setTimeout(() => {
      router.push(`/media/${linkId}`)
    }, 300)
  }
}

// 监听 itemId 变化，加载详情数据
watch(itemId, async (newId) => {
  if (newId && !state.itemData) {
    state.loading = true
    try {
      const data = await mediaAPI.getInfo(newId)
      state.itemData = data
    } catch (err) {
      console.error('加载媒体详情失败:', err)
    } finally {
      state.loading = false
    }
  }
}, { immediate: true })

// 检测到 has_children 时，加载子媒体列表
watch(() => item.value?.has_children, async (hasChildren) => {
  if (hasChildren && item.value?.id) {
    childrenLoading.value = true
    try {
      const response = await mediaAPI.getList({ linked_item_ids: String(item.value.id), limit: 100 })
      childrenItems.value = response.items || []
      await nextTick()
      childrenSectionRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    } catch (err) {
      console.error('加载子媒体失败:', err)
    } finally {
      childrenLoading.value = false
    }
  }
})
</script>

<style scoped lang="scss">
.media-detail-drawer {
  :deep(.el-drawer__body) {
    padding: 0;
    display: flex;
    flex-direction: column;
    height: 100%;
    background: var(--imm-bg-primary);
  }
}

.drawer-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  gap: 12px;
  color: var(--imm-text-tertiary);

  .loading-icon {
    animation: spin 1s linear infinite;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

// ===== 头部海报区 =====
.drawer-hero {
  position: relative;
  background: var(--imm-bg-secondary);
  overflow: hidden;
}

.hero-backdrop {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;

  .backdrop-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
      180deg,
      rgba(0,0,0,0.4) 0%,
      var(--imm-bg-secondary) 100%
    );
  }
}

.hero-content {
  position: relative;
  z-index: 2;
  padding: 20px 24px 24px;
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(0,0,0,0.5);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;

  &:hover {
    background: var(--imm-accent);
  }
}

.poster-wrapper {
  width: 140px;
  aspect-ratio: 3/5;
  border-radius: 12px;
  overflow: hidden;
  background: var(--imm-bg-tertiary);
  box-shadow: 0 8px 24px rgba(0,0,0,0.4);
  margin-bottom: 16px;
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--imm-text-disabled);
}

.hero-info {
  .info-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 12px;
  }

  .badge {
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;

    &.type-badge {
      background: var(--imm-accent-bg);
      color: var(--imm-accent);
      border: 1px solid var(--imm-accent);
    }

    &.year-badge {
      background: rgba(255,255,255,0.08);
      color: rgba(255,255,255,0.7);
    }

    &.rating-badge {
      background: rgba(255, 193, 7, 0.15);
      color: #FFC107;
      display: flex;
      align-items: center;
      gap: 4px;
    }
  }

  .hero-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 6px;
    color: var(--imm-text-primary);
    line-height: 1.3;
  }

  .hero-tagline {
    font-size: 0.875rem;
    color: var(--imm-text-tertiary);
    margin: 0 0 10px;
    font-style: italic;
  }

  .hero-overview {
    font-size: 0.8125rem;
    line-height: 1.6;
    color: var(--imm-text-secondary);
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}

// ===== 详情内容区 =====
.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
}

.detail-section {
  margin-bottom: 24px;

  &:last-child {
    margin-bottom: 0;
  }
}

.section-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--imm-text-primary);
  margin: 0 0 12px;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.meta-item {
  padding: 10px 14px;
  background: var(--imm-hover);
  border-radius: 8px;

  .meta-label {
    display: block;
    font-size: 0.6875rem;
    color: var(--imm-text-tertiary);
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .meta-value {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--imm-text-primary);
  }
}

.link-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 8px;
}

.link-card-mini {
  padding: 10px 14px;
  background: var(--imm-hover);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: var(--imm-hover-strong);
  }

  .link-name {
    display: block;
    font-size: 0.8125rem;
    font-weight: 500;
    color: var(--imm-text-primary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .link-sub {
    display: block;
    font-size: 0.6875rem;
    color: var(--imm-text-tertiary);
    margin-top: 2px;
  }
}

.empty-hint {
  text-align: center;
  color: var(--imm-text-disabled);
  font-size: 0.8125rem;
  padding: 12px 0;
}

// ===== 底部操作栏 =====
.drawer-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--imm-divider);
  background: var(--imm-bg-secondary);

  .action-btn {
    width: 100%;
    height: 44px;
    border-radius: 10px;
    font-size: 0.9375rem;
    font-weight: 500;

    .el-icon {
      margin-right: 6px;
    }
  }
}
</style>
