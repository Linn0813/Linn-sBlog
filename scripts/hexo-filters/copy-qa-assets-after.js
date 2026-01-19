const fs = require('fs');
const path = require('path');

// Hexo Filter: 在生成后自动复制 QA 前端资源文件到 public/qa/assets/
// 这样用户直接使用 hexo generate 时也会自动复制资源文件

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
      const qaTargetPath = path.join(hexo.base_dir, 'public', 'qa', 'assets');
      
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
      console.log('INFO  Copying QA assets to public/qa/assets/...');
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
