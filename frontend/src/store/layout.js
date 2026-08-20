/**
 * 布局状态管理
 */

import { ref } from 'vue'

export function useLayoutStore() {
  const sidebarCollapsed = ref(localStorage.getItem('sidebar_collapsed') === 'true')
  // 移动端抽屉菜单开关：仅会话内有效，不持久化
  const mobileMenuOpen = ref(false)

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
    localStorage.setItem('sidebar_collapsed', sidebarCollapsed.value)
  }

  function setMobileMenuOpen(open) {
    mobileMenuOpen.value = open
  }

  return {
    sidebarCollapsed,
    toggleSidebar,
    mobileMenuOpen,
    setMobileMenuOpen,
  }
}