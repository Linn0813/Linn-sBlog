# 问答系统环境变量配置说明

## 前端环境变量配置

在问答前端项目的 `frontend/.env.production` 文件中配置：

```bash
# 后端 API 地址（生产环境）
# 请根据实际后端部署地址修改
VITE_API_BASE_URL=https://api.yourdomain.com

# 或者如果后端和前端在同一域名下，可以使用相对路径
# VITE_API_BASE_URL=
```

## 后端环境变量配置

在问答后端项目的环境变量或 `.env` 文件中配置：

```bash
# LLM 配置（本地部署的 Ollama）
AI_DEMO_LLM_BASE_URL=http://localhost:11434
AI_DEMO_DEFAULT_MODEL=qwen2.5:7b

# 后端服务配置
AI_DEMO_BACKEND_HOST=0.0.0.0
AI_DEMO_BACKEND_PORT=8113

# CORS 配置（重要！必须包含博客域名）
AI_DEMO_CORS_ORIGINS=https://linn0813.github.io,https://api.yourdomain.com

# 飞书应用配置
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
FEISHU_REDIRECT_URI=https://api.yourdomain.com/api/v1/feishu/oauth/callback

# 前端地址（用于 OAuth 回调）
FRONTEND_URL=https://linn0813.github.io
```

## 配置步骤

1. **配置前端 API 地址**
   ```bash
   cd /Users/yuxiaoling/PycharmProjects/ai_demo_service/frontend
   # 编辑 .env.production 文件，设置后端 API 地址
   ```

2. **配置后端 CORS**
   ```bash
   cd /Users/yuxiaoling/PycharmProjects/ai_demo_service/backend
   # 设置环境变量或创建 .env 文件
   export AI_DEMO_CORS_ORIGINS=https://linn0813.github.io
   ```

3. **启动后端服务**
   ```bash
   cd /Users/yuxiaoling/PycharmProjects/ai_demo_service/backend
   python -m app.main
   ```

4. **构建并集成前端**
   ```bash
   cd /Users/yuxiaoling/Blog
   ./scripts/integrate-qa.sh
   ```

5. **生成并部署博客**
   ```bash
   cd /Users/yuxiaoling/Blog
   hexo generate
   hexo deploy
   ```

## 注意事项

- **CORS 配置**：后端必须正确配置 CORS，允许博客域名访问
- **API 地址**：确保前端配置的 API 地址可以正常访问
- **OAuth 回调**：飞书 OAuth 回调地址需要配置为后端地址
- **HTTPS**：生产环境建议使用 HTTPS，需要配置 SSL 证书

