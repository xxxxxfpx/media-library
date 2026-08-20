<template>
  <div ref="cardRef" class="media-card" :class="{ 'disable-click': effectiveDisableClick }" @click="handleClick">
    <div class="poster-wrapper">
      <!-- 高斯模糊背景保留：AdaptiveImage 内部 ai-bg 层 blur 20px -->
      <AdaptiveImage
        :src="primaryImageUrl"
        :alt="item.name"
        mode="contain"
      >
        <div class="poster-placeholder" :class="`type-${(item.type || 'unknown').toLowerCase()}`">
          <AppIcon :name="typeIcon" :size="40" />
        </div>
      </AdaptiveImage>

      <div v-if="!effectiveHideOverlay" class="poster-overlay"></div>

      <!-- 顶部标签行 -->
      <div class="poster-top">
        <div v-if="!effectiveHideTypeBadge" class="type-badge">{{ getTypeLabel(item.type) }}</div>
        <button v-if="!effectiveDisableFavorite" class="favorite-btn" :class="{ active: isFavorite }" @click.stop="toggleFavorite" :title="isFavorite ? '取消收藏' : '收藏'">
          <AppIcon :name="'star'" :size="14" :filled="isFavorite" />
        </button>
      </div>

      <!-- 底部信息浮层（封面内） -->
      <div class="poster-bottom">
        <div v-if="durationText" class="duration-badge">
          <AppIcon name="clock" :size="10" />
          <span>{{ durationText }}</span>
        </div>
        <div v-if="!effectiveHideRatingBadge && item.community_rating" class="rating-badge">
          <AppIcon name="star" :size="11" :filled="true" />
          <span>{{ item.community_rating.toFixed(1) }}</span>
        </div>
      </div>

      <!-- Hover 播放按钮 -->
      <div class="play-btn">
        <AppIcon name="play" :size="18" />
      </div>
    </div>

    <div v-if="!effectiveHideCardInfo" class="card-info">
      <h3 class="media-title" :title="item.name">{{ item.name || '未知' }}</h3>
      <div class="media-meta">
        <span v-if="item.production_year" class="meta-year">{{ item.production_year }}</span>
        <span v-if="item.production_year && (durationText || item.official_rating)" class="meta-dot">·</span>
        <span v-if="durationText" class="meta-duration">{{ durationText }}</span>
        <span v-if="durationText && item.official_rating" class="meta-dot">·</span>
        <span v-if="item.official_rating" class="meta-rating">{{ item.official_rating }}</span>
        <span v-if="(item.community_rating || item.official_rating) && premiereYear" class="meta-dot">·</span>
        <span v-if="premiereYear && premiereYear !== item.production_year" class="meta-premiere">{{ premiereYear }}</span>
      </div>
      <div v-if="tagLine" class="media-sub">
        <span class="sub-dot"></span>
        <span class="sub-text">{{ tagLine }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { userAPI } from '@/api'
import { ElMessage } from 'element-plus'
import AdaptiveImage from '@/components/AdaptiveImage.vue'
import AppIcon from '@/components/ui/AppIcon.vue'
import { getTypeLabel, getTypeIconName } from '@/constants/mediaTypes'
import { getPrimaryImageUrl } from '@/utils/url'

const props = defineProps({
  item: { type: Object, required: true },
  disableClick: { type: Boolean, default: false },
  disableFavorite: { type: Boolean, default: false },
  setting: { type: Object, default: null }
})

const effectiveSetting = computed(() => props.setting || {})

const cardRef = ref(null)
const favLoading = ref(false)
const isFavorite = ref(props.item?.userdata?.is_favorite ?? false)
const primaryImageUrl = computed(() => getPrimaryImageUrl(props.item))
const typeIcon = computed(() => getTypeIconName(props.item.type))

const effectiveDisableClick = computed(() => effectiveSetting.value.disableClick ?? props.disableClick)
const effectiveDisableFavorite = computed(() => effectiveSetting.value.disableFavorite ?? props.disableFavorite)
const effectiveHideOverlay = computed(() => effectiveSetting.value.hideOverlay ?? false)
const effectiveHideTypeBadge = computed(() => effectiveSetting.value.hideTypeBadge ?? false)
const effectiveHideRatingBadge = computed(() => effectiveSetting.value.hideRatingBadge ?? false)
const effectiveHideCardInfo = computed(() => effectiveSetting.value.hideCardInfo ?? false)

const durationText = computed(() => {
  const ticks = props.item?.run_time_ticks
  if (!ticks) return ''
  const totalSec = Math.floor(ticks / 10000000)
  if (!totalSec) return ''
  const h = Math.floor(totalSec / 3600)
  const m = Math.floor((totalSec % 3600) / 60)
  if (h > 0) return `${h}:${String(m).padStart(2, '0')}:00`.replace(':00', `h ${m}m`).replace(/^(\d+)h 0m$/, '$1h')
  return `${m}分`
})

const premiereYear = computed(() => {
  const d = props.item?.premiere_date
  if (!d) return ''
  try { return String(new Date(d).getFullYear()) } catch { return '' }
})

const tagLine = computed(() => {
  const links = props.item?.links || []
  const tags = links.filter(l => l.linked_item?.type === 'Genre' || l.linked_item?.type === 'Tag').slice(0, 2).map(l => l.linked_item?.name).filter(Boolean)
  if (tags.length) return tags.join(' · ')
  return props.item?.tagline || ''
})

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
  transition: transform var(--duration-base) var(--ease-standard);

  &:hover {
    transform: translateY(-6px);

    .poster-wrapper {
      box-shadow: var(--video-card-shadow-hover);
      border-color: var(--video-card-border-hover);
    }

    .poster-overlay { opacity: 0.9; }
    .play-btn { opacity: 1; transform: translate(-50%, -50%) scale(1); }
    .favorite-btn { opacity: 1; transform: translateY(0); }
    .card-info .media-title { color: var(--color-accent); }
  }

  &.disable-click {
    cursor: default;

    &:hover {
      transform: none;

      .poster-wrapper { box-shadow: var(--video-card-shadow); border-color: var(--video-card-border); }
      .poster-overlay { opacity: 0.82; }
      .play-btn { opacity: 0; transform: translate(-50%, -50%) scale(0.92); }
      .card-info .media-title { color: var(--color-text-primary); }
    }
  }
}

.poster-wrapper {
  position: relative;
  aspect-ratio: 2 / 3;
  border-radius: var(--video-card-radius);
  overflow: hidden;
  background: linear-gradient(135deg, var(--color-bg-elevated) 0%, var(--color-bg-surface) 100%);
  border: 1px solid var(--video-card-border);
  box-shadow: var(--video-card-shadow);
  transition: box-shadow var(--duration-base) var(--ease-standard), border-color var(--duration-base) var(--ease-standard), transform var(--duration-base) var(--ease-standard);
}

.poster-placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  color: var(--color-text-disabled);

  &.type-series, &.type-movie, &.type-episode {
    background: linear-gradient(135deg, var(--color-accent) 0%, color-mix(in oklch, var(--color-accent) 72%, black) 100%);
    color: white;
  }
  &.type-audio {
    background: linear-gradient(135deg, var(--color-success) 0%, color-mix(in oklch, var(--color-success) 68%, black) 100%);
    color: white;
  }
  &.type-photo {
    background: linear-gradient(135deg, var(--color-warning) 0%, color-mix(in oklch, var(--color-warning) 68%, black) 100%);
    color: white;
  }
  &.type-book {
    background: linear-gradient(135deg, var(--purple-400) 0%, var(--purple-800) 100%);
    color: white;
  }
}

.poster-overlay {
  position: absolute; inset: 0;
  background: var(--video-poster-overlay);
  opacity: 0.82; transition: opacity var(--duration-base) var(--ease-standard); z-index: 2;
  pointer-events: none;
}

.poster-top {
  position: absolute; top: 8px; left: 8px; right: 8px;
  display: flex; align-items: center; justify-content: space-between; gap: 8px; z-index: 4;
}

.type-badge {
  padding: 3px 8px; background: color-mix(in oklch, var(--color-accent) 92%, white 8%); color: white;
  font-size: 0.66rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px;
  border-radius: 6px; line-height: 1; border: 1px solid color-mix(in oklch, white 18%, transparent);
  box-shadow: 0 2px 8px color-mix(in oklch, black 35%, transparent);
  backdrop-filter: blur(6px);
}

.favorite-btn {
  width: 28px; height: 28px; border-radius: 50%; border: 1px solid color-mix(in oklch, white 18%, transparent);
  background: color-mix(in oklch, black 58%, transparent); backdrop-filter: blur(8px);
  color: color-mix(in oklch, white 88%, transparent); cursor: pointer; z-index: 5;
  display: flex; align-items: center; justify-content: center;
  opacity: 0; transform: translateY(-6px);
  transition: all var(--duration-base) var(--ease-standard);
  flex-shrink: 0;

  &:hover { background: color-mix(in oklch, black 72%, transparent); color: var(--color-warning); transform: scale(1.06); }
  &.active { opacity: 1; transform: none; color: var(--color-warning); background: color-mix(in oklch, var(--color-warning) 22%, black 58%); border-color: color-mix(in oklch, var(--color-warning) 38%, transparent); }
  &:active .app-icon { transform: scale(0.92); }
}

.poster-bottom {
  position: absolute; left: 8px; right: 8px; bottom: 8px;
  display: flex; align-items: center; gap: 6px; z-index: 4; pointer-events: none;
}

.duration-badge,
.rating-badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 4px 7px; border-radius: 6px; font-size: 0.72rem; font-weight: 700; line-height: 1;
  backdrop-filter: blur(8px); border: 1px solid color-mix(in oklch, white 14%, transparent);
}

.duration-badge {
  background: color-mix(in oklch, black 62%, transparent); color: color-mix(in oklch, white 92%, transparent);
}

.rating-badge {
  background: color-mix(in oklch, var(--color-warning) 92%, black 8%); color: white; border-color: color-mix(in oklch, white 18%, transparent);
}

.play-btn {
  position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%) scale(0.92);
  width: 44px; height: 44px; border-radius: 50%;
  background: color-mix(in oklch, var(--color-accent) 92%, white 8%); color: white;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 8px 20px color-mix(in oklch, black 45%, transparent), 0 0 0 1px color-mix(in oklch, white 18%, transparent);
  opacity: 0; z-index: 5; pointer-events: none;
  transition: all var(--duration-base) var(--ease-standard);
}

.card-info {
  padding: 10px 2px 2px;

  .media-title {
    font-size: 0.875rem; font-weight: 650; color: var(--color-text-primary);
    margin: 0 0 5px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    line-height: 1.35; letter-spacing: -0.01em;
    transition: color var(--duration-fast) var(--ease-standard);
  }

  .media-meta {
    display: flex; align-items: center; gap: 5px; flex-wrap: wrap;
    font-size: 0.74rem; color: var(--color-text-tertiary); line-height: 1;

    .meta-year { color: var(--color-text-secondary); font-weight: 600; }
    .meta-duration { color: var(--color-text-tertiary); }
    .meta-rating { padding: 2px 5px; background: var(--color-hover); border: 1px solid var(--color-border-subtle); border-radius: 4px; font-size: 0.68rem; font-weight: 600; color: var(--color-text-secondary); }
    .meta-dot { opacity: 0.45; font-weight: 700; }
    .meta-premiere { color: var(--color-text-tertiary); }
  }

  .media-sub {
    display: flex; align-items: center; gap: 6px; margin-top: 5px;
    font-size: 0.7rem; color: var(--color-text-disabled); overflow: hidden;

    .sub-dot { width: 4px; height: 4px; border-radius: 50%; background: var(--color-accent); opacity: 0.9; flex-shrink: 0; }
    .sub-text { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  }
}

@media (max-width: 480px) {
  .poster-wrapper { border-radius: var(--video-card-radius-sm); }
  .type-badge { font-size: 0.6rem; padding: 3px 6px; }
  .duration-badge, .rating-badge { font-size: 0.66rem; padding: 3px 6px; }
  .play-btn { width: 38px; height: 38px; }
  .card-info .media-title { font-size: 0.82rem; }
}

@media (prefers-reduced-motion: reduce) {
  .media-card, .poster-wrapper, .play-btn, .favorite-btn { transition: none !important; }
  .media-card:hover { transform: none !important; }
}
</style>
