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
            <AppIcon name="search" :size="16" />
          </template>
        </el-input>

        <div v-if="showViewToggle" class="view-toggle">
          <el-button
            :class="{ active: viewMode === 'grid' }"
            circle
            @click="viewMode = 'grid'"
          >
            <AppIcon name="layout-grid" :size="16" />
          </el-button>
          <el-button
            :class="{ active: viewMode === 'list' }"
            circle
            @click="viewMode = 'list'"
          >
            <AppIcon name="list" :size="16" />
          </el-button>
        </div>
      </div>
    </div>

    <!-- Type Filter -->
    <div v-if="showTypeFilter" class="type-filter-bar">
      <button
        v-for="item in TYPE_OPTIONS"
        :key="item.value"
        class="type-btn"
        :class="{ active: filters.types.includes(item.value) }"
        @click="toggleType(item.value)"
      >
        <AppIcon :name="getTypeIconName(item.value)" :size="14" class="type-icon" />
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
            <AppIcon name="video" :size="64" class="empty-icon" />
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
            <AppIcon :name="getTypeIconName(item.type)" :size="20" />
          </div>
        </div>
        <div class="list-info">
          <h3 class="list-title">{{ item.name }}</h3>
          <p class="list-meta">
            <span v-if="item.production_year">{{ item.production_year }}</span>
            <span v-if="item.type">{{ getTypeLabel(item.type) }}</span>
            <span v-if="item.community_rating" class="rating">
              <AppIcon name="star" :size="14" :filled="true" /> {{ item.community_rating.toFixed(1) }}
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
  // 空状态定制：emptyText 文案 + emptyAction 引导按钮文本 + emptyActionTo 跳转路由
  emptyText: { type: String, default: '暂无内容' },
  emptyAction: { type: String, default: '' },
  emptyActionTo: { type: String, default: '' }
})

const emit = defineEmits(['item-click'])

// 是否存在搜索关键词或类型筛选（用于区分"初始为空"与"筛选无结果"的提示）
const isFiltering = computed(() =>
  Boolean(searchQuery.value?.trim()) || filters.value.types.length > 0
)

// 空状态文案：筛选中但未命中 → 提示清除筛选；否则用自定义空文案
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

// 搜索防抖：300ms 内连续输入只触发一次请求
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
  gap: 16px;
}

// Toolbar
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;

  .item-count {
    font-size: 0.8125rem;
    color: var(--imm-text-disabled);
    white-space: nowrap;
  }
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
}

.search-input {
  width: 260px;

  :deep(.el-input__wrapper) {
    background: var(--imm-hover) !important;
    border: 1px solid var(--imm-border);
    border-radius: 10px;
    box-shadow: none;
    padding: 4px 16px;

    &:hover, &:focus, &.is-focus {
      border-color: var(--imm-accent);
      box-shadow: 0 0 0 3px var(--imm-accent-bg);
    }
  }

  :deep(.el-input__inner) {
    color: var(--imm-text-primary);

    &::placeholder {
      color: var(--imm-text-disabled);
    }
  }

  :deep(.el-input__prefix) {
    color: var(--imm-text-disabled);
    margin-right: 8px;
  }
}

.view-toggle {
  display: flex;
  gap: 8px;
  padding: 4px;
  background: var(--imm-hover);
  border-radius: 10px;

  .el-button {
    background: transparent !important;
    border: none !important;
    color: var(--imm-text-tertiary) !important;

    &:hover {
      color: var(--imm-text-secondary) !important;
      background: var(--imm-hover-strong) !important;
    }

    &.active {
      background: var(--imm-accent-bg) !important;
      color: var(--imm-accent) !important;
    }
  }
}

// Type Filter Bar
.type-filter-bar {
  display: flex;
  gap: 8px;
  padding: 8px 0;
  overflow-x: auto;
  flex-wrap: nowrap;
  scrollbar-width: none;
  -webkit-overflow-scrolling: touch;

  &::-webkit-scrollbar {
    display: none;
  }

  .type-btn {
    flex-shrink: 0;
  }
}

.type-btn {
  padding: 6px 16px;
  border-radius: 20px;
  border: 1px solid var(--imm-divider);
  background: transparent;
  color: var(--imm-text-secondary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;

  .type-icon {
    opacity: 0.7;
  }

  &:hover {
    border-color: var(--imm-accent);
    color: var(--imm-accent);
    background: var(--imm-accent-bg);
  }

  &.active {
    background: var(--imm-accent);
    border-color: var(--imm-accent);
    color: var(--color-text-inverse);
  }
}

// Grid View
.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 24px;
  align-items: start;
  min-height: 100px;
}

.grid-empty {
  grid-column: 1 / -1;
  padding: 60px 0;

  .empty-icon {
    color: var(--imm-divider);
  }

  .empty-action {
    margin-top: 8px;
  }
}

// List View
.media-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.list-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: var(--imm-hover);
  border: 1px solid var(--imm-divider);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: var(--imm-hover-strong);
    border-color: var(--imm-border);
    transform: translateX(4px);
  }
}

.list-poster {
  width: 60px;
  height: 90px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  background: linear-gradient(135deg, var(--imm-accent) 0%, var(--imm-accent-dark) 100%);

  img {
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
    color: var(--imm-text-secondary);
    font-size: 1.5rem;
  }
}

.list-info {
  flex: 1;
  min-width: 0;

  .list-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--imm-text-primary);
    margin: 0 0 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .list-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 0 0 6px;
    font-size: 0.8125rem;
    color: var(--imm-text-tertiary);

    .rating {
      display: flex;
      align-items: center;
      gap: 4px;
      color: var(--imm-warning);

      .el-icon {
        font-size: 0.875rem;
      }
    }
  }

  .list-overview {
    margin: 0;
    font-size: 0.8125rem;
    color: var(--imm-text-disabled);
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}

.list-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  padding: 80px 0;
}

// Pagination
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding-top: 16px;

  :deep(.el-pagination) {
    .el-pagination__total,
    .el-pagination__sizes {
      color: var(--imm-text-tertiary);
    }

    button, .el-pager li {
      background: transparent !important;
      color: var(--imm-text-secondary) !important;
      border-radius: 8px;

      &:hover {
        background: var(--imm-hover-strong) !important;
        color: var(--imm-text-primary) !important;
      }

      &.is-active {
        background: var(--imm-accent) !important;
        color: var(--imm-text-primary) !important;
      }

      &:disabled {
        color: var(--imm-text-disabled) !important;
      }
    }

    .el-input__wrapper {
      background: var(--imm-hover) !important;
      border: 1px solid var(--imm-border);
      box-shadow: none !important;

      &:hover {
        border-color: var(--imm-accent);
      }
    }

    .el-input__inner {
      color: var(--imm-text-primary);
    }

    .el-pagination__jump {
      color: var(--imm-text-tertiary);

      .el-input__inner {
        color: var(--imm-text-primary);
      }
    }
  }
}
</style>
