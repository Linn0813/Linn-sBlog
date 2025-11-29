const fs = require('fs');
const path = require('path');

// Hexo Generator for Series Pages
// 自动生成系列页面，使用与分类/归档页面相同的样式

hexo.extend.generator.register('series', function(locals) {
  const config = this.config;
  const posts = locals.posts;
  const seriesMap = new Map();
  
  // 收集所有系列文章
  posts.data.forEach(post => {
    if (post.series) {
      const seriesName = post.series;
      if (!seriesMap.has(seriesName)) {
        seriesMap.set(seriesName, []);
      }
      seriesMap.get(seriesName).push(post);
    }
  });
  
  // 按日期排序每个系列的文章
  for (const [seriesName, seriesPosts] of seriesMap.entries()) {
    seriesPosts.sort((a, b) => {
      const dateA = a.date ? new Date(a.date) : new Date(0);
      const dateB = b.date ? new Date(b.date) : new Date(0);
      return dateA - dateB;
    });
  }
  
  const results = [];
  
  // 为每个系列生成页面
  for (const [seriesName, seriesPosts] of seriesMap.entries()) {
    // 生成安全的文件名
    const fileName = seriesName
      .replace(/[\/\\:*?"<>|]/g, '-')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');
    
    // 生成页面内容 - 使用归档页面的样式
    let content = `---
title: "${seriesName}"
date: ${new Date().toISOString().split('T')[0]}
layout: page
comments: false
series: ${seriesName}
---

# ${seriesName}

<div class="archives-group">
`;
    
    // 按日期分组显示文章
    let currentYear = '';
    let currentMonth = '';
    
    seriesPosts.forEach((post, index) => {
      const postDate = post.date ? new Date(post.date) : new Date();
      const postYear = postDate.getFullYear().toString();
      const postMonth = String(postDate.getMonth() + 1).padStart(2, '0');
      
      // 年份分组
      if (postYear !== currentYear) {
        currentYear = postYear;
        currentMonth = '';
        if (index > 0) {
          content += '</div>\n';
        }
        content += `  <h3 class="archives-year">${currentYear}</h3>\n`;
        content += '  <div class="archives-year-group">\n';
      }
      
      // 月份分组
      if (postMonth !== currentMonth) {
        currentMonth = postMonth;
        content += `    <h4 class="archives-month">${currentYear}-${currentMonth}</h4>\n`;
      }
      
      // 文章项 - 使用相对路径或直接使用post.path
      const dateStr = `${postMonth}-${String(postDate.getDate()).padStart(2, '0')}`;
      // 直接使用post.path，Hexo会自动处理URL
      const postUrl = post.path || '';
      content += `    <div class="archive-item">
      <time class="archive-date">${dateStr}</time>
      <a href="/${postUrl}" class="archive-title">${post.title || post.slug}</a>
    </div>\n`;
    });
    
    if (seriesPosts.length > 0) {
      content += '  </div>\n';
    }
    
    content += `</div>

<style>
.archives-group {
  max-width: 800px;
  margin: 0 auto;
}
.archives-year {
  font-size: 1.8rem;
  color: #333;
  margin-top: 2rem;
  margin-bottom: 1rem;
  border-left: 4px solid #3eaf7c;
  padding-left: 10px;
}
.archives-year-group {
  margin-left: 14px;
}
.archives-month {
  font-size: 1.4rem;
  color: #666;
  margin-top: 1.5rem;
  margin-bottom: 0.8rem;
  padding-left: 14px;
}
.archive-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}
.archive-date {
  width: 80px;
  color: #999;
  font-size: 0.9rem;
  flex-shrink: 0;
}
.archive-title {
  color: #333;
  text-decoration: none;
  flex-grow: 1;
  padding-left: 1rem;
  transition: color 0.3s;
}
.archive-title:hover {
  color: #3eaf7c;
}
</style>
`;
    
    results.push({
      path: `series/${fileName}/index.html`,
      data: {
        content: content,
        layout: 'page',
        title: seriesName,
        series: seriesName
      }
    });
  }
  
  return results;
});

