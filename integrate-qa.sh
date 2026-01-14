#!/bin/bash

# 博客与问答系统集成脚本
# 用途：将问答前端构建并集成到博客项目中

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置路径
BLOG_DIR="/Users/yuxiaoling/Blog"
QA_FRONTEND_DIR="${BLOG_DIR}/qa-service/frontend"
QA_TARGET_DIR="${BLOG_DIR}/public/qa"

# 可选配置
# AUTO_SYNC_BLOG: 是否在集成时自动同步博客文章（默认 false）
# QA_BACKEND_URL: 后端服务地址（默认 http://localhost:8113）
AUTO_SYNC_BLOG="${AUTO_SYNC_BLOG:-false}"
QA_BACKEND_URL="${QA_BACKEND_URL:-http://localhost:8113}"

echo -e "${GREEN}开始集成问答系统到博客...${NC}"

# 1. 检查问答项目目录是否存在
if [ ! -d "$QA_FRONTEND_DIR" ]; then
    echo -e "${RED}错误：问答前端目录不存在: $QA_FRONTEND_DIR${NC}"
    exit 1
fi

# 2. 检查博客目录是否存在
if [ ! -d "$BLOG_DIR" ]; then
    echo -e "${RED}错误：博客目录不存在: $BLOG_DIR${NC}"
    exit 1
fi

# 3. 进入问答前端目录
echo -e "${YELLOW}进入问答前端目录...${NC}"
cd "$QA_FRONTEND_DIR"

# 4. 检查 node_modules 是否存在
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}检测到未安装依赖，正在安装...${NC}"
    npm install
fi

# 5. 检查是否有 .env.production 文件
if [ ! -f ".env.production" ]; then
    echo -e "${YELLOW}未找到 .env.production 文件，创建示例配置...${NC}"
    cat > .env.production << EOF
# 生产环境 API 地址
# 请根据实际后端部署地址修改
VITE_API_BASE_URL=http://localhost:8113
EOF
    echo -e "${YELLOW}已创建 .env.production 文件，请编辑并设置正确的 API 地址${NC}"
    echo -e "${YELLOW}文件位置: $QA_FRONTEND_DIR/.env.production${NC}"
fi

# 6. 构建前端
echo -e "${YELLOW}开始构建问答前端...${NC}"
npm run build

# 检查构建是否成功
if [ ! -d "dist" ]; then
    echo -e "${RED}错误：构建失败，dist 目录不存在${NC}"
    exit 1
fi

# 7. 复制构建文件到博客目录
echo -e "${YELLOW}复制构建文件到博客目录...${NC}"
rm -rf "$QA_TARGET_DIR"
mkdir -p "$QA_TARGET_DIR"
cp -r dist/* "$QA_TARGET_DIR/"

# 8. 从构建后的 index.html 中提取资源路径
echo -e "${YELLOW}提取资源路径...${NC}"
JS_FILE=$(grep -oE 'assets/[^"]+\.js' dist/index.html | head -1)
CSS_FILE=$(grep -oE 'assets/[^"]+\.css' dist/index.html | head -1)

if [ -n "$JS_FILE" ] && [ -n "$CSS_FILE" ]; then
    echo -e "${GREEN}找到资源文件:${NC}"
    echo -e "  JS: $JS_FILE"
    echo -e "  CSS: $CSS_FILE"
    
    # 更新博客页面中的资源路径
    QA_PAGE_FILE="${BLOG_DIR}/source/qa/index.md"
    if [ -f "$QA_PAGE_FILE" ]; then
        # 使用 sed 更新资源路径
        sed -i.bak "s|/qa/assets/index[^.]*\.js|/qa/$JS_FILE|g" "$QA_PAGE_FILE"
        sed -i.bak "s|/qa/assets/index[^.]*\.css|/qa/$CSS_FILE|g" "$QA_PAGE_FILE"
        rm -f "${QA_PAGE_FILE}.bak"
        echo -e "${GREEN}✓ 已更新博客页面中的资源路径${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  无法自动提取资源路径，请手动更新${NC}"
fi

echo -e "${GREEN}✓ 问答前端已成功集成到博客${NC}"

# 9. 可选：自动同步博客文章到向量数据库
if [ "${AUTO_SYNC_BLOG}" = "true" ]; then
    echo -e "${YELLOW}同步博客文章到向量数据库...${NC}"
    export QA_BACKEND_URL
    if node "${BLOG_DIR}/tools/sync-blog-posts.js" 2>&1; then
        echo -e "${GREEN}✓ 博客文章同步成功${NC}"
    else
        echo -e "${YELLOW}⚠️  博客文章同步失败，可以稍后手动同步${NC}"
        echo -e "   提示：可以运行 npm run sync-blog 手动同步"
    fi
fi
echo -e "${GREEN}目标目录: $QA_TARGET_DIR${NC}"

# 8. 检查博客页面入口是否存在
QA_PAGE_FILE="${BLOG_DIR}/source/qa/index.md"
if [ ! -f "$QA_PAGE_FILE" ]; then
    echo -e "${YELLOW}未找到问答页面入口文件，正在创建...${NC}"
    mkdir -p "${BLOG_DIR}/source/qa"
    cat > "$QA_PAGE_FILE" << 'EOF'
---
title: 知识库问答
date: 2025-01-01
layout: page
permalink: /qa/
---

<div id="app"></div>

<!-- 加载问答系统的 CSS 和 JS -->
<link rel="stylesheet" href="/qa/assets/index.css">
<script type="module" src="/qa/assets/index.js"></script>

<style>
  /* 确保问答应用占满整个页面 */
  #app {
    width: 100%;
    min-height: 100vh;
  }
  
  /* 隐藏博客页面的默认样式，让问答系统完全控制 */
  .page {
    padding: 0 !important;
  }
  
  .page-title {
    display: none;
  }
</style>
EOF
    echo -e "${GREEN}✓ 已创建问答页面入口文件${NC}"
fi

# 10. 提示下一步操作
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}集成完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "下一步操作："
echo -e "1. ${YELLOW}检查并配置后端 API 地址${NC}"
echo -e "   编辑文件: $QA_FRONTEND_DIR/.env.production"
echo -e "   设置 VITE_API_BASE_URL 为你的后端地址"
echo ""
echo -e "2. ${YELLOW}在博客导航菜单中添加问答入口${NC}"
echo -e "   编辑文件: $BLOG_DIR/_config.butterfly.yml"
echo -e "   在 menu 部分添加: ${GREEN}知识库问答: /qa/ || fa fa-comments${NC}"
echo ""
echo -e "3. ${YELLOW}生成并部署博客${NC}"
echo -e "   cd $BLOG_DIR"
echo -e "   hexo generate"
echo -e "   hexo deploy"
echo ""
echo -e "4. ${YELLOW}确保后端服务已启动并配置 CORS${NC}"
echo -e "   后端需要允许博客域名访问"
echo -e "   设置环境变量: AI_DEMO_CORS_ORIGINS=https://linn0813.github.io"
echo ""

