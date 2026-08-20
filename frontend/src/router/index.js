/**
 * 路由配置 —— 现代化：meta 增加 title/layout/icon 驱动模块化布局与侧边栏
 * - meta.title: 页面标题（布局头部读取）
 * - meta.layout: 布局 key（默认 main，见 layouts/registry.js）
 * - meta.icon: 侧边栏菜单图标（lucide 名，MainLayout 菜单读取）
 * - meta.menu: 是否显示在侧边栏
 */

import { createRouter, createWebHistory } from 'vue-router'
import { authAPI } from '@/api'
import { useAppStore } from '@/store'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false, title: '登录', layout: 'blank' }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true, title: '首页', icon: 'home', menu: true }
  },
  {
    path: '/library',
    name: 'Library',
    component: () => import('@/views/Library.vue'),
    meta: { requiresAuth: true, title: '媒体库', icon: 'clapperboard', menu: true }
  },
  {
    path: '/recent',
    name: 'Recent',
    component: () => import('@/views/Recent.vue'),
    meta: { requiresAuth: true, title: '最近添加', icon: 'clock-plus', menu: true }
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('@/views/Favorites.vue'),
    meta: { requiresAuth: true, title: '收藏', icon: 'star', menu: true }
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('@/views/History.vue'),
    meta: { requiresAuth: true, title: '最近观看', icon: 'history', menu: true }
  },
  {
    path: '/media/:id',
    name: 'Media',
    component: () => import('@/views/Media.vue'),
    meta: { requiresAuth: true, title: '媒体详情' }
  },
  {
    path: '/player',
    name: 'Player',
    component: () => import('@/views/VideoPlayer.vue'),
    meta: { requiresAuth: true, title: '播放器' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { requiresAuth: true, title: '设置', icon: 'settings', menu: true }
  },
  {
    path: '/system',
    name: 'System',
    component: () => import('@/views/System.vue'),
    meta: { requiresAuth: true, requiresAdmin: true, title: '系统监控', icon: 'monitor', menu: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { requiresAuth: false, title: '404', layout: 'blank' }
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

  // 同步文档标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 媒体库管理系统`
  }

  next()
})

export default router
