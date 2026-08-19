/**
 * 布局注册表 —— 模块化布局架构的核心（需求 5）
 *
 * 新增布局只需在此登记一个 key -> 异步组件 的映射，
 * 然后在路由的 meta.layout 中引用该 key 即可，核心代码零侵入。
 */
import { defineAsyncComponent } from 'vue'

export const layoutRegistry = {
  // 默认主布局：侧边栏 + 头部 + 内容区
  main: defineAsyncComponent(() => import('./MainLayout.vue')),
  // 空壳布局：全屏页（登录、404）
  blank: defineAsyncComponent(() => import('./BlankLayout.vue')),
  // 演示：顶部导航布局（零侵入示例，见 TopNavLayout.vue；使用时在路由 meta.layout='topnav' 即可）
  topnav: defineAsyncComponent(() => import('./TopNavLayout.vue')),
}

/** 取布局组件；未知 layout 名回退到主布局 */
export function resolveLayout(name) {
  return layoutRegistry[name] || layoutRegistry.main
}
