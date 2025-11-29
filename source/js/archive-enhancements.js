/**
 * 归档页面增强脚本
 * 添加时间线视图和统计信息
 */

(function() {
  'use strict';

  function enhanceArchivePage() {
    const archivePage = document.querySelector('.archive-page');
    if (!archivePage) return;

    // 获取所有归档项
    const archiveItems = archivePage.querySelectorAll('.archive-year, .archive-month, .archive-post-item');
    
    if (archiveItems.length === 0) return;

    // 创建时间线容器
    const timelineContainer = document.createElement('div');
    timelineContainer.className = 'archive-timeline';
    
    // 统计信息
    const stats = {
      totalPosts: archiveItems.length,
      years: new Set(),
      months: new Set()
    };

    archiveItems.forEach(item => {
      const year = item.querySelector('.archive-year-title')?.textContent;
      const month = item.querySelector('.archive-month-title')?.textContent;
      
      if (year) stats.years.add(year);
      if (month) stats.months.add(month);
    });

    // 创建统计卡片
    const statsCard = document.createElement('div');
    statsCard.className = 'archive-stats';
    statsCard.innerHTML = `
      <div class="archive-stat-item">
        <div class="stat-number">${stats.totalPosts}</div>
        <div class="stat-label">总文章数</div>
      </div>
      <div class="archive-stat-item">
        <div class="stat-number">${stats.years.size}</div>
        <div class="stat-label">年份数</div>
      </div>
      <div class="archive-stat-item">
        <div class="stat-number">${stats.months.size}</div>
        <div class="stat-label">月份数</div>
      </div>
    `;

    // 插入统计卡片
    if (archivePage.parentElement) {
      archivePage.parentElement.insertBefore(statsCard, archivePage);
    }
  }

  // 初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceArchivePage);
  } else {
    enhanceArchivePage();
  }
})();

