/**
 * 主题状态管理
 */

import { ref } from 'vue'
import { userAPI } from '@/api'

export function useThemeStore() {
  const theme = ref(localStorage.getItem('theme') || 'dark')
  const userSetting = ref({ theme_mode: theme.value })

  async function setTheme(newTheme, persist = true) {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    document.documentElement.setAttribute('data-theme', newTheme)
    userSetting.value.theme_mode = newTheme
    if (persist) {
      try {
        await userAPI.updateSetting({ theme_mode: newTheme })
      } catch (error) {
        // 静默处理
      }
    }
  }

  function toggleTheme() {
    setTheme(theme.value === 'dark' ? 'light' : 'dark')
  }

  return {
    theme,
    userSetting,
    setTheme,
    toggleTheme,
  }
}
