/**
 * 用户相关 API
 */

import api from './http'

export const userAPI = {
  updateUserData: (data) => api.post('/api/user/userdata', data),
  getHistory: (params) => api.get('/api/user/history', { params }),
  getSetting: () => api.get('/api/user/setting'),
  updateSetting: (setting) => api.post('/api/user/setting', setting),
}
