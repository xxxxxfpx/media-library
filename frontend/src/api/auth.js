/**
 * 认证相关 API
 */

import api from './http'

export const authAPI = {
  login: (username, password) => api.post('/api/user/login', { username, password }),
  refresh: (refreshToken) => api.post('/api/user/refresh', { refresh_token: refreshToken }),
  getInfo: () => api.get('/api/user/info'),
  logout: () => api.post('/api/user/logout'),
}
