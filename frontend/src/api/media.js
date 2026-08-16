/**
 * 媒体相关 API
 */

import api from './http'

export const mediaAPI = {
  getList: (params, config) => api.get('/api/media/list', { params, ...config }),
  getInfo: (id) => api.get('/api/media/info', { params: { id } }),
  getStats: () => api.get('/api/media/stats'),
}
