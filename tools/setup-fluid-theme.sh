#!/bin/bash

# Fluid 主题安装和配置脚本

echo "🎨 开始安装 Fluid 主题..."

# 检查是否已安装
if [ -d "themes/fluid" ]; then
    echo "⚠️  Fluid 主题已存在，跳过安装"
else
    echo "📦 正在安装 Fluid 主题..."
    git clone https://github.com/fluid-dev/hexo-theme-fluid.git themes/fluid
    cd themes/fluid
    git checkout $(git describe --tags --abbrev=0)
    cd ../..
    echo "✅ Fluid 主题安装完成"
fi

# 检查 package.json 中是否包含 fluid
if grep -q "hexo-theme-fluid" package.json; then
    echo "✅ hexo-theme-fluid 已在 package.json 中"
else
    echo "📝 添加 hexo-theme-fluid 到 package.json..."
    npm install hexo-theme-fluid --save
fi

# 复制配置文件
if [ ! -f "_config.fluid.yml" ]; then
    echo "📋 创建 Fluid 主题配置文件..."
    cp themes/fluid/_config.yml _config.fluid.yml
    echo "✅ 配置文件已创建: _config.fluid.yml"
    echo "💡 请编辑 _config.fluid.yml 进行配置"
else
    echo "✅ Fluid 配置文件已存在"
fi

echo ""
echo "🎉 Fluid 主题设置完成！"
echo ""
echo "📝 下一步："
echo "   1. 编辑 _config.fluid.yml 配置 Fluid 主题"
echo "   2. 运行 'npm run theme:fluid' 切换到 Fluid 主题"
echo "   3. 运行 'npm run switch:fluid' 切换并重新生成"
