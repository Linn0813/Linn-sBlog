#!/usr/bin/env node

/**
 * 同步博客文章到向量数据库
 * 用法: node tools/sync-blog-posts.js [backend_url]
 */

const http = require('http');
const https = require('https');
const { URL } = require('url');

const backendUrl = process.env.QA_BACKEND_URL || process.argv[2] || 'http://localhost:8113';
const urlObj = new URL(`${backendUrl}/api/v1/knowledge-base/sync`);
const isHttps = urlObj.protocol === 'https:';
const httpModule = isHttps ? https : http;

const postData = JSON.stringify({
  incremental: true
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
  timeout: 300000  // 5分钟超时
};

console.log(`正在同步博客文章到向量数据库 (${backendUrl})...`);

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
          console.log(`✓ 同步成功！`);
          console.log(`  文章总数: ${result.document_count || 0}`);
          console.log(`  新增: ${result.new_count || 0}`);
          console.log(`  更新: ${result.updated_count || 0}`);
          console.log(`  跳过: ${result.skipped_count || 0}`);
          if (result.deleted_count > 0) {
            console.log(`  删除: ${result.deleted_count}`);
          }
          process.exit(0);
        } else {
          console.error(`✗ 同步失败: ${result.message || 'Unknown error'}`);
          process.exit(1);
        }
      } catch (e) {
        console.error(`✗ 解析响应失败: ${e.message}`);
        console.error(`  响应内容: ${data.substring(0, 200)}`);
        process.exit(1);
      }
    } else {
      console.error(`✗ 同步失败 (HTTP ${res.statusCode}): ${data.substring(0, 200)}`);
      process.exit(1);
    }
  });
});

req.on('error', (error) => {
  if (error.code === 'ECONNREFUSED') {
    console.error(`✗ 无法连接到后端服务 (${backendUrl})`);
    console.error(`  请确保后端服务已启动，或设置 QA_BACKEND_URL 环境变量`);
  } else if (error.code === 'ETIMEDOUT') {
    console.error(`✗ 请求超时，后端可能仍在处理中`);
  } else {
    console.error(`✗ 同步失败: ${error.message}`);
  }
  process.exit(1);
});

req.on('timeout', () => {
  req.destroy();
  console.error(`✗ 请求超时（超过5分钟）`);
  process.exit(1);
});

req.write(postData);
req.end();

