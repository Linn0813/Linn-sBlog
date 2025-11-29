const fs = require('fs');
const path = require('path');

const POSTS_DIR = path.join(__dirname, '..', 'source', '_posts');
const SERIES_DIR = path.join(__dirname, '..', 'source', 'series');

// 确保 series 目录存在
if (!fs.existsSync(SERIES_DIR)) {
  fs.mkdirSync(SERIES_DIR, { recursive: true });
}

// 提取 Front Matter
function extractFrontMatter(content) {
  const start = content.indexOf('---');
  if (start !== 0) return null;
  const end = content.indexOf('\n---', start + 3);
  if (end === -1) return null;
  const fm = content.slice(start + 3, end).trim();
  const body = content.slice(end + 4);
  return { fm, body };
}

// 从 Front Matter 中提取字段
function getField(fm, fieldName) {
  // 支持多种格式：series: value 或 series: "value"
  const regex = new RegExp(`^${fieldName}:\\s*(.+)$`, 'm');
  const match = fm.match(regex);
  if (!match) return null;
  
  let value = match[1].trim();
  // 处理带引号的值
  if ((value.startsWith('"') && value.endsWith('"')) || 
      (value.startsWith("'") && value.endsWith("'"))) {
    value = value.slice(1, -1);
  }
  // 移除可能的注释
  value = value.split('#')[0].trim();
  return value || null;
}

// 获取日期字段
function getDate(fm) {
  const dateMatch = fm.match(/^date:\s*(.+)$/m);
  return dateMatch ? dateMatch[1].trim() : new Date().toISOString().split('T')[0];
}

// 生成安全的文件名（将特殊字符替换为连字符）
function sanitizeFileName(name) {
  return name
    .replace(/[\/\\:*?"<>|]/g, '-')  // 替换特殊字符
    .replace(/\s+/g, '-')              // 空格替换为连字符
    .replace(/-+/g, '-')               // 多个连字符合并为一个
    .replace(/^-|-$/g, '');            // 移除首尾连字符
}

// 主函数
function main() {
  const files = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
  const seriesMap = new Map();
  
  // 扫描所有文章，收集系列信息
  for (const file of files) {
    const filePath = path.join(POSTS_DIR, file);
    const content = fs.readFileSync(filePath, 'utf8');
    const parsed = extractFrontMatter(content);
    
    if (!parsed) continue;
    
    const seriesName = getField(parsed.fm, 'series');
    if (!seriesName) continue;
    
    if (!seriesMap.has(seriesName)) {
      seriesMap.set(seriesName, []);
    }
    
    const title = getField(parsed.fm, 'title') || file.replace('.md', '');
    const date = getDate(parsed.fm);
    const description = getField(parsed.fm, 'description') || '';
    
    // 生成文章 URL（根据 permalink 规则）
    const fileName = file.replace('.md', '');
    const url = `/${fileName}.html`;
    
    seriesMap.get(seriesName).push({
      title,
      date,
      description,
      url,
      file: fileName
    });
  }
  
  // 按日期排序每个系列的文章
  for (const [seriesName, posts] of seriesMap.entries()) {
    posts.sort((a, b) => new Date(a.date) - new Date(b.date));
  }
  
  // 生成系列页面
  for (const [seriesName, posts] of seriesMap.entries()) {
    const fileName = sanitizeFileName(seriesName);
    const filePath = path.join(SERIES_DIR, `${fileName}.md`);
    
    // 生成系列页面内容 - 使用主题统一的文章列表样式
    // 将 title 中的特殊字符替换为连字符，避免 URL 解析错误
    const safeTitle = seriesName.replace(/[\/\\:*?"<>|]/g, '-');
    let content = `---
title: "${safeTitle}"
date: ${new Date().toISOString().split('T')[0]}
layout: page
comments: false
series: ${seriesName}
---

# ${seriesName}

`;
    
    // 添加文章列表 - 使用简洁格式，让主题处理样式
    posts.forEach((post, index) => {
      // 提取日期部分（去掉时间）
      const dateOnly = post.date.split(' ')[0] || post.date.split('T')[0];
      
      content += `## [${post.title}](${post.url})\n\n`;
      
      if (post.description) {
        content += `${post.description}\n\n`;
      }
      
      content += `**发布时间:** ${dateOnly}\n\n`;
      
      if (index < posts.length - 1) {
        content += '---\n\n';
      }
    });
    
    // 写入文件
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✓ 生成系列页面: ${seriesName} -> ${fileName}.md (${posts.length} 篇文章)`);
  }
  
  // 更新系列索引页面
  updateSeriesIndex(seriesMap);
  
  console.log(`\n完成！共生成 ${seriesMap.size} 个系列页面。`);
}

// 更新系列索引页面
function updateSeriesIndex(seriesMap) {
  const indexPath = path.join(SERIES_DIR, 'index.md');
  
  let content = `---
title: 文章系列
date: ${new Date().toISOString().split('T')[0]}
layout: page
comments: false
---

# 文章系列

这里汇集了我编写的主题系列文章，方便您系统学习相关知识。

`;
  
  // 按系列名称排序
  const sortedSeries = Array.from(seriesMap.entries()).sort((a, b) => 
    a[0].localeCompare(b[0], 'zh-CN')
  );
  
  for (const [seriesName, posts] of sortedSeries) {
    const fileName = sanitizeFileName(seriesName);
    content += `## [${seriesName}](./${fileName}.html)\n\n`;
    content += `**共 ${posts.length} 篇文章**\n\n`;
  }
  
  fs.writeFileSync(indexPath, content, 'utf8');
  console.log('✓ 更新系列索引页面');
}

main();

