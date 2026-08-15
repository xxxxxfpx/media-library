# 媒体库管理系统 - Vue 3 前端

## 技术栈

- Vue 3 (Composition API)
- Vue Router 4
- Pinia (状态管理)
- Element Plus (UI 组件库)
- Axios (HTTP 客户端)
- Vite (构建工具)
- Sass (CSS 预处理器)

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

前端将在 http://localhost:3000 启动，并自动代理 API 请求到后端 http://localhost:8000

### 3. 构建生产版本

```bash
npm run build
```

构建产物将输出到 `dist` 目录

## 项目结构

```
frontend/
├── index.html          # HTML 入口
├── package.json        # 项目配置
├── vite.config.js     # Vite 配置
└── src/
    ├── main.js         # Vue 应用入口
    ├── App.vue         # 根组件
    ├── style.scss      # 全局样式
    ├── api/            # API 接口
    │   └── index.js
    ├── components/      # 公共组件
    │   └── MediaCard.vue
    ├── router/         # 路由配置
    │   └── index.js
    ├── store/          # 状态管理
    │   └── index.js
    └── views/          # 页面组件
        ├── Login.vue
        ├── Home.vue
        ├── Library.vue
        ├── Favorites.vue
        ├── History.vue
        ├── Settings.vue
        └── System.vue
```

## 功能特性

- ✅ 用户登录/登出
- ✅ 媒体库浏览（支持分页、筛选）
- ✅ 收藏管理
- ✅ 观看记录
- ✅ 个人设置
- ✅ 系统监控
- ✅ 主题切换（深色/浅色）
- ✅ 响应式布局

## API 代理

开发环境下，Vite 会将 `/api` 请求代理到后端服务器。

如果后端运行在不同端口，请修改 `vite.config.js` 中的 `proxy.target`。

## 注意事项

1. 确保后端服务器已启动（http://localhost:8000）
2. 首次登录使用默认账户: `admin` / `admin123`
3. Token 会自动存储在 localStorage 中
