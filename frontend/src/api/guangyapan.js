import api from './http'

export const guangYaPanAPI = {
  getConfig: () => api.get('/api/drives/guangyapan/config'),
  updateConfig: (config) => api.put('/api/drives/guangyapan/config', config),
  testConfig: (payload) => api.post('/api/drives/guangyapan/test', payload),
}
