/**
 * 应用状态管理 - 组合入口
 */

import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import { useThemeStore, THEMES } from './theme'
import { useLayoutStore } from './layout'

export const useAppStore = defineStore('app', () => {
  const auth = useAuthStore()
  const theme = useThemeStore()
  const layout = useLayoutStore()

  return {
    // 认证
    token: auth.token,
    userInfo: auth.userInfo,
    isLoading: auth.isLoading,
    isLoggedIn: auth.isLoggedIn,
    isAdmin: auth.isAdmin,
    login: auth.login,
    logout: auth.logout,
    fetchUserInfo: auth.fetchUserInfo,

    // 主题
    theme: theme.theme,
    themes: THEMES,
    userSetting: theme.userSetting,
    setTheme: theme.setTheme,
    toggleTheme: theme.toggleTheme,

    // 布局
    sidebarCollapsed: layout.sidebarCollapsed,
    toggleSidebar: layout.toggleSidebar,
  }
})
