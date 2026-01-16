const { execSync } = require('child_process');
const path = require('path');
const http = require('http');
const https = require('https');
const { URL } = require('url');

// Hexo Filter: 在生成后自动同步博客文章到向量数据库
// 这样用户直接使用 hexo generate 时也会自动同步文章

// 使用全局变量防止重复执行（在同一个 Node 进程内）
const globalKey = Symbol('hexo-blog-synced');

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
  
  // 检查是否启用自动同步（可以通过环境变量控制）
  const autoSync = process.env.HEXO_AUTO_SYNC_BLOG !== 'false';
  if (!autoSync) {
    console.log('INFO  Auto-sync blog posts is disabled (set HEXO_AUTO_SYNC_BLOG=false to disable)');
    return;
  }
  
  // 获取后端 API 地址（默认从环境变量或配置读取）
  const backendUrl = process.env.QA_BACKEND_URL || 'http://localhost:8113';
  
  // 异步执行同步，不阻塞生成流程
  // 注意：使用setTimeout确保在generate完成后执行，但可能会在hexo进程退出前未完成
  console.log('INFO  Preparing to sync blog posts to vector database after generation...');
  
  // 使用Promise确保同步完成（但不会阻塞hexo进程）
  const syncPromise = new Promise((resolve) => {
    setTimeout(() => {
      try {
        console.log('INFO  Syncing blog posts to vector database...');
        global[globalKey] = true; // 标记为已执行
        
        // 调用后端 API 同步博客文章
        const urlObj = new URL(`${backendUrl}/api/v1/knowledge-base/sync`);
        const isHttps = urlObj.protocol === 'https:';
        const httpModule = isHttps ? https : http;
        
        const postData = JSON.stringify({
          incremental: true  // 使用增量同步
        });
        
        const options = {
          hostname: urlObj.hostname,
          port: urlObj.port || (isHttps ? 443 : 80),
          path: urlObj.pathname + urlObj.search,
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postData)
          },
          timeout: 300000  // 5分钟超时（同步可能需要较长时间）
        };
        
        const req = httpModule.request(options, (res) => {
          let data = '';
          
          res.on('data', (chunk) => {
            data += chunk;
          });
          
          res.on('end', () => {
            if (res.statusCode === 200) {
              try {
                const result = JSON.parse(data);
                if (result.success) {
                  console.log(`INFO  ✓ Blog posts synced successfully: ${result.document_count || 0} posts (${result.new_count || 0} new, ${result.updated_count || 0} updated, ${result.skipped_count || 0} skipped)`);
                } else {
                  console.warn(`WARN  Blog sync completed with warnings: ${result.message || 'Unknown error'}`);
                }
              } catch (e) {
                console.warn('WARN  Failed to parse sync response:', e.message);
              }
            } else {
              console.warn(`WARN  Blog sync failed with status ${res.statusCode}: ${data.substring(0, 100)}`);
            }
            resolve();
          });
        });
        
        req.on('error', (error) => {
          // 如果后端服务不可用，只记录警告，不阻止生成流程
          if (error.code === 'ECONNREFUSED' || error.code === 'ETIMEDOUT') {
            console.warn(`WARN  Backend service is not available (${backendUrl}), skipping blog sync.`);
            console.warn('      You can sync manually using: npm run sync-blog');
            console.warn('      Or start the backend service and run hexo generate again.');
          } else {
            console.warn(`WARN  Failed to sync blog posts: ${error.message}`);
          }
          resolve();
        });
        
        req.on('timeout', () => {
          req.destroy();
          console.warn('WARN  Blog sync request timeout, but generation continues.');
          console.warn('      You can sync manually using: npm run sync-blog');
          resolve();
        });
        
        req.write(postData);
        req.end();
        
      } catch (error) {
        console.warn('WARN  Failed to sync blog posts:', error.message);
        console.warn('      You can sync manually using: npm run sync-blog');
        resolve();
      }
    }, 500); // 延迟 500ms 执行，确保生成流程已完成
  });
  
  // 注意：这里不await，让hexo进程可以继续，但同步会在后台进行
  // 如果需要在同步完成后才退出，可以取消下面的注释
  // hexo.extend.filter.register('after_generate', async () => {
  //   await syncPromise;
  // });
});

