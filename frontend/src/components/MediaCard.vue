<template>
  <div ref="cardRef" class="media-card" :class="{ 'disable-click': effectiveDisableClick }" @click="handleClick">
    <div class="poster-wrapper">
      <AdaptiveImage
        :src="primaryImageUrl"
        :alt="item.name"
        mode="contain"
      >
        <div class="poster-placeholder" :class="`type-${(item.type || 'unknown').toLowerCase()}`">
          <el-icon :size="48">
            <component :is="typeIcon" />
          </el-icon>
        </div>
      </AdaptiveImage>

      <div v-if="!effectiveHideOverlay" class="poster-overlay"></div>

      <button v-if="!effectiveDisableFavorite" class="favorite-btn" @click.stop="toggleFavorite">
        <el-icon :size="18">
          <StarFilled v-if="isFavorite" />
          <Star v-else />
        </el-icon>
      </button>

      <div v-if="!effectiveHideRatingBadge && item.community_rating" class="rating-badge">
        <el-icon><StarFilled /></el-icon>
        <span>{{ item.community_rating.toFixed(1) }}</span>
      </div>

      <div v-if="!effectiveHideTypeBadge" class="type-badge">{{ getTypeLabel(item.type) }}</div>
    </div>
    
    <div v-if="!effectiveHideCardInfo" class="card-info">
      <h3 class="media-title" :title="item.name">{{ item.name || '未知' }}</h3>
      <div class="media-meta">
        <span v-if="item.production_year" class="year">{{ item.production_year }}</span>
        <span v-if="item.production_year && item.official_rating" class="divider">·</span>
        <span v-if="item.official_rating" class="rating-text">{{ item.official_rating }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, toRaw } from 'vue'
import { userAPI } from '@/api'
import { ElMessage } from 'element-plus'
import { openMediaDetail } from '@/composables/useMediaNavigation'
import AdaptiveImage from '@/components/AdaptiveImage.vue'
import { getTypeLabel, getTypeIcon } from '@/constants/mediaTypes'
import { getPrimaryImageUrl } from '@/utils/url'
import {
  Star, StarFilled
} from '@element-plus/icons-vue'

const props = defineProps({
  item: { type: Object, required: true },
  disableClick: { type: Boolean, default: false },
  disableFavorite: { type: Boolean, default: false },
  setting: { type: Object, default: null }
})

const effectiveSetting = computed(() => {
  const result = props.setting || {}
  return result
})

const cardRef = ref(null)
const favLoading = ref(false)
const isFavorite = ref(props.item?.userdata?.is_favorite ?? false)
const primaryImageUrl = computed(() => getPrimaryImageUrl(props.item))

const typeIcon = computed(() => getTypeIcon(props.item.type))

const effectiveDisableClick = computed(() => effectiveSetting.value.disableClick ?? props.disableClick)
const effectiveDisableFavorite = computed(() => effectiveSetting.value.disableFavorite ?? props.disableFavorite)
const effectiveHideOverlay = computed(() => effectiveSetting.value.hideOverlay ?? false)
const effectiveHideTypeBadge = computed(() => effectiveSetting.value.hideTypeBadge ?? false)
const effectiveHideRatingBadge = computed(() => effectiveSetting.value.hideRatingBadge ?? false)
const effectiveHideCardInfo = computed(() => effectiveSetting.value.hideCardInfo ?? false)

const emit = defineEmits(['click'])

function handleClick() {
  if (effectiveDisableClick.value) return
  emit('click', props.item)
}

async function toggleFavorite() {
  if (favLoading.value) return
  favLoading.value = true
  try {
    const newValue = !isFavorite.value
    await userAPI.updateUserData({ item_id: props.item.id, is_favorite: newValue })
    isFavorite.value = newValue
  } catch {
    ElMessage.warning('操作失败，请稍后重试')
  } finally {
    favLoading.value = false
  }
}
</script>

<style scoped lang="scss">
.media-card {
  cursor: pointer;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

  &:hover {
    transform: scale(1.05) translateY(-4px);

    .poster-wrapper {
      box-shadow: 0 20px 40px var(--imm-overlay), 0 0 0 1px var(--imm-border);
    }

    .poster-overlay { opacity: 0.6; }
    .favorite-btn { opacity: 1; transform: translateY(0); }
    .card-info .media-title { color: var(--imm-accent); }
  }

  &.disable-click {
    cursor: default;

    &:hover {
      transform: none;

      .poster-wrapper {
        box-shadow: 0 4px 20px var(--imm-overlay);
      }

      .poster-overlay { opacity: 0.8; }
      .card-info .media-title { color: var(--imm-text-primary); }
    }
  }
}

.poster-wrapper {
  position: relative;
  aspect-ratio: 3/5;
  border-radius: 12px;
  overflow: hidden;
  background: linear-gradient(135deg, var(--imm-bg-tertiary) 0%, var(--imm-bg-secondary) 100%);
  box-shadow: 0 4px 20px var(--imm-overlay);
  transition: box-shadow 0.3s ease;
}

.poster-placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  color: var(--imm-text-disabled);

  &.type-series, &.type-movie, &.type-episode {
    background: linear-gradient(135deg, var(--imm-accent) 0%, var(--imm-accent-dark) 100%);
    color: var(--imm-text-primary);
  }
  &.type-audio {
    background: linear-gradient(135deg, var(--imm-success) 0%, #388E3C 100%);
    color: var(--imm-text-primary);
  }
  &.type-photo {
    background: linear-gradient(135deg, var(--imm-warning) 0%, #F57C00 100%);
    color: var(--imm-text-primary);
  }
  &.type-book {
    background: linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%);
    color: var(--imm-text-primary);
  }
}

.poster-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.4) 40%, transparent 70%);
  opacity: 0.8; transition: opacity 0.3s ease; z-index: 2;
}

.favorite-btn {
  position: absolute; top: 10px; right: 10px;
  width: 36px; height: 36px; border-radius: 50%; border: none;
  background: rgba(0,0,0,0.6); backdrop-filter: blur(8px);
  color: var(--imm-text-secondary); cursor: pointer; z-index: 10;
  display: flex; align-items: center; justify-content: center;
  opacity: 0; transform: translateY(-10px);
  transition: all 0.3s ease;

  &:hover {
    background: rgba(0,0,0,0.8); color: var(--imm-warning); transform: scale(1.1);
  }
  &:active .el-icon { transform: scale(0.9); }
}

.rating-badge {
  position: absolute; bottom: 10px; left: 10px;
  display: flex; align-items: center; gap: 4px;
  padding: 4px 8px; background: rgba(0,0,0,0.7); backdrop-filter: blur(8px);
  border-radius: 6px; color: var(--imm-warning); font-size: 0.8125rem; font-weight: 600; z-index: 5;
  .el-icon { font-size: 0.75rem; }
}

.type-badge {
  position: absolute; top: 10px; left: 10px;
  padding: 4px 10px; background: var(--imm-accent-bg); backdrop-filter: blur(8px);
  border-radius: 6px; color: var(--imm-accent); font-size: 0.6875rem;
  font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
  border: 1px solid var(--imm-accent);
  z-index: 10;
}

.card-info {
  padding: 12px 4px 4px;
  
  .media-title {
    font-size: 0.9375rem; font-weight: 600; color: var(--imm-text-primary);
    margin: 0 0 6px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    transition: color 0.3s ease;
  }
  
  .media-meta {
    display: flex; align-items: center; gap: 6px;
    font-size: 0.8125rem; color: var(--imm-text-tertiary);
    
    .year { font-weight: 500; }
    .divider { opacity: 0.5; }
    .rating-text {
      padding: 2px 6px; background: var(--imm-hover); border-radius: 4px;
      font-size: 0.6875rem;
    }
  }
}
</style>
