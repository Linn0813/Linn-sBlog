import { createRouter, createWebHistory } from 'vue-router'
import AiModule from '../views/ai/AiModule.vue'

const routes = [
  {
    path: '/',
    redirect: '/ai/knowledge-base'  // 默认跳转到知识库问答
  },
  {
    path: '/ai',
    component: AiModule,
    children: [
      { path: '', redirect: '/ai/knowledge-base' },  // 默认显示知识库问答
      {
        path: 'test-case-generator',
        name: 'AITestCaseGenerate',
        component: () => import('../views/ai/AITestCaseGenerate.vue'),
        meta: { title: 'AI测试用例生成' }
      },
      {
        path: 'knowledge-base',
        name: 'KnowledgeBase',
        component: () => import('../views/ai/KnowledgeBase.vue'),
        meta: { title: '知识库问答' }
      }
    ]
  }
]

// 根据环境设置基础路径：生产环境使用 /qa，开发环境使用 /
const basePath = import.meta.env.PROD ? '/qa' : ''

const router = createRouter({
  history: createWebHistory(basePath),
  routes
})

export default router
