import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import router from './router'
import App from './App.vue'

// 等待 DOM 加载完成
function initApp() {
  const appElement = document.getElementById('app')
  if (!appElement) {
    console.error('找不到 #app 元素，无法挂载 Vue 应用')
    return
  }

  const app = createApp(App)

  // 注册所有图标
  for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }

  app.use(ElementPlus)
  app.use(router)
  app.mount('#app')
  
  console.log('Vue 应用已成功挂载')
}

// 如果 DOM 已经加载完成，立即初始化；否则等待 DOMContentLoaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp)
} else {
  initApp()
}
