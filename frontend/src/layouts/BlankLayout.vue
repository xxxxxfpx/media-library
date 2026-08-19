<template>
  <!-- 空壳布局：无侧边栏/头部，直接渲染页面（登录页、404 等全屏页） -->
  <router-view v-slot="{ Component }">
    <transition name="route" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>
