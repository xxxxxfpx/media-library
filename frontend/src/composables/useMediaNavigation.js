/**
 * 全局媒体导航组合式函数
 * 
 * 提供全局路由跳转方法，任何组件都可以通过 openMediaDetail 跳转到媒体详情页
 * 
 * 使用方式：
 * import { openMediaDetail } from '@/composables/useMediaNavigation'
 * openMediaDetail(itemId)  // 跳转到媒体详情页
 */

import { reactive } from 'vue'
import router from '@/router'

const detailState = reactive({
  visible: false,
  itemId: null,
  itemData: null,
  loading: false,
})

/**
 * 打开媒体详情页 - 直接路由跳转
 * @param {number|string} itemId - 媒体项ID
 * @param {Object} options - 选项
 * @param {boolean} options.replace - 是否使用 replace 而非 push
 */
export function openMediaDetail(itemId, options = {}) {
  const { replace = false } = options

  if (!itemId) return

  const path = `/media/${itemId}`

  if (replace) {
    router.replace(path)
  } else {
    router.push(path)
  }
}

/**
 * 关闭媒体详情抽屉
 */
export function closeMediaDetail() {
  detailState.visible = false
  detailState.itemId = null
  detailState.itemData = null
  detailState.loading = false
}

/**
 * 在组合式函数中使用（组件内）
 * 返回响应式状态和操作方法
 */
export function useMediaNavigation() {
  return {
    state: detailState,
    openMediaDetail,
    closeMediaDetail,
  }
}

export default {
  open: openMediaDetail,
  close: closeMediaDetail,
}
