<template>
  <div class="settings-container">
    <el-page-header content="设置" class="mb-4" @back="$router.push('/')" />
    
    <el-card class="mb-4">
      <template #header>
        <span>个人信息</span>
      </template>
      <div class="detail-list">
        <div class="detail-row">
          <span class="detail-label">用户名</span>
          <span class="detail-value">{{ store.userInfo?.username }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">邮箱</span>
          <span class="detail-value">{{ store.userInfo?.email || '未设置' }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">账户类型</span>
          <span class="detail-value">
            <el-tag :type="store.isAdmin ? 'danger' : 'info'">
              {{ store.isAdmin ? '管理员' : '普通用户' }}
            </el-tag>
          </span>
        </div>
      </div>
    </el-card>

    <el-card class="mb-4">
      <template #header>
        <span>外观设置</span>
      </template>
      <div class="setting-item">
        <div class="setting-label">
          <span>深色模式</span>
          <span class="setting-desc">开启后使用深色主题</span>
        </div>
        <el-switch v-model="isDark" />
      </div>
    </el-card>

    <el-card class="mb-4">
      <template #header>
        <span>播放设置</span>
      </template>
      <div class="setting-item">
        <div class="setting-label">
          <span>自动播放</span>
          <span class="setting-desc">进入播放页面时自动开始播放（浏览器限制：必须同时开启静音）</span>
        </div>
        <el-switch v-model="autoplay" />
      </div>
      <div class="setting-item">
        <div class="setting-label">
          <span>默认静音</span>
          <span class="setting-desc">播放开始时是否静音（自动播放时强制开启）</span>
        </div>
        <el-switch v-model="defaultMuted" :disabled="autoplay" />
      </div>
      <div class="setting-item">
        <div class="setting-label">
          <span>播放进度同步频率</span>
          <span class="setting-desc">定时保存播放进度的时间间隔（秒）</span>
        </div>
        <el-select v-model="syncInterval" placeholder="请选择" style="width: 150px">
          <el-option label="1 秒" :value="1000" />
          <el-option label="2 秒" :value="2000" />
          <el-option label="4 秒" :value="4000" />
          <el-option label="8 秒" :value="8000" />
          <el-option label="16 秒" :value="16000" />
          <el-option label="32 秒" :value="32000" />
        </el-select>
      </div>
    </el-card>

    <el-card class="mb-4">
      <template #header>
        <span>安全设置</span>
      </template>
      <div class="setting-item">
        <div class="setting-label">
          <span>修改密码</span>
          <span class="setting-desc">更新您的账户密码</span>
        </div>
        <el-button type="primary" plain @click="openPasswordDialog">修改密码</el-button>
      </div>
    </el-card>

    <el-dialog v-model="showPasswordDialog" title="修改密码" width="420px" destroy-on-close>
      <el-form label-width="90px" @submit.prevent>
        <el-form-item label="旧密码">
          <el-input v-model="passwordForm.oldPassword" type="password" show-password placeholder="请输入旧密码" />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="passwordForm.newPassword" type="password" show-password placeholder="至少 6 位" />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password placeholder="再次输入新密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" :loading="passwordLoading" @click="submitPasswordChange">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useAppStore } from '@/store'
import { userAPI } from '@/api'
import { ElMessage } from 'element-plus'

const store = useAppStore()

const isDark = computed({
  get: () => store.theme === 'dark',
  set: (val) => store.setTheme(val ? 'dark' : 'light')
})

const showPasswordDialog = ref(false)
const passwordLoading = ref(false)
const passwordForm = ref({ oldPassword: '', newPassword: '', confirmPassword: '' })
const autoplay = ref(false)
const defaultMuted = ref(false)
const syncInterval = ref(8000)

onMounted(async () => {
  try {
    const settings = await userAPI.getSetting()
    autoplay.value = localStorage.getItem('video_autoplay') === 'true'
    defaultMuted.value = localStorage.getItem('video_default_muted') === 'true'
    if (settings.auto_sync_interval) syncInterval.value = settings.auto_sync_interval * 1000
  } catch {
    // 获取设置失败时使用默认值，静默忽略
  }
})

async function saveSettings() {
  try {
    // 如果开启自动播放，强制开启默认静音
    const finalDefaultMuted = autoplay.value ? true : defaultMuted.value

    localStorage.setItem('video_autoplay', String(autoplay.value))
    localStorage.setItem('video_default_muted', String(finalDefaultMuted))
    await userAPI.updateSetting({ auto_sync_interval: Math.round(syncInterval.value / 1000) })
  } catch {
    ElMessage.error('保存失败')
  }
}

// 防抖：300ms 内多次变更只保存一次
let saveTimer = null
watch([autoplay, defaultMuted, syncInterval], () => {
  if (saveTimer) clearTimeout(saveTimer)
  saveTimer = setTimeout(saveSettings, 300)
})

onUnmounted(() => {
  if (saveTimer) clearTimeout(saveTimer)
})

function openPasswordDialog() {
  passwordForm.value = { oldPassword: '', newPassword: '', confirmPassword: '' }
  showPasswordDialog.value = true
}

async function submitPasswordChange() {
  const { oldPassword, newPassword, confirmPassword } = passwordForm.value
  if (!oldPassword || !newPassword) {
    ElMessage.warning('请填写旧密码和新密码')
    return
  }
  if (newPassword.length < 6) {
    ElMessage.warning('新密码长度至少 6 位')
    return
  }
  if (newPassword !== confirmPassword) {
    ElMessage.warning('两次输入的新密码不一致')
    return
  }

  passwordLoading.value = true
  try {
    await userAPI.changePassword({ old_password: oldPassword, new_password: newPassword })
    ElMessage.success('密码修改成功，请重新登录')
    showPasswordDialog.value = false
    setTimeout(() => store.logout(), 800)
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '密码修改失败')
  } finally {
    passwordLoading.value = false
  }
}
</script>

<style scoped lang="scss">
.settings-container {
  padding: 20px;
  max-width: 800px;
}

.mb-4 {
  margin-bottom: 16px;
}

.detail-list {
  display: flex;
  flex-direction: column;
}

.detail-row {
  display: flex;
  align-items: center;
  padding: 14px 20px;
  border-bottom: 1px solid var(--imm-divider);
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  min-width: 130px;
  font-size: 13px;
  color: var(--imm-text-tertiary);
  flex-shrink: 0;
}

.detail-value {
  flex: 1;
  font-size: 14px;
  color: var(--imm-text-primary);
  font-weight: 500;
  word-break: break-word;
  line-height: 1.5;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
}

.setting-label {
  display: flex;
  flex-direction: column;
  
  span:first-child {
    font-weight: 500;
  }
  
  .setting-desc {
    font-size: 12px;
    color: var(--imm-text-tertiary);
    margin-top: 4px;
  }
}
</style>
