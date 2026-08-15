/**
 * URL 工具函数
 */

export function getFileDataUrl(fileId) {
  const token = localStorage.getItem('access_token')
  const base = `/api/file/data?file_id=${fileId}`
  return token ? `${base}&token=${encodeURIComponent(token)}` : base
}

export function getPrimaryImageUrl(item) {
  if (!item?.files) return ''
  const primary = item.files.find(f => f.image_type === 'Primary')
  return primary ? getFileDataUrl(primary.id) : ''
}
