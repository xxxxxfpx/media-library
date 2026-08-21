import api from './http'

export const collectionAPI = {
  // 采集源 CRUD
  listSources: () => api.get('/api/collection/sources'),
  createSource: (data) => api.post('/api/collection/sources', data),
  getSource: (id) => api.get(`/api/collection/sources/${id}`),
  updateSource: (id, data) => api.put(`/api/collection/sources/${id}`, data),
  deleteSource: (id) => api.delete(`/api/collection/sources/${id}`),
  toggleSource: (id, data) => api.post(`/api/collection/sources/${id}/toggle`, data),
  // 操作
  testSource: (id) => api.post(`/api/collection/sources/${id}/test`),
  triggerCollect: (id) => api.post(`/api/collection/sources/${id}/trigger`),
  // 日志
  listLogs: (sourceId = null, limit = 50) => {
    const params = {}
    if (sourceId != null) params.source_id = sourceId
    if (limit) params.limit = limit
    return api.get('/api/collection/logs', { params })
  },
}
