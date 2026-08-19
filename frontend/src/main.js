import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import App from './App.vue'
import router from './router'

// 设计令牌（顺序即层叠顺序：语义派生 → 主题 → EP 桥接；tokens/index.css 末尾已含 element-bridge）
import './styles/tokens/index.css'
import './styles/tailwind.css'
import './styles/immersive.scss'
import './style.scss'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus, { locale: zhCn })

app.mount('#app')
