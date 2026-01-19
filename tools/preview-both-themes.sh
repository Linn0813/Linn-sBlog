#!/bin/bash

# 本地双主题预览脚本
# 同时生成 Butterfly 和 Fluid 两个主题，支持通过路径切换
# 
# 使用方法：
#   npm run preview:both
#   或
#   bash tools/preview-both-themes.sh

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  本地双主题预览${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 获取脚本所在目录的父目录（博客根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLOG_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$BLOG_DIR"

echo -e "${YELLOW}工作目录: ${BLOG_DIR}${NC}"
echo ""

# 1. 生成 Butterfly 主题
echo -e "${YELLOW}[1/2] 生成 Butterfly 主题...${NC}"

# 切换到 Butterfly 主题
node tools/theme-switcher.js butterfly

# 生成静态文件到 public-butterfly 目录
echo -e "  生成静态文件到 public-butterfly..."
hexo clean > /dev/null 2>&1

# 临时修改 public_dir 配置
CONFIG_FILE="$BLOG_DIR/_config.yml"
ORIGINAL_PUBLIC_DIR=$(grep "^public_dir:" "$CONFIG_FILE" | cut -d: -f2 | tr -d ' ' || echo "public")

# 备份并修改配置
if grep -q "^public_dir:" "$CONFIG_FILE"; then
  sed -i.bak 's|^public_dir:.*|public_dir: public-butterfly|' "$CONFIG_FILE"
else
  echo "public_dir: public-butterfly" >> "$CONFIG_FILE"
fi

hexo generate

# 恢复配置
if [ -f "$CONFIG_FILE.bak" ]; then
  mv "$CONFIG_FILE.bak" "$CONFIG_FILE"
else
  sed -i.bak "s|^public_dir:.*|public_dir: $ORIGINAL_PUBLIC_DIR|" "$CONFIG_FILE" 2>/dev/null || true
  rm -f "$CONFIG_FILE.bak" 2>/dev/null || true
fi

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Butterfly 主题生成失败${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Butterfly 主题生成完成${NC}"
echo ""

# 2. 生成 Fluid 主题
echo -e "${YELLOW}[2/2] 生成 Fluid 主题...${NC}"

# 切换到 Fluid 主题
node tools/theme-switcher.js fluid

# 配置 root 路径（本地预览时使用 /fluid 路径）
CONFIG_FILE="$BLOG_DIR/_config.yml"
if [ -f "$CONFIG_FILE" ]; then
  if grep -q "^root:" "$CONFIG_FILE"; then
    sed -i.bak 's|^root:.*|root: /fluid/|' "$CONFIG_FILE"
    rm -f "$CONFIG_FILE.bak"
  else
    sed -i.bak '/^url:/a\
root: /fluid/
' "$CONFIG_FILE"
    rm -f "$CONFIG_FILE.bak"
  fi
fi

# 生成静态文件到 public-fluid 目录
echo -e "  生成静态文件到 public-fluid..."
hexo clean > /dev/null 2>&1

# 临时修改 public_dir 配置
ORIGINAL_PUBLIC_DIR=$(grep "^public_dir:" "$CONFIG_FILE" | cut -d: -f2 | tr -d ' ' || echo "public")

# 备份并修改配置
if grep -q "^public_dir:" "$CONFIG_FILE"; then
  sed -i.bak 's|^public_dir:.*|public_dir: public-fluid|' "$CONFIG_FILE"
else
  echo "public_dir: public-fluid" >> "$CONFIG_FILE"
fi

hexo generate

# 恢复配置
if [ -f "$CONFIG_FILE.bak" ]; then
  mv "$CONFIG_FILE.bak" "$CONFIG_FILE"
else
  sed -i.bak "s|^public_dir:.*|public_dir: $ORIGINAL_PUBLIC_DIR|" "$CONFIG_FILE" 2>/dev/null || true
  rm -f "$CONFIG_FILE.bak" 2>/dev/null || true
fi

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Fluid 主题生成失败${NC}"
    # 恢复 root 配置
    sed -i.bak '/^root:/d' "$CONFIG_FILE" 2>/dev/null || true
    rm -f "$CONFIG_FILE.bak" 2>/dev/null || true
    exit 1
fi

# 恢复 root 配置
sed -i.bak '/^root:/d' "$CONFIG_FILE" 2>/dev/null || true
rm -f "$CONFIG_FILE.bak" 2>/dev/null || true

echo -e "${GREEN}✓ Fluid 主题生成完成${NC}"
echo ""

# 恢复默认主题为 Butterfly（预览完成后）
echo -e "${YELLOW}[恢复] 恢复默认主题为 Butterfly...${NC}"
node tools/theme-switcher.js butterfly
echo -e "${GREEN}✓ 默认主题已恢复${NC}"
echo ""

# 3. 创建合并的 public 目录
echo -e "${YELLOW}[3/3] 合并两个主题到 public 目录...${NC}"

# 清理并创建 public 目录
rm -rf public
mkdir -p public

# 复制 Butterfly 主题（根路径）
echo -e "  复制 Butterfly 主题到根路径..."
cp -r public-butterfly/* public/

# 创建 fluid 子目录并复制 Fluid 主题
echo -e "  复制 Fluid 主题到 /fluid 路径..."
mkdir -p public/fluid
cp -r public-fluid/* public/fluid/

# 验证合并结果
if [ ! -f "public/index.html" ]; then
  echo -e "${RED}✗ 错误：根路径缺少 index.html${NC}"
  exit 1
fi

if [ ! -f "public/fluid/index.html" ]; then
  echo -e "${RED}✗ 错误：/fluid 路径缺少 index.html${NC}"
  exit 1
fi

echo -e "${GREEN}✓ 合并完成${NC}"
echo ""

# 4. 启动服务器
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  预览服务器启动中...${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "访问地址："
echo -e "  ${BLUE}Butterfly:${NC} http://localhost:$PORT/"
echo -e "  ${BLUE}Fluid:${NC}     http://localhost:$PORT/fluid/"
echo ""
echo -e "${YELLOW}提示：${NC}"
echo -e "  - 根路径 (/) 显示 Butterfly 主题"
echo -e "  - /fluid 路径显示 Fluid 主题"
echo -e "  - 主题切换按钮会自动跳转到对应路径"
echo -e "  - 如果看到错误的主题，请清除浏览器缓存（Ctrl+Shift+R 或 Cmd+Shift+R）"
echo -e "${YELLOW}按 Ctrl+C 停止服务器${NC}"
echo ""

# 检查端口是否被占用，如果被占用则使用其他端口
PORT=4000
if lsof -ti:$PORT > /dev/null 2>&1; then
  echo -e "${YELLOW}警告：端口 $PORT 已被占用，尝试使用端口 4001${NC}"
  PORT=4001
  if lsof -ti:$PORT > /dev/null 2>&1; then
    echo -e "${YELLOW}警告：端口 $PORT 也被占用，尝试使用端口 4002${NC}"
    PORT=4002
  fi
fi

# 启动 Hexo 服务器（在后台启动，以便可以在退出时恢复主题）
hexo server -p $PORT &
SERVER_PID=$!

# 等待服务器启动
sleep 2

# 设置退出时恢复默认主题
trap "echo ''; echo -e '${YELLOW}正在恢复默认主题...${NC}'; node tools/theme-switcher.js butterfly > /dev/null 2>&1; echo -e '${GREEN}✓ 默认主题已恢复为 Butterfly${NC}'; kill $SERVER_PID 2>/dev/null; exit" INT TERM

# 等待服务器进程
wait $SERVER_PID
