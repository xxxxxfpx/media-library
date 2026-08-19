<script setup>
/**
 * 侧边栏模块 —— 从 MainLayout 抽离的可复用导航模块
 * 供 AppShell 组合式布局复用；样式令牌化，支持折叠与抽屉态。
 */
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/store'
import AppIcon from '@/components/ui/AppIcon.vue'

const route = useRoute()
const store = useAppStore()

const menuItems = [
  { to: '/', icon: 'home', title: '首页' },
  { to: '/library', icon: 'clapperboard', title: '媒体库' },
  { to: '/favorites', icon: 'star', title: '收藏' },
  { to: '/history', icon: 'history', title: '最近观看' },
]
const adminItems = [
  { to: '/settings', icon: 'settings', title: '设置' },
  { to: '/system', icon: 'monitor', title: '系统监控', adminOnly: true },
]
const visibleAdminItems = computed(() => adminItems.filter((i) => !i.adminOnly || store.isAdmin))
</script>

<template>
  <div class="sidebar-module">
    <div class="brand">
      <AppIcon name="clapperboard" :size="28" class="brand-icon" />
      <span v-show="!store.sidebarCollapsed" class="brand-text">Media Library</span>
    </div>
    <el-menu :default-active="route.path" router class="nav-menu" :collapse="store.sidebarCollapsed" :collapse-transition="false">
      <el-menu-item v-for="item in menuItems" :key="item.to" :index="item.to">
        <AppIcon :name="item.icon" :size="18" />
        <template #title>{{ item.title }}</template>
      </el-menu-item>
      <div class="nav-divider" />
      <el-menu-item v-for="item in visibleAdminItems" :key="item.to" :index="item.to">
        <AppIcon :name="item.icon" :size="18" />
        <template #title>{{ item.title }}</template>
      </el-menu-item>
    </el-menu>
    <div class="sidebar-footer">
      <div class="user-info">
        <el-avatar :size="store.sidebarCollapsed ? 32 : 36" class="user-avatar">{{ store.userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}</el-avatar>
        <div v-show="!store.sidebarCollapsed" class="user-meta">
          <div class="user-name">{{ store.userInfo?.username || '用户' }}</div>
          <div class="user-role">{{ store.isAdmin ? '管理员' : '普通用户' }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.sidebar-module { display: flex; flex-direction: column; height: 100%; padding: 24px 12px; }
.brand { display: flex; align-items: center; gap: 12px; padding: 0 12px 24px; margin-bottom: 16px; border-bottom: 1px solid var(--imm-divider); color: var(--imm-text-primary); white-space: nowrap; .brand-icon { color: var(--imm-accent); } .brand-text { font-size: 1.125rem; font-weight: 600; } }
.nav-menu { flex: 1; background: transparent !important; border: none !important; :deep(.el-menu-item) { color: var(--imm-text-tertiary) !important; border-radius: 10px; margin: 4px 0; height: 48px; .app-icon { margin-right: 12px; } &:hover { background: var(--imm-hover) !important; } &.is-active { background: var(--imm-accent-bg) !important; color: var(--imm-accent) !important; } } }
.nav-divider { height: 1px; background: var(--imm-divider); margin: 16px 12px; }
.sidebar-footer { padding-top: 16px; border-top: 1px solid var(--imm-divider); .user-info { display:flex; align-items:center; gap:12px; padding:0 12px; .user-avatar { background: linear-gradient(135deg, var(--imm-accent) 0%, var(--imm-accent-dark) 100%); color: var(--color-text-inverse); font-weight:600; } .user-meta .user-name{ color:var(--imm-text-primary); font-weight:500; font-size:.875rem;} .user-meta .user-role{ color:var(--imm-text-disabled); font-size:.75rem;} } }
</style>
