<template>
  <div class="settings-container">
    <button class="back-link" @click="$router.push('/')">
      <AppIcon name="arrow-left" :size="16" /> 返回
    </button>

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
          <span>光鸭云盘</span>
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

        <!-- 测试连接按钮与结果 -->
        <el-form-item label="目录连通性">
          <div class="test-connection-row">
            <el-button
              :loading="guangYaPanTesting"
              :disabled="guangYaPanSaving"
              @click="testGuangYaPanConfig"
            >
              {{ guangYaPanTesting ? '测试中...' : '测试连接' }}
            </el-button>
            <div v-if="guangYaPanTestResult" class="test-result test-success">
              <span class="test-icon">✓</span>
              <span>目录可访问 · 共 {{ guangYaPanTestResult.total }} 项</span>
              <span v-if="guangYaPanTestResult.sample?.length" class="test-samples">
                示例：{{ guangYaPanTestResult.sample.map(s => s.name).join('、') }}
              </span>
            </div>
            <div v-else-if="guangYaPanTestError" class="test-result test-error">
              <span class="test-icon">✗</span>
              <span>{{ guangYaPanTestError }}</span>
            </div>
            <div v-else class="test-result test-pending">
              <span>点击「测试连接」验证目录 ID 是否有效</span>
            </div>
          </div>
        </el-form-item>

        <div class="drive-actions">
          <span v-if="guangYaPanConfig.updated_at" class="setting-desc">
            最近更新：{{ formatDate(guangYaPanConfig.updated_at) }}
          </span>
          <el-button type="primary" :loading="guangYaPanSaving" :disabled="guangYaPanTesting" @click="saveGuangYaPanConfig">
            保存云盘设置
          </el-button>
        </div>
      </el-form>
    </el-card>

    <!-- 采集源管理（仅管理员可见） -->
    <el-card v-if="store.isAdmin" class="collection-card mb-4">
      <template #header>
        <div class="card-header-row">
          <div class="card-header-title">
            <span class="card-title-icon">📡</span>
            <span>采集源管理</span>
          </div>
          <el-button type="primary" size="small" @click="openSourceDialog()">+ 添加采集源</el-button>
        </div>
      </template>

      <el-table :data="collectionSources" v-loading="sourcesLoading" stripe size="small" class="source-table">
        <el-table-column prop="name" label="名称" width="100" />
        <el-table-column prop="base_url" label="API地址" show-overflow-tooltip min-width="200" />
        <el-table-column label="开关" width="120" align="center">
          <template #default="{ row }">
            <div class="switch-group">
              <el-tooltip content="启用采集源" placement="top">
                <el-switch v-model="row.enabled" size="small" @change="(val) => toggleSource(row.id, { enabled: val })" />
              </el-tooltip>
              <el-tooltip content="自动采集" placement="top">
                <el-switch v-model="row.auto_collect" size="small" @change="(val) => toggleSource(row.id, { auto_collect: val })" />
              </el-tooltip>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-tag
              v-if="row.last_status"
              :type="row.last_status === 'success' ? 'success' : row.last_status === 'failed' ? 'danger' : 'warning'"
              size="small"
              effect="dark"
              round
            >
              {{ row.last_status === 'success' ? '成功' : row.last_status === 'failed' ? '失败' : '运行中' }}
            </el-tag>
            <span v-else class="col-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="上次采集" width="120">
          <template #default="{ row }">
            <span v-if="row.last_collected_at" class="col-muted">{{ formatDate(row.last_collected_at) }}</span>
            <span v-else class="col-muted">未采集</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300" align="center">
          <template #default="{ row }">
            <div class="action-group">
              <el-button size="small" @click="testSource(row.id)" :loading="row._testing" text>测试</el-button>
              <el-button size="small" type="primary" @click="triggerCollect(row.id)" :loading="row._triggering">采集</el-button>
              <el-button size="small" @click="openSourceDialog(row)" text>编辑</el-button>
              <el-button size="small" type="danger" @click="deleteSource(row.id)">删除</el-button>
              <el-tag size="small" type="info" effect="plain" class="interval-tag">{{ row.interval_minutes }}分</el-tag>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分隔线 -->
      <div v-if="collectionLogs.length" class="logs-divider">
        <span>采集日志</span>
      </div>

      <!-- 采集日志 -->
      <el-table v-if="collectionLogs.length" :data="collectionLogs" size="small" stripe class="logs-table">
        <el-table-column label="触发" width="60" align="center">
          <template #default="{ row }">
            <el-tag size="small" :type="row.trigger_type === 'manual' ? 'warning' : 'info'" effect="plain" round>
              {{ row.trigger_type === 'manual' ? '手动' : '自动' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="60" align="center">
          <template #default="{ row }">
            <el-tag size="small" :type="row.status === 'success' ? 'success' : row.status === 'failed' ? 'danger' : 'warning'" effect="plain" round>
              {{ row.status === 'success' ? '成功' : row.status === 'failed' ? '失败' : '运行中' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="新增" width="50" align="center">
          <template #default="{ row }">
            <span class="log-count log-new">{{ row.new_count }}</span>
          </template>
        </el-table-column>
        <el-table-column label="更新" width="50" align="center">
          <template #default="{ row }">
            <span class="log-count log-update">{{ row.update_count }}</span>
          </template>
        </el-table-column>
        <el-table-column label="错误" width="50" align="center">
          <template #default="{ row }">
            <span :class="['log-count', row.error_count > 0 ? 'log-error' : '']">{{ row.error_count }}</span>
          </template>
        </el-table-column>
        <el-table-column label="拉取" width="55" align="center">
          <template #default="{ row }">{{ row.total_fetched }}</template>
        </el-table-column>
        <el-table-column label="耗时" width="60" align="center">
          <template #default="{ row }">
            <span v-if="row.started_at && row.finished_at" class="col-muted">
              {{ Math.round((new Date(row.finished_at) - new Date(row.started_at)) / 1000) }}s
            </span>
            <span v-else class="col-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="时间" min-width="130">
          <template #default="{ row }">
            <span class="col-muted">{{ formatDate(row.started_at) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="error_message" label="备注" show-overflow-tooltip min-width="100">
          <template #default="{ row }">
            <span v-if="row.error_message" class="error-text">{{ row.error_message }}</span>
            <span v-else class="col-muted">-</span>
          </template>
        </el-table-column>
      </el-table>
      <div v-else class="empty-hint">暂无采集日志</div>
    </el-card>

    <!-- 采集源添加/编辑对话框 -->
    <el-dialog v-model="showSourceDialog" :title="editingSource?.id ? '编辑采集源' : '添加采集源'" width="480px" destroy-on-close>
      <el-form label-position="top" @submit.prevent>
        <el-form-item label="采集源名称">
          <el-input v-model="sourceForm.name" placeholder="如：155资源" />
        </el-form-item>
        <el-form-item label="API基础URL">
          <el-input v-model="sourceForm.base_url" placeholder="https://155api.com/api.php/provide/vod/" />
        </el-form-item>
        <div class="form-grid">
          <el-form-item label="启用">
            <el-switch v-model="sourceForm.enabled" />
          </el-form-item>
          <el-form-item label="自动采集">
            <el-switch v-model="sourceForm.auto_collect" />
          </el-form-item>
        </div>
        <el-form-item label="轮询间隔（分钟）">
          <el-select v-model="sourceForm.interval_minutes" style="width: 100%">
            <el-option label="15 分钟" :value="15" />
            <el-option label="30 分钟" :value="30" />
            <el-option label="1 小时" :value="60" />
            <el-option label="2 小时" :value="120" />
            <el-option label="6 小时" :value="360" />
            <el-option label="12 小时" :value="720" />
            <el-option label="24 小时" :value="1440" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSourceDialog = false">取消</el-button>
        <el-button type="primary" :loading="sourceSaving" @click="saveSource">保存</el-button>
      </template>
    </el-dialog>

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
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useAppStore } from '@/store'
import { guangYaPanAPI, userAPI, collectionAPI } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import AppIcon from '@/components/ui/AppIcon.vue'

const store = useAppStore()

const showPasswordDialog = ref(false)
const passwordLoading = ref(false)
const passwordForm = ref({ oldPassword: '', newPassword: '', confirmPassword: '' })
const autoplay = ref(false)
const defaultMuted = ref(false)
const syncInterval = ref(8000)
const guangYaPanSaving = ref(false)
const guangYaPanTesting = ref(false)
const guangYaPanTestResult = ref(null) // { ok, parent_id, total, sample }
const guangYaPanTestError = ref('')
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
  } catch {
    // 获取设置失败时使用默认值，静默忽略
  }

  if (store.isAdmin) {
    // 加载光鸭配置
    try {
      const config = await guangYaPanAPI.getConfig()
      guangYaPanConfig.value = config
      guangYaPanForm.value.client_id = config.client_id || ''
      guangYaPanForm.value.device_id = config.device_id || ''
      guangYaPanForm.value.default_parent_id = config.default_parent_id || ''
    } catch {
      // 光鸭配置加载失败不影响其他功能
    }
    // 加载采集源
    await loadSources()
    await loadLogs()
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

async function testGuangYaPanConfig() {
  guangYaPanTesting.value = true
  guangYaPanTestResult.value = null
  guangYaPanTestError.value = ''
  try {
    const payload = { ...guangYaPanForm.value }
    const result = await guangYaPanAPI.testConfig(payload)
    guangYaPanTestResult.value = result
  } catch (error) {
    guangYaPanTestError.value = error.response?.data?.detail || '测试失败'
  } finally {
    guangYaPanTesting.value = false
  }
}

async function saveGuangYaPanConfig() {
  guangYaPanSaving.value = true
  try {
    // 保存前先测试：确保凭据和目录可用
    const payload = { ...guangYaPanForm.value }
    try {
      const testResult = await guangYaPanAPI.testConfig(payload)
      if (!testResult.ok) {
        guangYaPanTestError.value = '测试未通过，请检查配置'
        ElMessage.error('保存前测试未通过，无法保存')
        return
      }
      guangYaPanTestResult.value = testResult
    } catch (testError) {
      guangYaPanTestError.value = testError.response?.data?.detail || '连接测试失败'
      ElMessage.error('保存前连接测试失败，请检查 Token 和目录 ID')
      return
    }

    if (!payload.access_token) delete payload.access_token
    if (!payload.refresh_token) delete payload.refresh_token
    const config = await guangYaPanAPI.updateConfig(payload)
    guangYaPanConfig.value = config
    guangYaPanForm.value.access_token = ''
    guangYaPanForm.value.refresh_token = ''
    guangYaPanTestError.value = ''
    ElMessage.success('光鸭云盘设置已保存')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '光鸭云盘设置保存失败')
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

// ── 采集源管理 ──
const collectionSources = ref([])
const collectionLogs = ref([])
const sourcesLoading = ref(false)
const showSourceDialog = ref(false)
const editingSource = ref(null)
const sourceSaving = ref(false)
const sourceForm = ref({
  name: '',
  base_url: '',
  enabled: true,
  auto_collect: false,
  interval_minutes: 60,
})

async function loadSources() {
  if (!store.isAdmin) return
  sourcesLoading.value = true
  try {
    collectionSources.value = await collectionAPI.listSources()
  } catch (e) {
    ElMessage.error('加载采集源失败')
  } finally {
    sourcesLoading.value = false
  }
}

async function loadLogs() {
  if (!store.isAdmin) return
  try {
    collectionLogs.value = await collectionAPI.listLogs(null, 10)
  } catch {
    // 静默忽略
  }
}

function openSourceDialog(source = null) {
  if (source) {
    editingSource.value = source
    sourceForm.value = {
      name: source.name,
      base_url: source.base_url,
      enabled: source.enabled,
      auto_collect: source.auto_collect,
      interval_minutes: source.interval_minutes,
    }
  } else {
    editingSource.value = null
    sourceForm.value = {
      name: '',
      base_url: '',
      enabled: true,
      auto_collect: false,
      interval_minutes: 60,
    }
  }
  showSourceDialog.value = true
}

async function saveSource() {
  if (!sourceForm.value.name || !sourceForm.value.base_url) {
    ElMessage.warning('请填写名称和API地址')
    return
  }
  sourceSaving.value = true
  try {
    if (editingSource.value) {
      await collectionAPI.updateSource(editingSource.value.id, sourceForm.value)
      ElMessage.success('更新成功')
    } else {
      await collectionAPI.createSource(sourceForm.value)
      ElMessage.success('添加成功')
    }
    showSourceDialog.value = false
    await loadSources()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  } finally {
    sourceSaving.value = false
  }
}

async function deleteSource(id) {
  try {
    await ElMessageBox.confirm('确定删除此采集源？相关日志也会一并删除。', '确认删除', { type: 'warning' })
    await collectionAPI.deleteSource(id)
    ElMessage.success('删除成功')
    await loadSources()
  } catch {
    // 取消或失败
  }
}

async function testSource(id) {
  const src = collectionSources.value.find(s => s.id === id)
  if (src) src._testing = true
  try {
    const result = await collectionAPI.testSource(id)
    ElMessage.success(`连接成功！共 ${result.total} 条数据`)
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '测试失败')
  } finally {
    if (src) src._testing = false
  }
}

async function triggerCollect(id) {
  const src = collectionSources.value.find(s => s.id === id)
  if (src) src._triggering = true
  try {
    await collectionAPI.triggerCollect(id)
    ElMessage.success('采集已触发，请稍候查看日志')
    setTimeout(async () => {
      await loadSources()
      await loadLogs()
    }, 3000)
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '触发失败')
  } finally {
    if (src) src._triggering = false
  }
}

async function toggleSource(id, data) {
  try {
    await collectionAPI.toggleSource(id, data)
    ElMessage.success('已更新')
    await loadSources()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  }
}
</script>

<style scoped lang="scss">
.settings-container {
  padding: 20px;
  max-width: 800px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 16px;
  padding: 6px 12px;
  border: 1px solid var(--imm-divider);
  border-radius: 8px;
  background: transparent;
  color: var(--imm-text-secondary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: var(--imm-hover);
    color: var(--imm-text-primary);
    border-color: var(--imm-border);
  }
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

.test-connection-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex-wrap: wrap;
}

.test-result {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 13px;
  line-height: 1.4;
  flex: 1;
  min-width: 200px;
}

.test-icon {
  font-weight: bold;
}

.test-success {
  background: var(--el-color-success-light-9, #f0f9eb);
  color: var(--el-color-success, #67c23a);
  border: 1px solid var(--el-color-success-light-7, #e1f3d8);
}

.test-error {
  background: var(--el-color-danger-light-9, #fef0f0);
  color: var(--el-color-danger, #f56c6c);
  border: 1px solid var(--el-color-danger-light-7, #fde2e2);
}

.test-pending {
  background: var(--el-color-info-light-9, #f4f4f5);
  color: var(--el-color-info, #909399);
  border: 1px dashed var(--el-color-info-light-5, #d3d4d6);
}

.test-samples {
  color: inherit;
  opacity: 0.8;
  margin-left: 6px;
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

// ── 采集源管理卡片 ──
.collection-card {
  .card-header-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    font-size: 15px;
  }

  .card-title-icon {
    font-size: 18px;
  }

  .col-muted {
    color: var(--color-text-tertiary);
    font-size: 12px;
  }

  // 开关组
  .switch-group {
    display: flex;
    align-items: center;
    gap: 6px;
    justify-content: center;
  }

  // 操作按钮组 - 禁止换行，横向展开
  .action-group {
    display: flex;
    align-items: center;
    gap: 2px;
    flex-wrap: nowrap;
    justify-content: center;
    white-space: nowrap;
  }

  .interval-tag {
    margin-left: 4px;
    font-size: 11px;
  }

  // 日志分隔线
  .logs-divider {
    display: flex;
    align-items: center;
    margin: 12px 0 8px;
    gap: 12px;

    &::before, &::after {
      content: '';
      flex: 1;
      height: 1px;
      background: var(--color-border-subtle);
    }

    span {
      font-size: 12px;
      color: var(--color-text-tertiary);
      font-weight: 500;
      white-space: nowrap;
    }
  }

  // 日志表格
  .logs-table {
    :deep(.el-table__cell) {
      padding: 6px 0;
    }
  }

  .log-count {
    font-weight: 600;
    font-size: 13px;

    &.log-new {
      color: var(--color-accent);
    }

    &.log-update {
      color: var(--color-warning, #e6a23c);
    }

    &.log-error {
      color: var(--color-danger, #f56c6c);
    }
  }

  .error-text {
    color: var(--color-danger, #f56c6c);
    font-size: 12px;
  }

  .empty-hint {
    text-align: center;
    padding: 16px;
    color: var(--color-text-tertiary);
    font-size: 13px;
  }

  // 源表格紧凑化，允许横向滚动
  .source-table {
    :deep(.el-table__cell) {
      padding: 8px 0;
    }

    :deep(.el-table__body-wrapper) {
      overflow-x: auto;
    }

    // 隐藏表头的横向滚动条，只保留底部一条
    :deep(.el-table__header-wrapper) {
      overflow-x: hidden;
    }

    :deep(.el-table__header-wrapper .el-scrollbar__bar.is-horizontal) {
      display: none;
    }
  }
}
</style>
