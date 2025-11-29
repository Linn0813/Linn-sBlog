/**
 * 标签页面增强脚本
 * 添加标签云和统计信息
 */

(function() {
  'use strict';

  function enhanceTagPage() {
    const tagPage = document.querySelector('.tag-page, .tag-list');
    if (!tagPage) return;

    // 获取所有标签
    const tagItems = tagPage.querySelectorAll('.tag-list-item, .tag-list a, .tag-cloud a');
    
    if (tagItems.length === 0) return;

    // 创建标签云容器
    const cloudContainer = document.createElement('div');
    cloudContainer.className = 'tag-cloud-enhanced';
    
    // 收集标签数据
    const tags = [];
    tagItems.forEach(item => {
      const link = item.tagName === 'A' ? item : item.querySelector('a');
      if (!link) return;
      
      const tagName = link.textContent.trim();
      const count = item.querySelector('.tag-list-count')?.textContent || '0';
      const countNum = parseInt(count.replace(/[^\d]/g, '')) || 0;
      
      tags.push({
        name: tagName,
        count: countNum,
        link: link.href
      });
    });

    // 按数量排序
    tags.sort((a, b) => b.count - a.count);

    // 计算字体大小范围
    const maxCount = Math.max(...tags.map(t => t.count));
    const minCount = Math.min(...tags.map(t => t.count));
    const sizeRange = 24 - 12; // 12px 到 24px

    // 创建标签云
    tags.forEach(tag => {
      const size = maxCount === minCount 
        ? 16 
        : 12 + (sizeRange * (tag.count - minCount) / (maxCount - minCount));
      
      const tagElement = document.createElement('a');
      tagElement.href = tag.link;
      tagElement.className = 'tag-cloud-item';
      tagElement.style.fontSize = size + 'px';
      tagElement.textContent = tag.name;
      tagElement.title = `${tag.name} (${tag.count} 篇文章)`;
      
      cloudContainer.appendChild(tagElement);
    });

    // 插入标签云
    if (tagPage.parentElement) {
      tagPage.parentElement.insertBefore(cloudContainer, tagPage);
    }

    // 创建统计信息
    const statsCard = document.createElement('div');
    statsCard.className = 'tag-stats';
    statsCard.innerHTML = `
      <div class="tag-stat-item">
        <div class="stat-number">${tags.length}</div>
        <div class="stat-label">总标签数</div>
      </div>
      <div class="tag-stat-item">
        <div class="stat-number">${tags.reduce((sum, t) => sum + t.count, 0)}</div>
        <div class="stat-label">总文章数</div>
      </div>
    `;

    if (tagPage.parentElement) {
      tagPage.parentElement.insertBefore(statsCard, tagPage);
    }
  }

  // 初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceTagPage);
  } else {
    enhanceTagPage();
  }
})();

