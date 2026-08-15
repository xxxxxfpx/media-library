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
          <el-icon :size="64"><VideoCamera /></el-icon>
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
                <el-icon><User /></el-icon>
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
                <el-icon><Lock /></el-icon>
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
import { User, Lock, VideoCamera } from '@element-plus/icons-vue'

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
  background: #000000;
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
      radial-gradient(ellipse 80% 50% at 50% -20%, rgba(33, 150, 243, 0.3), transparent),
      radial-gradient(ellipse 60% 40% at 80% 100%, rgba(33, 150, 243, 0.15), transparent);
  }
  
  .bg-pattern {
    position: absolute;
    inset: 0;
    background-image: 
      radial-gradient(circle at 25% 25%, rgba(33, 150, 243, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 75% 75%, rgba(33, 150, 243, 0.05) 0%, transparent 50%);
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
    background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    box-shadow: 
      0 20px 40px rgba(33, 150, 243, 0.4),
      0 0 80px rgba(33, 150, 243, 0.2);
    animation: float 6s ease-in-out infinite;
  }
  
  .brand-title {
    font-size: 3rem;
    font-weight: 700;
    margin: 0 0 12px;
    background: linear-gradient(135deg, #fff 0%, rgba(255, 255, 255, 0.7) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
  }
  
  .brand-subtitle {
    font-size: 1.125rem;
    color: rgba(255, 255, 255, 0.5);
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
  background: rgba(26, 26, 26, 0.8);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 
    0 24px 48px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  
  @media (max-width: 768px) {
    padding: 32px 24px;
  }
}

.login-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #fff;
  margin: 0 0 8px;
  text-align: center;
}

.login-subtitle {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
  margin: 0 0 32px;
  text-align: center;
}

.login-form {
  .el-form-item {
    margin-bottom: 20px;
  }
  
  :deep(.el-input__wrapper) {
    background: rgba(0, 0, 0, 0.5) !important;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 4px 16px;
    box-shadow: none;
    
    &:hover, &:focus, &.is-focus {
      border-color: #2196F3;
      box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.2);
    }
  }
  
  :deep(.el-input__inner) {
    color: #fff;
    height: 44px;
    
    &::placeholder {
      color: rgba(255, 255, 255, 0.4);
    }
  }
  
  :deep(.el-input__prefix) {
    color: rgba(255, 255, 255, 0.5);
    margin-right: 12px;
  }
  
  :deep(.el-input__suffix) {
    color: rgba(255, 255, 255, 0.5);
  }
}

.login-error {
  margin-bottom: 20px;
  border-radius: 8px;
  background: rgba(244, 67, 54, 0.1) !important;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.login-btn {
  width: 100%;
  height: 52px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
  border: none;
  box-shadow: 0 8px 20px rgba(33, 150, 243, 0.4);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(33, 150, 243, 0.5);
  }
  
  &:active {
    transform: translateY(0);
  }
}

.login-footer {
  margin-top: 24px;
  text-align: center;
  
  p {
    color: rgba(255, 255, 255, 0.4);
    font-size: 0.8125rem;
    margin: 0;
  }
  
  .highlight {
    color: #2196F3;
    font-weight: 500;
  }
}
</style>