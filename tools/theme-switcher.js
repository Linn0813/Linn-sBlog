#!/usr/bin/env node

/**
 * 主题切换脚本
 * 用于切换到 butterfly 主题
 * 
 * 使用方法：
 *   node tools/theme-switcher.js butterfly
 *   或使用 npm 脚本：
 *   npm run theme:butterfly
 */

const fs = require('fs');
const path = require('path');

const THEME = {
  name: 'butterfly',
  configFile: '_config.butterfly.yml',
  packageName: 'hexo-theme-butterfly'
};

function switchTheme() {
  const configPath = path.join(__dirname, '..', '_config.yml');
  const config = fs.readFileSync(configPath, 'utf8');
  
  // 替换主题配置
  const newConfig = config.replace(
    /^theme:\s*.*$/m,
    `theme: ${THEME.name}`
  );

  fs.writeFileSync(configPath, newConfig, 'utf8');
  
  console.log(`✅ 已切换到主题: ${THEME.name}`);
  console.log(`📝 配置文件已更新: _config.yml`);
  console.log(`\n💡 提示:`);
  console.log(`   1. 请确保已安装 ${THEME.packageName}`);
  console.log(`   2. 请确保存在配置文件 ${THEME.configFile}`);
  console.log(`   3. 运行 'hexo clean && hexo generate' 重新生成静态文件`);
}

// 主函数
const targetTheme = process.argv[2];

if (targetTheme && targetTheme !== 'butterfly') {
  console.error(`❌ 未知的主题: ${targetTheme}`);
  console.log(`当前只支持 butterfly 主题`);
  process.exit(1);
}

switchTheme();
