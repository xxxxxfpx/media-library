/**
 * 认证状态管理
 */

import { ref, computed } from 'vue'
import { authAPI } from '@/api'

export function useAuthStore() {
  const token = ref(sessionStorage.getItem('access_token') || '')
  const userInfo = ref(null)
  const isLoading = ref(false)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.is_admin === true)

  async function login(username, password) {
    try {
      isLoading.value = true
      const response = await authAPI.login(username, password)

      token.value = response.access_token
      sessionStorage.setItem('access_token', response.access_token)
      sessionStorage.setItem('refresh_token', response.refresh_token)

      await fetchUserInfo()
      return { success: true }
    } catch (error) {
      return { success: false, message: error.response?.data?.detail || '登录失败' }
    } finally {
      isLoading.value = false
    }
  }

  async function logout() {
    token.value = ''
    userInfo.value = null
    sessionStorage.removeItem('access_token')
    sessionStorage.removeItem('refresh_token')
  }

  async function fetchUserInfo() {
    try {
      userInfo.value = await authAPI.getInfo()
    } catch (error) {
      // 静默处理，由 API 拦截器统一处理 401
    }
  }

  return {
    token,
    userInfo,
    isLoading,
    isLoggedIn,
    isAdmin,
    login,
    logout,
    fetchUserInfo,
  }
}
