/**
 * 在文章页面元数据区域显示系列信息
 * 样式与分类保持一致
 */

(function() {
  'use strict';

  function addSeriesToMeta() {
    // 查找文章元数据容器
    const metaWrap = document.querySelector('.article-meta-wrap');
    if (!metaWrap) return;

    // 检查是否已经有系列信息
    if (metaWrap.querySelector('.article-meta__series')) return;

    // 从页面中获取系列信息
    // 方法1: 从系列卡片中获取
    const seriesCard = document.querySelector('.card_post_series');
    if (!seriesCard) return;

    // 尝试多种方式获取系列名称
    let seriesName = '';
    let seriesUrl = '/series/';
    
    // 方法1: 从标题获取
    const seriesTitle = seriesCard.querySelector('.card_post_series_title, h3, .item-headline span');
    if (seriesTitle) {
      seriesName = seriesTitle.textContent.trim();
    }
    
    // 方法2: 从第一个链接的文本获取
    if (!seriesName) {
      const firstLink = seriesCard.querySelector('a[href*="series"]');
      if (firstLink) {
        seriesName = firstLink.textContent.trim();
        seriesUrl = firstLink.getAttribute('href');
      }
    }
    
    if (!seriesName) return;

    // 获取系列页面链接 - 查找指向系列页面的链接
    const seriesLinks = seriesCard.querySelectorAll('a[href*="series"]');
    if (seriesLinks.length > 0) {
      // 优先使用系列列表页面的链接（包含系列名称的链接）
      const listLink = Array.from(seriesLinks).find(link => {
        const href = link.getAttribute('href');
        return href && href.includes('series') && !href.match(/\/\d+\//);
      });
      if (listLink) {
        seriesUrl = listLink.getAttribute('href');
      } else {
        // 使用第一个链接，但需要提取系列页面URL
        const firstLinkHref = seriesLinks[0].getAttribute('href');
        // 如果是文章链接，提取系列页面URL
        if (firstLinkHref && firstLinkHref.includes('series')) {
          // 尝试从URL中提取系列名称并构建系列页面URL
          const match = firstLinkHref.match(/series\/([^\/]+)/);
          if (match) {
            seriesUrl = `/series/${match[1]}/`;
          } else {
            seriesUrl = firstLinkHref.split('/').slice(0, -1).join('/') + '/';
          }
        } else {
          seriesUrl = firstLinkHref || '/series/';
        }
      }
    }

    // 查找分类显示的位置
    const categoriesMeta = metaWrap.querySelector('.article-meta__categories');
    if (!categoriesMeta) return;

    // 创建系列元数据显示元素（样式与分类一致）
    const seriesMeta = document.createElement('span');
    seriesMeta.className = 'article-meta article-meta__series';
    
    // 添加分隔符
    const separator = document.createElement('span');
    separator.className = 'article-meta-separator';
    separator.textContent = '|';
    
    // 创建系列链接
    const seriesLinkElement = document.createElement('a');
    seriesLinkElement.className = 'article-meta__series-link';
    seriesLinkElement.href = seriesUrl;
    seriesLinkElement.title = seriesName;
    
    // 添加图标和文本（使用与分类相同的图标样式）
    const icon = document.createElement('i');
    icon.className = 'fas fa-book';
    seriesLinkElement.appendChild(icon);
    seriesLinkElement.appendChild(document.createTextNode(' ' + seriesName));

    seriesMeta.appendChild(separator);
    seriesMeta.appendChild(seriesLinkElement);

    // 插入到分类后面（与分类在同一行）
    const categoriesContainer = categoriesMeta.closest('.article-meta');
    if (categoriesContainer && categoriesContainer.nextSibling) {
      categoriesContainer.parentNode.insertBefore(seriesMeta, categoriesContainer.nextSibling);
    } else if (categoriesContainer && categoriesContainer.parentNode) {
      categoriesContainer.parentNode.appendChild(seriesMeta);
    } else {
      metaWrap.appendChild(seriesMeta);
    }
  }

  // 等待页面加载完成后执行
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(addSeriesToMeta, 800);
    });
  } else {
    setTimeout(addSeriesToMeta, 800);
  }
})();

