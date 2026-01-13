# 知识库问答服务

这个目录包含了知识库问答系统的完整代码，现在统一在博客项目中管理。

## 📁 目录结构

```
qa-service/
├── backend/          # 后端代码（Python FastAPI）
│   ├── app/         # 应用入口
│   ├── api/         # API 路由
│   ├── domain/      # 业务逻辑
│   ├── infrastructure/  # 基础设施（LLM、向量数据库等）
│   └── ...
├── frontend/         # 前端代码（Vue 3 + Vite）
│   ├── src/         # 源代码
│   └── ...
├── storage/         # 存储目录（向量数据库、上传文件等）
├── data/           # 数据目录
└── ...
```

## 🚀 快速开始

### 安装依赖

**后端：**
```bash
cd backend
pip install -e .
# 或
pip install -r requirements.txt  # 如果有 requirements.txt
```

**前端：**
```bash
cd frontend
npm install
```

### 配置环境变量

**后端：**
创建 `backend/.env` 文件：
```bash
AI_DEMO_LLM_BASE_URL=http://localhost:11434
AI_DEMO_DEFAULT_MODEL=qwen2.5:7b
AI_DEMO_CORS_ORIGINS=https://linn0813.github.io,http://localhost:4000
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
FEISHU_REDIRECT_URI=http://localhost:8113/api/v1/feishu/oauth/callback
FRONTEND_URL=http://localhost:4000
```

**前端：**
创建 `frontend/.env.production` 文件：
```bash
VITE_API_BASE_URL=http://localhost:8113
```

### 启动服务

**后端：**
```bash
cd backend
python -m app.main
```

**前端（开发模式）：**
```bash
cd frontend
npm run dev
```

**前端（生产构建）：**
```bash
cd frontend
npm run build
```

## 🔧 集成到博客

使用集成脚本将前端构建并集成到博客：

```bash
cd /Users/yuxiaoling/Blog
./scripts/integrate-qa.sh
```

脚本会自动：
1. 构建前端代码
2. 将构建文件复制到 `public/qa/` 目录
3. 准备博客部署

## 📝 相关文档

- [迁移说明](./MIGRATION.md) - 了解如何迁移到博客项目
- [集成指南](../QA_INTEGRATION_GUIDE.md) - 详细的集成步骤
- [完整方案文档](../INTEGRATION_PLAN.md) - 所有集成方案对比
- [环境变量配置](../scripts/qa-env-example.md) - 环境变量详细说明

## ⚠️ 注意事项

1. **环境变量**：`.env` 文件不会被提交到 Git，需要单独配置
2. **存储目录**：`storage/` 和 `data/` 目录中的文件不会被提交
3. **依赖文件**：`node_modules/` 和 `__pycache__/` 等不会被提交
4. **Git 管理**：现在所有代码都在博客项目的 Git 仓库中统一管理

## 🔄 项目历史

本项目使用 `git subtree` 从原始项目位置合并而来，保留了完整的提交历史。
