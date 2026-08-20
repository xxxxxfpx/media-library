<template>
  <div ref="wrapperRef" class="media-grid-wrapper">
    <!-- Toolbar -->
    <div class="toolbar">
      <div class="toolbar-left">
        <slot name="toolbar-left" />
        <span v-if="showCount" class="item-count">{{ total }} 个项目</span>
      </div>

      <div class="toolbar-right">
        <el-input
          v-if="showSearch"
          v-model="searchQuery"
          placeholder="搜索媒体..."
          class="search-input"
          clearable
        >
          <template #prefix>
            <AppIcon name="search" :size="15" />
          </template>
        </el-input>

        <div v-if="showViewToggle" class="view-toggle">
          <el-button
            :class="{ active: viewMode === 'grid' }"
            circle
            @click="viewMode = 'grid'"
          >
            <AppIcon name="layout-grid" :size="15" />
          </el-button>
          <el-button
            :class="{ active: viewMode === 'list' }"
            circle
            @click="viewMode = 'list'"
          >
            <AppIcon name="list" :size="15" />
          </el-button>
        </div>
      </div>
    </div>

    <!-- Type Filter - 粘性醒目筛选栏 -->
    <div v-if="showTypeFilter" class="type-filter-bar">
      <button
        v-for="item in TYPE_OPTIONS"
        :key="item.value"
        class="type-btn"
        :class="{ active: filters.types.includes(item.value) }"
        @click="toggleType(item.value)"
      >
        <AppIcon :name="getTypeIconName(item.value)" :size="13" class="type-icon" />
        {{ item.label }}
      </button>
    </div>

    <!-- Grid View -->
    <div v-if="viewMode === 'grid'" v-loading="loading" class="media-grid">
      <MediaCard
        v-for="item in items"
        :key="item.id"
        :item="item"
        :setting="listConfig"
        @click="handleItemClick(item)"
      />
      <div v-if="!loading && (!items || !items.length)" class="grid-empty">
        <el-empty :description="emptyDesc">
          <template #image>
            <AppIcon name="video" :size="56" class="empty-icon" />
          </template>
          <el-button v-if="emptyAction && !isFiltering" type="primary" class="empty-action" @click="handleEmptyAction">
            {{ emptyAction }}
          </el-button>
        </el-empty>
      </div>
    </div>

    <!-- List View -->
    <div v-else v-loading="loading" class="media-list">
      <div
        v-for="item in items"
        :key="item.id"
        class="list-item"
        @click="handleItemClick(item)"
      >
        <div class="list-poster">
          <img v-if="item.poster_url" :src="item.poster_url" :alt="item.name" />
          <div v-else class="poster-placeholder">
            <AppIcon :name="getTypeIconName(item.type)" :size="18" />
          </div>
        </div>
        <div class="list-info">
          <h3 class="list-title">{{ item.name }}</h3>
          <p class="list-meta">
            <span v-if="item.production_year">{{ item.production_year }}</span>
            <span v-if="item.type">{{ getTypeLabel(item.type) }}</span>
            <span v-if="item.community_rating" class="rating">
              <AppIcon name="star" :size="12" :filled="true" /> {{ item.community_rating.toFixed(1) }}
            </span>
          </p>
          <p v-if="item.overview" class="list-overview">{{ item.overview }}</p>
        </div>
        <div class="list-actions">
          <slot name="list-actions" :item="item" />
        </div>
      </div>
      <el-empty
        v-if="!loading && (!items || !items.length)"
        :description="emptyDesc"
        class="empty-state"
      >
        <el-button v-if="emptyAction && !isFiltering" type="primary" class="empty-action" @click="handleEmptyAction">
          {{ emptyAction }}
        </el-button>
      </el-empty>
    </div>

    <!-- Pagination -->
    <div v-if="total > 0" class="pagination-wrapper">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="pagination.pageSizes"
        :total="total"
        :layout="pagination.layout"
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { mediaAPI } from '@/api'
import { openMediaDetail } from '@/composables/useMediaNavigation'
import MediaCard from '@/components/MediaCard.vue'
import AppIcon from '@/components/ui/AppIcon.vue'

const router = useRouter()

const listConfig = {
  disableClick: false,
  disableFavorite: false,
  hideTypeBadge: false,
  hideRatingBadge: false,
  hideOverlay: false,
  hideCardInfo: false
}
import { TYPE_OPTIONS, getTypeLabel, getTypeIconName } from '@/constants/mediaTypes'

const props = defineProps({
  params: { type: Object, default: () => ({}) },
  pagination: {
    type: Object,
    default: () => ({
      pageSize: 60,
      pageSizes: [60, 120],
      layout: 'total, sizes, prev, pager, next'
    })
  },
  showSearch: { type: Boolean, default: true },
  showTypeFilter: { type: Boolean, default: true },
  showViewToggle: { type: Boolean, default: true },
  showCount: { type: Boolean, default: true },
  emptyText: { type: String, default: '暂无内容' },
  emptyAction: { type: String, default: '' },
  emptyActionTo: { type: String, default: '' }
})

const emit = defineEmits(['item-click'])

const isFiltering = computed(() =>
  Boolean(searchQuery.value?.trim()) || filters.value.types.length > 0
)

const emptyDesc = computed(() =>
  isFiltering.value ? '未找到匹配内容，试试清除筛选条件' : props.emptyText
)

function handleEmptyAction() {
  if (props.emptyActionTo) {
    router.push(props.emptyActionTo)
  }
}

const items = ref([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(props.pagination.pageSize || 60)
const viewMode = ref('grid')
const searchQuery = ref('')
const filters = ref({ types: [] })
const currentSearchId = ref(0)
const wrapperRef = ref(null)

let abortController = null
let searchTimer = null

function toggleType(type) {
  const index = filters.value.types.indexOf(type)
  if (index > -1) {
    filters.value.types.splice(index, 1)
  } else {
    filters.value.types.push(type)
  }
}

function handleItemClick(item) {
  openMediaDetail(item.id)
  emit('item-click', item)
}

function handleSizeChange() {
  wrapperRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function handleCurrentChange() {
  wrapperRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

async function fetchData() {
  loading.value = true
  if (abortController) abortController.abort()
  abortController = new AbortController()
  try {
    const params = {
      ...props.params,
      limit: pageSize.value,
      offset: (currentPage.value - 1) * pageSize.value
    }
    if (filters.value.types.length > 0) {
      params.types = filters.value.types.join(',')
    }

    const response = await mediaAPI.getList(params, { signal: abortController.signal })
    items.value = response.items || []
    total.value = response.total || 0
  } catch (error) {
    if (error.name === 'CanceledError' || error.__CANCEL__) return
    console.error('[MediaGrid] Fetch error:', error)
    items.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

async function searchData() {
  currentSearchId.value++
  const searchId = currentSearchId.value
  loading.value = true
  if (abortController) abortController.abort()
  abortController = new AbortController()
  try {
    const params = {
      ...props.params,
      limit: pageSize.value,
      offset: (currentPage.value - 1) * pageSize.value
    }
    if (filters.value.types.length > 0) {
      params.types = filters.value.types.join(',')
    }
    if (searchQuery.value) params.search = searchQuery.value

    const response = await mediaAPI.getList(params, { signal: abortController.signal })
    if (searchId !== currentSearchId.value) return
    items.value = response.items || []
    total.value = response.total || 0
  } catch (error) {
    if (error.name === 'CanceledError' || error.__CANCEL__) return
    if (searchId !== currentSearchId.value) return
    console.error('[MediaGrid] Search error:', error)
    items.value = []
    total.value = 0
  } finally {
    if (searchId === currentSearchId.value) {
      loading.value = false
    }
  }
}

watch([currentPage, pageSize], fetchData, { immediate: true })

watch(() => filters.value.types, () => {
  currentPage.value = 1
  fetchData()
}, { deep: true })

watch(searchQuery, (val) => {
  currentPage.value = 1
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    if (val && val.trim()) {
      searchData()
    } else {
      fetchData()
    }
  }, 300)
})

watch(
  () => props.params,
  () => {
    currentPage.value = 1
    fetchData()
  },
  { deep: true }
)
</script>

<style scoped lang="scss">
.media-grid-wrapper {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

// Toolbar - 更紧凑，信息层级清晰
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 4px 0 2px;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;

  .item-count {
    font-size: 0.8125rem;
    font-weight: 600;
    color: var(--color-text-secondary);
    white-space: nowrap;
    letter-spacing: -0.01em;
  }
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.search-input {
  width: 220px;

  :deep(.el-input__wrapper) {
    background: var(--color-bg-elevated) !important;
    border: 1px solid var(--color-border-subtle);
    border-radius: 999px;
    box-shadow: none;
    padding: 3px 14px;

    &:hover, &:focus, &.is-focus {
      border-color: var(--color-accent);
      box-shadow: 0 0 0 3px var(--color-accent-soft);
    }
  }

  :deep(.el-input__inner) {
    color: var(--color-text-primary);
    font-size: 0.875rem;

    &::placeholder { color: var(--color-text-disabled); }
  }

  :deep(.el-input__prefix) {
    color: var(--color-text-disabled);
    margin-right: 6px;
  }
}

.view-toggle {
  display: flex;
  gap: 4px;
  padding: 3px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-subtle);
  border-radius: 999px;

  .el-button {
    width: 30px; height: 30px;
    background: transparent !important;
    border: none !important;
    color: var(--color-text-tertiary) !important;

    &:hover {
      color: var(--color-text-primary) !important;
      background: var(--color-hover) !important;
    }

    &.active {
      background: var(--color-accent) !important;
      color: white !important;
      box-shadow: 0 2px 8px var(--color-accent-glow);
    }
  }
}

// Type Filter Bar - 粘性醒目，方便快速过滤
.type-filter-bar {
  position: sticky;
  top: 0;
  z-index: 5;
  display: flex;
  gap: 8px;
  padding: 10px 0 12px;
  margin: 0 -2px;
  background: var(--video-filter-sticky-bg);
  backdrop-filter: blur(12px) saturate(160%);
  -webkit-backdrop-filter: blur(12px) saturate(160%);
  border-bottom: 1px solid var(--color-border-subtle);
  overflow-x: auto;
  flex-wrap: nowrap;
  scrollbar-width: none;
  -webkit-overflow-scrolling: touch;

  &::-webkit-scrollbar { display: none; }

  .type-btn { flex-shrink: 0; }
}

.type-btn {
  padding: 7px 14px;
  border-radius: 999px;
  border: 1px solid var(--color-border-default);
  background: var(--color-bg-elevated);
  color: var(--color-text-secondary);
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-standard);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;

  .type-icon { opacity: 0.75; }

  &:hover {
    border-color: var(--video-chip-border);
    color: var(--color-accent);
    background: var(--video-chip-bg);
    transform: translateY(-1px);
  }

  &.active {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
    box-shadow: 0 4px 12px var(--color-accent-glow);
  }
}

// Grid View - 高密度
.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(168px, 1fr));
  gap: var(--video-grid-gap);
  align-items: start;
  min-height: 120px;

  @media (max-width: 1280px) {
    grid-template-columns: repeat(auto-fill, minmax(156px, 1fr));
    gap: 12px;
  }

  @media (max-width: 768px) {
    grid-template-columns: repeat(auto-fill, minmax(132px, 1fr));
    gap: 10px;
  }

  @media (max-width: 480px) {
    grid-template-columns: repeat(auto-fill, minmax(108px, 1fr));
    gap: 8px;
  }
}

.grid-empty {
  grid-column: 1 / -1;
  padding: 48px 0;

  .empty-icon { color: var(--color-border-strong); }
  .empty-action { margin-top: 8px; }
}

// List View - 密度优化，保留详情阅读
.media-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.list-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 12px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-subtle);
  border-radius: 12px;
  cursor: pointer;
  transition: all var(--duration-base) var(--ease-standard);

  &:hover {
    background: var(--color-hover-strong);
    border-color: var(--video-card-border-hover);
    transform: translateX(3px);
    box-shadow: var(--shadow-sm);
  }
}

.list-poster {
  width: 52px;
  height: 78px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  background: linear-gradient(135deg, var(--color-accent) 0%, color-mix(in oklch, var(--color-accent) 68%, black) 100%);

  img { width: 100%; height: 100%; object-fit: cover; }

  .poster-placeholder {
    width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    color: white; opacity: 0.9;
  }
}

.list-info {
  flex: 1; min-width: 0;

  .list-title {
    font-size: 0.9375rem; font-weight: 650; color: var(--color-text-primary);
    margin: 0 0 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    letter-spacing: -0.01em;
  }

  .list-meta {
    display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
    margin: 0 0 4px; font-size: 0.76rem; color: var(--color-text-tertiary);

    .rating {
      display: inline-flex; align-items: center; gap: 3px;
      color: var(--color-warning); font-weight: 700;
    }
  }

  .list-overview {
    margin: 0; font-size: 0.76rem; color: var(--color-text-disabled);
    line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden;
  }
}

.list-actions { display: flex; gap: 6px; flex-shrink: 0; }
.empty-state { padding: 64px 0; }

// Pagination - 清晰聚焦浏览
.pagination-wrapper {
  display: flex; justify-content: center;
  padding: 14px 0 4px;
  border-top: 1px solid var(--color-border-subtle);

  :deep(.el-pagination) {
    .el-pagination__total, .el-pagination__sizes { color: var(--color-text-tertiary); font-size: 0.8125rem; }

    button, .el-pager li {
      background: var(--color-bg-elevated) !important;
      color: var(--color-text-secondary) !important;
      border-radius: 8px; border: 1px solid var(--color-border-subtle); margin: 0 3px; min-width: 32px; height: 32px;

      &:hover {
        background: var(--color-hover-strong) !important;
        color: var(--color-text-primary) !important;
        border-color: var(--color-border-default);
      }

      &.is-active {
        background: var(--color-accent) !important;
        color: white !important;
        border-color: var(--color-accent) !important;
        box-shadow: 0 2px 8px var(--color-accent-glow);
      }

      &:disabled { opacity: 0.45; }
    }

    .el-input__wrapper {
      background: var(--color-bg-elevated) !important;
      border: 1px solid var(--color-border-subtle);
      box-shadow: none !important;
      border-radius: 8px;

      &:hover { border-color: var(--color-accent); }
    }

    .el-input__inner { color: var(--color-text-primary); }
    .el-pagination__jump { color: var(--color-text-tertiary); font-size: 0.8125rem; }
  }
}
</style>
