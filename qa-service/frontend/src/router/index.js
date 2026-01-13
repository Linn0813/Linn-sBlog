import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/knowledge-base'  // 默认跳转到知识库问答
  },
  {
    path: '/knowledge-base',
    name: 'KnowledgeBase',
    component: () => import('../views/ai/KnowledgeBase.vue'),
    meta: { title: '知识库问答' }
  }
]

// 根据环境设置基础路径：生产环境使用 /qa，开发环境使用 /
const basePath = import.meta.env.PROD ? '/qa' : ''

const router = createRouter({
  history: createWebHistory(basePath),
  routes
})

export default router
