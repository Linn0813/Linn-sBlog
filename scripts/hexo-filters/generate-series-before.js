const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Hexo Filter: 在生成前自动运行系列页面生成脚本
// 这样用户直接使用 hexo generate 时也会自动生成系列页面

// 使用全局变量防止重复执行（在同一个 Node 进程内）
const globalKey = Symbol('hexo-series-generated');

hexo.on('generateBefore', function() {
  // 检查是否在 generate 命令中（避免在 clean 等其他命令中执行）
  const command = hexo.env.cmd || '';
  if (command !== 'generate' && command !== 'server') {
    return;
  }
  
  // 如果已经执行过，直接返回
  if (global[globalKey]) {
    return;
  }
  
  // 检查系列页面文件是否在最近2秒内被修改（说明刚刚执行过）
  const seriesDir = path.join(hexo.base_dir, 'source', 'series');
  if (fs.existsSync(seriesDir)) {
    const files = fs.readdirSync(seriesDir).filter(f => f.endsWith('.md'));
    if (files.length > 0) {
      const latestFile = files.map(f => {
        const filePath = path.join(seriesDir, f);
        return { path: filePath, mtime: fs.statSync(filePath).mtime };
      }).sort((a, b) => b.mtime - a.mtime)[0];
      
      const timeSinceModified = Date.now() - latestFile.mtime.getTime();
      if (timeSinceModified < 2000) { // 2秒内
        return; // 认为已经执行过了
      }
    }
  }
  
  const scriptPath = path.join(hexo.base_dir, 'scripts', 'generate_series_pages.js');
  try {
    console.log('INFO  Running series pages generator...');
    global[globalKey] = true; // 标记为已执行
    execSync(`node "${scriptPath}"`, { 
      cwd: hexo.base_dir,
      stdio: 'inherit'
    });
  } catch (error) {
    console.error('ERROR Failed to generate series pages:', error.message);
    // 不阻止生成流程，只是记录错误
  }
});

