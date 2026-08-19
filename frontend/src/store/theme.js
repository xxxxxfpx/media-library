/**
 * 主题状态管理（升级版）
 * - 支持 6 套主题（现代黑 / 现代白 为必备）
 * - 兼容旧 localStorage 键 'theme'（dark/light）的迁移
 * - 首屏 data-theme 由 index.html 内联脚本设置，本 store 仅做同步与持久化
 */

import { ref } from 'vue'
import { userAPI } from '@/api'

export const THEMES = [
  { id: 'modern-dark',  name: '现代黑', dark: true,  swatch: { page: '#0f0f12', surface: '#1b1b1f', accent: '#6366f1' } },
  { id: 'modern-light', name: '现代白', dark: false, swatch: { page: '#ffffff', surface: '#f4f4f5', accent: '#4f46e5' } },
  { id: 'indigo-night', name: '靛夜蓝', dark: true,  swatch: { page: '#0f172a', surface: '#1e293b', accent: '#38bdf8' } },
  { id: 'emerald-mist', name: '翡翠雾', dark: false, swatch: { page: '#f0fdf4', surface: '#ffffff', accent: '#10b981' } },
  { id: 'amber-sand',   name: '琥珀砂', dark: false, swatch: { page: '#fffbeb', surface: '#ffffff', accent: '#f59e0b' } },
  { id: 'rose-dusk',    name: '玫瑰暮', dark: true,  swatch: { page: '#1e1b2e', surface: '#2a2740', accent: '#f472b6' } },
]

const THEME_IDS = THEMES.map((t) => t.id)
const STORAGE_KEY = 'ui.theme'

function migrateLegacy(value) {
  if (value === 'dark') return 'modern-dark'
  if (value === 'light') return 'modern-light'
  return value
}

function resolveInitial() {
  try {
    const stored = migrateLegacy(localStorage.getItem(STORAGE_KEY) || localStorage.getItem('theme') || '')
    if (THEME_IDS.includes(stored)) return stored
  } catch (e) { /* ignore */ }
  try {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    return prefersDark ? 'modern-dark' : 'modern-light'
  } catch (e) { /* ignore */ }
  return 'modern-dark'
}

export function useThemeStore() {
  const theme = ref(resolveInitial())
  const userSetting = ref({ theme_mode: theme.value })
  const followSystem = ref(false)

  function apply(id) {
    document.documentElement.setAttribute('data-theme', id)
  }

  async function setTheme(newTheme, persist = true) {
    if (!THEME_IDS.includes(newTheme)) return
    // View Transitions API 圆形扩散（支持则平滑，不支持则直接切换）
    const doSwitch = () => {
      theme.value = newTheme
      apply(newTheme)
      userSetting.value.theme_mode = newTheme
    }
    if (typeof document !== 'undefined' && document.startViewTransition) {
      try { document.startViewTransition(doSwitch); } catch { doSwitch() }
    } else {
      doSwitch()
    }
    if (persist) {
      try { localStorage.setItem(STORAGE_KEY, newTheme) } catch (e) { /* ignore */ }
      try { await userAPI.updateSetting({ theme_mode: newTheme }) } catch (e) { /* 静默处理 */ }
    }
  }

  // 头部快捷按钮：在两个必备主题间快速切换
  function toggleTheme() {
    setTheme(theme.value === 'modern-dark' ? 'modern-light' : 'modern-dark')
  }

  // 初始化即应用（与 index.html 防闪烁脚本对齐）
  apply(theme.value)

  return { theme, userSetting, followSystem, themes: THEMES, setTheme, toggleTheme }
}
