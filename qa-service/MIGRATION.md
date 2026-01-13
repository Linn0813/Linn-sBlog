# 问答项目迁移说明

## 📦 迁移完成

问答项目（`ai-demo-service`）已经成功合并到博客项目中，现在统一在博客仓库中管理。

## 🔄 迁移方式

使用 `git subtree` 将问答项目的完整历史合并到博客项目中：

```bash
git subtree add --prefix=qa-service --squash /path/to/ai_demo_service main
```

## 📁 目录结构

```
Blog/
└── qa-service/
    ├── backend/          # 后端代码（Python FastAPI）
    ├── frontend/         # 前端代码（Vue 3 + Vite）
    ├── storage/          # 存储目录（向量数据库、上传文件等）
    ├── data/            # 数据目录
    └── ...              # 其他项目文件
```

## 🚀 使用方式

### 开发环境

所有开发工作现在都在博客项目中：

```bash
# 启动后端
cd qa-service/backend
python -m app.main

# 启动前端（新终端）
cd qa-service/frontend
npm run dev
```

### 集成到博客

使用集成脚本：

```bash
cd /Users/yuxiaoling/Blog
./scripts/integrate-qa.sh
```

## 📝 后续更新

如果需要从原始项目位置同步更新（如果还有修改）：

```bash
cd /Users/yuxiaoling/Blog
git subtree pull --prefix=qa-service --squash /Users/yuxiaoling/PycharmProjects/ai_demo_service main
```

**注意**：建议后续所有修改都在博客项目的 `qa-service` 目录中进行，不再使用原始项目位置。

## 🗑️ 清理原始项目（可选）

如果确认不再需要原始项目位置，可以：

1. **备份**（如果需要）：
   ```bash
   cp -r /Users/yuxiaoling/PycharmProjects/ai_demo_service /path/to/backup/
   ```

2. **删除原始项目**：
   ```bash
   rm -rf /Users/yuxiaoling/PycharmProjects/ai_demo_service
   ```

## ⚠️ 注意事项

1. **环境变量**：`.env` 文件已被 `.gitignore` 忽略，需要单独配置
2. **依赖安装**：首次使用需要安装依赖
   - 后端：`pip install -e qa-service/backend`
   - 前端：`cd qa-service/frontend && npm install`
3. **存储目录**：`storage/` 和 `data/` 目录中的文件不会被提交到 Git

## 🔗 相关文档

- [集成指南](../QA_INTEGRATION_GUIDE.md)
- [完整方案文档](../INTEGRATION_PLAN.md)
- [环境变量配置](../scripts/qa-env-example.md)

