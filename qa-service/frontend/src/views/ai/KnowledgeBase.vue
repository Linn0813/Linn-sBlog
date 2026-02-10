<template>
  <div class="knowledge-base-container">
    <!-- 问答区域 -->
    <el-card class="qa-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-content">
            <h1>知识库问答</h1>
            <p class="subtitle">基于博客文章的智能问答系统</p>
          </div>
        </div>
      </template>
      <div class="qa-content">
          <!-- 问题输入 -->
          <div class="question-input">
            <el-input
              v-model="question"
              type="textarea"
              :rows="3"
              placeholder="请输入您的问题..."
              @keydown.ctrl.enter="handleAsk"
              @keydown.meta.enter="handleAsk"
            />
            <div class="input-actions">
              <el-button
                type="primary"
                :loading="asking"
                @click="handleAsk"
                :disabled="!question.trim()"
              >
                {{ asking ? '回答中...' : '提问' }}
              </el-button>
              <el-button @click="clearHistory">清空历史</el-button>
            </div>
          </div>

          <!-- 答案展示 -->
          <div v-if="currentAnswer" class="answer-section">
            <h3>{{ currentAnswer.question_type === 'document_list' ? '相关文档列表' : '答案' }}</h3>
            <div class="answer-content" v-html="formatAnswer(currentAnswer.answer)"></div>
            
            <!-- 文档列表模式提示 -->
            <div v-if="currentAnswer.question_type === 'document_list' && currentAnswer.sources && currentAnswer.sources.length > 0" class="document-list-tip">
              <el-alert
                type="info"
                :closable="false"
                show-icon
              >
                <template #title>
                  <span>找到 {{ currentAnswer.sources.length }} 个相关文档，点击文档标题可查看完整内容</span>
                </template>
              </el-alert>
            </div>

            <!-- 引用来源 / 文档列表 -->
            <div v-if="currentAnswer.sources && currentAnswer.sources.length > 0" class="sources-section">
              <h4>{{ currentAnswer.question_type === 'document_list' ? '文档列表' : '引用来源' }}</h4>
              <ul class="sources-list" :class="{ 'document-list-mode': currentAnswer.question_type === 'document_list' }">
                <li v-for="(source, index) in currentAnswer.sources" :key="index" class="source-item">
                  <a
                    :href="source.url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="source-link"
                  >
                    {{ index + 1 }}. {{ source.title }}
                  </a>
                  <span v-if="source.similarity > 0" class="similarity">
                    {{ currentAnswer.question_type === 'document_list' ? '相关性' : '相似度' }}: {{ (source.similarity * 100).toFixed(1) }}%
                  </span>
                </li>
              </ul>
            </div>
          </div>

          <!-- 历史记录 -->
          <div v-if="history.length > 0" class="history-section">
            <h3>历史记录</h3>
            <div
              v-for="(item, index) in history"
              :key="index"
              class="history-item"
            >
              <div class="history-question">
                <strong>Q:</strong> {{ item.question }}
              </div>
              <div class="history-answer">
                <strong>A:</strong> {{ item.answer }}
              </div>
              <div v-if="item.sources && item.sources.length > 0" class="history-sources">
                <strong>来源:</strong>
                <span
                  v-for="(source, idx) in item.sources"
                  :key="idx"
                  class="source-tag"
                >
                  <a :href="source.url" target="_blank">{{ source.title }}</a>
                </span>
              </div>
            </div>
          </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { aiApi } from '@/apis/ai'

const question = ref('')
const asking = ref(false)
const currentAnswer = ref(null)
const history = ref([])

const handleAsk = async () => {
  if (!question.value.trim()) {
    ElMessage.warning('请输入问题')
    return
  }

  asking.value = true
  const currentQuestion = question.value.trim()

  try {
    // 不限定分类，搜索所有文章
    const response = await aiApi.askQuestion(
      currentQuestion, 
      null,
      false // 不使用网络搜索
    )
    if (response.data && response.data.code === 0) {
      const data = response.data.data
      currentAnswer.value = {
        answer: data.answer,
        sources: data.sources || [],
        max_similarity: data.max_similarity || 0,
        question_type: data.question_type || 'content_qa' // 记录问题类型
      }
      
      // 如果是文档列表查询，显示特殊提示
      if (data.question_type === 'document_list') {
        console.log('文档列表查询模式，找到', data.sources?.length || 0, '个文档')
      }

      // 添加到历史记录
      history.value.unshift({
        question: currentQuestion,
        answer: data.answer,
        sources: data.sources || []
      })

      // 清空问题输入
      question.value = ''
    } else {
      ElMessage.error(response.data?.message || '回答失败')
    }
  } catch (error) {
    console.error('提问失败:', error)
    const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message || '未知错误'
    ElMessage.error('提问失败: ' + errorMsg)
  } finally {
    asking.value = false
  }
}

const clearHistory = () => {
  history.value = []
  currentAnswer.value = null
  ElMessage.success('历史记录已清空')
}

const formatAnswer = (text) => {
  // 简单的Markdown格式化（可以后续增强）
  return text
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
}

</script>

<style scoped>
.knowledge-base-container {
  width: 100%;
  min-height: 100%;
}

.qa-card {
  width: 100%;
  border-radius: 8px;
  border: none !important;
}

.qa-card :deep(.el-card) {
  border: none !important;
}

.qa-card :deep(.el-card__body) {
  border: none;
}

.card-header {
  padding: 0;
}

.header-content {
  text-align: center;
  padding: 8px 0;
}

.header-content h1 {
  font-size: 24px;
  margin: 0 0 8px 0;
  font-weight: 600;
  color: #303133;
}

.subtitle {
  color: #909399;
  font-size: 13px;
  margin: 0;
}

.qa-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 4px 0;
}

.question-input {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.input-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 4px;
}

.answer-section {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}

.answer-section h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.answer-content {
  line-height: 1.8;
  color: #333;
  margin-bottom: 20px;
}

.sources-section {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}

.sources-section h4 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 16px;
}

.sources-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.source-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #e4e7ed;
}

.source-link {
  color: #409eff;
  text-decoration: none;
}

.source-link:hover {
  text-decoration: underline;
}

.similarity {
  color: #909399;
  font-size: 12px;
}

.document-list-mode .source-item {
  padding: 12px 0;
}

.document-list-mode .source-link {
  font-size: 15px;
  font-weight: 500;
}

.document-list-tip {
  margin-top: 15px;
  margin-bottom: 10px;
}

.history-section {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e4e7ed;
}

.history-section h3 {
  margin-bottom: 15px;
  font-size: 18px;
}

.history-item {
  padding: 15px;
  background: #f9f9f9;
  border-radius: 4px;
  margin-bottom: 15px;
}

.history-question {
  margin-bottom: 10px;
  color: #409eff;
}

.history-answer {
  margin-bottom: 10px;
  color: #333;
}

.history-sources {
  font-size: 12px;
  color: #666;
}

.source-tag {
  margin-left: 8px;
}

.source-tag a {
  color: #409eff;
  text-decoration: none;
}

.source-tag a:hover {
  text-decoration: underline;
}
</style>
