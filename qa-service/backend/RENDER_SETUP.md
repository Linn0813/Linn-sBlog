# Render 部署配置说明

## 环境变量配置

在 Render Dashboard 中，为你的 Web Service 设置以下环境变量：

### 必需的环境变量

1. **Embedding 服务配置**（必须设置，否则会尝试连接本地 Ollama）
   ```
   AI_DEMO_EMBEDDING_PROVIDER=sentence-transformers
   ```

2. **LLM 服务配置**（使用 Groq API）
   ```
   AI_DEMO_LLM_PROVIDER=openai
   AI_DEMO_LLM_BASE_URL=https://api.groq.com/openai/v1
   AI_DEMO_LLM_API_KEY=your-groq-api-key-here
   AI_DEMO_DEFAULT_MODEL=llama-3.1-70b-versatile
   ```

3. **CORS 配置**（允许博客域名访问）
   ```
   AI_DEMO_CORS_ORIGINS=https://linn0813.github.io
   ```

### 可选的环境变量

- `AI_DEMO_EMBEDDING_MODEL`: Embedding 模型名称（默认：`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`）
- `AI_DEMO_EMBEDDING_DEVICE`: 运行设备（默认：`cpu`）
- `AI_DEMO_EMBEDDING_BATCH_SIZE`: 批量处理大小（默认：`32`）

## 构建命令

在 Render Dashboard 的 "Build Command" 中设置：

```bash
pip install -e ".[embedding]"
```

这会安装 `sentence-transformers` 作为可选依赖。

## 启动命令

在 Render Dashboard 的 "Start Command" 中设置：

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 注意事项

1. **首次启动时间**：首次启动时，`sentence-transformers` 会从 HuggingFace 下载模型（约 471MB），可能需要几分钟时间。

2. **内存使用**：`sentence-transformers` 模型会占用一定内存，确保 Render 实例有足够的内存。

3. **同步博客文章**：部署完成后，需要手动同步博客文章：
   ```bash
   QA_BACKEND_URL=https://linn-sblog.onrender.com npm run sync-blog
   ```
