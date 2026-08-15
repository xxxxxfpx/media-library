/**
 * 文件相关 API
 */
import api from './http'

export const fileAPI = {
  /**
   * 获取文件信息
   * @param {number} fileId - 文件ID
   * @returns {Promise<Object>} 文件信息
   */
  getInfo: (fileId) => api.get('/api/file/info', { params: { file_id: fileId } }),

  /**
   * 获取文件数据URL
   * @param {number} fileId - 文件ID
   * @returns {string} 文件数据URL
   */
  getDataUrl: (fileId) => {
    const token = localStorage.getItem('access_token')
    const base = `/api/file/data?file_id=${fileId}`
    return token ? `${base}&token=${encodeURIComponent(token)}` : base
  },
}
