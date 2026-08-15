/**
 * 布局状态管理
 */

import { ref } from 'vue'

export function useLayoutStore() {
  const sidebarCollapsed = ref(localStorage.getItem('sidebar_collapsed') === 'true')

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
    localStorage.setItem('sidebar_collapsed', sidebarCollapsed.value)
  }

  return {
    sidebarCollapsed,
    toggleSidebar,
  }
}
