/**
 * 侧边栏系列列表卡片
 * 在所有页面显示系列列表，类似分类卡片和标签卡片
 */

(function() {
  'use strict';

  function createSeriesCard() {
    // 检查是否已有系列卡片
    if (document.querySelector('.card-widget.card-series')) return;

    // 获取侧边栏容器 - 更精确的选择器
    // Butterfly 主题的侧边栏通常在 #aside-content 中
    let sidebar = document.querySelector('#aside-content');
    
    // 如果找不到，尝试其他选择器
    if (!sidebar) {
      sidebar = document.querySelector('aside#aside-content');
    }
    if (!sidebar) {
      sidebar = document.querySelector('.aside_content');
    }
    if (!sidebar) {
      sidebar = document.querySelector('aside');
    }
    
    // 验证是否真的是侧边栏（包含其他卡片）
    if (sidebar && !sidebar.querySelector('.card-widget')) {
      sidebar = null;
    }
    
    if (!sidebar) {
      console.log('未找到侧边栏容器');
      return;
    }

    // 默认系列数据（如果无法动态获取，使用默认数据）
    const defaultSeriesData = [
      {
        name: '🧠 LLM/Agent 从入门到精通：告别浅尝辄止',
        url: '/series/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/',
        count: 3
      }
    ];

    // 创建系列卡片 - 使用与分类卡片相同的结构
    const seriesCard = document.createElement('div');
    seriesCard.className = 'card-widget card-series';
    seriesCard.innerHTML = `
      <div class="item-headline">
        <i class="fas fa-book"></i>
        <span>系列</span>
        <a class="card-more-btn" href="/series/" title="查看更多">
          <i class="fas fa-angle-right"></i>
        </a>
      </div>
      <ul class="card-series-list" id="aside-series-list">
        ${defaultSeriesData.map(series => `
          <li class="card-series-list-item">
            <a class="card-series-list-link" href="${series.url}" title="${series.name}">
              <span class="card-series-list-name">${series.name}</span>
              <span class="card-series-list-count">${series.count}</span>
            </a>
          </li>
        `).join('')}
      </ul>
    `;

    // 插入到侧边栏（按照导航栏顺序：分类 -> 标签 -> 归档 -> 系列 -> 网站信息）
    // 获取所有卡片，找到归档卡片的位置，然后插入到归档之后
    const allCards = sidebar.querySelectorAll('.card-widget');
    let insertAfterCard = null;
    
    // 按顺序查找：归档卡片 -> 标签卡片 -> 分类卡片
    for (let i = 0; i < allCards.length; i++) {
      const card = allCards[i];
      // 找到归档卡片，插入到它之后
      if (card.classList.contains('card-archives')) {
        insertAfterCard = card;
        break;
      }
    }
    
    // 如果没找到归档卡片，尝试找标签卡片
    if (!insertAfterCard) {
      for (let i = 0; i < allCards.length; i++) {
        const card = allCards[i];
        if (card.classList.contains('card-tags')) {
          insertAfterCard = card;
          break;
        }
      }
    }
    
    // 如果还没找到，尝试找分类卡片
    if (!insertAfterCard) {
      for (let i = 0; i < allCards.length; i++) {
        const card = allCards[i];
        if (card.classList.contains('card-categories')) {
          insertAfterCard = card;
          break;
        }
      }
    }
    
    // 插入卡片
    if (insertAfterCard) {
      // 插入到找到的卡片之后
      if (insertAfterCard.nextSibling) {
        insertAfterCard.parentNode.insertBefore(seriesCard, insertAfterCard.nextSibling);
      } else {
        insertAfterCard.parentNode.appendChild(seriesCard);
      }
    } else {
      // 如果都找不到，尝试找到网站信息卡片，插入到它之前
      const webinfoCard = sidebar.querySelector('.card-widget.card-webinfo');
      if (webinfoCard) {
        webinfoCard.parentNode.insertBefore(seriesCard, webinfoCard);
      } else {
        // 最后尝试插入到侧边栏末尾
        sidebar.appendChild(seriesCard);
      }
    }
  }

  // 从当前页面获取系列数据
  function fetchSeriesData() {
    // 尝试从当前页面的系列索引列表中提取数据
    const seriesItems = document.querySelectorAll('.category-list-item');
    if (seriesItems.length > 0) {
      const seriesData = [];
      seriesItems.forEach(item => {
        const link = item.querySelector('.category-list-link');
        const count = item.querySelector('.category-list-count');
        if (link && count) {
          seriesData.push({
            name: link.textContent.trim(),
            url: link.getAttribute('href'),
            count: parseInt(count.textContent.trim()) || 0
          });
        }
      });
      if (seriesData.length > 0) {
        return seriesData;
      }
    }
    return null;
  }

  // 通过 AJAX 获取系列索引页面的数据
  function fetchSeriesIndexData() {
    return fetch('/series/')
      .then(response => response.text())
      .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const seriesItems = doc.querySelectorAll('.category-list-item');
        const seriesData = [];
        seriesItems.forEach(item => {
          const link = item.querySelector('.category-list-link');
          const count = item.querySelector('.category-list-count');
          if (link && count) {
            seriesData.push({
              name: link.textContent.trim(),
              url: link.getAttribute('href'),
              count: parseInt(count.textContent.trim()) || 0
            });
          }
        });
        return seriesData.length > 0 ? seriesData : null;
      })
      .catch(err => {
        console.log('无法获取系列数据:', err);
        return null;
      });
  }

  // 更新系列卡片内容
  function updateSeriesCard(seriesData) {
    const seriesCard = document.querySelector('.card-widget.card-series');
    if (seriesCard) {
      const seriesList = seriesCard.querySelector('.card-series-list');
      if (seriesList) {
        seriesList.innerHTML = seriesData.map(series => `
          <li class="card-series-list-item">
            <a class="card-series-list-link" href="${series.url}" title="${series.name}">
              <span class="card-series-list-name">${series.name}</span>
              <span class="card-series-list-count">${series.count}</span>
            </a>
          </li>
        `).join('');
      }
    }
  }

  // 动态更新系列数据
  function updateSeriesData() {
    // 先尝试从当前页面获取
    let seriesData = fetchSeriesData();
    
    if (seriesData && seriesData.length > 0) {
      updateSeriesCard(seriesData);
    } else {
      // 如果当前页面没有，尝试通过 AJAX 获取
      setTimeout(() => {
        fetchSeriesIndexData().then(data => {
          if (data && data.length > 0) {
            updateSeriesCard(data);
          }
        });
      }, 1000);
    }
  }

  // 初始化
  function init() {
    // 延迟执行，确保侧边栏已加载
    setTimeout(() => {
      createSeriesCard();
      // 尝试更新系列数据
      updateSeriesData();
    }, 800);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
