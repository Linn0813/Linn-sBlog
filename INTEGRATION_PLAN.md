# 博客与知识库问答系统集成方案

## 项目概况

- **博客项目**：Hexo 静态博客，部署在 GitHub Pages (`https://linn0813.github.io`)
- **问答项目**：前后端分离的知识库问答系统
  - 后端：FastAPI (Python)，默认端口 8113
  - 前端：Vue 3 + Vite + Element Plus，默认端口 3000
  - 大模型：本地部署（Ollama）
  - 向量数据库：ChromaDB

---

## 方案一：独立部署 + 链接跳转（最简单）⭐ 推荐新手

### 架构说明
```
博客 (GitHub Pages)         问答系统 (独立部署)
https://linn0813.github.io  →  https://qa.yourdomain.com
     ↓                              ↓
   静态页面                    前端 + 后端 + 大模型
```

### 实施步骤

#### 1. 部署问答系统后端
```bash
# 在服务器上部署后端（需要能访问本地大模型）
cd /Users/yuxiaoling/PycharmProjects/ai_demo_service/backend

# 安装依赖
pip install -r requirements.txt  # 或根据 pyproject.toml 安装

# 配置环境变量
export AI_DEMO_LLM_BASE_URL=http://localhost:11434
export AI_DEMO_DEFAULT_MODEL=qwen2.5:7b
export FEISHU_APP_ID=your_app_id
export FEISHU_APP_SECRET=your_app_secret
export FEISHU_REDIRECT_URI=https://qa.yourdomain.com/api/v1/feishu/oauth/callback
export FRONTEND_URL=https://qa.yourdomain.com
export AI_DEMO_CORS_ORIGINS=https://qa.yourdomain.com,https://linn0813.github.io

# 启动后端服务
python -m app.main
# 或使用 gunicorn/uvicorn 生产环境部署
```

#### 2. 部署问答系统前端
```bash
cd /Users/yuxiaoling/PycharmProjects/ai_demo_service/frontend

# 配置生产环境 API 地址
# 创建 .env.production 文件
echo "VITE_API_BASE_URL=https://api.yourdomain.com" > .env.production

# 构建前端
npm run build

# 将 dist 目录部署到静态服务器（Nginx、Vercel、Netlify 等）
```

#### 3. 在博客中添加链接
在博客的导航栏或侧边栏添加问答入口链接。

**修改位置**：博客主题配置文件或导航配置

---

### 优点
- ✅ 实施简单，不影响博客现有功能
- ✅ 前后端完全分离，易于维护
- ✅ 可以独立扩展和升级
- ✅ 不影响博客的静态部署

### 缺点
- ❌ 需要单独部署和维护问答系统
- ❌ 需要配置域名和 SSL 证书
- ❌ 跨域配置需要处理

### 适用场景
- 快速上线，不想修改博客结构
- 问答系统需要独立域名
- 希望保持两个项目的独立性

---

## 方案二：博客内嵌问答页面（推荐）⭐⭐⭐

### 架构说明
```
博客 (GitHub Pages)
https://linn0813.github.io
     ├── / (博客首页)
     ├── /qa (问答页面，内嵌 Vue 应用)
     └── 后端 API (独立部署)
         https://api.yourdomain.com
```

### 实施步骤

#### 1. 构建问答前端为静态文件
```bash
cd /Users/yuxiaoling/PycharmProjects/ai_demo_service/frontend

# 配置生产环境 API 地址
cat > .env.production << EOF
VITE_API_BASE_URL=https://api.yourdomain.com
EOF

# 构建前端
npm run build

# 构建后的文件在 dist 目录
```

#### 2. 将前端文件复制到博客项目
```bash
# 复制构建后的文件到博客的 public 目录
cp -r /Users/yuxiaoling/PycharmProjects/ai_demo_service/frontend/dist/* \
      /Users/yuxiaoling/Blog/public/qa/

# 或者创建一个专门的目录
mkdir -p /Users/yuxiaoling/Blog/public/qa
cp -r /Users/yuxiaoling/PycharmProjects/ai_demo_service/frontend/dist/* \
      /Users/yuxiaoling/Blog/public/qa/
```

#### 3. 创建博客页面入口
在博客的 `source` 目录创建问答页面：

```markdown
# source/qa/index.md
---
title: 知识库问答
date: 2025-01-01
layout: page
---

<div id="qa-app"></div>
<script type="module" src="/qa/assets/index.js"></script>
```

#### 4. 配置博客路由
在 Hexo 配置中确保 `/qa` 路径可以正常访问。

#### 5. 部署后端（同方案一）
后端需要独立部署，配置 CORS 允许博客域名访问。

---

### 优点
- ✅ 统一入口，用户体验好
- ✅ 不需要单独域名
- ✅ SEO 友好（可以添加页面描述）
- ✅ 博客和问答系统在同一域名下

### 缺点
- ❌ 需要修改博客配置
- ❌ 每次更新问答前端需要重新构建和部署博客
- ❌ 需要处理路由冲突（如果问答系统使用 Vue Router）

### 适用场景
- 希望统一用户体验
- 问答系统更新频率不高
- 希望保持博客和问答系统的紧密集成

---

## 方案三：子路径部署 + 自动化集成（最完善）⭐⭐

### 架构说明
```
博客 (GitHub Pages)
https://linn0813.github.io
     ├── / (博客首页)
     ├── /qa (问答页面，通过脚本自动集成)
     └── 后端 API (独立部署)
         https://api.yourdomain.com
```

### 实施步骤

#### 1. 创建自动化集成脚本
创建一个脚本，自动将问答前端集成到博客中。

#### 2. 配置 Hexo 部署流程
在博客的部署脚本中集成问答系统的构建和部署。

#### 3. 处理路由问题
由于 GitHub Pages 是静态托管，需要处理 Vue Router 的 history 模式问题。

---

### 优点
- ✅ 自动化程度高
- ✅ 统一域名和用户体验
- ✅ 可以自动化部署流程

### 缺点
- ❌ 实施复杂度较高
- ❌ 需要处理路由和构建问题
- ❌ 调试相对复杂

---

## 推荐方案对比

| 方案 | 实施难度 | 用户体验 | 维护成本 | 推荐指数 |
|------|---------|---------|---------|---------|
| 方案一：独立部署 | ⭐ 简单 | ⭐⭐ 一般 | ⭐⭐ 中等 | ⭐⭐⭐ |
| 方案二：博客内嵌 | ⭐⭐ 中等 | ⭐⭐⭐ 优秀 | ⭐⭐ 中等 | ⭐⭐⭐⭐⭐ |
| 方案三：自动化集成 | ⭐⭐⭐ 复杂 | ⭐⭐⭐ 优秀 | ⭐ 低 | ⭐⭐⭐⭐ |

---

## 详细实施指南（方案二）

### 步骤 1：配置问答前端构建

创建生产环境配置文件：

```bash
cd /Users/yuxiaoling/PycharmProjects/ai_demo_service/frontend
cat > .env.production << EOF
VITE_API_BASE_URL=https://api.yourdomain.com
EOF
```

### 步骤 2：修改 Vite 配置以支持子路径部署

修改 `vite.config.js`：

```javascript
export default defineConfig({
  plugins: [vue()],
  base: '/qa/',  // 添加这行，设置基础路径
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  // ... 其他配置
})
```

### 步骤 3：修改 Vue Router 配置

如果使用 Vue Router，需要配置 base：

```javascript
const router = createRouter({
  history: createWebHistory('/qa/'),  // 设置基础路径
  routes: [...]
})
```

### 步骤 4：创建博客页面入口

在博客的 `source/qa/index.md`：

```markdown
---
title: 知识库问答
date: 2025-01-01
layout: page
permalink: /qa/
---

<div id="app"></div>
<link rel="stylesheet" href="/qa/assets/index.css">
<script type="module" src="/qa/assets/index.js"></script>
```

### 步骤 5：自动化部署脚本

创建部署脚本 `scripts/deploy-qa.sh`：

```bash
#!/bin/bash
# 构建问答前端
cd /Users/yuxiaoling/PycharmProjects/ai_demo_service/frontend
npm run build

# 复制到博客目录
rm -rf /Users/yuxiaoling/Blog/public/qa
mkdir -p /Users/yuxiaoling/Blog/public/qa
cp -r dist/* /Users/yuxiaoling/Blog/public/qa/

# 部署博客（如果需要）
cd /Users/yuxiaoling/Blog
hexo generate
hexo deploy
```

### 步骤 6：配置后端 CORS

确保后端允许博客域名访问：

```python
# backend/app/main.py
cors_origins = [
    "https://linn0813.github.io",
    "https://qa.yourdomain.com",  # 如果有独立域名
    "http://localhost:4000",  # 本地开发
]
```

---

## 后端部署建议

### 使用 Docker 部署（推荐）

创建 `Dockerfile`：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装依赖
COPY backend/pyproject.toml .
RUN pip install --no-cache-dir -e .

# 复制代码
COPY backend/ .

# 暴露端口
EXPOSE 8113

# 启动命令
CMD ["python", "-m", "app.main"]
```

### 使用 systemd 服务（Linux）

创建 `/etc/systemd/system/qa-service.service`：

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
ExecStart=/usr/bin/python3 -m app.main
Restart=always

[Install]
WantedBy=multi-user.target
```

### 使用 Nginx 反向代理

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
    }
}
```

---

## 注意事项

### 1. CORS 配置
确保后端正确配置 CORS，允许博客域名访问。

### 2. 路由处理
GitHub Pages 不支持服务端路由，如果使用 Vue Router 的 history 模式，需要：
- 使用 hash 模式，或
- 配置 404.html 重定向

### 3. 环境变量
生产环境需要正确配置：
- 后端 API 地址
- 飞书 OAuth 回调地址
- CORS 允许的域名

### 4. SSL 证书
如果使用独立域名，需要配置 SSL 证书（Let's Encrypt 免费）。

### 5. 大模型访问
确保后端服务器可以访问本地部署的大模型（Ollama）。

---

## 快速开始（方案二）

1. **构建问答前端**：
```bash
cd /Users/yuxiaoling/PycharmProjects/ai_demo_service/frontend
npm run build
```

2. **复制到博客**：
```bash
cp -r dist/* /Users/yuxiaoling/Blog/public/qa/
```

3. **创建博客页面**：
在 `source/qa/index.md` 创建入口页面

4. **部署后端**：
按照上述后端部署建议部署后端服务

5. **生成和部署博客**：
```bash
cd /Users/yuxiaoling/Blog
hexo generate
hexo deploy
```

---

## 后续优化建议

1. **自动化部署**：使用 GitHub Actions 自动化构建和部署流程
2. **CDN 加速**：将静态资源部署到 CDN
3. **监控和日志**：添加后端服务的监控和日志
4. **缓存优化**：优化向量数据库查询性能
5. **用户体验**：添加加载动画和错误提示

---

## 需要帮助？

如果在实施过程中遇到问题，可以：
1. 检查后端日志
2. 检查浏览器控制台错误
3. 验证 CORS 配置
4. 确认 API 地址配置正确

