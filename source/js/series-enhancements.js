/**
 * 系列文章功能增强
 * 添加系列进度条、导航等
 */

(function() {
  'use strict';

  function enhanceSeriesNavigation() {
    const seriesCard = document.querySelector('.card_post_series');
    if (!seriesCard) return;

    const seriesLinks = seriesCard.querySelectorAll('a');
    if (seriesLinks.length === 0) return;

    const currentUrl = window.location.pathname;
    let currentIndex = -1;

    // 找到当前文章在系列中的位置
    seriesLinks.forEach((link, index) => {
      const href = link.getAttribute('href');
      if (href && (currentUrl.includes(href.split('/').pop()) || href.includes(currentUrl.split('/').pop()))) {
        currentIndex = index;
        link.classList.add('current-series-post');
      }
    });

    // 如果找到当前文章，添加进度条
    if (currentIndex >= 0) {
      const progress = ((currentIndex + 1) / seriesLinks.length) * 100;
      
      const progressBar = document.createElement('div');
      progressBar.className = 'series-progress-bar';
      progressBar.innerHTML = `
        <div class="series-progress-fill" style="width: ${progress}%"></div>
        <div class="series-progress-text">${currentIndex + 1} / ${seriesLinks.length}</div>
      `;
      
      seriesCard.insertBefore(progressBar, seriesCard.firstChild);

      // 添加上一篇/下一篇导航
      const navContainer = document.createElement('div');
      navContainer.className = 'series-navigation';
      navContainer.style.marginTop = '15px';
      navContainer.style.display = 'flex';
      navContainer.style.justifyContent = 'space-between';
      navContainer.style.gap = '10px';

      if (currentIndex > 0) {
        const prevLink = seriesLinks[currentIndex - 1];
        const prevBtn = document.createElement('a');
        prevBtn.href = prevLink.getAttribute('href');
        prevBtn.className = 'series-nav-btn series-nav-prev';
        prevBtn.innerHTML = '<i class="fa fa-chevron-left"></i> 上一篇';
        navContainer.appendChild(prevBtn);
      }

      if (currentIndex < seriesLinks.length - 1) {
        const nextLink = seriesLinks[currentIndex + 1];
        const nextBtn = document.createElement('a');
        nextBtn.href = nextLink.getAttribute('href');
        nextBtn.className = 'series-nav-btn series-nav-next';
        nextBtn.innerHTML = '下一篇 <i class="fa fa-chevron-right"></i>';
        navContainer.appendChild(nextBtn);
      }

      if (navContainer.children.length > 0) {
        seriesCard.appendChild(navContainer);
      }
    }
  }

  // 初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceSeriesNavigation);
  } else {
    setTimeout(enhanceSeriesNavigation, 500);
  }
})();

