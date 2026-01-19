#!/bin/bash

# 双主题部署脚本
# 用于后台服务自动部署 Butterfly 和 Fluid 两个主题

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 恢复配置的函数（确保总是执行）
restore_config() {
  echo -e "\n${YELLOW}正在恢复配置...${NC}" >&2
  
  # 恢复 root 配置
  CONFIG_FILE="$BLOG_DIR/_config.yml"
  if [ -f "$CONFIG_FILE" ]; then
    # 移除 root 配置行
    sed -i.bak '/^root:/d' "$CONFIG_FILE" 2>/dev/null || true
    rm -f "$CONFIG_FILE.bak" 2>/dev/null || true
    echo -e "  ✓ root 配置已恢复" >&2
  fi
  
  # 恢复默认主题为 Butterfly
  if node tools/theme-switcher.js butterfly > /dev/null 2>&1; then
    echo -e "  ✓ 默认主题已恢复为 Butterfly" >&2
  else
    echo -e "  ${RED}✗ 恢复主题失败，请手动运行: npm run theme:butterfly${NC}" >&2
  fi
}

# 设置退出时恢复配置（确保即使脚本出错也会恢复）
trap restore_config EXIT INT TERM

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  双主题自动部署脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 获取脚本所在目录的父目录（博客根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLOG_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$BLOG_DIR"

echo -e "${YELLOW}工作目录: ${BLOG_DIR}${NC}"
echo ""

# 1. 部署 Butterfly 主题
echo -e "${YELLOW}[1/2] 部署 Butterfly 主题...${NC}"

# 切换到 Butterfly 主题
node tools/theme-switcher.js butterfly

# 生成静态文件
echo -e "  生成静态文件..."
hexo clean > /dev/null 2>&1
hexo generate

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Butterfly 主题生成失败${NC}"
    exit 1
fi

# 部署到主仓库
echo -e "  部署到 GitHub Pages..."
hexo deploy

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Butterfly 主题部署失败${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Butterfly 主题部署完成${NC}"
echo ""

# 2. 部署 Fluid 主题
echo -e "${YELLOW}[2/2] 部署 Fluid 主题...${NC}"

# 切换到 Fluid 主题
node tools/theme-switcher.js fluid

# 配置 root 路径（部署在子路径时需要）
echo -e "  配置 root 路径为 /fluid-blog/..."
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
  echo -e "  ✓ root 路径已配置"
else
  echo -e "  ${RED}✗ 配置文件不存在: $CONFIG_FILE${NC}"
  exit 1
fi

# 生成静态文件
echo -e "  生成静态文件..."
hexo clean > /dev/null 2>&1
hexo generate

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Fluid 主题生成失败${NC}"
    exit 1
fi

# 部署到 fluid-blog 仓库
echo -e "  部署到 fluid-blog 仓库..."
cd public

# 初始化 git（如果还没有）
if [ ! -d .git ]; then
    git init
fi

# 配置 git
git config user.name "GitHub Actions" || true
git config user.email "actions@github.com" || true

# 添加文件
git add .

# 提交
git commit -m "Deploy Fluid theme - $(date +'%Y-%m-%d %H:%M:%S')" || true

# 设置分支
git branch -M main

# 配置远程仓库
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/Linn0813/fluid-blog.git

# 推送（强制推送，因为每次都是重新生成）
git push -f origin main

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Fluid 主题部署失败${NC}"
    exit 1
fi

cd ..

# 恢复 root 配置（避免影响后续操作）
echo -e "  恢复 root 配置..."
CONFIG_FILE="$BLOG_DIR/_config.yml"
if [ -f "$CONFIG_FILE" ]; then
  # 移除 root 配置行
  sed -i.bak '/^root:/d' "$CONFIG_FILE" 2>/dev/null || true
  rm -f "$CONFIG_FILE.bak" 2>/dev/null || true
  echo -e "  ✓ root 配置已恢复"
fi

echo -e "${GREEN}✓ Fluid 主题部署完成${NC}"
echo ""

# 恢复默认主题（在正常流程中）
restore_config

# 取消 trap（因为已经手动恢复了，避免重复执行）
trap - EXIT INT TERM
echo ""

# 完成
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  双主题部署完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "访问地址："
echo -e "  ${BLUE}Butterfly:${NC} https://linn0813.github.io"
echo -e "  ${BLUE}Fluid:${NC}     https://linn0813.github.io/fluid-blog"
echo ""
echo -e "${YELLOW}提示：${NC}默认主题已恢复为 Butterfly"
echo ""
