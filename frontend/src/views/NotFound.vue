<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <h1 class="error-code">404</h1>
      <p class="error-message">页面未找到</p>
      <p class="error-desc">您访问的页面不存在或已被移除</p>
      <el-button type="primary" size="large" @click="$router.push('/')">
        返回首页
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.not-found-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: var(--imm-bg-primary);
}

.not-found-content {
  text-align: center;
}

.error-code {
  font-size: 8rem;
  font-weight: 900;
  color: var(--imm-accent);
  margin: 0;
  line-height: 1;
  opacity: 0.6;
}

.error-message {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--imm-text-primary);
  margin: 16px 0 8px;
}

.error-desc {
  font-size: 0.9375rem;
  color: var(--imm-text-tertiary);
  margin-bottom: 32px;
}
</style>
