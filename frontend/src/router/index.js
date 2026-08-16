/**
 * 路由配置
 */

import { createRouter, createWebHistory } from 'vue-router'
import { authAPI } from '@/api'
import { useAppStore } from '@/store'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/library',
    name: 'Library',
    component: () => import('@/views/Library.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('@/views/Favorites.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('@/views/History.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/media/:id',
    name: 'Media',
    component: () => import('@/views/Media.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/player',
    name: 'Player',
    component: () => import('@/views/VideoPlayer.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/system',
    name: 'System',
    component: () => import('@/views/System.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const token = sessionStorage.getItem('access_token')

  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  if (to.name === 'Login' && token) {
    next({ name: 'Home' })
    return
  }

  // 检查管理员权限：优先使用 store 缓存，避免每次导航都请求用户信息
  if (to.meta.requiresAdmin && token) {
    const store = useAppStore()
    try {
      let userInfo = store.userInfo
      if (!userInfo) {
        userInfo = await authAPI.getInfo()
        store.userInfo = userInfo
      }
      if (!userInfo.is_admin) {
        next({ name: 'Home' })
        return
      }
    } catch (error) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
  }

  next()
})

export default router
