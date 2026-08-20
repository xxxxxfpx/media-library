<template>
  <div class="system-container">
    <button class="back-link" @click="$router.push('/')">
      <AppIcon name="arrow-left" :size="16" /> 返回
    </button>

    <el-row :gutter="20" class="mb-4">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <AppIcon name="monitor" :size="32" style="color: var(--color-info)" />
            <div class="stat-info">
              <div class="stat-value">{{ systemInfo.ip || '--' }}</div>
              <div class="stat-label">IP 地址</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <AppIcon name="cpu" :size="32" style="color: var(--color-success)" />
            <div class="stat-info">
              <div class="stat-value">{{ systemInfo.cpu?.toFixed(1) || '0' }}%</div>
              <div class="stat-label">CPU 使用率</div>
            </div>
          </div>
          <el-progress :percentage="systemInfo.cpu || 0" :stroke-width="8" :show-text="false" :color="getProgressColor(systemInfo.cpu)" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <AppIcon name="coins" :size="32" style="color: var(--color-warning)" />
            <div class="stat-info">
              <div class="stat-value">{{ systemInfo.memory_percent?.toFixed(1) || '0' }}%</div>
              <div class="stat-label">内存使用</div>
            </div>
          </div>
          <el-progress :percentage="systemInfo.memory_percent || 0" :stroke-width="8" :show-text="false" :color="getProgressColor(systemInfo.memory_percent)" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <AppIcon name="folder" :size="32" style="color: var(--color-danger)" />
            <div class="stat-info">
              <div class="stat-value">{{ systemInfo.disk_percent?.toFixed(1) || '0' }}%</div>
              <div class="stat-label">磁盘使用</div>
            </div>
          </div>
          <el-progress :percentage="systemInfo.disk_percent || 0" :stroke-width="8" :show-text="false" :color="getProgressColor(systemInfo.disk_percent)" />
        </el-card>
      </el-col>
    </el-row>

    <el-card>
      <template #header>
        <span>详细信息</span>
      </template>
      <div class="detail-list">
        <div class="detail-row">
          <span class="detail-label">系统平台</span>
          <span class="detail-value">{{ systemInfo.platform }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Python 版本</span>
          <span class="detail-value">{{ systemInfo.python_version }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">运行时间</span>
          <span class="detail-value">{{ systemInfo.uptime }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">服务器负载</span>
          <span class="detail-value">{{ systemInfo.load }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">内存详情</span>
          <span class="detail-value">{{ systemInfo.memory_used }} / {{ systemInfo.memory_total }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">磁盘详情</span>
          <span class="detail-value">{{ systemInfo.disk_used }} / {{ systemInfo.disk_total }}</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { systemAPI } from '@/api'
import AppIcon from '@/components/ui/AppIcon.vue'

const systemInfo = ref({})
let timer = null

async function fetchSystemInfo() {
  try {
    const data = await systemAPI.getInfo()
    systemInfo.value = data || {}
  } catch (error) {
    console.error('获取系统信息失败:', error)
    systemInfo.value = {}
  }
}

function getProgressColor(value) {
  if (value > 90) return 'var(--color-danger)'
  if (value > 70) return 'var(--color-warning)'
  return 'var(--color-success)'
}

function startPolling() {
  stopPolling()
  timer = setInterval(fetchSystemInfo, 5000)
}

function stopPolling() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

function onVisibilityChange() {
  if (document.hidden) {
    stopPolling()
  } else {
    fetchSystemInfo()
    startPolling()
  }
}

onMounted(() => {
  fetchSystemInfo()
  startPolling()
  document.addEventListener('visibilitychange', onVisibilityChange)
})

onUnmounted(() => {
  stopPolling()
  document.removeEventListener('visibilitychange', onVisibilityChange)
})
</script>

<style scoped lang="scss">
.system-container {
  padding: 20px;
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

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
}

.stat-label {
  font-size: 12px;
  color: var(--imm-text-tertiary);
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
</style>
