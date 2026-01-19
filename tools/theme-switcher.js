#!/usr/bin/env node

/**
 * 主题切换脚本
 * 用于在 butterfly 和 fluid 主题之间快速切换
 * 
 * 使用方法：
 *   node tools/theme-switcher.js butterfly
 *   node tools/theme-switcher.js fluid
 *   或使用 npm 脚本：
 *   npm run theme:butterfly
 *   npm run theme:fluid
 */

const fs = require('fs');
const path = require('path');

const THEMES = {
  butterfly: {
    name: 'butterfly',
    configFile: '_config.butterfly.yml',
    packageName: 'hexo-theme-butterfly'
  },
  fluid: {
    name: 'fluid',
    configFile: '_config.fluid.yml',
    packageName: 'hexo-theme-fluid'
  }
};

function switchTheme(targetTheme) {
  if (!THEMES[targetTheme]) {
    console.error(`❌ 未知的主题: ${targetTheme}`);
    console.log(`可用主题: ${Object.keys(THEMES).join(', ')}`);
    process.exit(1);
  }

  const configPath = path.join(__dirname, '..', '_config.yml');
  const config = fs.readFileSync(configPath, 'utf8');
  
  // 替换主题配置
  const newConfig = config.replace(
    /^theme:\s*.*$/m,
    `theme: ${targetTheme}`
  );

  fs.writeFileSync(configPath, newConfig, 'utf8');
  
  console.log(`✅ 已切换到主题: ${targetTheme}`);
  console.log(`📝 配置文件已更新: _config.yml`);
  console.log(`\n💡 提示:`);
  console.log(`   1. 请确保已安装 ${THEMES[targetTheme].packageName}`);
  console.log(`   2. 请确保存在配置文件 ${THEMES[targetTheme].configFile}`);
  console.log(`   3. 运行 'hexo clean && hexo generate' 重新生成静态文件`);
}

// 主函数
const targetTheme = process.argv[2];

if (!targetTheme) {
  console.log('📖 主题切换工具');
  console.log('\n使用方法:');
    console.log('  node tools/theme-switcher.js <theme-name>');
    console.log('  或使用 npm 脚本: npm run theme:<theme-name>');
  console.log('\n可用主题:');
  Object.keys(THEMES).forEach(theme => {
    console.log(`  - ${theme}`);
  });
  process.exit(0);
}

switchTheme(targetTheme);
