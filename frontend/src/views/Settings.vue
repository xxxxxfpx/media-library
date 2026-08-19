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
          <span>主题配色</span>
          <span class="setting-desc">共 6 套主题，现代黑 / 现代白为默认两套；选中即生效并自动保存</span>
        </div>
      </div>
      <div class="theme-grid">
        <div
          v-for="t in store.themes"
          :key="t.id"
          class="theme-card"
          :class="{ active: t.id === store.theme }"
          role="button"
          :aria-label="`选择主题 ${t.name}`"
          @click="store.setTheme(t.id)"
        >
          <div class="swatches">
            <span class="sw" :style="{ background: t.swatch.page }" />
            <span class="sw" :style="{ background: t.swatch.surface }" />
            <span class="sw" :style="{ background: t.swatch.accent }" />
          </div>
          <div class="meta">
            <span class="name">{{ t.name }}</span>
            <AppIcon v-if="t.id === store.theme" name="check" :size="14" class="tick" />
          </div>
        </div>
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

    <el-card v-if="store.isAdmin" class="mb-4">
      <template #header>
        <div class="card-header-row">
          <span>光芽云盘</span>
          <el-tag :type="guangYaPanConfig.configured ? 'success' : 'info'" size="small">
            {{ guangYaPanConfig.configured ? '已配置' : '未配置' }}
          </el-tag>
        </div>
      </template>
      <el-form label-position="top" class="drive-form" @submit.prevent>
        <el-form-item label="Access Token">
          <el-input
            v-model="guangYaPanForm.access_token"
            type="password"
            show-password
            placeholder="留空表示保持当前 Token"
            autocomplete="new-password"
          />
        </el-form-item>
        <el-form-item label="Refresh Token">
          <el-input
            v-model="guangYaPanForm.refresh_token"
            type="password"
            show-password
            placeholder="留空表示保持当前 Refresh Token"
            autocomplete="new-password"
          />
        </el-form-item>
        <div class="form-grid">
          <el-form-item label="Client ID">
            <el-input v-model="guangYaPanForm.client_id" placeholder="可选" />
          </el-form-item>
          <el-form-item label="Device ID">
            <el-input v-model="guangYaPanForm.device_id" placeholder="可选" />
          </el-form-item>
        </div>
        <el-form-item label="默认网盘目录 ID">
          <el-input
            v-model="guangYaPanForm.default_parent_id"
            placeholder="上传和离线下载共用此目录 ID"
          />
          <div class="setting-desc">上传和离线下载统一使用此目录；文件名由源 URL 的 SHA-256 自动生成。</div>
        </el-form-item>
        <div class="drive-actions">
          <span v-if="guangYaPanConfig.updated_at" class="setting-desc">
            最近更新：{{ formatDate(guangYaPanConfig.updated_at) }}
          </span>
          <el-button type="primary" :loading="guangYaPanSaving" @click="saveGuangYaPanConfig">
            保存云盘设置
          </el-button>
        </div>
      </el-form>
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
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useAppStore } from '@/store'
import { guangYaPanAPI, userAPI } from '@/api'
import { ElMessage } from 'element-plus'
import AppIcon from '@/components/ui/AppIcon.vue'

const store = useAppStore()

const showPasswordDialog = ref(false)
const passwordLoading = ref(false)
const passwordForm = ref({ oldPassword: '', newPassword: '', confirmPassword: '' })
const autoplay = ref(false)
const defaultMuted = ref(false)
const syncInterval = ref(8000)
const guangYaPanSaving = ref(false)
const guangYaPanConfig = ref({ configured: false, updated_at: null })
const guangYaPanForm = ref({
  access_token: '',
  refresh_token: '',
  client_id: '',
  device_id: '',
  default_parent_id: ''
})

onMounted(async () => {
  try {
    const settings = await userAPI.getSetting()
    autoplay.value = localStorage.getItem('video_autoplay') === 'true'
    defaultMuted.value = localStorage.getItem('video_default_muted') === 'true'
    if (settings.auto_sync_interval) syncInterval.value = settings.auto_sync_interval * 1000
    if (store.isAdmin) {
      const config = await guangYaPanAPI.getConfig()
      guangYaPanConfig.value = config
      guangYaPanForm.value.client_id = config.client_id || ''
      guangYaPanForm.value.device_id = config.device_id || ''
      guangYaPanForm.value.default_parent_id = config.default_parent_id || ''
    }
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

async function saveGuangYaPanConfig() {
  guangYaPanSaving.value = true
  try {
    const payload = { ...guangYaPanForm.value }
    if (!payload.access_token) delete payload.access_token
    if (!payload.refresh_token) delete payload.refresh_token
    const config = await guangYaPanAPI.updateConfig(payload)
    guangYaPanConfig.value = config
    guangYaPanForm.value.access_token = ''
    guangYaPanForm.value.refresh_token = ''
    ElMessage.success('光芽云盘设置已保存')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '光芽云盘设置保存失败')
  } finally {
    guangYaPanSaving.value = false
  }
}

function formatDate(value) {
  return value ? new Date(value).toLocaleString() : ''
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
  overflow-wrap: break-word;
  line-height: 1.5;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
}

.card-header-row,
.drive-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.drive-form {
  max-width: 640px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
    gap: 0;
  }
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

/* ===== 主题选择器（6 套色板，与 ThemeSwitcher 一致） ===== */
.theme-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.theme-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-subtle);
  cursor: pointer;
  transition:
    border-color var(--duration-fast) var(--ease-standard),
    background var(--duration-fast) var(--ease-standard),
    transform var(--duration-fast) var(--ease-standard);

  &:hover {
    border-color: var(--color-accent);
    transform: translateY(-2px);
  }

  &.active {
    border-color: var(--color-accent);
    background: var(--color-selected);
  }

  .swatches {
    display: flex;
    gap: 4px;
  }

  .sw {
    flex: 1;
    height: 24px;
    border-radius: 4px;
    border: 1px solid var(--color-border-subtle);
  }

  .meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .name {
    font-size: 0.8125rem;
    color: var(--color-text-primary);
    font-weight: 500;
  }

  .tick {
    color: var(--color-accent);
  }
}

@media (max-width: 480px) {
  .theme-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
