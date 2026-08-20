<template>
  <div class="layout-container" :class="{ 'is-mobile': isMobile }">
    <!-- 移动端遮罩层 -->
    <transition name="fade">
      <div
        v-if="isMobile && store.mobileMenuOpen"
        class="mobile-mask"
        @click="store.setMobileMenuOpen(false)"
      ></div>
    </transition>

    <!-- 左侧侧边栏（移动端为抽屉） -->
    <el-aside
      :width="isMobile ? '240px' : sidebarWidth"
      class="sidebar"
      :class="{ 'is-drawer': isMobile, 'is-open': isMobile && store.mobileMenuOpen }"
    >
      <div class="sidebar-inner">
        <div class="brand">
          <AppIcon name="clapperboard" :size="28" class="brand-icon" />
          <span v-show="isMobile || !store.sidebarCollapsed" class="brand-text">Media Library</span>
        </div>

        <el-menu
          :default-active="route.path"
          router
          class="nav-menu"
          :collapse="!isMobile && store.sidebarCollapsed"
          :collapse-transition="false"
          @select="handleNavSelect"
        >
          <el-menu-item v-for="item in menuItems" :key="item.to" :index="item.to">
            <AppIcon :name="item.icon" :size="18" />
            <template #title>{{ item.title }}</template>
          </el-menu-item>

          <div class="nav-divider"></div>

          <el-menu-item v-for="item in visibleAdminItems" :key="item.to" :index="item.to">
            <AppIcon :name="item.icon" :size="18" />
            <template #title>{{ item.title }}</template>
          </el-menu-item>
        </el-menu>

        <div class="sidebar-footer">
          <div class="user-info">
            <el-avatar :size="isMobile || !store.sidebarCollapsed ? 36 : 32" class="user-avatar">
              {{ store.userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}
            </el-avatar>
            <div v-show="isMobile || !store.sidebarCollapsed" class="user-meta">
              <div class="user-name">{{ store.userInfo?.username || '用户' }}</div>
              <div class="user-role">{{ store.isAdmin ? '管理员' : '普通用户' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 收缩按钮 -->
      <button class="collapse-btn" @click="store.toggleSidebar">
        <AppIcon :name="store.sidebarCollapsed ? 'panel-left-open' : 'panel-left-close'" :size="16" />
      </button>
    </el-aside>

    <!-- 右侧内容区 -->
    <div class="main-area">
      <!-- 头部 -->
      <el-header class="header">
        <div class="header-left">
          <button v-if="isMobile" class="icon-btn hamburger-btn" @click="store.setMobileMenuOpen(true)" aria-label="打开菜单">
            <AppIcon name="menu" :size="20" />
          </button>
          <h2 class="page-title">{{ pageTitle }}</h2>
        </div>
        <div class="header-right">
          <ThemeSwitcher />

          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-menu-trigger">
              <el-avatar :size="32" class="user-avatar-small">
                {{ store.userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}
              </el-avatar>
              <AppIcon name="chevron-down" :size="14" class="dropdown-icon" />
            </div>
            <template #dropdown>
              <el-dropdown-menu class="user-dropdown">
                <el-dropdown-item command="settings">
                  <AppIcon name="settings" :size="16" /> 个人设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <AppIcon name="log-out" :size="16" /> 退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 动态内容 -->
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="route" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/store'
import { authAPI } from '@/api'
import AppIcon from '@/components/ui/AppIcon.vue'
import ThemeSwitcher from '@/components/ui/ThemeSwitcher.vue'

const route = useRoute()
const router = useRouter()
const store = useAppStore()

// 移动端断点检测：<768px 视为移动端，侧边栏变抽屉
const MOBILE_BREAKPOINT = 768
const isMobile = ref(window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`).matches)
const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`)
function handleMqlChange(e) {
  isMobile.value = e.matches
  if (e.matches) store.setMobileMenuOpen(false)
}
mql.addEventListener('change', handleMqlChange)
onBeforeUnmount(() => mql.removeEventListener('change', handleMqlChange))

const sidebarWidth = computed(() => (store.sidebarCollapsed ? '72px' : '240px'))

// 侧边栏菜单：由路由 meta 驱动（新增页面只需在 router/index.js 注册 meta.icon + meta.menu）
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

// 仅管理员可见的菜单（adminOnly 项）
const visibleAdminItems = computed(() =>
  adminItems.filter((item) => !item.adminOnly || store.isAdmin)
)

const pageTitle = computed(() => route.meta.title || '首页')

// 移动端点击菜单项后关闭抽屉
function handleNavSelect() {
  if (isMobile.value) store.setMobileMenuOpen(false)
}

function handleCommand(command) {
  if (command === 'logout') {
    authAPI.logout().catch(() => {})
    store.logout()
    router.push('/login')
  } else if (command === 'settings') {
    router.push('/settings')
  }
}
</script>

<style scoped lang="scss">
.layout-container {
  height: 100vh;
  display: flex;
  background: var(--imm-bg-primary);
  overflow: hidden;
}

// ===== 侧边栏 =====
.sidebar {
  position: relative;
  background: var(--imm-bg-secondary);
  border-right: 1px solid var(--imm-divider);
  display: flex;
  flex-direction: column;
  transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  z-index: 10;
}

.sidebar-inner {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 24px 12px;
  overflow: hidden;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 12px 24px;
  margin-bottom: 16px;
  border-bottom: 1px solid var(--imm-divider);
  color: var(--imm-text-primary);
  white-space: nowrap;

  .brand-icon {
    color: var(--imm-accent);
  }

  .brand-text {
    font-size: 1.125rem;
    font-weight: 600;
    background: linear-gradient(135deg, var(--imm-text-primary) 0%, var(--imm-text-secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
}

.nav-menu {
  flex: 1;
  background: transparent !important;
  border: none !important;

  :deep(.el-menu-item) {
    color: var(--imm-text-tertiary) !important;
    border-radius: 10px;
    margin: 4px 0;
    height: 48px;
    line-height: 48px;
    font-size: 0.9375rem;
    white-space: nowrap;

    .app-icon {
      margin-right: 12px;
    }

    &:hover {
      background: var(--imm-hover) !important;
      color: var(--imm-text-secondary) !important;
    }

    &.is-active {
      background: var(--imm-accent-bg) !important;
      color: var(--imm-accent) !important;
      font-weight: 500;
    }
  }

  // 收缩模式下图标居中
  &:not(:deep(.el-menu--collapse)) {
    .el-menu-item .app-icon {
      margin-right: 12px;
    }
  }
}

.nav-divider {
  height: 1px;
  background: var(--imm-divider);
  margin: 16px 12px;
}

.sidebar-footer {
  padding-top: 16px;
  border-top: 1px solid var(--imm-divider);
  white-space: nowrap;

  .user-info {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 12px;

    .user-avatar {
      background: linear-gradient(135deg, var(--imm-accent) 0%, var(--imm-accent-dark) 100%);
      color: var(--color-text-inverse);
      font-weight: 600;
      flex-shrink: 0;
    }

    .user-meta {
      flex: 1;
      min-width: 0;

      .user-name {
        color: var(--imm-text-primary);
        font-weight: 500;
        font-size: 0.875rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .user-role {
        color: var(--imm-text-disabled);
        font-size: 0.75rem;
      }
    }
  }
}

// 收缩按钮
.collapse-btn {
  position: absolute;
  bottom: 24px;
  right: -16px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid var(--imm-border);
  background: var(--imm-bg-elevated);
  color: var(--imm-text-tertiary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 11;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px var(--imm-overlay);

  &:hover {
    background: var(--imm-accent);
    color: var(--color-text-inverse);
    border-color: var(--imm-accent);
    box-shadow: 0 4px 12px var(--color-accent-glow);
  }
}

// ===== 主内容区 =====
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: var(--imm-bg-primary);
}

// 头部
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--imm-glass-bg);
  backdrop-filter: var(--imm-backdrop);
  border-bottom: 1px solid var(--imm-divider);
  padding: 0 32px;
  height: 64px !important;
  flex-shrink: 0;
}

.header-left {
  .page-title {
    font-size: 1.375rem;
    font-weight: 600;
    color: var(--imm-text-primary);
    margin: 0;
    letter-spacing: -0.01em;
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-menu-trigger {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 4px 8px 4px 4px;
  border-radius: 10px;
  transition: background 0.3s ease;

  &:hover {
    background: var(--imm-hover);
  }

  .user-avatar-small {
    background: linear-gradient(135deg, var(--imm-accent) 0%, var(--imm-accent-dark) 100%);
    color: var(--color-text-inverse);
    font-weight: 600;
  }

  .dropdown-icon {
    color: var(--imm-text-disabled);
  }
}

// 主内容
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 0;
  background: var(--imm-bg-primary);
}

// 下拉菜单
:deep(.user-dropdown) {
  background: var(--imm-bg-elevated) !important;
  border: 1px solid var(--imm-border) !important;
  border-radius: 12px !important;
  box-shadow: 0 16px 48px var(--imm-overlay) !important;
  padding: 8px !important;

  .el-dropdown-menu__item {
    color: var(--imm-text-secondary) !important;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 0.875rem;

    .app-icon {
      margin-right: 10px;
    }

    &:hover {
      background: var(--imm-accent-bg) !important;
      color: var(--imm-accent) !important;
    }
  }
}

// ===== 移动端响应式 =====
@media (max-width: 767px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    height: 100%;
    transform: translateX(-100%);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1000;
    box-shadow: none;
    width: 240px !important;

    &.is-open {
      transform: translateX(0);
      box-shadow: 16px 0 48px var(--imm-overlay);
    }

    .collapse-btn {
      display: none;
    }
  }

  .layout-container.is-mobile .sidebar.is-drawer + .main-area {
    width: 100%;
  }
}

.mobile-mask {
  position: fixed;
  inset: 0;
  background: var(--imm-overlay);
  z-index: 999;
}

.header-left {
  .hamburger-btn {
    margin-right: 4px;
  }
}

// 通用图标按钮
.icon-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 1px solid var(--imm-border);
  background: var(--imm-bg-elevated);
  color: var(--imm-text-secondary);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;

  &:hover {
    background: var(--imm-hover);
    color: var(--imm-text-primary);
  }
}

// 遮罩淡入淡出
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
