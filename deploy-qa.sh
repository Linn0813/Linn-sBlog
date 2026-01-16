#!/bin/bash

# 问答系统快速部署脚本
# 用途：一键部署问答系统（前端集成 + 博客生成 + 部署）

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置路径
BLOG_DIR="/Users/yuxiaoling/Blog"
QA_FRONTEND_DIR="${BLOG_DIR}/qa-service/frontend"
QA_BACKEND_DIR="${BLOG_DIR}/qa-service/backend"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  问答系统快速部署脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查参数
SKIP_BUILD=false
SKIP_INTEGRATE=false
SKIP_GENERATE=false
SKIP_DEPLOY=false
AUTO_SYNC=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --skip-build)
      SKIP_BUILD=true
      shift
      ;;
    --skip-integrate)
      SKIP_INTEGRATE=true
      shift
      ;;
    --skip-generate)
      SKIP_GENERATE=true
      shift
      ;;
    --skip-deploy)
      SKIP_DEPLOY=true
      shift
      ;;
    --auto-sync)
      AUTO_SYNC=true
      shift
      ;;
    *)
      echo -e "${RED}未知参数: $1${NC}"
      echo "用法: $0 [--skip-build] [--skip-integrate] [--skip-generate] [--skip-deploy] [--auto-sync]"
      exit 1
      ;;
  esac
done

# 1. 检查后端服务是否运行
echo -e "${YELLOW}[1/5] 检查后端服务...${NC}"
if curl -s http://localhost:8113/healthz > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 后端服务运行正常${NC}"
else
    echo -e "${RED}✗ 后端服务未运行！${NC}"
    echo -e "${YELLOW}请先启动后端服务：${NC}"
    echo -e "  cd ${QA_BACKEND_DIR}"
    echo -e "  source .venv/bin/activate"
    echo -e "  python -m app.main"
    echo ""
    read -p "是否继续部署前端？（y/N）: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 2. 构建前端（如果未跳过）
if [ "$SKIP_BUILD" = false ]; then
    echo -e "${YELLOW}[2/5] 构建前端...${NC}"
    cd "$QA_FRONTEND_DIR"
    
    # 检查依赖
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}检测到未安装依赖，正在安装...${NC}"
        npm install
    fi
    
    # 检查环境变量文件
    if [ ! -f ".env.production" ]; then
        echo -e "${YELLOW}未找到 .env.production 文件，创建示例配置...${NC}"
        cat > .env.production << EOF
# 生产环境 API 地址
# 请根据实际后端部署地址修改
VITE_API_BASE_URL=http://localhost:8113
EOF
        echo -e "${YELLOW}已创建 .env.production 文件，请编辑并设置正确的 API 地址${NC}"
    fi
    
    # 构建
    npm run build
    
    if [ ! -d "dist" ]; then
        echo -e "${RED}✗ 构建失败，dist 目录不存在${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 前端构建完成${NC}"
else
    echo -e "${YELLOW}[2/5] 跳过前端构建${NC}"
fi

# 3. 集成前端到博客（如果未跳过）
if [ "$SKIP_INTEGRATE" = false ]; then
    echo -e "${YELLOW}[3/5] 集成前端到博客...${NC}"
    cd "$BLOG_DIR"
    
    # 使用集成脚本
    if [ -f "./integrate-qa.sh" ]; then
        if [ "$AUTO_SYNC" = true ]; then
            AUTO_SYNC_BLOG=true ./integrate-qa.sh
        else
            ./integrate-qa.sh
        fi
    else
        echo -e "${RED}✗ 未找到集成脚本 integrate-qa.sh${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 前端集成完成${NC}"
else
    echo -e "${YELLOW}[3/5] 跳过前端集成${NC}"
fi

# 4. 生成博客静态文件（如果未跳过）
if [ "$SKIP_GENERATE" = false ]; then
    echo -e "${YELLOW}[4/5] 生成博客静态文件...${NC}"
    cd "$BLOG_DIR"
    
    # 设置自动同步环境变量（如果启用）
    if [ "$AUTO_SYNC" = true ]; then
        export HEXO_AUTO_SYNC_BLOG=true
    fi
    
    hexo generate
    
    echo -e "${GREEN}✓ 博客生成完成${NC}"
else
    echo -e "${YELLOW}[4/5] 跳过博客生成${NC}"
fi

# 5. 部署博客（如果未跳过）
if [ "$SKIP_DEPLOY" = false ]; then
    echo -e "${YELLOW}[5/5] 部署博客...${NC}"
    cd "$BLOG_DIR"
    
    # 使用部署脚本（如果存在）
    if [ -f "./deploy_with_retry.sh" ]; then
        ./deploy_with_retry.sh
    else
        hexo deploy
    fi
    
    echo -e "${GREEN}✓ 博客部署完成${NC}"
else
    echo -e "${YELLOW}[5/5] 跳过博客部署${NC}"
fi

# 完成
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  部署完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "下一步："
echo -e "1. ${YELLOW}访问问答页面${NC}"
echo -e "   本地: http://localhost:4000/qa/"
echo -e "   生产: https://linn0813.github.io/qa/"
echo ""
echo -e "2. ${YELLOW}验证后端服务${NC}"
echo -e "   curl http://localhost:8113/healthz"
echo ""
echo -e "3. ${YELLOW}如需手动同步博客文章${NC}"
echo -e "   npm run sync-blog"
echo ""
