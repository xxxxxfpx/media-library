<template>
  <div
    ref="containerRef"
    class="video-player-container"
    @mousemove="showControls"
    @mouseleave="hideControls"
  >
    <video
      ref="videoRef"
      class="video-element"
      :src="videoUrl"
      :loop="false"
      :controls="false"
      @loadedmetadata="onLoadedMetadata"
      @timeupdate="onTimeUpdate"
      @play="handlePlay"
      @pause="handlePause"
      @ended="onVideoEnded"
      @playing="showPlayIcon = false"
      @volumechange="onVolumeChange"
      @click="togglePlay"
    />

    <!-- 加载中 -->
    <transition name="fade">
      <div v-if="isLoading" class="loading-overlay">
        <div class="loading-content">
          <div class="loading-spinner"></div>
          <p class="loading-text">正在加载视频...</p>
        </div>
      </div>
    </transition>

    <!-- 拖拽进度加载动画 -->
    <transition name="scale-fade">
      <div v-if="isSeeking && isBuffering" class="seeking-overlay">
        <div class="seeking-spinner"></div>
        <p class="seeking-text">{{ formatTimeLocal(seekTime) }}</p>
      </div>
    </transition>

    <!-- 播放/暂停图标 -->
    <transition name="scale-fade">
      <div v-if="showPlayIcon" class="play-icon-overlay" @click="togglePlay">
        <el-icon :size="80">
          <VideoPlay v-if="!isPlaying" />
          <VideoPause v-else />
        </el-icon>
      </div>
    </transition>

    <!-- 顶部信息栏 -->
    <transition name="slide-down">
      <div v-if="controlsVisible" class="top-bar">
        <div class="video-info">
          <h2 class="video-title">{{ videoTitle }}</h2>
          <span v-if="currentQuality" class="quality-badge">{{ currentQuality }}</span>
        </div>
        <el-button class="close-btn" circle @click="goBack">
          <el-icon size="24"><ArrowLeft /></el-icon>
        </el-button>
      </div>
    </transition>

    <!-- 底部控制栏 -->
    <transition name="slide-up">
      <div v-if="controlsVisible" class="bottom-bar">
        <!-- 进度条 -->
        <div 
          class="progress-container" 
          @click="seek"
          @mousedown="handleSeekStart"
          @mousemove="handleSeekMove"
          @mouseup="handleSeekEnd"
          @mouseleave="handleSeekEnd"
        >
          <div class="progress-bar">
            <div class="progress-buffered" :style="{ width: bufferedPercent + '%' }"></div>
            <div class="progress-current" :style="{ width: progressPercent + '%' }"></div>
            <div class="progress-thumb" :style="{ left: progressPercent + '%' }"></div>
            <!-- 拖拽时的预览进度 -->
            <div 
              v-if="isSeeking" 
              class="progress-preview" 
              :style="{ width: seekingPercent + '%' }"
            ></div>
          </div>
        </div>

        <!-- 控制按钮 -->
        <div class="controls-row">
          <div class="controls-left">
            <button class="control-btn play-pause-btn" :class="{ 'is-playing': isPlaying }" @click="togglePlay">
              <el-icon :size="24">
                <VideoPlay v-if="!isPlaying" />
                <VideoPause v-else />
              </el-icon>
            </button>

            <!-- 音量控制 -->
            <div class="volume-control">
              <button class="control-btn volume-btn" :class="{ 'is-muted': isMuted || volume === 0 }" @click="toggleMute">
                <span class="volume-icon-wrapper">
                  <el-icon :size="20">
                    <Notification />
                  </el-icon>
                  <el-icon v-if="isMuted || volume === 0" :size="12" class="mute-forbidden-icon">
                    <CircleCloseFilled />
                  </el-icon>
                </span>
              </button>
              <div class="volume-slider-wrapper">
                <input
                  type="range"
                  class="volume-slider"
                  min="0"
                  max="1"
                  step="0.05"
                  :value="volume"
                  @input="handleVolumeInput"
                />
              </div>
            </div>

            <span class="time-display">
              {{ formatTimeLocal(currentTime) }} / {{ formatTimeLocal(duration) }}
            </span>
          </div>

          <div class="controls-right">
            <!-- 倍速播放 -->
            <div class="speed-dropdown">
              <button class="control-btn speed-btn" :class="{ 'is-active': playbackRate !== 1 }" @click="showSpeedMenu = !showSpeedMenu">
                <el-icon :size="18" style="margin-right: 4px;"><Clock /></el-icon>
                {{ playbackRate }}x
              </button>
              <transition name="fade">
                <div v-if="showSpeedMenu" class="speed-menu">
                  <button
                    v-for="rate in speedOptions"
                    :key="rate"
                    class="speed-menu-item"
                    :class="{ 'is-selected': playbackRate === rate }"
                    @click="selectSpeed(rate)"
                  >
                    {{ rate }}x{{ rate === 1 ? ' (正常)' : '' }}
                  </button>
                </div>
              </transition>
            </div>

            <!-- 视频信息 -->
            <button class="control-btn" @click="showInfo = !showInfo">
              <el-icon :size="20"><InfoFilled /></el-icon>
            </button>

            <!-- 全屏 -->
            <button class="control-btn" @click="toggleFullscreen">
              <el-icon :size="20">
                <FullScreen v-if="!isFullscreen" />
                <Close v-else />
              </el-icon>
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- 视频信息面板 -->
    <transition name="slide-right">
      <div v-if="showInfo" class="info-panel">
        <h3>视频信息</h3>
        <div class="info-list">
          <div class="info-item">
            <span class="info-label">分辨率</span>
            <span class="info-value">{{ videoInfo.resolution || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">编码</span>
            <span class="info-value">{{ videoInfo.codec || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">码率</span>
            <span class="info-value">{{ videoInfo.bitrate || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">时长</span>
            <span class="info-value">{{ videoInfo.duration || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">大小</span>
            <span class="info-value">{{ videoInfo.size || '-' }}</span>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { mediaAPI, fileAPI, userAPI } from '@/api'
import { formatFileSize, parseFFmpegInfo } from '@/utils/format'
import { usePlayerState } from '@/composables/usePlayerState'
import {
  VideoPlay, VideoPause, ArrowLeft, FullScreen, Close,
  Notification, CircleCloseFilled, InfoFilled, Clock
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const containerRef = ref(null)
const videoRef = ref(null)

const videoId = ref(route.query.videoId)
const fileId = ref(route.query.file_id)
const itemId = ref(route.query.item_id)

// 使用播放器状态管理
const playerState = usePlayerState(itemId, videoRef)
const {
  currentTime,
  duration,
  volume,
  playbackRate,
  isMuted,
  syncInterval,
  setCurrentTime,
  setVolume,
  setPlaybackRate,
  setMuted,
  syncPlayback,
  startSyncTimer,
  stopSyncTimer,
  loadUserSettings,
  applyUserSettings,
  onEnded,
  onPause,
  onPlay,
  dispose,
} = playerState

const isLoading = ref(true)
const isPlaying = ref(false)
const isFullscreen = ref(false)
const showPlayIcon = ref(false)
const controlsVisible = ref(true)
const showInfo = ref(false)
const showSpeedMenu = ref(false)

const speedOptions = [0.5, 0.75, 1, 1.25, 1.5, 2]
const isSeeking = ref(false)
const isBuffering = ref(false)
const seekTime = ref(0)
const seekingPercent = ref(0)

const bufferedPercent = ref(0)

const videoTitle = ref('')
const videoUrl = ref('')
const userData = ref(null)
const userSettings = ref(null)
const videoInfo = ref({
  resolution: '',
  codec: '',
  bitrate: '',
  duration: '',
  size: ''
})

let controlsTimer = null
let bufferCheckTimer = null
let lastClickTime = 0

// 更新音量滑块样式
function updateVolumeSliderStyle() {
  const slider = document.querySelector('.volume-slider')
  if (slider) {
    const percent = volume.value * 100
    slider.style.setProperty('--volume-percent', `${percent}%`)
  }
}

watch(volume, () => {
  updateVolumeSliderStyle()
})

onMounted(() => {
  updateVolumeSliderStyle()
})

const progressPercent = computed(() => {
  if (!duration.value) return 0
  return (currentTime.value / duration.value) * 100
})

const currentQuality = computed(() => {
  if (!videoInfo.value.resolution) return ''
  return videoInfo.value.resolution
})

function formatTimeLocal(seconds) {
  if (!seconds || isNaN(seconds)) return '00:00'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  if (h > 0) {
    return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  }
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

async function loadVideo() {
  try {
    isLoading.value = true

    // 加载用户设置
    try {
      userSettings.value = await loadUserSettings()
    } catch {
    }

    let fileData
    if (fileId.value) {
      const res = await fileAPI.getInfo(parseInt(fileId.value))
      fileData = res
    } else if (itemId.value) {
      const res = await mediaAPI.getInfo(parseInt(itemId.value))
      fileData = res.files?.find(f => f.type === 'Video')
    }

    if (!fileData) {
      throw new Error('未找到视频文件')
    }

    videoTitle.value = fileData.name || '视频播放'
    videoUrl.value = fileAPI.getDataUrl(parseInt(fileId.value || fileData.id))

    const ffmpegData = fileData.ffmpeg
    const parsed = parseFFmpegInfo(ffmpegData, fileData.size)
    videoInfo.value = parsed

    if (itemId.value) {
      try {
        const mediaInfo = await mediaAPI.getInfo(parseInt(itemId.value))
        userData.value = mediaInfo.userdata || null
      } catch {
      }
    }
  } catch (error) {
    console.error('加载视频失败:', error)
  } finally {
    isLoading.value = false
  }
}

function applySettings() {
  applyUserSettings(userSettings.value)
}

function onLoadedMetadata() {
  duration.value = videoRef.value.duration

  // 从 video 元素回退获取视频信息（当 ffmpeg 元数据不可用时）
  if (!videoInfo.value.resolution) {
    const vw = videoRef.value.videoWidth
    const vh = videoRef.value.videoHeight
    if (vh >= 2160) videoInfo.value.resolution = '4K'
    else if (vh >= 1080) videoInfo.value.resolution = '1080p'
    else if (vh >= 720) videoInfo.value.resolution = '720p'
    else if (vh >= 480) videoInfo.value.resolution = '480p'
    else if (vw && vh) videoInfo.value.resolution = `${vw}x${vh}`
  }
  if (!videoInfo.value.duration) {
    videoInfo.value.duration = formatTimeLocal(duration.value)
  }
  
  if (userData.value) {
    if (userData.value.playback_position_ticks) {
      setCurrentTime(userData.value.playback_position_ticks)
    }
    if (userData.value.playback_rate) {
      setPlaybackRate(userData.value.playback_rate)
    }
  }

  // 应用用户设置（自动播放、默认静音）
  applySettings()
  
  isLoading.value = false
}

function onTimeUpdate() {
  if (videoRef.value) {
    currentTime.value = videoRef.value.currentTime

    if (videoRef.value.buffered.length > 0) {
      const buffered = videoRef.value.buffered.end(videoRef.value.buffered.length - 1)
      bufferedPercent.value = (buffered / duration.value) * 100
    }
  }
}

// 拖拽进度条相关函数
function handleSeekStart(event) {
  isSeeking.value = true
  updateSeekPosition(event)
}

function handleSeekMove(event) {
  if (!isSeeking.value) return
  updateSeekPosition(event)
}

function handleSeekEnd(event) {
  if (!isSeeking.value) return
  isSeeking.value = false
  
  // 执行拖拽后的跳转
  if (videoRef.value && duration.value) {
    const newTime = (seekingPercent.value / 100) * duration.value
    setCurrentTime(newTime)
    
    // 检查是否已缓冲
    const isBuffered = videoRef.value.buffered.length > 0 && 
      videoRef.value.buffered.end(videoRef.value.buffered.length - 1) >= newTime
    
    if (!isBuffered) {
      isBuffering.value = true
      // 等待缓冲完成
       bufferCheckTimer = setInterval(() => {
         if (!videoRef.value) {
           clearInterval(bufferCheckTimer)
           bufferCheckTimer = null
           return
         }
         if (videoRef.value.buffered.length > 0 &&
             videoRef.value.buffered.end(videoRef.value.buffered.length - 1) >= newTime) {
           isBuffering.value = false
           clearInterval(bufferCheckTimer)
           bufferCheckTimer = null
         }
       }, 200)
    }
  }
}

function updateSeekPosition(event) {
  if (!videoRef.value || !duration.value) return
  
  const rect = event.currentTarget.getBoundingClientRect()
  const x = event.clientX - rect.left
  const percent = Math.max(0, Math.min(100, (x / rect.width) * 100))
  seekingPercent.value = percent
  seekTime.value = (percent / 100) * duration.value
}

function onVolumeChange() {
  if (!videoRef.value) return
  volume.value = videoRef.value.volume
  isMuted.value = videoRef.value.muted
}

function onVideoEnded() {
  isPlaying.value = false
  showPlayIcon.value = true
  onEnded()
}

function handlePlay() {
  isPlaying.value = true
  onPlay() // call playerState's onPlay (sync timer)
}

function handlePause() {
  isPlaying.value = false
  onPause() // call playerState's onPause (sync + stop timer)
}

function togglePlay() {
  if (!videoRef.value) return

  const now = Date.now()
  if (now - lastClickTime < 300) {
    lastClickTime = now
    return
  }
  lastClickTime = now

  if (videoRef.value.paused) {
    videoRef.value.play()
    startSyncTimer()
    showPlayIcon.value = true
    setTimeout(() => {
      showPlayIcon.value = false
    }, 500)
  } else {
    videoRef.value.pause()
    onPause()
    showPlayIcon.value = true
  }
}

function seek(event) {
  if (!videoRef.value || !duration.value) return
  const rect = event.currentTarget.getBoundingClientRect()
  const percent = (event.clientX - rect.left) / rect.width
  const newTime = percent * duration.value
  setCurrentTime(newTime)
}

function toggleMute() {
  if (!videoRef.value) return
  setMuted(!isMuted.value)
}

function handleVolumeInput(event) {
  setVolume(parseFloat(event.target.value))
}

function selectSpeed(rate) {
  if (!videoRef.value) return
  setPlaybackRate(rate)
  showSpeedMenu.value = false
  // 确保控制栏保持可见
  setTimeout(() => {
    controlsVisible.value = true
  }, 100)
}

function toggleFullscreen() {
  if (!containerRef.value) return

  if (!document.fullscreenElement) {
    containerRef.value.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

function onFullscreenChange() {
  isFullscreen.value = !!document.fullscreenElement
  if (document.fullscreenElement) {
    controlsVisible.value = true
    if (controlsTimer) clearTimeout(controlsTimer)
  }
}

function onFullscreenError() {
  console.warn('全屏操作失败，当前浏览器可能不支持全屏')
}

onMounted(() => {
  loadVideo()
  document.addEventListener('keydown', handleKeydown)
  document.addEventListener('fullscreenchange', onFullscreenChange)
  document.addEventListener('fullscreenerror', onFullscreenError)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('fullscreenchange', onFullscreenChange)
  document.removeEventListener('fullscreenerror', onFullscreenError)
  if (controlsTimer) clearTimeout(controlsTimer)
  if (bufferCheckTimer) clearInterval(bufferCheckTimer)
  dispose()
  if (document.fullscreenElement) {
    document.exitFullscreen()
  }
})

function showControls() {
  controlsVisible.value = true
  if (controlsTimer) clearTimeout(controlsTimer)
  controlsTimer = setTimeout(() => {
    if (isPlaying.value) {
      controlsVisible.value = false
    }
  }, 3000)
}
function hideControls() {
  if (controlsTimer) clearTimeout(controlsTimer)
  controlsTimer = setTimeout(() => {
    if (isPlaying.value) {
      controlsVisible.value = false
      showSpeedMenu.value = false
    }
  }, 1000)
}

function goBack() {
  router.back()
}

function handleKeydown(event) {
  if (!videoRef.value) return

  switch (event.key) {
    case ' ':
    case 'k':
      event.preventDefault()
      togglePlay()
      break
    case 'ArrowUp':
      event.preventDefault()
      setVolume(Math.min(volume.value + 0.1, 1))
      break
    case 'ArrowDown':
      event.preventDefault()
      setVolume(Math.max(volume.value - 0.1, 0))
      break
    case 'm':
      toggleMute()
      break
    case 'f':
      toggleFullscreen()
      break
    case 'Escape':
      if (document.fullscreenElement) {
        document.exitFullscreen()
      }
      isFullscreen.value = !!document.fullscreenElement
      break
  }
}

watch(isPlaying, (playing) => {
  if (!playing) {
    controlsVisible.value = true
    if (controlsTimer) clearTimeout(controlsTimer)
  }
})

</script>

<style scoped lang="scss">
.video-player-container {
  position: fixed;
  inset: 0;
  background: #000;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  cursor: none;

  &:hover {
    cursor: default;
  }
}

.video-element {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.loading-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 255, 255, 0.15);
  border-top-color: var(--imm-accent);
  border-right-color: var(--imm-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-text {
  color: white;
  font-size: 0.9375rem;
  margin: 0;
  opacity: 0.9;
  letter-spacing: 0.5px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

// 拖拽进度加载动画
.seeking-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  z-index: 50;
  pointer-events: none;
}

.seeking-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(255, 255, 255, 0.15);
  border-top-color: var(--imm-accent);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.seeking-text {
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  background: rgba(0, 0, 0, 0.8);
  padding: 4px 12px;
  border-radius: 4px;
  backdrop-filter: blur(4px);
  letter-spacing: 0.5px;
}

.play-icon-overlay {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  border-radius: 50%;
  color: white;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);

  &:hover {
    transform: scale(1.15);
    background: rgba(0, 0, 0, 0.8);
  }

  .el-icon {
    animation: pulse 2s ease-in-out infinite;
  }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

.top-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.8), transparent);
}

.video-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.video-title {
  color: white;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.quality-badge {
  padding: 4px 10px;
  background: var(--imm-accent);
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 4px;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
  }
}

.bottom-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px 24px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
}

.progress-container {
  padding: 10px 0;
  cursor: pointer;
}

.progress-bar {
  position: relative;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  transition: height 0.2s ease;

  .progress-container:hover & {
    height: 6px;
  }
}

.progress-buffered {
  position: absolute;
  height: 100%;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.progress-current {
  position: absolute;
  height: 100%;
  background: var(--imm-accent);
  border-radius: 2px;
}

.progress-preview {
  position: absolute;
  height: 100%;
  background: var(--imm-accent);
  opacity: 0.4;
  border-radius: 2px;
  pointer-events: none;
}

.progress-thumb {
  position: absolute;
  top: 50%;
  width: 14px;
  height: 14px;
  background: var(--imm-accent);
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(0);
  transition: transform 0.2s ease;

  .progress-container:hover & {
    transform: translate(-50%, -50%) scale(1);
  }
}

.controls-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
}

.controls-left,
.controls-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: scale(1.05);
  }

  &:active {
    transform: scale(0.95);
  }

  &.is-playing {
    background: rgba(255, 255, 255, 0.2);
    color: var(--imm-accent);
  }

  &.is-muted {
    color: var(--imm-warning);
  }
}

.volume-icon-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.mute-forbidden-icon {
  position: absolute;
  top: -4px;
  right: -6px;
  color: var(--imm-warning, #e6a23c);
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 6px;
}

.volume-slider-wrapper {
  position: relative;
  width: 80px;
  height: 4px;
  display: flex;
  align-items: center;
}

.volume-slider {
  width: 100%;
  height: 4px;
  appearance: none;
  background: linear-gradient(to right, 
    var(--imm-accent) 0%, 
    var(--imm-accent) var(--volume-percent, 50%),
    rgba(255, 255, 255, 0.2) var(--volume-percent, 50%),
    rgba(255, 255, 255, 0.2) 100%
  );
  border-radius: 2px;
  cursor: pointer;
  transition: background 0.2s ease;

  &::-webkit-slider-thumb {
    appearance: none;
    width: 12px;
    height: 12px;
    background: white;
    border-radius: 50%;
    cursor: pointer;
  }
}

.time-display {
  color: white;
  font-size: 0.875rem;
  font-variant-numeric: tabular-nums;
  margin-left: 12px;
}

.speed-btn {
  width: auto;
  padding: 0 12px;
  font-size: 0.875rem;
  font-weight: 500;

  &.is-active {
    color: var(--imm-accent);
    background: rgba(255, 255, 255, 0.1);
  }
}

.speed-dropdown {
  position: relative;
}

.speed-menu {
  position: absolute;
  bottom: 100%;
  right: 0;
  margin-bottom: 8px;
  background: rgba(30, 30, 30, 0.95);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 4px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  min-width: 120px;
  z-index: 200;
}

.speed-menu-item {
  display: block;
  width: 100%;
  padding: 8px 16px;
  background: transparent;
  border: none;
  border-radius: 4px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.875rem;
  text-align: left;
  cursor: pointer;
  transition: all 0.15s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
  }

  &.is-selected {
    color: var(--imm-accent);
    font-weight: 600;
    background: rgba(255, 255, 255, 0.05);
  }
}

.info-panel {
  position: absolute;
  top: 80px;
  right: 24px;
  width: 300px;
  max-height: calc(100vh - 120px);
  overflow-y: auto;
  padding: 20px;
  background: rgba(0, 0, 0, 0.9);
  border-radius: 12px;
  backdrop-filter: blur(12px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 100;

  h3 {
    color: white;
    font-size: 1rem;
    margin: 0 0 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  }
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
}

.info-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.875rem;
}

.info-value {
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
}

// 动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}

.scale-fade-enter-active,
.scale-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.scale-fade-enter-from,
.scale-fade-leave-to {
  opacity: 0;
  transform: scale(0.5);
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.slide-right-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(20px);
  opacity: 0;
}
</style>
