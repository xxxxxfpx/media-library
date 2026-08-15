/**
 * 系统信息 API
 */
import api from './http'

export const systemAPI = {
  /**
   * 获取系统信息
   * @returns {Promise<Object>} 系统信息
   */
  async getInfo() {
    return await api.get('/api/system/info')
  }
}
