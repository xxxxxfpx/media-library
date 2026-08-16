/**
 * HTTP 客户端配置 - axios 实例与拦截器
 */

import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

let isRefreshing = false
let refreshSubscribers = []

function onTokenRefreshed(newToken, error = null) {
  refreshSubscribers.forEach(({ resolve, reject, request }) => {
    if (error) {
      reject(error)
      return
    }
    request.headers.Authorization = `Bearer ${newToken}`
    resolve(api(request))
  })
  refreshSubscribers = []
}

function addRefreshSubscriber(request) {
  return new Promise((resolve, reject) => {
    refreshSubscribers.push({ resolve, reject, request })
  })
}

function logoutAndRedirect() {
  sessionStorage.removeItem('access_token')
  sessionStorage.removeItem('refresh_token')
  if (window.location.pathname !== '/login') {
    window.location.href = '/login'
  }
}

api.interceptors.request.use(
  config => {
    const token = sessionStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  response => {
    return response.data
  },
  async error => {
    const originalRequest = error.config

    if (error.response?.status !== 401) {
      return Promise.reject(error)
    }

    if (originalRequest.url?.includes('/api/user/refresh')) {
      logoutAndRedirect()
      return Promise.reject(error)
    }

    const refreshToken = sessionStorage.getItem('refresh_token')
    if (!refreshToken) {
      logoutAndRedirect()
      return Promise.reject(error)
    }

    if (isRefreshing) {
      return addRefreshSubscriber(originalRequest)
    }

    isRefreshing = true

    try {
      const response = await api.post('/api/user/refresh', {
        refresh_token: refreshToken
      })

       const newAccessToken = response.access_token
       const newRefreshToken = response.refresh_token

      sessionStorage.setItem('access_token', newAccessToken)
      sessionStorage.setItem('refresh_token', newRefreshToken)

      originalRequest.headers.Authorization = `Bearer ${newAccessToken}`

      onTokenRefreshed(newAccessToken)

      return api(originalRequest)
    } catch (refreshError) {
      onTokenRefreshed(null, refreshError)
      logoutAndRedirect()
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  }
)

export default api
