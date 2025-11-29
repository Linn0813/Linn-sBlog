/**
 * 分类页面增强脚本
 * 优化分类页面显示，不添加额外卡片，只优化现有样式
 */

(function() {
  'use strict';

  function enhanceCategoryPage() {
    // 只在分类列表页面（所有分类）执行，不在单个分类页面执行
    const categoryListPage = document.querySelector('.category-list');
    if (!categoryListPage) return;
    
    // 检查是否在分类列表页面（/categories/），而不是单个分类页面
    const isCategoryListPage = window.location.pathname.includes('/categories/') && 
                                !window.location.pathname.match(/\/categories\/[^\/]+\/[^\/]+/);
    
    if (!isCategoryListPage) return;

    // 优化分类列表项的样式
    const categoryItems = categoryListPage.querySelectorAll('.category-list-item, .category-list a, li');
    
    categoryItems.forEach(item => {
      // 添加简单的悬停效果
      if (!item.classList.contains('category-item-enhanced')) {
        item.classList.add('category-item-enhanced');
        item.style.transition = 'all 0.3s ease';
        item.style.cursor = 'pointer';
        
        item.addEventListener('mouseenter', function() {
          this.style.transform = 'translateX(5px)';
          this.style.color = '#49b1f5';
        });
        
        item.addEventListener('mouseleave', function() {
          this.style.transform = 'translateX(0)';
          this.style.color = '';
        });
      }
    });
  }

  // 初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceCategoryPage);
  } else {
    enhanceCategoryPage();
  }
})();

