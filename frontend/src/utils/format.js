/**
 * 格式化工具函数
 */

export function formatDate(dateStr) {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}年${month}月${day}日`
  } catch {
    return dateStr
  }
}

export function formatFileSize(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

export function formatTime(seconds) {
  if (!seconds || isNaN(seconds)) return '00:00'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  if (h > 0) {
    return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  }
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

export function parseFFmpegInfo(ffmpeg, fileSize) {
  if (!ffmpeg) return {}
  const format = ffmpeg.format || {}
  const streams = ffmpeg.streams || []
  const videoStream = streams.find(s => s.codec_type === 'video')

  let resolution = ''
  if (videoStream?.height) {
    if (videoStream.height >= 2160) resolution = '4K'
    else if (videoStream.height >= 1080) resolution = '1080p'
    else if (videoStream.height >= 720) resolution = '720p'
    else if (videoStream.height >= 480) resolution = '480p'
    else resolution = `${videoStream.width}x${videoStream.height}`
  }

  let bitrate = ''
  if (format.bit_rate) {
    const mbps = parseInt(format.bit_rate) / 1000000
    bitrate = `${mbps.toFixed(2)} Mbps`
  } else if (videoStream?.bit_rate) {
    const mbps = parseInt(videoStream.bit_rate) / 1000000
    bitrate = `${mbps.toFixed(2)} Mbps`
  }

  let duration = ''
  if (format.duration) {
    duration = formatTime(parseFloat(format.duration))
  }

  let size = ''
  if (format.size) {
    size = formatFileSize(format.size)
  } else if (fileSize) {
    size = formatFileSize(fileSize)
  }

  return {
    resolution,
    codec: videoStream?.codec_name?.toUpperCase() || '',
    bitrate,
    duration,
    size,
  }
}
