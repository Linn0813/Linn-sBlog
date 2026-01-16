<template>
  <div class="knowledge-base-container">
    <div class="header">
      <h1>知识库问答</h1>
      <p class="subtitle">基于博客文章的智能问答系统</p>
    </div>

    <div class="content">
      <!-- 问答区域 -->
      <el-card class="qa-card" shadow="hover">
        <template #header>
          <div class="card-header">
          <span>智能问答</span>
          </div>
        </template>
        <div class="qa-content">
          <!-- 博客分类选择 -->
          <div class="space-selector" style="margin-bottom: 15px;">
            <el-select
              v-model="selectedCategory"
              placeholder="选择博客分类（不选择则搜索所有文章）"
              clearable
              style="width: 100%"
              :loading="loadingCategories"
            >
              <el-option
                v-for="category in categories"
                :key="category.space_id"
                :label="category.name"
                :value="category.space_id"
              >
                <span>{{ category.name }}</span>
                <span v-if="category.description" style="color: #8492a6; font-size: 12px; margin-left: 10px;">
                  {{ category.description }}
                </span>
              </el-option>
            </el-select>
          </div>

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
            <!-- 网络搜索选项 -->
            <div class="web-search-option">
              <el-checkbox v-model="useWebSearch">
                <span>🌐 启用网络搜索</span>
                <el-tooltip content="当知识库结果不理想时，自动使用网络搜索补充信息" placement="top">
                  <span style="margin-left: 5px; color: #909399; cursor: help;">❓</span>
                </el-tooltip>
              </el-checkbox>
            </div>
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

            <!-- 网络搜索建议按钮 -->
            <div v-if="currentAnswer.suggest_web_search && !currentAnswer.has_web_search && currentAnswer.sources && currentAnswer.sources.length > 0" class="web-search-suggestion">
              <el-alert
                type="warning"
                :closable="false"
                show-icon
              >
                <template #title>
                  <div class="suggestion-content">
                    <p v-if="currentAnswer.max_similarity < 0.5">
                      💡 知识库文档相似度较低（{{ (currentAnswer.max_similarity * 100).toFixed(1) }}%），建议使用网络搜索获取更多信息
                    </p>
                    <p v-else-if="currentAnswer.max_similarity < 0.7">
                      💡 知识库文档相似度中等（{{ (currentAnswer.max_similarity * 100).toFixed(1) }}%），如需更详细的信息，建议使用网络搜索补充
                    </p>
                    <p v-else>
                      💡 如需更详细的信息，建议使用网络搜索补充
                    </p>
                    <el-button
                      type="primary"
                      size="small"
                      :loading="asking"
                      @click="searchWithWeb"
                      style="margin-top: 10px;"
                    >
                      🌐 使用网络搜索
                    </el-button>
                  </div>
                </template>
              </el-alert>
            </div>

            <!-- 已使用网络搜索提示 -->
            <div v-if="currentAnswer.has_web_search" class="web-search-used">
              <el-tag type="success" size="small">
                ✓ 已使用网络搜索补充信息
              </el-tag>
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
                  <span v-else-if="source.source === 'web_search'" class="web-source">🌐 网络搜索</span>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { aiApi } from '@/apis/ai'

const question = ref('')
const asking = ref(false)
const currentAnswer = ref(null)
const history = ref([])
const categories = ref([]) // 博客分类列表
const selectedCategory = ref(null) // 选中的博客分类
const loadingCategories = ref(false) // 加载分类列表状态
const useWebSearch = ref(false) // 是否启用网络搜索
const lastQuestion = ref('') // 保存上次的问题，用于网络搜索

const handleAsk = async () => {
  if (!question.value.trim()) {
    ElMessage.warning('请输入问题')
    return
  }

  asking.value = true
  const currentQuestion = question.value.trim()
  lastQuestion.value = currentQuestion // 保存问题，用于网络搜索

  try {
    // 传递选中的分类和网络搜索选项
    const response = await aiApi.askQuestion(
      currentQuestion, 
      selectedCategory.value || null,
      useWebSearch.value
    )
    if (response.data && response.data.code === 0) {
      const data = response.data.data
      currentAnswer.value = {
        answer: data.answer,
        sources: data.sources || [],
        suggest_web_search: data.suggest_web_search || false,
        has_web_search: data.has_web_search || false,
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
        sources: data.sources || [],
        has_web_search: data.has_web_search || false
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

// 使用网络搜索
const searchWithWeb = async () => {
  if (!lastQuestion.value.trim()) {
    ElMessage.warning('没有可搜索的问题')
    return
  }

  asking.value = true
  try {
    // 使用相同的问题，但启用网络搜索
    const response = await aiApi.askQuestion(
      lastQuestion.value,
      selectedCategory.value || null,
      true // 启用网络搜索
    )
    if (response.data && response.data.code === 0) {
      const data = response.data.data
      currentAnswer.value = {
        answer: data.answer,
        sources: data.sources || [],
        suggest_web_search: false, // 已经使用了，不再建议
        has_web_search: data.has_web_search || false,
        max_similarity: data.max_similarity || 0
      }

      // 更新历史记录中的最后一条
      if (history.value.length > 0 && history.value[0].question === lastQuestion.value) {
        history.value[0] = {
          question: lastQuestion.value,
          answer: data.answer,
          sources: data.sources || [],
          has_web_search: true
        }
      }

      ElMessage.success('已使用网络搜索补充信息')
    } else {
      ElMessage.error(response.data?.message || '网络搜索失败')
    }
  } catch (error) {
    console.error('网络搜索失败:', error)
    ElMessage.error('网络搜索失败: ' + (error.message || '未知错误'))
  } finally {
    asking.value = false
  }
}

// 加载博客分类列表
const loadCategories = async () => {
  loadingCategories.value = true
  try {
    const response = await aiApi.getWikiSpaces()
    if (response.data && response.data.code === 0) {
      const data = response.data.data
      if (data.success && data.spaces) {
        categories.value = data.spaces
      } else {
        ElMessage.warning(data.message || '获取分类列表失败')
      }
    } else {
      const errorMsg = response.data?.message || response.data?.detail || '获取分类列表失败'
        ElMessage.error(errorMsg)
    }
  } catch (error) {
    console.error('加载分类列表失败:', error)
    const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message || '未知错误'
    ElMessage.error('加载分类列表失败: ' + errorMsg)
  } finally {
    loadingCategories.value = false
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

onMounted(async () => {
  // 加载博客分类列表
  await loadCategories()
})
</script>

<style scoped>
.knowledge-base-container {
  width: 100%;
  height: 100vh;
  margin: 0;
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 28px;
  margin-bottom: 10px;
}

.subtitle {
  color: #666;
  font-size: 14px;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.qa-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.qa-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-input {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.web-search-option {
  display: flex;
  align-items: center;
  padding: 8px 0;
}

.web-search-suggestion {
  margin-top: 20px;
}

.suggestion-content {
  display: flex;
  flex-direction: column;
}

.suggestion-content p {
  margin: 0;
  font-size: 14px;
}

.web-search-used {
  margin-top: 15px;
  margin-bottom: 10px;
}

.web-source {
  color: #67c23a;
  font-size: 12px;
  font-weight: 500;
}

.input-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.answer-section {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.answer-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
}

.answer-content {
  line-height: 1.8;
  color: #333;
  margin-bottom: 20px;
}

.sources-section {
  margin-top: 20px;
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
  margin-top: 30px;
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
