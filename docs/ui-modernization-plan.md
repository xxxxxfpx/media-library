# Web 前端 UI 全面现代化优化计划书

> 版本：v1.0 ｜ 日期：2026-08-19 ｜ 状态：待评审
> 范围：`frontend/`（Vue 3 SPA）为主，含后端冗余代码清理（第 8 章）

---

## 1. 概述

### 1.1 背景与目标

media-library 前端基于 Vue 3 + Vite + Element Plus + SCSS 构建，已稳定运行，但 UI 层存在**主题能力薄弱、颜色硬编码、图标体系单一、布局不可扩展**等结构性债务。本计划书给出一套完整的 UI 现代化改造方案，达成以下目标：

1. 建立多主题配色系统（必备「现代黑」「现代白」），全部颜色经设计令牌动态管理；
2. CSS / UI / 框架 / 布局 / 配色全面对齐现代化标准（CSS 变量、OKLCH、容器查询、View Transitions）；
3. 引入 Tailwind CSS 实现响应式布局；
4. 图标全面迁移到 Iconify 精细 SVG 图标（构建时按需打包），杜绝 Unicode 字符图标；
5. 布局采用模块化注册架构，未来新增布局零侵入；
6. 交互动效现代化、细腻自然，并尊重无障碍偏好；
7. 清理后端服务中遗留的冗余无用代码。

### 1.2 现状诊断（已实地核查）

| 维度 | 现状 | 问题 |
|---|---|---|
| 主题 | `styles/immersive.scss` 定义 `--imm-*` 变量，仅 暗色（默认）/ 亮色（`data-theme="light"`）两态 | 主题数量不足；色板为旧 Material Design（#2196F3 等）；无法扩展 |
| 颜色管理 | 语义变量与硬编码并存 | `FileRow.vue`（#4CAF50/#2196F3/#FF9800/#00BCD4）、`MediaCard.vue`（渐变硬编码）、`MediaDetailDrawer.vue`（rgba 黑/#FFC107）、`Home.vue`（**JS 数据内**写死图标色）等大量泄漏 |
| 图标 | 全量使用 `@element-plus/icons-vue` | 风格偏传统、可扩展性弱；未使用 Unicode 图标（迁移基础良好） |
| 布局 | 单一 `layouts/MainLayout.vue`（el-aside 侧边栏 + header + main） | 无布局注册机制，新增布局需改核心代码 |
| 样式组织 | `style.scss`（根）+ `styles/common.scss` + `styles/immersive.scss` 三处并存 | 冗余、职责不清 |
| 后端 | `backend/app/` 纯 REST API，无 StaticFiles / 模板 / HTML 渲染（已核实） | 后端无"页面代码"；冗余集中在 `backend/scripts/legacy/`（20+ 一次性迁移脚本，AGENTS.md 已禁止运行）及个别为旧 UI 服务的接口字段 |
| 构建 | Vite 5 + Sass，无 Tailwind、无 stylelint | 缺少样式层面的自动化约束 |

### 1.3 非目标（Out of Scope）

- 不重写业务逻辑与 API 层；
- 不更换 Vue 3 / Vite / Element Plus 核心框架（理由见 2.2）；
- `mobile/`（Flutter 客户端）不在本期范围；
- 不涉及数据库 schema 变更。

---

## 2. 总体技术方案

### 2.1 技术选型总览

| 领域 | 选型 | 版本基线 | 说明 |
|---|---|---|---|
| UI 组件库 | **保留 Element Plus** | ≥2.5 | 经 CSS 变量深度主题化（--el-* 桥接），避免整体重写 |
| 原子化 CSS | **Tailwind CSS** | v4.x（`@tailwindcss/vite`） | CSS-first `@theme` 与令牌系统天然契合；OKLCH 默认色板；Oxide 引擎按需生成 |
| 图标 | **Iconify（unplugin-icons）+ lucide 图标集** | 最新 | 构建时按需打包、离线可用、tree-shaking；lucide 为现代精细线条风格标杆 |
| 设计令牌 | CSS 自定义属性（三层架构） | — | OKLCH 色彩空间，感知均匀 |
| 动效 | CSS transition/animation + View Transitions API | — | 路由转场原生支持，降级方案 `<Transition>` |
| 状态 | Pinia（沿用） | ≥2.1 | 新增 `theme` 模块 |
| 质量门禁 | stylelint + ESLint + 既有 CI | — | 将"禁止硬编码颜色/Unicode 图标"固化为 lint 规则 |

> 备选：若团队更熟悉 Tailwind v3 插件生态，可降级为 3.4.x（`tailwind.config.js` + CSS 变量色板），令牌方案不变。默认推荐 v4。

### 2.2 为什么保留 Element Plus 而非重写为 headless 方案

1. 现有 24 个视图/组件深度依赖 EP 表格、表单、抽屉、菜单等复杂组件，重写成本与回归风险极高；
2. EP 官方支持 CSS 变量主题化（`--el-*` 全量暴露），配合语义令牌桥接可实现彻底换肤；
3. 本计划的重心是**令牌化 + 响应式 + 图标 + 动效**，均可在保留 EP 的前提下达成现代化标准。
4. 若未来追求完全定制视觉，可在令牌层不变的前提下逐步以自研组件替换 EP 组件（模块化架构保证兼容，见第 6 章）。

### 2.3 目标目录结构

```
frontend/src/
├── styles/
│   ├── tokens/
│   │   ├── primitives.css      # 基础色板（OKLCH 色阶，唯一定义色值处）
│   │   ├── semantic.css        # 语义令牌默认值
│   │   ├── themes/
│   │   │   ├── modern-dark.css   # 现代黑（必备）
│   │   │   ├── modern-light.css  # 现代白（必备）
│   │   │   ├── indigo-night.css  # 靛夜蓝
│   │   │   ├── emerald-mist.css  # 翡翠雾
│   │   │   ├── amber-sand.css    # 琥珀砂
│   │   │   └── rose-dusk.css     # 玫瑰暮
│   │   └── element-bridge.css  # --el-* ← 语义令牌桥接
│   ├── motion.css              # 动效令牌（时长/缓动）
│   ├── base.css                # reset 之外的少量全局基线
│   └── tailwind.css            # Tailwind 入口（@theme inline 映射令牌）
├── layouts/
│   ├── registry.js             # 布局注册表（唯一扩展点）
│   ├── AppShell.vue            # 组合式布局壳（slots: sidebar/header/aside/footer）
│   └── modules/                # 布局子模块（Sidebar.vue / Header.vue / ...）
├── components/
│   ├── ui/                     # 基础 UI（AppIcon.vue / ThemeSwitcher.vue / Skeleton...）
│   └── ...                     # 业务组件（现有）
├── composables/
│   ├── useTheme.js             # 主题读取/切换/持久化/跟随系统
│   └── useLayout.js            # 布局状态（侧栏折叠等）
└── icons/
    └── registry.js             # 图标名 → 组件 映射（动态图标白名单）
```

---

## 3. 主题配色系统（对应需求 1、7）

### 3.1 三层设计令牌架构

```
第 1 层 基础令牌 primitives    原始色板，OKLCH 色阶（--indigo-500、--zinc-900…）
        │                      全项目唯一直接书写色值的地方
        ▼
第 2 层 语义令牌 semantic      按用途命名，主题通过重定义取值换肤
        │                      （--color-bg-surface、--color-text-primary、--color-accent…）
        ▼
第 3 层 组件令牌 component     可选，个别组件细节（--card-radius、--sidebar-width…）
                               及 Element Plus 桥接（--el-color-primary ← --color-accent）
```

规则：**业务代码（模板/SCSS/JS）只允许引用第 2 层及以上令牌**；`styles/tokens/primitives.css` 是全项目唯一合法的色值定义文件。

示例：

```css
/* tokens/primitives.css —— 唯一色值源（节选） */
:root {
  --indigo-400: oklch(67% 0.17 275);   /* 现代黑强调色 */
  --indigo-600: oklch(55% 0.19 275);   /* 现代白强调色 */
  --zinc-950:  oklch(13% 0.01 265);
  --zinc-50:   oklch(98.5% 0 0);
}

/* tokens/themes/modern-dark.css */
[data-theme="modern-dark"] {
  --color-bg-page: var(--zinc-950);
  --color-bg-surface: oklch(17% 0.01 265);
  --color-text-primary: var(--zinc-50);
  --color-accent: var(--indigo-400);
  --color-accent-soft: oklch(67% 0.17 275 / 0.15);
  /* …完整语义集见 3.3 */
}

/* tokens/element-bridge.css —— EP 组件随主题联动 */
[data-theme="modern-dark"] {
  --el-color-primary: var(--color-accent);
  --el-bg-color: var(--color-bg-surface);
  --el-text-color-primary: var(--color-text-primary);
  --el-border-color: var(--color-border-subtle);
  /* …按 EP 变量清单全量桥接 */
}
```

### 3.2 主题清单（6 套）

| 主题 | 标识（`data-theme`） | 定位 | 页面底 / 表面 / 主文字 / 强调色 |
|---|---|---|---|
| **现代黑**（必备） | `modern-dark` | 默认主题。中性近黑 + 靛蓝强调，类 shadcn/ui 暗色风格 | `#0a0a0b` / `#17171a` / `#fafafa` / `#6366f1` |
| **现代白**（必备） | `modern-light` | 清爽留白 + 同源靛蓝，类 shadcn/ui 亮色风格 | `#ffffff` / `#f4f4f5` / `#18181b` / `#4f46e5` |
| 靛夜蓝 | `indigo-night` | 深蓝底 + 天青强调，影院感 | `#0f172a` / `#1e293b` / `#e2e8f0` / `#38bdf8` |
| 翡翠雾 | `emerald-mist` | 浅底 + 翡翠强调，清新 | `#f0fdf4` / `#ffffff` / `#14532d` / `#10b981` |
| 琥珀砂 | `amber-sand` | 暖浅底 + 琥珀强调 | `#fffbeb` / `#ffffff` / `#451a03` / `#f59e0b` |
| 玫瑰暮 | `rose-dusk` | 深紫底 + 玫粉强调 | `#1e1b2e` / `#2a2740` / `#ede9fe` / `#f472b6` |

> 上表十六进制仅为文档示意；实现一律使用 OKLCH 定义于 primitives，并经语义令牌消费。主题扩展 = 新增一个 `themes/*.css` 文件 + 注册表登记一行，零侵入。

### 3.3 语义令牌清单（v1 基线）

| 类别 | 令牌（节选） |
|---|---|
| 背景 | `--color-bg-page` `--color-bg-surface` `--color-bg-elevated` `--color-bg-inverse` |
| 文字 | `--color-text-primary` `--color-text-secondary` `--color-text-tertiary` `--color-text-disabled` `--color-text-inverse` |
| 强调/语义 | `--color-accent` `--color-accent-hover` `--color-accent-soft` `--color-success` `--color-warning` `--color-danger` `--color-info` |
| 边框/分割 | `--color-border-default` `--color-border-subtle` `--color-border-strong` |
| 交互状态 | `--color-hover` `--color-hover-strong` `--color-selected` `--color-overlay` `--color-backdrop` |
| 玻璃拟态 | `--glass-bg` `--glass-blur` |
| 图表/统计 | `--color-stat-video` `--color-stat-audio` `--color-stat-image` `--color-stat-book`（供 Home 统计卡等 JS 场景以 CSS 变量消费） |
| 圆角/阴影 | `--radius-sm/md/lg/xl` `--shadow-sm/md/lg` `--shadow-glow-accent` |

### 3.4 主题切换机制

```js
// composables/useTheme.js（要点）
const THEMES = ['modern-dark', 'modern-light', 'indigo-night',
                'emerald-mist', 'amber-sand', 'rose-dusk']

function applyTheme(id) {
  document.documentElement.dataset.theme = id          // 换肤唯一动作
  localStorage.setItem('ui.theme', id)
}
// 初始化顺序：localStorage → 用户系统偏好（prefers-color-scheme 映射到两套必备主题）→ 默认 modern-dark
// Pinia theme store 暴露 currentTheme / setTheme / followSystem
```

- 首屏防闪烁：`index.html` 内联 3 行脚本，在 CSS 加载前完成 `data-theme` 设置；
- `ThemeSwitcher` 组件（设置页 + 头部快捷入口）提供色板预览式选择；
- 旧 `--imm-*` 变量在过渡期保留为**别名**（`--imm-bg-primary: var(--color-bg-page)`），随组件改造逐步删除，最终移除 `immersive.scss`。

### 3.5 禁止硬编码颜色——工程化强制（对应需求 7）

1. **stylelint**（新增依赖，接入 `npm run lint`）：

```json
{
  "rules": {
    "declaration-property-value-disallowed-list": {
      "/^color$|^background|^border|^fill|^stroke|^box-shadow|^outline/":
        ["/#[0-9a-fA-F]{3,8}\\b/", "/^rgba?\\(/", "/^hsla?\\(/"]
    }
  }
}
```
   `styles/tokens/**` 加入 `ignoreFiles` 白名单（唯一定义处）。
   执行策略：先以 warning 跑通存量清理，切换为 error 作为长期门禁。

2. **ESLint**（no-restricted-syntax）：禁止 JS 中向样式相关 props/数据传十六进制色值（解决 `Home.vue` `color: '#2196F3'` 一类问题，统一改为令牌名，由模板 `var(--color-stat-video)` 消费）。

3. **CI 门禁**：`frontend` test 作业新增 `npx stylelint 'src/**/*.{vue,scss,css}'`，违例即失败。

---

## 4. Tailwind CSS 响应式布局（对应需求 8）

### 4.1 集成方式

```css
/* styles/tailwind.css */
@import "tailwindcss";

/* 语义令牌 → 工具类：inline 使工具类直接引用变量，随 data-theme 换肤 */
@theme inline {
  --color-bg-page:    var(--color-bg-page);
  --color-surface:    var(--color-bg-surface);
  --color-elevated:   var(--color-bg-elevated);
  --color-fg:         var(--color-text-primary);
  --color-muted:      var(--color-text-secondary);
  --color-accent:     var(--color-accent);
  --color-border:     var(--color-border-default);
  --radius-card:      var(--radius-lg);
}

/* 多主题场景下无需 dark: 变体——令牌本身随主题翻转；
   如个别处确需按主题分支，注册自定义变体： */
@custom-variant dark (&:where([data-theme="modern-dark"], [data-theme="indigo-night"], [data-theme="rose-dusk"] *));
```

```js
// vite.config.js
import tailwindcss from '@tailwindcss/vite'
export default defineConfig({ plugins: [vue(), tailwindcss()] })
```

> 由于令牌随主题翻转，`bg-surface text-fg border-border` 一类工具类**天然多主题**，无需为每个主题写变体分支——这正是"颜色不硬编码"在原子类层面的落点。

### 4.2 与 Element Plus 共存

- **preflight 冲突**：Tailwind preflight 会重置 `button` 等元素样式，影响 EP 组件。处理：将 EP 样式先引入、Tailwind 层后置（v4 默认 `@layer` 顺序下 utilities 优先级最高，仅覆盖同名属性）；对 `el-button` 等受影响组件以桥接令牌显式回填背景/边框。
- **类名纪律**：EP 组件尺寸/间距定制一律通过 `:deep()` + 令牌，不与工具类互相覆盖同一属性。
- 逐步以工具类替代组件内 SCSS 的布局代码（flex/grid/间距/响应式），SCSS 仅保留 EP 深度定制与复杂选择器。

### 4.3 响应式策略

| 断点（Tailwind 默认） | 目标设备 | 布局行为 |
|---|---|---|
| `<640px` | 手机 | 侧边栏 → 抽屉（overlay + 玻璃拟态）；栅格 2 列；底部安全区 |
| `≥640px` | 平板竖屏 | 侧边栏图标态；栅格 3 列 |
| `≥1024px` | 笔记本 | 完整侧边栏；栅格 4-5 列 |
| `≥1280px` | 桌面 | 内容区 max-width 约束 + 阅读友好行宽 |

- 媒体网格等局部自适应改用**容器查询**（`@container`），使组件不依赖视口宽度（模块化布局兼容性的关键，见第 6 章）；
- 移动端触控目标 ≥44px、`100dvh` 动态视口单位替代 `100vh`；
- 走查清单：360 / 768 / 1024 / 1440 / 1920px 五档，纳入验收。

---

## 5. 图标体系：Iconify 精细 SVG 图标（对应需求 4）

### 5.1 方案：unplugin-icons 构建时集成

- 依赖：`unplugin-icons` + `@iconify-json/lucide`（图标数据本地化，**离线可用**，不依赖 Iconify CDN 运行时请求）；
- 主图标集 **lucide**：现代、精细、统一线条风格（stroke 2px、圆角端点），与主题令牌的 `currentColor` 机制无缝配合；
- 按需加载：仅打包实际使用的图标，构建产物增量可控（每个图标约 0.5-1KB）。

```js
// vite.config.js
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import Components from 'unplugin-vue-components/resolvers'
// Components({ resolvers: [IconsResolver({ prefix: 'i', enabledCollections: ['lucide'] })] })
```

静态用法（模板中自动导入）：`<i-lucide-home />`、`<i-lucide-clapperboard />`

### 5.2 动态图标：注册表白名单

`Home.vue` 等场景存在 JS 数据驱动图标（`icon: 'VideoCamera'`）。为兼顾按需打包与动态性，建立显式注册表：

```js
// icons/registry.js
import Home        from '~icons/lucide/home'
import Clapperboard from '~icons/lucide/clapperboard'
import Star        from '~icons/lucide/star'
import History     from '~icons/lucide/history'
import Settings    from '~icons/lucide/settings'
import Monitor     from '~icons/lucide/monitor'
import Headphones  from '~icons/lucide/headphones'
import Image       from '~icons/lucide/image'
import BookOpen    from '~icons/lucide/book-open'
export const iconRegistry = { home: Home, clapperboard: Clapperboard, star: Star,
  history: History, settings: Settings, monitor: Monitor,
  headphones: Headphones, image: Image, 'book-open': BookOpen }
```

```vue
<!-- components/ui/AppIcon.vue：统一出口 -->
<script setup>
import { computed } from 'vue'
import { iconRegistry } from '@/icons/registry'
const props = defineProps({ name: { type: String, required: true }, size: { type: [Number, String], default: 18 } })
const comp = computed(() => iconRegistry[props.name])
</script>
<template>
  <component :is="comp" :width="size" :height="size" class="app-icon" aria-hidden="true" />
</template>
<style scoped>
.app-icon { display: inline-block; flex-shrink: 0; color: inherit; /* stroke 随文字/令牌变色 */ }
</style>
```

规则：**任何图标消费只走 `AppIcon` / `i-lucide-*` 前缀**，注册表即动态图标的唯一白名单。

### 5.3 存量迁移映射表（@element-plus/icons-vue → lucide）

| 现有 | 用途 | 迁移目标 |
|---|---|---|
| `VideoCamera` | 品牌/媒体库 | `lucide:clapperboard`（品牌）/ `lucide:video` |
| `HomeFilled` | 首页 | `lucide:home` |
| `Star` | 收藏 | `lucide:star` |
| `Clock` | 最近观看 | `lucide:history` |
| `Setting` | 设置 | `lucide:settings` |
| `Monitor` | 系统监控 | `lucide:activity`（监控语义）/ `lucide:monitor` |
| `Sunny` / `Moon` | 主题切换 | `lucide:sun` / `lucide:moon` |
| `Fold` / `Expand` | 侧栏折叠 | `lucide:panel-left-close` / `lucide:panel-left-open` |
| `ArrowDown` | 下拉指示 | `lucide:chevron-down` |
| `SwitchButton` | 退出登录 | `lucide:log-out` |
| `Headset` | 音乐统计 | `lucide:headphones` |
| `Picture` | 图片统计 | `lucide:image` |
| `Document` | 电子书统计 | `lucide:book-open` |

迁移完成后移除 `@element-plus/icons-vue` 依赖（约减 60KB+ 打包体积）。

### 5.4 禁止 Unicode 字符图标——工程化强制

1. ESLint `no-restricted-syntax` + 正则（`vue-eslint-parser` 模板层），拦截 `▶ ✕ ★ ●` 等符号字符出现在模板文本与 JS 字符串；
2. 代码评审清单项：新增 UI 必须使用 `AppIcon`；
3. 当前代码库已核查**无 Unicode 图标存量**，规则从第一天即可设为 error。

---

## 6. 模块化布局架构（对应需求 5）

### 6.1 布局注册表 + 路由驱动

```js
// layouts/registry.js —— 未来新增布局的唯一扩展点
import { markRaw } from 'vue'
import MainLayout from './MainLayout.vue'
import BlankLayout from './BlankLayout.vue'      // 登录页等全屏场景
export const layoutRegistry = {
  main:  { component: markRaw(MainLayout),  title: '主布局' },
  blank: { component: markRaw(BlankLayout), title: '空白布局' },
  // 未来示例：
  // immersive: { component: markRaw(ImmersiveLayout), title: '沉浸式播放布局' },
  // topnav:    { component: markRaw(TopNavLayout),    title: '顶部导航布局' },
}
```

```js
// 路由声明：布局由 meta 声明，router-view 分层
{ path: '/login', component: () => import('@/views/Login.vue'), meta: { layout: 'blank' } }
{ path: '/media/:id', component: () => import('@/views/Media.vue'), meta: { layout: 'main' } }
```

```vue
<!-- App.vue -->
<template>
  <component :is="layout.component">
    <router-view v-slot="{ Component }">
      <transition name="route" mode="out-in"><component :is="Component" /></transition>
    </router-view>
  </component>
</template>
```

**兼容性承诺**：新增布局 = 新建 `layouts/XxxLayout.vue` + 注册表登记一行 + 路由 `meta` 引用；**不改 App.vue / router 核心 / 任何现有布局代码**。

### 6.2 AppShell 组合式布局壳

将现有 `MainLayout` 的骨架抽为可复用壳，布局差异通过 slot 与子模块组合表达：

```
AppShell（CSS Grid 骨架 + 响应式行为 + 布局状态注入）
├── #sidebar → layouts/modules/Sidebar.vue（导航菜单、折叠、抽屉态）
├── #header  → layouts/modules/Header.vue（页面标题、主题切换、用户菜单）
├── #aside   → （可选）上下文面板，如筛选器
└── default  → 内容区（router-view）
```

- 骨架用 CSS Grid：`grid-template: "sidebar header" 1fr "sidebar content" auto / auto 1fr`；移动端切抽屉；
- `MainLayout = AppShell + Sidebar + Header` 的具名插槽装配；
- 未来 `TopNavLayout` 复用同一批 modules，仅换 Grid 模板——模块资产不重复建设。

### 6.3 布局级样式规范

- 布局尺寸全部令牌化：`--sidebar-width`（256px）/ `--sidebar-width-collapsed`（64px）/ `--header-height`（60px）；
- 内容区滚动容器隔离（`overflow: auto` 限定在 content 区，侧栏/头部固定），避免全局滚动;
- 组件自适应一律容器查询，视口断点只出现在布局层——保证组件在任意布局中表现一致。

---

## 7. 交互体验与动效（对应需求 3）

### 7.1 动效令牌（styles/motion.css）

```css
:root {
  --duration-fast: 150ms;   /* hover、按压、焦点 */
  --duration-base: 250ms;   /* 面板、抽屉、菜单 */
  --duration-slow: 400ms;   /* 路由转场、大区域 */
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);   /* 常规 */
  --ease-emphasized: cubic-bezier(0.3, 0, 0, 1); /* 进入强调 */
  --ease-exit: cubic-bezier(0.4, 0, 1, 1);       /* 退出 */
}
```

原则：所有动效时长/缓动**只引用令牌**（与颜色同等级的纪律）；时长超 400ms 的动效需专门评审。

### 7.2 微交互清单（v1 落地项）

| 场景 | 动效 | 令牌组合 |
|---|---|---|
| 媒体卡片 hover | 上浮 2px + 阴影抬升 + 封面缓慢缩放 1.03 | base / standard |
| 按钮按压 | `scale(0.97)` | fast / standard |
| 侧栏折叠 | 宽度过渡 + 文字淡出淡入 | base / emphasized |
| 列表加载 | Skeleton 骨架屏（柔和呼吸，非旋转 spinner） | base / standard |
| 抽屉/弹层 | 进入强调曲线 + 背景 overlay 渐显 + 玻璃拟态模糊 | slow / emphasized |
| 下拉/悬浮菜单 | 4px 位移 + 渐显（transform+opacity 合成层） | fast / standard |
| 空状态 | 插画式图标轻微浮动 + 引导按钮 | slow / standard |
| 主题切换 | 顶层 View Transition 圆形扩散揭示新主题 | slow / emphasized |

### 7.3 路由转场

- 优先 **View Transitions API**（Chrome/Edge 原生），实现页面间平滑变形（如列表 → 详情的封面连续性）；
- 降级方案：`<Transition name="route" mode="out-in">` 的 fade + 12px 位移（现有骨架已支持，见 6.1）。

### 7.4 无障碍与性能红线

- `@media (prefers-reduced-motion: reduce)`：全部非必要动效归零（透明度过渡保留 ≤100ms）；
- 仅动画 `transform / opacity`（合成层，60fps）；禁止动画 `width/height/top/left`；
- 交互反馈延迟感知红线：hover/press 类反馈 ≤150ms 必须开始。

---

## 8. 后端冗余代码清理（对应需求 6）

### 8.1 现状结论（已实地核查）

- `backend/app/` 为纯 REST API：**无** StaticFiles 挂载、无模板引擎、无 HTMLResponse、无内嵌前端页面代码；
- 因此"过往冗余无用的布局代码"的实际载体为以下三类，清理范围据此界定：

### 8.2 清理范围与动作

| # | 对象 | 动作 | 风险控制 |
|---|---|---|---|
| 1 | `backend/scripts/legacy/`（20+ 一次性迁移脚本，AGENTS.md 已标注禁止运行） | 产出清单 → 评审确认 → **整体目录处置**（删除或移入独立归档仓），同步更新 AGENTS.md 相应条目 | git 历史可回溯；分批（≤10 文件/批）；每批后跑 `pytest` |
| 2 | 为旧 UI 服务的 API 冗余字段 | 对照前端实际消费字段（grep 全部 API 调用点）产出《字段审计表》→ 悬空字段标记 deprecated → 下版本移除 | 兼容期一个版本；字段删除需 schema + 测试同步更新 |
| 3 | 前端侧冗余样式载体 | 合并 `style.scss` / `styles/common.scss` / `styles/immersive.scss` → 令牌体系（第 3 章）；`--imm-*` 别名过渡后删除 | 过渡期别名兼容；stylelint 兜底 |

### 8.3 流程纪律（与仓库规范对齐）

1. 先产出完整删除/变更清单（路径 + 行数 + 理由），**经确认后**执行；
2. 每批次后运行 `cd backend; .\.venv\Scripts\python.exe -m pytest` 全量测试；
3. 涉及 API 面变更时同步检查 `CLAUDE.md` / `docs/`；
4. 提交遵循 `{type}({keyword}):中文摘要}` 规范，清理类使用 `chore(cleanup)` 前缀，一批一提交。

---

## 9. 实施路线图

```
阶段0 基线规范 ──► 阶段1 令牌主题 ──► 阶段2 Tailwind+布局 ──► 阶段3 图标迁移 ──► 阶段4 动效打磨 ──► 阶段6 回归上线
                                                      └──► 阶段5 后端清理（与阶段4并行）──┘
```

| 阶段 | 内容 | 关键产出 | 里程碑验收 |
|---|---|---|---|
| **0 基线与规范**（约 1 周） | 9 个核心页面截图基线归档；引入 stylelint/ESLint 规则（warning 态）；tokens 目录骨架 | lint 体系可运行；基线截图库 | M0：CI 中 lint 步骤就位 |
| **1 令牌与主题系统**（约 2 周） | primitives/semantic/6 主题/EP 桥接；`useTheme` + ThemeSwitcher；`--imm-*` 别名兼容 | 多主题切换可用 | M1：6 主题切换即时生效、持久化、首屏无闪烁 |
| **2 Tailwind + 布局模块化**（约 2 周） | Tailwind v4 集成与 EP 共存调优；AppShell + 注册表 + 路由 meta；响应式改造（侧栏抽屉化等） | 新布局架构 | M2：五档断点走查通过；演示"新增布局零侵入" |
| **3 图标体系迁移**（约 1.5 周） | unplugin-icons + AppIcon + registry；按映射表全量替换；移除旧图标依赖 | 全量 Iconify 图标 | M3：构建产物中无 @element-plus/icons-vue；grep 无 Unicode 图标 |
| **4 动效与交互打磨**（约 1.5 周） | 动效令牌落地；微交互清单逐项实现；路由转场；skeleton/空状态统一 | 动效体系 | M4：动效走查清单通过；reduced-motion 生效 |
| **5 后端清理**（约 1 周，可与 4 并行） | legacy 脚本处置；API 字段审计；前端冗余样式合并 | 清理清单闭环 | M5：pytest 全绿；审计报告归档 |
| **6 回归与上线**（约 0.5 周） | 视觉回归对比基线；性能预算校验；CI 全绿；生产发布 | 验收报告 | M6：第 10 章验收标准全过 |

> 总工作量约 9-10 周（单人全职折算）。阶段 1 完成后即可合入主干（别名机制保证存量页面无损），后续各阶段独立可交付，随时可暂停回滚。

---

## 10. 验收标准（与需求逐条对应）

| # | 需求 | 验收方式 |
|---|---|---|
| 1 | 多主题，含现代黑/现代白 | 设置页主题选择器 ≥6 套；含必备两套；切换即时生效、持久化、跟随系统可选 |
| 2 | CSS/UI/框架/布局/配色现代化 | 三层令牌 + OKLCH；CSS Grid + 容器查询；View Transitions；EP CSS 变量深度主题化 |
| 3 | 交互舒适、动效细腻自然 | 第 7.2 节微交互清单逐项走查；60fps（无 layout 抖动）；`prefers-reduced-motion` 生效 |
| 4 | Iconify SVG 图标，禁 Unicode | 全部图标经 unplugin-icons/lucide；ESLint 拦截规则 error 态；grep 模板/JS 无符号字符图标 |
| 5 | 模块化布局，未来新布局兼容 | 新增演示布局（如 TopNav）仅通过"新文件 + 注册表一行 + meta 引用"完成，核心代码 0 改动 |
| 6 | 清理后端冗余布局代码 | legacy 目录处置完毕；字段审计表归档；每批次后 pytest 全绿 |
| 7 | 颜色禁止硬编码 | stylelint + ESLint 规则 error 态 0 违例（`tokens/primitives.css` 白名单除外） |
| 8 | Tailwind 响应式布局 | 360/768/1024/1440/1920 五档走查；容器查询覆盖媒体网格；触控目标 ≥44px |

---

## 11. 风险与应对

| 风险 | 概率 | 影响 | 应对 |
|---|---|---|---|
| Tailwind preflight 与 Element Plus 样式冲突 | 高 | 中 | 引入顺序 + @layer 控制；受影响组件清单化回归；保留关闭 preflight 的降级开关 |
| EP 深度主题化个别组件粒度不足 | 中 | 中 | --el-* 桥接覆盖 90% 场景；残余用 `:deep()` + 语义令牌定点覆盖 |
| unplugin-icons 动态图标名失控 | 中 | 低 | 注册表白名单机制；缺失即构建警告 |
| 存量硬编码清理量大（约 30+ 处） | 高 | 低 | 阶段 1 别名机制先保运行；lint 分 warning→error 两步走 |
| 视觉回归遗漏 | 中 | 中 | 阶段 0 基线截图 + 逐阶段人工走查 + 验收清单 |
| 后端删除误伤 | 低 | 高 | 清单确认制 + git 可回溯 + 每批 pytest 门禁 + 一批一提交 |
| 动效过度设计 | 中 | 低 | 令牌纪律约束时长；动效清单外不自由发挥 |

---

## 12. 附录

### 12.1 新增依赖清单

| 包 | 用途 |
|---|---|
| `tailwindcss` + `@tailwindcss/vite` | 原子化 CSS（v4） |
| `stylelint` + `stylelint-config-standard-scss` + `stylelint-config-recommended-vue` | 样式门禁 |
| `unplugin-icons` + `@iconify-json/lucide` | Iconify 构建时图标 |
| （可选）`@vueuse/core` | `usePreferredColorScheme` 等组合式工具 |

移除依赖：`@element-plus/icons-vue`（阶段 3 末）。

### 12.2 命令速查

```bash
cd frontend
npm install                       # 安装新依赖
npm run lint                      # ESLint + stylelint（含颜色/图标门禁）
npm run test && npm run build     # 测试与构建
```

### 12.3 与现有规范的衔接

- 本计划不改动 `AGENTS.md` 既定工作流（测试、提交规范、重启验证等）；
- 阶段 5 的后端清理需同步更新 `AGENTS.md` 中 legacy 脚本相关条目；
- 架构层面变更落地时同步修订 `CLAUDE.md` 与 `docs/architecture.md`。
