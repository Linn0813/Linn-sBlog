const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Hexo Filter: 在生成后自动修复 sitemap.xml 中的重复 URL
// 这样用户直接使用 hexo generate 时也会自动修复 sitemap

// 使用全局变量防止重复执行（在同一个 Node 进程内）
const globalKey = Symbol('hexo-sitemap-fixed');

hexo.on('generateAfter', function() {
  // 检查是否在 generate 命令中（避免在 clean 等其他命令中执行）
  const command = hexo.env.cmd || '';
  if (command !== 'generate' && command !== 'server') {
    return;
  }
  
  // 如果已经执行过，直接返回
  if (global[globalKey]) {
    return;
  }
  
  // 等待 sitemap.xml 生成（最多等待 2 秒）
  const sitemapPath = path.join(hexo.base_dir, 'public', 'sitemap.xml');
  let attempts = 0;
  const maxAttempts = 20;
  
  const checkAndFix = () => {
    if (fs.existsSync(sitemapPath)) {
      const scriptPath = path.join(hexo.base_dir, 'tools', 'fix-sitemap-duplicates.py');
      try {
        console.log('INFO  Fixing sitemap.xml duplicates...');
        global[globalKey] = true; // 标记为已执行
        execSync(`python3 "${scriptPath}"`, { 
          cwd: hexo.base_dir,
          stdio: 'inherit'
        });
      } catch (error) {
        console.error('ERROR Failed to fix sitemap:', error.message);
        // 不阻止生成流程，只是记录错误
      }
    } else if (attempts < maxAttempts) {
      attempts++;
      setTimeout(checkAndFix, 100); // 等待 100ms 后重试
    }
  };
  
  // 延迟一点执行，确保 sitemap 已经生成
  setTimeout(checkAndFix, 200);
});

