<template>
  <router-view v-if="isPublicRoute" />
  <AppShell v-else />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'
import { useAppStore } from '@/store'
import AppShell from '@/layouts/AppShell.vue'

const route = useRoute()
const store = useAppStore()

const isPublicRoute = computed(() => {
  const path = route.path
  return path === '/login' || path.startsWith('/login') || path === '/404'
})

onMounted(async () => {
  if (store.isLoggedIn) {
    await store.fetchUserInfo()
  }
  store.setTheme(store.theme, false)
})
</script>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}

/* 路由转场：优先 View Transitions API，降级为 fade+位移；全部引用动效令牌 */
.route-enter-active { transition: opacity var(--route-enter) var(--ease-standard), transform var(--route-enter) var(--ease-standard); }
.route-leave-active { transition: opacity var(--route-exit) var(--ease-exit), transform var(--route-exit) var(--ease-exit); }
.route-enter-from { opacity: 0; transform: translateY(12px); }
.route-leave-to { opacity: 0; transform: translateY(-8px); }

/* View Transitions 顶层平滑（Chrome/Edge 原生） */
::view-transition-old(root), ::view-transition-new(root) { animation-duration: var(--duration-slow); }

/* 无障碍：尊重 prefers-reduced-motion，全部非必要动效归零 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .route-enter-active, .route-leave-active { transition-duration: 0.01ms !important; }
}
</style>
