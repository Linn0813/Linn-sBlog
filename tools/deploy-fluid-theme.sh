#!/bin/bash

# 部署 Fluid 主题到 fluid-blog 仓库
# 使用方法: bash tools/deploy-fluid-theme.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取脚本所在目录
BLOG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BLOG_DIR"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}部署 Fluid 主题${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 恢复配置函数（确保它总是运行）
restore_config() {
  echo -e "\n${YELLOW}正在恢复默认配置...${NC}"
  CONFIG_FILE="$BLOG_DIR/_config.yml"
  
  # 恢复主题为 butterfly
  if [ -f "$CONFIG_FILE" ]; then
    node tools/theme-switcher.js butterfly > /dev/null 2>&1 || true
  fi
  
  # 移除 root 配置
  if [ -f "$CONFIG_FILE" ] && grep -q "^root:" "$CONFIG_FILE"; then
    sed -i.bak '/^root:/d' "$CONFIG_FILE" 2>/dev/null || true
    rm -f "$CONFIG_FILE.bak" 2>/dev/null || true
  fi
  
  echo -e "${GREEN}✓ 默认配置已恢复${NC}"
}

# 设置 trap 确保退出时恢复配置
trap restore_config EXIT INT TERM

# 切换到 Fluid 主题
echo -e "${YELLOW}[1/3] 切换到 Fluid 主题...${NC}"
node tools/theme-switcher.js fluid

# 配置 root 路径（部署在子路径时需要）
echo -e "${YELLOW}[2/3] 配置 root 路径为 /fluid-blog/...${NC}"
CONFIG_FILE="$BLOG_DIR/_config.yml"
if [ -f "$CONFIG_FILE" ]; then
  # 检查是否已有 root 配置
  if grep -q "^root:" "$CONFIG_FILE"; then
    # 更新现有的 root 配置
    sed -i.bak 's|^root:.*|root: /fluid-blog/|' "$CONFIG_FILE"
    rm -f "$CONFIG_FILE.bak"
  else
    # 在 url 配置后添加 root
    sed -i.bak '/^url:/a\
root: /fluid-blog/
' "$CONFIG_FILE"
    rm -f "$CONFIG_FILE.bak"
  fi
  echo -e "  ${GREEN}✓ root 路径已配置${NC}"
else
  echo -e "  ${RED}✗ 配置文件不存在: $CONFIG_FILE${NC}"
  exit 1
fi

# 生成静态文件
echo -e "${YELLOW}[3/3] 生成静态文件...${NC}"
hexo clean > /dev/null 2>&1
hexo generate

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Fluid 主题生成失败${NC}"
    exit 1
fi

# 部署到 fluid-blog 仓库
echo -e "${YELLOW}部署到 fluid-blog 仓库...${NC}"
cd public

# 初始化 git（如果还没有）
if [ ! -d .git ]; then
    git init
fi

# 配置 git
git config user.name "GitHub Actions" || true
git config user.email "actions@github.com" || true

# 添加远程仓库（如果还没有）
if ! git remote | grep -q "^origin$"; then
    git remote add origin git@github.com:Linn0813/fluid-blog.git
else
    git remote set-url origin git@github.com:Linn0813/fluid-blog.git
fi

# 添加所有文件
git add -A

# 提交
git commit -m "Deploy Fluid theme: $(date '+%Y-%m-%d %H:%M:%S')" || {
    echo -e "${YELLOW}⚠️  没有更改需要提交${NC}"
}

# 推送到 main 分支
echo -e "${YELLOW}推送到 GitHub...${NC}"
git push -f origin HEAD:main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Fluid 主题部署成功${NC}"
    echo -e "${GREEN}访问地址: https://linn0813.github.io/fluid-blog/${NC}"
else
    echo -e "${RED}✗ Fluid 主题部署失败${NC}"
    exit 1
fi

cd "$BLOG_DIR"

# 正常退出，恢复配置
restore_config
trap - EXIT INT TERM

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}部署完成！${NC}"
echo -e "${GREEN}========================================${NC}"
