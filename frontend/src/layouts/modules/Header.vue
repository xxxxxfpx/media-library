<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/store'
import { authAPI } from '@/api'
import AppIcon from '@/components/ui/AppIcon.vue'
import ThemeSwitcher from '@/components/ui/ThemeSwitcher.vue'

const route = useRoute()
const router = useRouter()
const store = useAppStore()
const pageTitle = computed(() => route.meta.title || '首页')
function handleCommand(c) {
  if (c === 'logout') { authAPI.logout().catch(() => {}); store.logout(); router.push('/login') }
  else if (c === 'settings') router.push('/settings')
}
</script>

<template>
  <div class="header-module">
    <h2 class="page-title">{{ pageTitle }}</h2>
    <div class="header-right">
      <ThemeSwitcher />
      <el-dropdown trigger="click" @command="handleCommand">
        <div class="user-menu-trigger">
          <el-avatar :size="32" class="user-avatar-small">{{ store.userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}</el-avatar>
          <AppIcon name="chevron-down" :size="14" class="dropdown-icon" />
        </div>
        <template #dropdown>
          <el-dropdown-menu class="user-dropdown">
            <el-dropdown-item command="settings"><AppIcon name="settings" :size="16" /> 个人设置</el-dropdown-item>
            <el-dropdown-item divided command="logout"><AppIcon name="log-out" :size="16" /> 退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<style scoped lang="scss">
.header-module { display:flex; justify-content:space-between; align-items:center; width:100%; height:100%; }
.page-title { font-size:1.375rem; font-weight:600; color:var(--imm-text-primary); margin:0; letter-spacing:-.01em; }
.header-right { display:flex; align-items:center; gap:12px; }
.user-menu-trigger { display:flex; align-items:center; gap:6px; cursor:pointer; padding:4px 8px 4px 4px; border-radius:10px; transition: background var(--duration-fast) var(--ease-standard); &:hover{ background:var(--imm-hover);} .user-avatar-small{ background:linear-gradient(135deg, var(--imm-accent) 0%, var(--imm-accent-dark) 100%); color:var(--color-text-inverse); font-weight:600;} .dropdown-icon{ color:var(--imm-text-disabled);} }
:deep(.user-dropdown){ background:var(--imm-bg-elevated)!important; border:1px solid var(--imm-border)!important; border-radius:12px!important; box-shadow:var(--shadow-lg)!important; .el-dropdown-menu__item{ color:var(--imm-text-secondary)!important; border-radius:8px; padding:10px 16px; .app-icon{ margin-right:10px;} &:hover{ background:var(--imm-accent-bg)!important; color:var(--imm-accent)!important;}} }
</style>
