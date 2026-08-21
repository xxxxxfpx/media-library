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
              <AppIcon name="check" class="test-icon" :size="16" />
              <span>目录可访问 · 共 {{ guangYaPanTestResult.total }} 项</span>
              <span v-if="guangYaPanTestResult.sample?.length" class="test-samples">
                示例：{{ guangYaPanTestResult.sample.map(s => s.name).join('、') }}
              </span>
            </div>
            <div v-else-if="guangYaPanTestError" class="test-result test-error">
              <AppIcon name="x" class="test-icon" :size="16" />
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

      <!-- 采集源卡片列表 -->
      <div v-loading="sourcesLoading" class="source-list">
        <div
          v-for="source in collectionSources"
          :key="source.id"
          class="source-item"
          :class="{ expanded: expandedIds.has(source.id) }"
        >
          <!-- 卡片头部 -->
          <div class="source-header" @click="toggleExpand(source.id)">
            <div class="expand-icon">
              <AppIcon v-if="expandedIds.has(source.id)" name="chevron-down" :size="16" />
              <AppIcon v-else name="chevrons-up-down" :size="16" />
            </div>
            <div class="source-info">
              <div class="source-name">{{ source.name }}</div>
              <div class="source-meta">
                <span class="meta-url">{{ source.base_url }}</span>
                <span class="meta-stats">
                  <span class="stat-chip">
                    <AppIcon name="database" :size="11" />
                    {{ source.total_count || 0 }}
                  </span>
                  <span class="stat-chip">
                    <AppIcon name="hash" :size="11" />
                    {{ source.last_max_id || 0 }}
                  </span>
                </span>
              </div>
            </div>
            <div class="source-actions" @click.stop>
              <el-switch
                :model-value="source.enabled"
                size="small"
                @change="(val) => toggleSource(source.id, { enabled: val })"
              />
              <el-tag
                v-if="mockTasks[source.id]?.status === 'running'"
                type="primary"
                effect="dark"
                size="small"
                round
                class="status-tag running"
              >运行中</el-tag>
              <el-tag
                v-else-if="source.last_status === 'success'"
                type="success"
                effect="dark"
                size="small"
                round
              >成功</el-tag>
              <el-tag
                v-else-if="source.last_status === 'failed'"
                type="danger"
                effect="dark"
                size="small"
                round
              >失败</el-tag>
              <el-tag v-else type="info" effect="dark" size="small" round>空闲</el-tag>
              
              <el-button
                size="small"
                type="primary"
                @click="startMockCollect(source.id)"
                :disabled="!source.enabled || mockTasks[source.id]?.status === 'running'"
              ><AppIcon name="play" :size="12" style="margin-right:4px" />采集</el-button>
              <el-button size="small" @click="openSourceDialog(source)" text>编辑</el-button>
              <el-button size="small" type="danger" @click="deleteSource(source.id)" text>删除</el-button>
            </div>
          </div>

          <!-- 展开区域 -->
          <div class="source-body" v-if="expandedIds.has(source.id)">
            <!-- 运行中面板 -->
            <div v-if="mockTasks[source.id]?.status === 'running'" class="task-panel">
              <div class="task-header">
                <div class="task-title"><AppIcon name="loader-circle" :size="14" style="display:inline-block;margin-right:6px;animation:spin 1s linear infinite" />正在采集</div>
                <div class="task-time">
                  开始于 {{ mockTasks[source.id].startTimeText }} · 已运行 {{ mockTasks[source.id].elapsed }}s
                </div>
              </div>

              <!-- 进度条 -->
              <div class="progress-section">
                <div class="progress-header">
                  <div class="progress-text">
                    进度: <strong>{{ mockTasks[source.id].current }}</strong> / {{ mockTasks[source.id].total }} 条
                  </div>
                  <div class="progress-percent">{{ mockTasks[source.id].percent }}%</div>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: mockTasks[source.id].percent + '%' }"></div>
                </div>
              </div>

              <!-- 统计 -->
              <div class="stats-grid">
                <div class="stat-item">
                  <div class="stat-label">总数</div>
                  <div class="stat-value total">{{ mockTasks[source.id].total }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">成功</div>
                  <div class="stat-value success">{{ mockTasks[source.id].success }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">失败</div>
                  <div class="stat-value error">{{ mockTasks[source.id].errors }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">速度</div>
                  <div class="stat-value speed">{{ mockTasks[source.id].speed }}/s</div>
                </div>
              </div>

              <!-- 当前正在爬取 -->
              <div class="current-fetch" v-if="mockTasks[source.id].currentFetch">
                <div class="fetch-label"><AppIcon name="activity" :size="12" style="display:inline-block;margin-right:4px" />正在爬取</div>
                <div class="fetch-title">{{ mockTasks[source.id].currentFetch.title }}</div>
                <div class="fetch-detail">{{ mockTasks[source.id].currentFetch.detail }}</div>
              </div>

              <!-- 实时日志 -->
              <div class="log-section">
                <div class="log-title">
                  <span><AppIcon name="file-text" :size="14" style="display:inline-block;margin-right:4px" />实时日志</span>
                  <span class="log-clear" @click="clearMockLogs(source.id)">清空</span>
                </div>
                <div class="log-list">
                  <div v-for="(log, idx) in mockTasks[source.id].logs" :key="idx" class="log-item">
                    <span class="log-time">{{ log.time }}</span>
                    <span :class="['log-msg', log.type]">{{ log.msg }}</span>
                  </div>
                </div>
              </div>

              <div class="task-footer">
                <el-button size="small" type="danger" plain @click="stopMockCollect(source.id)"><AppIcon name="pause" :size="12" style="margin-right:4px" />停止采集</el-button>
              </div>
            </div>

            <!-- 空闲/历史面板 -->
            <div v-else class="task-panel">
              <div class="history-list" v-if="getMockHistory(source.id).length">
                <div v-for="(h, idx) in getMockHistory(source.id)" :key="idx" class="history-item">
                  <div class="history-left">
                    <AppIcon :name="h.trigger === '手动' ? 'mouse-pointer' : 'settings'" :size="13" class="history-icon" />
                    <span class="history-trigger">{{ h.trigger }}触发</span>
                    <span class="history-count">{{ h.total }}条 / {{ h.duration }}</span>
                  </div>
                  <div class="history-right">
                    <el-tag
                      :type="h.status === 'success' ? 'success' : 'danger'"
                      size="small"
                      effect="plain"
                    >
                      <AppIcon :name="h.status === 'success' ? 'check' : 'x'" :size="10" style="margin-right:2px" />
                      {{ h.status === 'success' ? '成功' : '失败' }}
                    </el-tag>
                    <span class="history-time">{{ h.time }}</span>
                  </div>
                </div>
              </div>
              <div v-else class="empty-hint">暂无采集历史</div>
            </div>
          </div>
        </div>

        <el-empty v-if="!collectionSources.length && !sourcesLoading" description="暂无采集源" :image-size="80" />
      </div>
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
        <el-form-item label="排序方式">
          <el-select v-model="sourceForm.sort_order" style="width: 100%">
            <el-option label="按更新时间" value="time" />
            <el-option label="按ID倒序" value="id" />
            <el-option label="按点击量" value="hits" />
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
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
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
  sort_order: 'time',
})

// ── 展开状态 ──
const expandedIds = reactive(new Set())

function toggleExpand(id) {
  if (expandedIds.has(id)) {
    expandedIds.delete(id)
  } else {
    expandedIds.add(id)
  }
}

// ── 模拟采集任务 ──
const mockTasks = reactive({})
const mockHistory = reactive({})
let mockTimer = null

// 模拟数据：标题池
const mockTitles = [
  '庆余年 第二季', '狂飙', '三体', '繁花', '与凤行',
  '封神第一部', '孤注一掷', '满江红', '消失的她', '长安三万里',
  '狂飙之下', '南风知我意', '墨雨云间', '度华年', '承欢记',
  '三体 Ⅱ', '流浪地球 3', '无间道 重启', '神雕侠侣 新版', '雪山飞狐',
]
const mockCategories = ['剧情', '古装', '悬疑', '喜剧', '动作', '爱情', '科幻']

function randomMockTitle() {
  return mockTitles[Math.floor(Math.random() * mockTitles.length)]
}

function randomMockCategory() {
  return mockCategories[Math.floor(Math.random() * mockCategories.length)]
}

function formatTimeStr(ts) {
  const d = new Date(ts)
  return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}:${String(d.getSeconds()).padStart(2, '0')}`
}

function startMockCollect(id) {
  const source = collectionSources.value.find(s => s.id === id)
  if (!source || !source.enabled) return

  // 初始化任务
  const startTime = Date.now()
  const total = 800 + Math.floor(Math.random() * 400)

  mockTasks[id] = {
    status: 'running',
    total,
    current: 0,
    success: 0,
    errors: 0,
    startTime,
    startTimeText: formatTimeStr(startTime),
    elapsed: 0,
    percent: 0,
    speed: 0,
    logs: [
      { time: formatTimeStr(startTime), type: 'info', msg: `开始采集 ${source.name}` },
      { time: formatTimeStr(startTime), type: 'info', msg: `连接 API: ${source.base_url}` },
      { time: formatTimeStr(startTime), type: 'info', msg: `获取列表成功，共 ${total} 条` },
    ],
    currentFetch: null,
  }

  // 确保展开
  expandedIds.add(id)

  // 启动模拟爬取
  runMockFetch(id)
}

function runMockFetch(id) {
  const task = mockTasks[id]
  if (!task || task.status !== 'running') return

  const batchSize = 1 + Math.floor(Math.random() * 3)
  const now = Date.now()
  task.elapsed = Math.round((now - task.startTime) / 1000)

  for (let i = 0; i < batchSize && task.current < task.total; i++) {
    task.current++

    if (Math.random() > 0.05) {
      task.success++
      const title = randomMockTitle()
      task.currentFetch = {
        title,
        detail: `ID: ${task.current} · 分类: ${randomMockCategory()}`,
      }
      task.logs.push({
        time: formatTimeStr(now),
        type: 'success',
        msg: `✓ [${task.current}/${task.total}] ${title}`,
      })
    } else {
      task.errors++
      task.logs.push({
        time: formatTimeStr(now),
        type: 'error',
        msg: `✗ [${task.current}/${task.total}] ID ${task.current} 获取失败`,
      })
    }
  }

  // 限制日志数量
  if (task.logs.length > 100) {
    task.logs = task.logs.slice(-50)
  }

  // 更新统计
  task.percent = Math.round((task.current / task.total) * 100)
  task.speed = task.elapsed > 0 ? (task.current / task.elapsed).toFixed(1) : '0.0'

  // 判断是否完成
  if (task.current >= task.total) {
    completeMockCollect(id)
    return
  }

  // 继续
  mockTimer = setTimeout(() => runMockFetch(id), 80 + Math.random() * 120)
}

function stopMockCollect(id) {
  const task = mockTasks[id]
  if (!task) return

  task.status = 'idle'
  task.logs.push({
    time: formatTimeStr(Date.now()),
    type: 'info',
    msg: '⏹ 用户手动停止采集',
  })

  // 保存到历史
  saveMockHistory(id)
}

function completeMockCollect(id) {
  const task = mockTasks[id]
  if (!task) return

  task.status = 'completed'
  task.logs.push({
    time: formatTimeStr(Date.now()),
    type: 'info',
    msg: `✅ 采集完成，共处理 ${task.total} 条`,
  })

  // 保存到历史
  saveMockHistory(id)
}

function saveMockHistory(id) {
  const task = mockTasks[id]
  if (!task) return

  if (!mockHistory[id]) mockHistory[id] = []

  mockHistory[id].unshift({
    time: formatDate(new Date()),
    trigger: '手动',
    status: 'success',
    total: task.total,
    duration: `${task.elapsed}s`,
  })

  // 只保留最近 5 条
  if (mockHistory[id].length > 5) {
    mockHistory[id] = mockHistory[id].slice(0, 5)
  }

  // 清理任务
  delete mockTasks[id]
}

function getMockHistory(id) {
  return mockHistory[id] || []
}

function clearMockLogs(id) {
  if (mockTasks[id]) {
    mockTasks[id].logs = []
  }
}

async function loadSources() {
  if (!store.isAdmin) return
  sourcesLoading.value = true
  try {
    collectionSources.value = await collectionAPI.listSources()
    // 为每个采集源初始化模拟历史数据
    collectionSources.value.forEach(source => {
      if (!mockHistory[source.id]) {
        mockHistory[source.id] = [
          {
            time: new Date(Date.now() - 3600000).toLocaleString('zh-CN'),
            trigger: source.auto_collect ? '自动' : '手动',
            status: 'success',
            total: 800 + Math.floor(Math.random() * 400),
            duration: `${60 + Math.floor(Math.random() * 120)}s`,
          },
          {
            time: new Date(Date.now() - 86400000).toLocaleString('zh-CN'),
            trigger: '自动',
            status: 'success',
            total: 800 + Math.floor(Math.random() * 400),
            duration: `${60 + Math.floor(Math.random() * 120)}s`,
          },
        ]
      }
    })
  } catch (e) {
    // API 失败时使用模拟数据
    console.warn('加载采集源失败，使用模拟数据:', e)
    collectionSources.value = [
      {
        id: 1,
        name: '杏吧',
        base_url: 'https://json.xingba222.com/api.php/provide/vod/',
        enabled: true,
        auto_collect: true,
        interval_minutes: 60,
        last_status: 'success',
        last_collected_at: new Date(Date.now() - 3600000).toISOString(),
        total_count: 12580,
        last_max_id: 12580,
      },
      {
        id: 2,
        name: '155API',
        base_url: 'https://155api.com/api.php/provide/vod/',
        enabled: true,
        auto_collect: false,
        interval_minutes: 30,
        last_status: 'success',
        last_collected_at: new Date(Date.now() - 7200000).toISOString(),
        total_count: 8360,
        last_max_id: 8360,
      },
      {
        id: 3,
        name: 'Slapibf',
        base_url: 'https://slapibf.com/api.php/provide/vod/',
        enabled: false,
        auto_collect: false,
        interval_minutes: 120,
        last_status: null,
        last_collected_at: null,
        total_count: 0,
        last_max_id: 0,
      },
    ]

    // 初始化模拟历史数据
    if (!mockHistory[1]) {
      mockHistory[1] = [
        {
          time: '2026/08/21 05:26:13',
          trigger: '手动',
          status: 'success',
          total: 1000,
          duration: '157s',
        },
        {
          time: '2026/08/20 18:30:00',
          trigger: '自动',
          status: 'success',
          total: 1000,
          duration: '180s',
        },
      ]
    }
  } finally {
    sourcesLoading.value = false
  }
}

// 加载采集日志（占位函数，当前使用模拟数据）
async function loadLogs() {
  // TODO: 当后端 API 就绪时，从 collectionAPI 获取真实日志
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
      sort_order: source.sort_order || 'time',
    }
  } else {
    editingSource.value = null
    sourceForm.value = {
      name: '',
      base_url: '',
      enabled: true,
      auto_collect: false,
      interval_minutes: 60,
      sort_order: 'time',
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
  background: transparent;
  color: var(--color-text-tertiary, #909399);
  border: none;
  padding: 8px 0;
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

  // ── 源卡片列表 ──
  .source-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .source-item {
    border: 1px solid var(--color-border-subtle);
    border-radius: 10px;
    overflow: hidden;
    transition: border-color 0.2s;

    &:hover {
      border-color: var(--color-border);
    }

    &.expanded {
      border-color: var(--color-accent);
    }
  }

  .source-header {
    display: flex;
    align-items: center;
    padding: 8px 14px;
    cursor: pointer;
    transition: background 0.15s;

    &:hover {
      background: var(--color-hover);
    }
  }

  .expand-icon {
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    background: var(--color-bg-hover, transparent);
    margin-right: 10px;
    transition: background 0.15s;
    flex-shrink: 0;
    color: var(--color-text-tertiary);

    .expanded & {
      background: var(--color-accent);
      color: white;
    }
  }

  .source-info {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 1px;
  }

  .source-name {
    font-weight: 600;
    font-size: 14px;
    line-height: 1.3;
  }

  .source-meta {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    line-height: 1.2;
  }

  .meta-url {
    color: var(--color-text-tertiary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 320px;
  }

  .meta-stats {
    display: flex;
    align-items: center;
    gap: 4px;
    flex-shrink: 0;
  }

  .stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    padding: 1px 6px;
    font-size: 11px;
    background: var(--color-bg-hover);
    border-radius: 8px;
    color: var(--color-text-secondary);
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
  }

  .source-actions {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
  }

  .status-tag.running {
    animation: pulse 1.5s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  // ── 展开区域 ──
  .source-body {
    border-top: 1px solid var(--color-border-subtle);
    background: var(--color-bg-page, #fafafa);
  }

  // ── 任务面板 ──
  .task-panel {
    padding: 12px 16px;
  }

  .task-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }

  .task-title {
    font-size: 14px;
    font-weight: 600;
  }

  .task-time {
    font-size: 12px;
    color: var(--color-text-tertiary);
  }

  // 进度条
  .progress-section {
    margin-bottom: 16px;
  }

  .progress-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
  }

  .progress-text {
    font-size: 13px;
    color: var(--color-text-tertiary);

    strong {
      color: var(--color-text-primary);
      font-weight: 600;
    }
  }

  .progress-percent {
    font-size: 18px;
    font-weight: 700;
    color: var(--color-accent);
  }

  .progress-bar {
    width: 100%;
    height: 8px;
    background: var(--color-border-subtle);
    border-radius: 4px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--color-accent), var(--color-success, #67c23a));
    border-radius: 4px;
    transition: width 0.3s ease;
  }

  // 统计网格
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 16px;
  }

  .stat-item {
    background: var(--color-bg-container, #fff);
    padding: 10px;
    border-radius: 8px;
    text-align: center;
    border: 1px solid var(--color-border-subtle);
  }

  .stat-label {
    font-size: 12px;
    color: var(--color-text-tertiary);
    margin-bottom: 2px;
  }

  .stat-value {
    font-size: 18px;
    font-weight: 700;

    &.total { color: var(--color-accent); }
    &.success { color: var(--color-success, #67c23a); }
    &.error { color: var(--color-danger, #f56c6c); }
    &.speed { color: var(--color-warning, #e6a23c); }
  }

  // 当前正在爬取
  .current-fetch {
    background: var(--color-accent-light-9, #ecf5ff);
    border: 1px solid var(--color-accent-light-7, #d9ecff);
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 16px;
  }

  .fetch-label {
    font-size: 11px;
    color: var(--color-accent);
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;

    &::before {
      content: '';
      width: 6px;
      height: 6px;
      background: var(--color-accent);
      border-radius: 50%;
      animation: blink 1s infinite;
    }
  }

  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }

  .fetch-title {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 2px;
  }

  .fetch-detail {
    font-size: 12px;
    color: var(--color-text-tertiary);
    font-family: 'Menlo', 'Monaco', monospace;
  }

  // 日志区域（仅运行中面板使用）
  .log-clear {
    font-size: 12px;
    color: var(--color-text-tertiary);
    cursor: pointer;

    &:hover { color: var(--color-text-primary); }
  }

  .log-list {
    max-height: 180px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 2px;

    &::-webkit-scrollbar { width: 4px; }
    &::-webkit-scrollbar-track { background: transparent; }
    &::-webkit-scrollbar-thumb { background: var(--color-border-subtle); border-radius: 2px; }
  }

  .log-item {
    display: flex;
    gap: 8px;
    font-size: 12px;
    padding: 2px 0;
    font-family: 'Menlo', 'Monaco', monospace;
  }

  .log-time {
    color: var(--color-text-tertiary);
    flex-shrink: 0;
  }

  .log-msg {
    flex: 1;

    &.success { color: var(--color-success, #67c23a); }
    &.error { color: var(--color-danger, #f56c6c); }
    &.info { color: var(--color-accent); }
  }

  .task-footer {
    margin-top: 12px;
    text-align: right;
  }

  // 历史记录
  .history-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .history-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 10px;
    background: var(--color-bg-container);
    border-left: 3px solid var(--color-accent);
    border-radius: 4px;
    transition: background 0.2s;

    &:hover {
      background: var(--color-bg-hover, var(--color-bg-container));
    }
  }

  .history-left {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
  }

  .history-icon {
    font-size: 13px;
  }

  .history-trigger {
    color: var(--color-text-secondary);
  }

  .history-count {
    color: var(--color-text-tertiary);
    font-size: 12px;
  }

  .history-right {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .history-time {
    font-size: 12px;
    color: var(--color-text-tertiary);
  }

  .empty-hint {
    text-align: center;
    padding: 16px;
    color: var(--color-text-tertiary);
    font-size: 13px;
  }

  @media (max-width: 600px) {
    .source-actions {
      flex-wrap: wrap;
      gap: 6px;
    }

    .stats-grid {
      grid-template-columns: repeat(2, 1fr);
    }

    .task-panel {
      padding: 10px 12px;
    }
  }
}
</style>
