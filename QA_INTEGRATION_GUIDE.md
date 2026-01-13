# 知识库问答系统集成指南（方案二）

## 📋 概述

本指南将帮助你将知识库问答系统集成到 Hexo 博客中，使用方案二（博客内嵌问答页面）。

## 🚀 快速开始

### 1. 配置后端 API 地址

编辑问答前端的生产环境配置文件：

```bash
cd /Users/yuxiaoling/PycharmProjects/ai_demo_service/frontend
nano .env.production
```

设置后端 API 地址：

```bash
# 根据实际后端部署地址修改
VITE_API_BASE_URL=https://api.yourdomain.com
# 或者本地测试
# VITE_API_BASE_URL=http://localhost:8113
```

### 2. 配置后端 CORS

确保后端允许博客域名访问。设置环境变量：

```bash
export AI_DEMO_CORS_ORIGINS=https://linn0813.github.io,http://localhost:4000
```

或者在 `.env` 文件中配置：

```bash
AI_DEMO_CORS_ORIGINS=https://linn0813.github.io,http://localhost:4000
```

### 3. 运行集成脚本

```bash
cd /Users/yuxiaoling/Blog
./scripts/integrate-qa.sh
```

这个脚本会：
- ✅ 构建问答前端
- ✅ 将构建文件复制到博客的 `public/qa/` 目录
- ✅ 创建博客页面入口（如果不存在）

### 4. 生成并部署博客

```bash
cd /Users/yuxiaoling/Blog
hexo generate
hexo deploy
```

## 📝 详细步骤

### 步骤 1：修改前端配置

前端配置已经自动修改完成：
- ✅ `vite.config.js` - 已设置 `base: '/qa/'`
- ✅ `src/router/index.js` - 已设置路由基础路径

### 步骤 2：配置后端服务

#### 启动后端服务

```bash
cd /Users/yuxiaoling/PycharmProjects/ai_demo_service/backend

# 安装依赖（如果还没安装）
pip install -e .

# 设置环境变量
export AI_DEMO_LLM_BASE_URL=http://localhost:11434
export AI_DEMO_DEFAULT_MODEL=qwen2.5:7b
export AI_DEMO_CORS_ORIGINS=https://linn0813.github.io,http://localhost:4000
export FEISHU_REDIRECT_URI=https://api.yourdomain.com/api/v1/feishu/oauth/callback
export FRONTEND_URL=https://linn0813.github.io

# 启动服务
python -m app.main
```

#### 使用 systemd 服务（Linux 服务器）

创建服务文件 `/etc/systemd/system/qa-service.service`：

```ini
[Unit]
Description=Knowledge Base QA Service
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/ai_demo_service/backend
Environment="AI_DEMO_LLM_BASE_URL=http://localhost:11434"
Environment="AI_DEMO_DEFAULT_MODEL=qwen2.5:7b"
Environment="AI_DEMO_CORS_ORIGINS=https://linn0813.github.io"
Environment="FEISHU_REDIRECT_URI=https://api.yourdomain.com/api/v1/feishu/oauth/callback"
Environment="FRONTEND_URL=https://linn0813.github.io"
ExecStart=/usr/bin/python3 -m app.main
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl enable qa-service
sudo systemctl start qa-service
```

### 步骤 3：使用 Nginx 反向代理（可选）

如果后端部署在服务器上，可以使用 Nginx 反向代理：

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8113;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 支持 WebSocket（如果需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 步骤 4：本地测试

1. **启动后端服务**（确保可以访问本地大模型）
2. **启动博客本地服务器**：
   ```bash
   cd /Users/yuxiaoling/Blog
   hexo server
   ```
3. **访问问答页面**：
   ```
   http://localhost:4000/qa/
   ```

## 🔧 常见问题

### 1. CORS 错误

**问题**：浏览器控制台显示 CORS 错误

**解决**：
- 检查后端 `AI_DEMO_CORS_ORIGINS` 环境变量是否包含博客域名
- 确保后端服务正在运行
- 检查 API 地址是否正确

### 2. 404 错误

**问题**：访问 `/qa/` 时显示 404

**解决**：
- 确保已运行 `hexo generate` 生成静态文件
- 检查 `public/qa/` 目录是否存在且包含文件
- 检查 `source/qa/index.md` 文件是否存在

### 3. 资源加载失败

**问题**：CSS 或 JS 文件加载失败

**解决**：
- 检查构建后的文件路径是否正确
- 确保 `vite.config.js` 中设置了 `base: '/qa/'`
- 检查浏览器控制台的错误信息

### 4. 路由跳转问题

**问题**：点击问答系统内的链接后页面空白

**解决**：
- 确保 `router/index.js` 中设置了正确的基础路径
- 检查 Vue Router 是否使用 `createWebHistory('/qa')`

### 5. API 请求失败

**问题**：无法连接到后端 API

**解决**：
- 检查 `.env.production` 中的 `VITE_API_BASE_URL` 是否正确
- 确保后端服务正在运行
- 检查网络连接和防火墙设置

## 📦 文件结构

集成后的文件结构：

```
Blog/
├── public/
│   └── qa/                    # 问答前端构建文件
│       ├── index.html
│       ├── assets/
│       └── ...
├── source/
│   └── qa/
│       └── index.md           # 问答页面入口
├── scripts/
│   └── integrate-qa.sh        # 集成脚本
└── _config.butterfly.yml      # 导航菜单配置（已添加问答入口）
```

## 🔄 更新流程

当问答系统有更新时：

1. **更新问答前端代码**
2. **运行集成脚本**：
   ```bash
   ./scripts/integrate-qa.sh
   ```
3. **重新生成博客**：
   ```bash
   hexo generate
   hexo deploy
   ```

## 📚 相关文档

- [完整集成方案文档](./INTEGRATION_PLAN.md)
- [环境变量配置说明](./scripts/qa-env-example.md)

## 🆘 需要帮助？

如果遇到问题：

1. 检查后端日志
2. 检查浏览器控制台错误
3. 验证环境变量配置
4. 确认所有服务都在运行

---

**提示**：首次部署建议先在本地测试，确认一切正常后再部署到生产环境。

