#!/bin/bash

# 验证主题合并脚本

BLOG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BLOG_DIR"

echo "检查主题合并情况..."
echo ""

# 检查目录
if [ ! -d "public" ]; then
  echo "❌ public 目录不存在"
  echo "请先运行: npm run preview:both"
  exit 1
fi

if [ ! -d "public-butterfly" ]; then
  echo "❌ public-butterfly 目录不存在"
  exit 1
fi

if [ ! -d "public-fluid" ]; then
  echo "❌ public-fluid 目录不存在"
  exit 1
fi

# 检查根路径
if [ ! -f "public/index.html" ]; then
  echo "❌ public/index.html 不存在"
  exit 1
fi

if [ ! -f "public/fluid/index.html" ]; then
  echo "❌ public/fluid/index.html 不存在"
  exit 1
fi

# 比较文件
ROOT_LINES=$(wc -l < public/index.html)
BUTTERFLY_LINES=$(wc -l < public-butterfly/index.html)
FLUID_LINES=$(wc -l < public-fluid/index.html)

echo "文件行数对比："
echo "  public/index.html:        $ROOT_LINES 行"
echo "  public-butterfly/index.html: $BUTTERFLY_LINES 行"
echo "  public-fluid/index.html:     $FLUID_LINES 行"
echo ""

if [ "$ROOT_LINES" -eq "$BUTTERFLY_LINES" ]; then
  echo "✅ 根路径 (/) 是 Butterfly 主题"
else
  echo "❌ 根路径不是 Butterfly 主题"
fi

if diff -q public/index.html public-butterfly/index.html > /dev/null 2>&1; then
  echo "✅ 根路径文件与 Butterfly 完全相同"
else
  echo "⚠️  根路径文件与 Butterfly 有差异"
fi

echo ""
echo "访问测试："
echo "  Butterfly: http://localhost:4000/"
echo "  Fluid:     http://localhost:4000/fluid/"
echo ""
echo "如果看到错误的主题，请："
echo "  1. 清除浏览器缓存（Ctrl+Shift+R 或 Cmd+Shift+R）"
echo "  2. 确认访问的是正确的 URL"
echo "  3. 检查浏览器地址栏是否显示正确的路径"
