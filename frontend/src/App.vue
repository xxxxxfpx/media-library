<template>
  <router-view v-if="isPublicRoute" />
  <MainLayout v-else />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'
import { useAppStore } from '@/store'
import MainLayout from '@/layouts/MainLayout.vue'

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
</style>
