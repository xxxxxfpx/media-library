<template>
  <div class="layout-container">
    <!-- 左侧侧边栏 -->
    <el-aside :width="sidebarWidth" class="sidebar">
      <div class="sidebar-inner">
        <div class="brand">
          <el-icon :size="28"><VideoCamera /></el-icon>
          <span v-show="!store.sidebarCollapsed" class="brand-text">Media Library</span>
        </div>

        <el-menu
          :default-active="route.path"
          router
          class="nav-menu"
          :collapse="store.sidebarCollapsed"
          :collapse-transition="false"
        >
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <template #title>首页</template>
          </el-menu-item>
          <el-menu-item index="/library">
            <el-icon><VideoCamera /></el-icon>
            <template #title>媒体库</template>
          </el-menu-item>
          <el-menu-item index="/favorites">
            <el-icon><Star /></el-icon>
            <template #title>收藏</template>
          </el-menu-item>
          <el-menu-item index="/history">
            <el-icon><Clock /></el-icon>
            <template #title>最近观看</template>
          </el-menu-item>
          <div class="nav-divider"></div>
          <el-menu-item index="/settings">
            <el-icon><Setting /></el-icon>
            <template #title>设置</template>
          </el-menu-item>
          <el-menu-item v-if="store.isAdmin" index="/system">
            <el-icon><Monitor /></el-icon>
            <template #title>系统监控</template>
          </el-menu-item>
        </el-menu>

        <div class="sidebar-footer">
          <div class="user-info">
            <el-avatar :size="store.sidebarCollapsed ? 32 : 36" class="user-avatar">
              {{ store.userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}
            </el-avatar>
            <div v-show="!store.sidebarCollapsed" class="user-meta">
              <div class="user-name">{{ store.userInfo?.username || '用户' }}</div>
              <div class="user-role">{{ store.isAdmin ? '管理员' : '普通用户' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 收缩按钮 -->
      <button class="collapse-btn" @click="store.toggleSidebar">
        <el-icon :size="16">
          <Fold v-if="!store.sidebarCollapsed" />
          <Expand v-else />
        </el-icon>
      </button>
    </el-aside>

    <!-- 右侧内容区 -->
    <div class="main-area">
      <!-- 头部 -->
      <el-header class="header">
        <div class="header-left">
          <h2 class="page-title">{{ pageTitle }}</h2>
        </div>
        <div class="header-right">
          <el-button
            circle
            class="theme-btn"
            @click="store.toggleTheme"
          >
            <el-icon :size="18">
              <component :is="store.theme === 'dark' ? Sunny : Moon" />
            </el-icon>
          </el-button>

          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-menu-trigger">
              <el-avatar :size="32" class="user-avatar-small">
                {{ store.userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}
              </el-avatar>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu class="user-dropdown">
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon> 个人设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon> 退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 动态内容 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/store'
import {
  VideoCamera, HomeFilled, Star, Clock, Setting, Monitor, Tools,
  Sunny, Moon, ArrowDown, SwitchButton, Fold, Expand
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const store = useAppStore()

const sidebarWidth = computed(() => store.sidebarCollapsed ? '72px' : '240px')

const pageTitle = computed(() => {
  const titles = {
    '/': '首页',
    '/library': '媒体库',
    '/favorites': '收藏',
    '/history': '最近观看',
    '/settings': '设置',
    '/system': '系统监控'
  }
  if (titles[route.path]) return titles[route.path]
  if (route.path.startsWith('/media/')) return '媒体详情'
  return '首页'
})

function handleCommand(command) {
  if (command === 'logout') {
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

    .el-icon {
      margin-right: 12px;
      font-size: 1.125rem;
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
    .el-menu-item .el-icon {
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
      color: #fff;
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
    color: #fff;
    border-color: var(--imm-accent);
    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.4);
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

  .theme-btn {
    width: 36px;
    height: 36px;
    background: var(--imm-hover) !important;
    border: 1px solid var(--imm-border) !important;
    color: var(--imm-text-secondary) !important;

    &:hover {
      background: var(--imm-hover-strong) !important;
      color: var(--imm-text-primary) !important;
    }
  }
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
    color: #fff;
    font-weight: 600;
  }

  .dropdown-icon {
    color: var(--imm-text-disabled);
    font-size: 0.75rem;
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

    .el-icon {
      margin-right: 10px;
      font-size: 1rem;
    }

    &:hover {
      background: var(--imm-accent-bg) !important;
      color: var(--imm-accent) !important;
    }
  }
}
</style>
