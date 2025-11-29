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
    const cover = getField(parsed.fm, 'cover') || getField(parsed.fm, 'top_img') || '';
    
    // 获取分类信息（根据 permalink 规则 :category/:title/）
    const categories = [];
    const lines = parsed.fm.split('\n');
    let inCategories = false;
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (line.match(/^categories:\s*$/)) {
        inCategories = true;
        continue;
      }
      if (inCategories) {
        // 检查是否是分类项
        const catMatch = line.match(/^\s*-\s*(.+)$/);
        if (catMatch) {
          let cat = catMatch[1].trim();
          // 移除引号
          if ((cat.startsWith('"') && cat.endsWith('"')) || 
              (cat.startsWith("'") && cat.endsWith("'"))) {
            cat = cat.slice(1, -1);
          }
          categories.push(cat);
        } else if (line.match(/^\s*$/) && categories.length > 0) {
          // 空行且已有分类，可能结束
          break;
        } else if (line.match(/^[a-zA-Z]/) && !line.match(/^\s/)) {
          // 遇到新的顶级字段，退出
          break;
        }
      }
    }
    
    // 生成文章 URL（根据 permalink 规则 :category/:title/）
    const fileName = file.replace('.md', '');
    let url = '';
    if (categories.length >= 2) {
      // 二级分类：/一级分类/二级分类/文章名/
      url = `/${categories[0]}/${categories[1]}/${fileName}/`;
    } else if (categories.length === 1) {
      // 一级分类：/分类/文章名/
      url = `/${categories[0]}/${fileName}/`;
    } else {
      // 无分类：/文章名/
      url = `/${fileName}/`;
    }
    
    seriesMap.get(seriesName).push({
      title,
      date,
      description,
      url,
      file: fileName,
      cover: cover,
      categories: categories
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
    
    // 生成系列页面内容 - 使用与分类页面完全相同的HTML结构和CSS类名
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

<div class="article-sort">
`;
    
    // 按日期倒序排列（最新的在前）
    const sortedPosts = [...posts].sort((a, b) => {
      const dateA = new Date(a.date);
      const dateB = new Date(b.date);
      return dateB - dateA; // 倒序
    });
    
    // 按年份分组
    const postsByYear = new Map();
    sortedPosts.forEach((post) => {
      const postDate = new Date(post.date);
      const year = postDate.getFullYear();
      if (!postsByYear.has(year)) {
        postsByYear.set(year, []);
      }
      postsByYear.get(year).push(post);
    });
    
    // 生成文章列表（使用与分类页面相同的结构）
    const sortedYears = Array.from(postsByYear.keys()).sort((a, b) => b - a); // 倒序
    
    sortedYears.forEach((year) => {
      // 年份标题
      content += `  <div class="article-sort-item year">${year}</div>
`;
      
      // 该年份的文章
      postsByYear.get(year).forEach((post) => {
        const postDate = new Date(post.date);
        const dateStr = `${postDate.getFullYear()}-${String(postDate.getMonth() + 1).padStart(2, '0')}-${String(postDate.getDate()).padStart(2, '0')}`;
        const coverImg = post.cover || '/img/404.jpg';
        
        content += `  <div class="article-sort-item">
    <a class="article-sort-item-img" href="${post.url}" title="${post.title}">
      <img src="${coverImg}" alt="${post.title}" onerror="this.onerror=null;this.src='/img/404.jpg'" loading="lazy">
    </a>
    <div class="article-sort-item-info">
      <div class="article-sort-item-time">
        <i class="far fa-calendar-alt"></i>
        <time class="post-meta-date-created" datetime="${postDate.toISOString()}" title="发表于 ${dateStr}">${dateStr}</time>
      </div>
      <a class="article-sort-item-title" href="${post.url}" title="${post.title}">${post.title}</a>
    </div>
  </div>
`;
      });
    });
    
    content += `</div>
`;
    
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

<div class="category-lists">
  <ul class="category-list">
`;
  
  // 按系列名称排序
  const sortedSeries = Array.from(seriesMap.entries()).sort((a, b) => 
    a[0].localeCompare(b[0], 'zh-CN')
  );
  
  for (const [seriesName, posts] of sortedSeries) {
    const fileName = sanitizeFileName(seriesName);
    content += `    <li class="category-list-item">
      <a class="category-list-link" href="/series/${fileName}.html">${seriesName}</a>
      <span class="category-list-count">${posts.length}</span>
    </li>
`;
  }
  
  content += `  </ul>
</div>
`;
  
  fs.writeFileSync(indexPath, content, 'utf8');
  console.log('✓ 更新系列索引页面');
}

main();

