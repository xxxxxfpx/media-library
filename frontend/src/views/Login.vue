<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bg-gradient"></div>
      <div class="bg-pattern"></div>
    </div>
    
    <div class="login-wrapper">
      <div class="brand-section">
        <div class="logo">
          <AppIcon name="clapperboard" :size="64" />
        </div>
        <h1 class="brand-title">Media Library</h1>
        <p class="brand-subtitle">沉浸式媒体管理体验</p>
      </div>
      
      <div class="login-card">
        <h2 class="login-title">欢迎回来</h2>
        <p class="login-subtitle">登录以继续探索</p>
        
        <el-form ref="formRef" :model="form" :rules="rules" class="login-form" @submit.prevent="handleLogin">
          <el-form-item prop="username">
            <el-input 
              v-model="form.username" 
              placeholder="用户名"
              size="large"
              class="imm-input"
            >
              <template #prefix>
                <AppIcon name="user" :size="16" />
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input 
              v-model="form.password" 
              type="password" 
              placeholder="密码"
              size="large"
              class="imm-input"
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

        <div class="login-footer">
          <p>默认账号: <span class="highlight">admin</span> / <span class="highlight">admin123</span></p>
        </div>
      </div>
    </div>
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
  password: ''
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

// 背景装饰
.bg-decoration {
  position: fixed;
  inset: 0;
  pointer-events: none;
  
  .bg-gradient {
    position: absolute;
    inset: 0;
    background: 
      radial-gradient(ellipse 80% 50% at 50% -20%, color-mix(in oklch, var(--color-accent) 30%, transparent), transparent),
      radial-gradient(ellipse 60% 40% at 80% 100%, color-mix(in oklch, var(--color-accent) 15%, transparent), transparent);
  }
  
  .bg-pattern {
    position: absolute;
    inset: 0;
    background-image: 
      radial-gradient(circle at 25% 25%, color-mix(in oklch, var(--color-accent) 10%, transparent) 0%, transparent 50%),
      radial-gradient(circle at 75% 75%, color-mix(in oklch, var(--color-accent) 5%, transparent) 0%, transparent 50%);
    opacity: 0.5;
  }
}

.login-wrapper {
  display: flex;
  align-items: center;
  gap: 80px;
  max-width: 1000px;
  width: 100%;
  z-index: 1;
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 40px;
  }
}

// 品牌区域
.brand-section {
  flex: 1;
  text-align: center;
  
  .logo {
    width: 120px;
    height: 120px;
    margin: 0 auto 24px;
    background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-hover) 100%);
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-text-inverse);
    box-shadow: 
      0 20px 40px var(--color-accent-glow),
      0 0 80px color-mix(in oklch, var(--color-accent) 20%, transparent);
    animation: float 6s ease-in-out infinite;
  }
  
  .brand-title {
    font-size: 3rem;
    font-weight: 700;
    margin: 0 0 12px;
    background: linear-gradient(135deg, var(--color-text-inverse) 0%, color-mix(in oklch, var(--color-text-inverse) 70%, transparent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
  }
  
  .brand-subtitle {
    font-size: 1.125rem;
    color: var(--color-text-tertiary);
    margin: 0;
    font-weight: 400;
  }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

// 登录卡片
.login-card {
  width: 100%;
  max-width: 400px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  border: 1px solid var(--color-border-subtle);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 
    var(--shadow-lg),
    inset 0 1px 0 color-mix(in oklch, var(--color-text-inverse) 5%, transparent);
  
  @media (max-width: 768px) {
    padding: 32px 24px;
  }
}

.login-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--color-text-inverse);
  margin: 0 0 8px;
  text-align: center;
}

.login-subtitle {
  font-size: 0.875rem;
  color: var(--color-text-tertiary);
  margin: 0 0 32px;
  text-align: center;
}

.login-form {
  .el-form-item {
    margin-bottom: 20px;
  }
  
  :deep(.el-input__wrapper) {
    background: var(--color-bg-elevated) !important;
    border: 1px solid var(--color-border-subtle);
    border-radius: 12px;
    padding: 4px 16px;
    box-shadow: none;
    
    &:hover, &:focus, &.is-focus {
      border-color: var(--color-accent);
      box-shadow: 0 0 0 3px var(--color-accent-soft);
    }
  }
  
  :deep(.el-input__inner) {
    color: var(--color-text-inverse);
    height: 44px;
    
    &::placeholder {
      color: var(--color-text-disabled);
    }
  }
  
  :deep(.el-input__prefix) {
    color: var(--color-text-tertiary);
    margin-right: 12px;
  }
  
  :deep(.el-input__suffix) {
    color: var(--color-text-tertiary);
  }
}

.login-error {
  margin-bottom: 20px;
  border-radius: 8px;
  background: color-mix(in oklch, var(--color-danger) 10%, transparent) !important;
  border: 1px solid color-mix(in oklch, var(--color-danger) 30%, transparent);
}

.login-btn {
  width: 100%;
  height: 52px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-hover) 100%);
  border: none;
  box-shadow: 0 8px 20px var(--color-accent-glow);
  transition: all var(--duration-base) var(--ease-standard);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px var(--color-accent-glow);
  }
  
  &:active {
    transform: translateY(0);
  }
}

.login-footer {
  margin-top: 24px;
  text-align: center;
  
  p {
    color: var(--color-text-disabled);
    font-size: 0.8125rem;
    margin: 0;
  }
  
  .highlight {
    color: var(--color-accent);
    font-weight: 500;
  }
}
</style>