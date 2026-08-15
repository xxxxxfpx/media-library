/**
 * 播放器状态管理组合式函数
 * 统一处理播放器状态变更和 UserData 同步
 */

import { ref, watch } from 'vue'
import { userAPI } from '@/api'

export function usePlayerState(itemId, videoRef) {
  // 状态
  const currentTime = ref(0)
  const duration = ref(0)
  const volume = ref(1)
  const playbackRate = ref(1)
  const isMuted = ref(false)

  // 同步定时器
  let syncTimer = null
  const syncInterval = ref(8000) // 默认 8 秒

  /**
   * 同步播放数据到后端
   */
  async function syncPlayback(extraData = {}) {
    if (!itemId.value) return
    try {
      await userAPI.updateUserData({
        item_id: parseInt(itemId.value),
        playback_position: currentTime.value,
        playback_rate: playbackRate.value,
        ...extraData,
      })
    } catch {
      // 静默失败
    }
  }

  /**
   * 启动定时同步
   */
  function startSyncTimer() {
    stopSyncTimer()
    syncTimer = setInterval(() => {
      syncPlayback()
    }, syncInterval.value)
  }

  /**
   * 停止定时同步
   */
  function stopSyncTimer() {
    if (syncTimer) {
      clearInterval(syncTimer)
      syncTimer = null
    }
  }

  /**
   * 设置当前时间（统一入口）
   */
  function setCurrentTime(time) {
    if (!videoRef.value) return
    videoRef.value.currentTime = time
    currentTime.value = time
    // 立即同步
    syncPlayback()
  }

  /**
   * 设置音量（统一入口）
   */
  function setVolume(vol) {
    if (!videoRef.value) return
    videoRef.value.volume = vol
    volume.value = vol
    isMuted.value = vol === 0
  }

  /**
   * 设置播放速率（统一入口）
   */
  function setPlaybackRate(rate) {
    if (!videoRef.value) return
    videoRef.value.playbackRate = rate
    playbackRate.value = rate
    // 立即同步
    syncPlayback()
  }

  /**
   * 设置静音（统一入口）
   */
  function setMuted(muted) {
    if (!videoRef.value) return
    videoRef.value.muted = muted
    isMuted.value = muted
    if (muted) {
      volume.value = 0
    }
  }

  /**
   * 从 video 元素同步状态到响应式变量
   */
  function syncStateFromVideo() {
    if (!videoRef.value) return
    currentTime.value = videoRef.value.currentTime
    duration.value = videoRef.value.duration
    volume.value = videoRef.value.volume
    playbackRate.value = videoRef.value.playbackRate
    isMuted.value = videoRef.value.muted
  }

  /**
   * 加载用户设置
   */
  async function loadUserSettings() {
    try {
      const settings = await userAPI.getSetting()
      if (settings.auto_sync_interval) {
        syncInterval.value = settings.auto_sync_interval * 1000
      }
      return settings
    } catch {
      return {}
    }
  }

  /**
   * 应用用户设置到播放器
   */
  function applyUserSettings(settings) {
    if (!videoRef.value) return

    const shouldAutoplay = localStorage.getItem('video_autoplay') === 'true'
    const shouldMuted = localStorage.getItem('video_default_muted') === 'true'

    if (shouldAutoplay) {
      videoRef.value.muted = true // 自动播放必须静音
      videoRef.value.play().catch(() => {
        console.log('自动播放被浏览器阻止')
      })
    } else if (shouldMuted) {
      videoRef.value.muted = true
    }
  }

  /**
   * 播放结束处理
   */
  function onEnded() {
    syncPlayback({ is_played: true })
    stopSyncTimer()
  }

  /**
   * 暂停处理
   */
  function onPause() {
    syncPlayback()
    stopSyncTimer()
  }

  /**
   * 播放处理
   */
  function onPlay() {
    startSyncTimer()
  }

  // 清理
  function dispose() {
    stopSyncTimer()
  }

  return {
    // 状态
    currentTime,
    duration,
    volume,
    playbackRate,
    isMuted,
    syncInterval,

    // 方法
    syncPlayback,
    startSyncTimer,
    stopSyncTimer,
    setCurrentTime,
    setVolume,
    setPlaybackRate,
    setMuted,
    syncStateFromVideo,
    loadUserSettings,
    applyUserSettings,
    onEnded,
    onPause,
    onPlay,
    dispose,
  }
}
