<template>
  <!-- 演示布局：顶部导航布局 —— 零侵入示例
       新增此文件 + registry.js 登记一行 + 路由 meta.layout='topnav' 即可启用，无需改动 App.vue / 其它布局 -->
  <div class="topnav-layout">
    <div class="topnav-header">
      <div class="topnav-brand">
        <AppIcon name="clapperboard" :size="22" class="brand-icon" />
        <span class="brand-text">Media Library</span>
      </div>
      <nav class="topnav-menu">
        <router-link v-for="item in menu" :key="item.to" :to="item.to" class="topnav-link" active-class="active">
          <AppIcon :name="item.icon" :size="16" /> {{ item.title }}
        </router-link>
      </nav>
      <div class="topnav-actions">
        <ThemeSwitcher />
        <span class="user-name">{{ store.userInfo?.username }}</span>
      </div>
    </div>
    <div class="topnav-content">
      <router-view v-slot="{ Component }">
        <transition name="route" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup>
import { useAppStore } from '@/store'
import AppIcon from '@/components/ui/AppIcon.vue'
import ThemeSwitcher from '@/components/ui/ThemeSwitcher.vue'

const store = useAppStore()
const menu = [
  { to: '/', icon: 'home', title: '首页' },
  { to: '/library', icon: 'clapperboard', title: '媒体库' },
  { to: '/favorites', icon: 'star', title: '收藏' },
  { to: '/history', icon: 'history', title: '最近观看' },
  { to: '/settings', icon: 'settings', title: '设置' },
]
</script>

<style scoped lang="scss">
.topnav-layout { min-height: 100vh; display:flex; flex-direction:column; background:var(--imm-bg-primary); }
.topnav-header { height: var(--header-height); display:flex; align-items:center; gap:24px; padding:0 24px; background:var(--imm-glass-bg); backdrop-filter:var(--imm-backdrop); border-bottom:1px solid var(--imm-divider); flex-shrink:0; }
.topnav-brand { display:flex; align-items:center; gap:10px; font-weight:600; color:var(--imm-text-primary); white-space:nowrap; .brand-icon{ color:var(--imm-accent);} }
.topnav-menu { display:flex; gap:4px; flex:1; .topnav-link{ display:inline-flex; align-items:center; gap:6px; padding:6px 14px; border-radius:999px; color:var(--imm-text-tertiary); font-size:.875rem; text-decoration:none; transition: all var(--duration-fast) var(--ease-standard); &:hover{ background:var(--imm-hover); color:var(--imm-text-primary);} &.active{ background:var(--imm-accent-bg); color:var(--imm-accent);} } }
.topnav-actions { display:flex; align-items:center; gap:12px; .user-name{ font-size:.875rem; color:var(--imm-text-secondary);} }
.topnav-content { flex:1; overflow:auto; }
</style>
