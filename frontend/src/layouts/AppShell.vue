<script setup>
/**
 * AppShell —— 组合式布局壳（需求 5）
 * 根据当前路由 meta.layout 动态解析布局组件并渲染。
 * 布局组件内部自行渲染 <router-view />。
 */
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { resolveLayout } from './registry'

const route = useRoute()
const Layout = computed(() => resolveLayout(route.meta.layout))
</script>

<template>
  <component :is="Layout" />
</template>
