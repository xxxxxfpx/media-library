<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="bg-decor">
      <div class="bg-orb bg-orb-1"></div>
      <div class="bg-orb bg-orb-2"></div>
      <div class="bg-grid"></div>
    </div>

    <main class="login-content">
      <!-- 品牌区（左侧） -->
      <section class="brand-side fade-in">
        <div class="brand-logo">
          <AppIcon name="clapperboard" :size="44" />
        </div>
        <h1 class="brand-title">Media Library</h1>
        <p class="brand-subtitle">沉浸式媒体管理体验</p>
        <ul class="brand-features">
          <li class="fade-in fade-in-delay-1">
            <span class="check">
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            </span>
            多端媒体统一管理
          </li>
          <li class="fade-in fade-in-delay-2">
            <span class="check">
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            </span>
            云盘流媒体直播
          </li>
          <li class="fade-in fade-in-delay-3">
            <span class="check">
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            </span>
            全平台数据同步
          </li>
        </ul>
      </section>

      <!-- 登录卡片（右侧） -->
      <section class="login-card fade-in fade-in-delay-2">
        <div class="card-header">
          <h2 class="card-title">欢迎回来</h2>
          <p class="card-subtitle">登录以继续探索</p>
        </div>

        <el-form ref="formRef" :model="form" :rules="rules" class="login-form" @submit.prevent="handleLogin">
          <el-form-item prop="username" required>
            <template #label>
              <span class="form-label-text"><span class="required-star">*</span>用户名</span>
            </template>
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              size="large"
              class="login-input"
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <AppIcon name="user" :size="16" />
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password" required>
            <template #label>
              <span class="form-label-text"><span class="required-star">*</span>密码</span>
            </template>
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              class="login-input"
              show-password
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <AppIcon name="lock" :size="16" />
              </template>
            </el-input>
          </el-form-item>

          <el-alert
            v-if="errorMessage"
            :title="errorMessage"
            type="error"
            show-icon
            :closable="false"
            class="login-error"
          />

          <div class="form-options">
            <el-checkbox v-model="form.remember">记住我</el-checkbox>
            <a href="#" class="forgot-link" @click.prevent>忘记密码？</a>
          </div>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="login-btn"
              @click="handleLogin"
            >
              {{ loading ? '登录中...' : '登 录' }}
            </el-button>
          </el-form-item>
        </el-form>

        <div class="card-footer">
          还没有账号？<a href="#" @click.prevent>申请访问权限</a>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/store'
import { ElMessage } from 'element-plus'
import AppIcon from '@/components/ui/AppIcon.vue'

const router = useRouter()
const store = useAppStore()

const formRef = ref(null)
const loading = ref(false)
const errorMessage = ref('')

const form = reactive({
  username: '',
  password: '',
  remember: false
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

async function handleLogin() {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch {
    return
  }

  loading.value = true
  errorMessage.value = ''

  const result = await store.login(form.username, form.password)

  loading.value = false

  if (result.success) {
    ElMessage.success('登录成功')
    router.push('/')
  } else {
    errorMessage.value = result.message
  }
}
</script>

<style scoped lang="scss">
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-page);
  position: relative;
  overflow: hidden;
  padding: 20px;
}

// ===== 背景装饰 =====
.bg-decor {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
}

.bg-orb-1 {
  width: 600px;
  height: 600px;
  top: -200px;
  left: -100px;
  background: radial-gradient(circle, var(--color-accent) 0%, transparent 70%);
  opacity: 0.25;
}

.bg-orb-2 {
  width: 500px;
  height: 500px;
  bottom: -150px;
  right: -100px;
  background: radial-gradient(circle, color-mix(in oklch, var(--color-accent) 60%, transparent) 0%, transparent 70%);
  opacity: 0.2;
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(var(--color-border-subtle) 1px, transparent 1px),
    linear-gradient(90deg, var(--color-border-subtle) 1px, transparent 1px);
  background-size: 60px 60px;
  -webkit-mask-image: radial-gradient(ellipse 80% 60% at 50% 50%, black 20%, transparent 70%);
  mask-image: radial-gradient(ellipse 80% 60% at 50% 50%, black 20%, transparent 70%);
  opacity: 0.3;
}

// ===== 主内容区 =====
.login-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 80px;
  max-width: 960px;
  width: 100%;

  @media (max-width: 768px) {
    flex-direction: column;
    gap: 40px;
  }
}

// ===== 品牌区 =====
.brand-side {
  flex: 1;
  text-align: center;
  padding-right: 20px;

  @media (max-width: 768px) {
    padding-right: 0;
  }
}

.brand-logo {
  width: 88px;
  height: 88px;
  margin: 0 auto 28px;
  background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-hover) 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-inverse);
  box-shadow:
    0 16px 48px var(--color-accent-glow),
    0 0 120px color-mix(in oklch, var(--color-accent) 15%, transparent);
  animation: float 6s ease-in-out infinite;
}

.brand-title {
  font-size: 2.75rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 8px;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.brand-subtitle {
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin: 0 0 32px;
  font-weight: 400;
}

.brand-features {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 240px;
  margin: 0 auto;

  @media (max-width: 768px) {
    display: none;
  }

  li {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.875rem;
    color: var(--color-text-tertiary);
  }

  .check {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: color-mix(in oklch, var(--color-accent) 20%, transparent);
    color: var(--color-accent);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
}

// ===== 登录卡片 =====
.login-card {
  width: 420px;
  flex-shrink: 0;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-xl);
  padding: 40px 36px;
  box-shadow:
    var(--shadow-lg),
    inset 0 1px 0 color-mix(in oklch, var(--color-text-inverse) 5%, transparent);

  @media (max-width: 768px) {
    width: 100%;
    max-width: 420px;
    padding: 32px 24px;
  }

  @media (max-width: 480px) {
    padding: 28px 20px;
    border-radius: var(--radius-lg);
  }
}

.card-header {
  margin-bottom: 28px;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 4px;
  text-align: left;
}

.card-subtitle {
  font-size: 0.875rem;
  color: var(--color-text-tertiary);
  margin: 0;
  text-align: left;
}

// ===== 表单 =====
.login-form {
  :deep(.el-form-item) {
    margin-bottom: 14px;
    display: flex !important;
    align-items: center !important;
  }

  :deep(.el-form-item__label) {
    float: none !important;
    padding: 0 !important;
    margin: 0 !important;
    line-height: 1 !important;
    height: auto !important;
    width: 64px !important;
    flex-shrink: 0;
    text-align: right !important;
  }

  // 隐藏默认的必填星号（form-label-text 自定义了样式）
  :deep(.el-form-item.is-required > .el-form-item__label::before) {
    display: none !important;
  }

  :deep(.el-form-item__content) {
    margin-left: 6px !important;
    line-height: 0 !important;
    flex: 1;
  }

  .form-label-text {
    font-size: 0.8125rem;
    font-weight: 500;
    color: var(--color-text-secondary);
    display: inline-flex;
    align-items: center;
    gap: 2px;
    white-space: nowrap;
  }

  .required-star {
    color: var(--el-color-danger);
    font-size: 0.8125rem;
    line-height: 1;
  }

  :deep(.el-input__wrapper) {
    background: var(--color-bg-elevated);
    border: 1px solid var(--color-border-default);
    border-radius: var(--radius-md);
    padding: 0 14px;
    box-shadow: none;
    height: 48px;

    &:hover {
      border-color: var(--color-border-strong);
    }

    &:focus, &.is-focus {
      border-color: var(--color-accent);
      box-shadow: 0 0 0 3px var(--color-accent-soft);
      background: color-mix(in oklch, var(--color-bg-elevated) 60%, transparent);
    }
  }

  :deep(.el-input__inner) {
    color: var(--color-text-primary);
    height: 46px;
    font-size: 0.9375rem;

    &::placeholder {
      color: var(--color-text-disabled);
    }
  }

  :deep(.el-input__prefix) {
    color: var(--color-text-tertiary);
    margin-right: 10px;
  }

  :deep(.el-input__suffix) {
    color: var(--color-text-tertiary);
  }
}

// ===== 选项行 =====
.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 20px 0 24px;
  font-size: 0.8125rem;

  :deep(.el-checkbox__label) {
    color: var(--color-text-secondary);
  }

  :deep(.el-checkbox__inner) {
    background: var(--color-bg-elevated);
    border-color: var(--color-border-default);
  }
}

.forgot-link {
  color: var(--color-text-tertiary);
  text-decoration: none;
  transition: color var(--duration-fast, 150ms) var(--ease-standard);

  &:hover {
    color: var(--color-accent);
  }
}

// ===== 错误提示 =====
.login-error {
  margin-bottom: 20px;
  border-radius: var(--radius-md);
  background: color-mix(in oklch, var(--color-danger) 10%, transparent) !important;
  border: 1px solid color-mix(in oklch, var(--color-danger) 30%, transparent);
}

// ===== 登录按钮 =====
.login-btn {
  width: 100%;
  height: 48px;
  font-size: 0.9375rem;
  font-weight: 600;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-hover) 100%);
  border: none;
  box-shadow: 0 8px 24px var(--color-accent-glow);
  transition: transform var(--duration-fast, 150ms) var(--ease-standard),
              box-shadow var(--duration-fast, 150ms) var(--ease-standard);

  &:hover:not(.is-disabled) {
    transform: translateY(-1px);
    box-shadow: 0 12px 32px var(--color-accent-glow);
  }

  &:active:not(.is-disabled) {
    transform: translateY(0);
  }
}

// ===== 页脚 =====
.card-footer {
  margin-top: 24px;
  text-align: center;
  font-size: 0.8125rem;
  color: var(--color-text-tertiary);

  a {
    color: var(--color-accent);
    text-decoration: none;
    font-weight: 500;

    &:hover {
      color: var(--color-accent-hover);
    }
  }
}

// ===== 动效 =====
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.fade-in {
  animation: fadeIn 0.6s var(--ease-standard) both;
}

.fade-in-delay-1 { animation-delay: 0.1s; }
.fade-in-delay-2 { animation-delay: 0.2s; }
.fade-in-delay-3 { animation-delay: 0.3s; }

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
