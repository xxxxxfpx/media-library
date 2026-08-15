import { describe, it, expect } from 'vitest'
import { formatDate, formatFileSize, formatTime, parseFFmpegInfo } from '@/utils/format'

describe('formatDate', () => {
  it('returns empty string for nullish input', () => {
    expect(formatDate(null)).toBe('')
    expect(formatDate('')).toBe('')
  })

  it('formats ISO date to zh-CN style', () => {
    expect(formatDate('2024-01-05')).toMatch(/^2024年01月\d{2}日$/)
  })
})

describe('formatFileSize', () => {
  it('handles zero bytes', () => {
    expect(formatFileSize(0)).toBe('0 B')
    expect(formatFileSize(null)).toBe('0 B')
  })

  it('converts units', () => {
    expect(formatFileSize(1024)).toBe('1 KB')
    expect(formatFileSize(5 * 1024 * 1024)).toBe('5 MB')
  })
})

describe('formatTime', () => {
  it('handles zero and NaN', () => {
    expect(formatTime(0)).toBe('00:00')
    expect(formatTime(NaN)).toBe('00:00')
  })

  it('formats minutes and hours', () => {
    expect(formatTime(65)).toBe('01:05')
    expect(formatTime(3725)).toBe('1:02:05')
  })
})

describe('parseFFmpegInfo', () => {
  it('returns empty object without ffmpeg data', () => {
    expect(parseFFmpegInfo(null)).toEqual({})
  })

  it('parses streams and format info', () => {
    const info = parseFFmpegInfo({
      format: { duration: '120.5', size: '104857600', bit_rate: '8000000' },
      streams: [{ codec_type: 'video', codec_name: 'h264', height: 1080 }],
    })
    expect(info.resolution).toBe('1080p')
    expect(info.codec).toBe('H264')
    expect(info.bitrate).toBe('8.00 Mbps')
    expect(info.duration).toBe('02:00')
    expect(info.size).toBe('100 MB')
  })
})
