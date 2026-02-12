const fs = require('fs');
const path = require('path');

// Hexo Filter: 在生成后自动复制 QA 前端资源文件到当前 public_dir/qa/assets/
// 使用 hexo.config.public_dir，确保资源在正确位置

// 使用全局变量防止重复执行（在同一个 Node 进程内）
const globalKey = Symbol('hexo-qa-assets-copied');

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
  
  // 延迟执行，确保 public 目录已经生成
  setTimeout(() => {
    try {
      const qaDistPath = path.join(hexo.base_dir, 'qa-service', 'frontend', 'dist', 'assets');
      const publicDir = hexo.config.public_dir || 'public';
      const qaTargetPath = path.join(hexo.base_dir, publicDir, 'qa', 'assets');
      
      // 检查源目录是否存在
      if (!fs.existsSync(qaDistPath)) {
        console.log('INFO  QA assets directory not found, skipping copy');
        return;
      }
      
      // 创建目标目录
      if (!fs.existsSync(qaTargetPath)) {
        fs.mkdirSync(qaTargetPath, { recursive: true });
      }
      
      // 复制文件
      console.log('INFO  Copying QA assets to ' + publicDir + '/qa/assets/...');
      const files = fs.readdirSync(qaDistPath);
      let copiedCount = 0;
      
      files.forEach(file => {
        const srcFile = path.join(qaDistPath, file);
        const destFile = path.join(qaTargetPath, file);
        
        // 只复制文件，不复制目录
        if (fs.statSync(srcFile).isFile()) {
          fs.copyFileSync(srcFile, destFile);
          copiedCount++;
        }
      });
      
      if (copiedCount > 0) {
        console.log(`INFO  ✓ Copied ${copiedCount} QA asset files`);
        global[globalKey] = true; // 标记为已执行
        // 用实际资源文件名修正生成的 QA 页面，避免 source 中旧 hash 导致 JS 404
        try {
          const qaIndexPath = path.join(hexo.base_dir, publicDir, 'qa', 'index.html');
          const distIndexPath = path.join(hexo.base_dir, 'qa-service', 'frontend', 'dist', 'index.html');
          if (fs.existsSync(qaIndexPath) && fs.existsSync(distIndexPath)) {
            const distHtml = fs.readFileSync(distIndexPath, 'utf8');
            const jsMatch = distHtml.match(/\/qa\/assets\/(index\.[^"']+\.js)/);
            const cssMatch = distHtml.match(/\/qa\/assets\/(index\.[^"']+\.css)/);
            if (jsMatch && cssMatch) {
              const actualJs = jsMatch[1];
              const actualCss = cssMatch[1];
              let qaHtml = fs.readFileSync(qaIndexPath, 'utf8');
              qaHtml = qaHtml.replace(/\/qa\/assets\/index\.[^"']+\.js/g, '/qa/assets/' + actualJs);
              qaHtml = qaHtml.replace(/\/qa\/assets\/index\.[^"']+\.css/g, '/qa/assets/' + actualCss);
              fs.writeFileSync(qaIndexPath, qaHtml, 'utf8');
              console.log('INFO  ✓ Updated QA page asset references to ' + actualJs + ', ' + actualCss);
            }
          }
        } catch (err) {
          console.warn('WARN  Could not update QA page asset refs:', err.message);
        }
      } else {
        console.log('WARN  No QA asset files found to copy');
      }
    } catch (error) {
      console.error('ERROR Failed to copy QA assets:', error.message);
      console.error('      You can copy manually using: bash integrate-qa.sh');
      // 不阻止生成流程，只是记录错误
    }
  }, 300); // 延迟 300ms 执行，确保 public 目录已经生成
});
