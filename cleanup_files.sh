#!/bin/bash

# 清理多余文件脚本
# 使用前请确认要删除的文件

set -e

BLOG_DIR="/Users/yuxiaoling/Blog"
cd "$BLOG_DIR"

echo "🧹 开始清理多余文件..."
echo ""

# 1. 删除 macOS 系统文件
echo "1. 删除 .DS_Store 文件..."
find . -name ".DS_Store" -type f -delete 2>/dev/null || true
echo "   ✓ 已删除 .DS_Store 文件"
echo ""

# 2. 删除重复/不需要的文档
echo "2. 删除重复/不需要的文档..."
FILES_TO_DELETE=(
    "QUICK_TEST.md"                          # 快速测试文档（测试完成后不需要）
    "qa-service/MIGRATION_PLAN.md"            # 迁移计划（迁移已完成）
    "qa-service/DEVELOPMENT_DECISION.md"      # 开发决策文档（历史文档）
    "qa-service/UPLOAD_STEPS.sh"             # 上传步骤脚本（可能不需要）
    "_config.landscape.yml"                   # 空的主题配置文件（不使用 landscape 主题）
)

for file in "${FILES_TO_DELETE[@]}"; do
    if [ -f "$file" ]; then
        echo "   删除: $file"
        rm "$file"
    fi
done
echo "   ✓ 已删除文档文件"
echo ""

# 3. 删除报告文件（可选，如果需要保留可以注释掉）
echo "3. 删除分析报告文件（可选）..."
if [ -d "reports" ]; then
    echo "   删除 reports/ 目录下的 JSON 文件"
    rm -f reports/*.json
    echo "   ✓ 已删除报告文件"
fi
echo ""

# 4. 检查 layout 目录是否为空
echo "4. 检查 layout 目录..."
if [ -d "layout" ]; then
    if [ -z "$(find layout -type f 2>/dev/null)" ]; then
        echo "   layout 目录为空，可以删除"
        # 取消注释下面这行来删除空目录
        # rmdir layout/includes/mixins layout/includes layout 2>/dev/null || true
    else
        echo "   layout 目录包含文件，保留"
    fi
fi
echo ""

echo "✅ 清理完成！"
echo ""
echo "📝 注意："
echo "   - readme 文件包含部署说明，建议保留或更新"
echo "   - 如果 layout 目录为空，可以手动删除"
echo "   - reports/ 目录已清空，如果需要可以删除整个目录"

