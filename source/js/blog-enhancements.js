/**
 * 博客功能增强脚本
 * 包括：搜索增强、阅读进度、收藏功能、阅读历史等
 */

(function() {
  'use strict';

  // ==================== 阅读进度条 ====================
  function initReadingProgress() {
    if (document.querySelector('.post-content') || document.querySelector('.article-content')) {
      const progressBar = document.createElement('div');
      progressBar.className = 'reading-progress-bar';
      progressBar.innerHTML = '<div class="reading-progress-fill"></div>';
      document.body.appendChild(progressBar);

      const progressFill = progressBar.querySelector('.reading-progress-fill');
      const article = document.querySelector('.post-content') || document.querySelector('.article-content') || document.querySelector('article');
      
      if (!article) return;

      function updateProgress() {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const articleTop = article.offsetTop;
        const articleHeight = article.offsetHeight;
        const scrollableHeight = documentHeight - windowHeight;
        
        let progress = 0;
        if (scrollTop >= articleTop) {
          const scrolledInArticle = scrollTop - articleTop;
          progress = Math.min((scrolledInArticle / articleHeight) * 100, 100);
        }
        
        progressFill.style.width = progress + '%';
      }

      window.addEventListener('scroll', updateProgress);
      updateProgress();
    }
  }

  // ==================== 文章收藏功能 ====================
  function initBookmark() {
    const bookmarkBtn = document.createElement('button');
    bookmarkBtn.className = 'bookmark-btn';
    bookmarkBtn.innerHTML = '<i class="fa fa-bookmark-o"></i> 收藏';
    bookmarkBtn.title = '收藏这篇文章';
    
    const articleTitle = document.querySelector('.post-title')?.textContent || document.title;
    const articleUrl = window.location.pathname;
    const bookmarkKey = 'blog_bookmarks';
    
    // 检查是否已收藏
    function isBookmarked() {
      const bookmarks = JSON.parse(localStorage.getItem(bookmarkKey) || '[]');
      return bookmarks.some(item => item.url === articleUrl);
    }
    
    // 更新按钮状态
    function updateBookmarkState() {
      if (isBookmarked()) {
        bookmarkBtn.classList.add('bookmarked');
        bookmarkBtn.innerHTML = '<i class="fa fa-bookmark"></i> 已收藏';
        bookmarkBtn.title = '取消收藏';
      } else {
        bookmarkBtn.classList.remove('bookmarked');
        bookmarkBtn.innerHTML = '<i class="fa fa-bookmark-o"></i> 收藏';
        bookmarkBtn.title = '收藏这篇文章';
      }
    }
    
    // 切换收藏状态
    bookmarkBtn.addEventListener('click', function() {
      const bookmarks = JSON.parse(localStorage.getItem(bookmarkKey) || '[]');
      const index = bookmarks.findIndex(item => item.url === articleUrl);
      
      if (index > -1) {
        bookmarks.splice(index, 1);
        localStorage.setItem(bookmarkKey, JSON.stringify(bookmarks));
      } else {
        bookmarks.push({
          title: articleTitle,
          url: articleUrl,
          date: new Date().toISOString()
        });
        localStorage.setItem(bookmarkKey, JSON.stringify(bookmarks));
      }
      
      updateBookmarkState();
      showNotification(isBookmarked() ? '已收藏' : '已取消收藏');
    });
    
    // 添加到文章头部
    const postHeader = document.querySelector('.post-header') || document.querySelector('.article-header');
    if (postHeader) {
      postHeader.appendChild(bookmarkBtn);
    }
    
    updateBookmarkState();
  }

  // ==================== 阅读历史记录 ====================
  function initReadingHistory() {
    const historyKey = 'blog_reading_history';
    const maxHistory = 50;
    
    const articleTitle = document.querySelector('.post-title')?.textContent || document.title;
    const articleUrl = window.location.pathname;
    
    if (articleUrl.includes('/post/') || articleUrl.includes('/2025/')) {
      let history = JSON.parse(localStorage.getItem(historyKey) || '[]');
      
      // 移除重复项
      history = history.filter(item => item.url !== articleUrl);
      
      // 添加到开头
      history.unshift({
        title: articleTitle,
        url: articleUrl,
        date: new Date().toISOString()
      });
      
      // 限制数量
      if (history.length > maxHistory) {
        history = history.slice(0, maxHistory);
      }
      
      localStorage.setItem(historyKey, JSON.stringify(history));
    }
  }

  // ==================== 搜索增强 ====================
  function enhanceSearch() {
    const searchInput = document.querySelector('#local-search-input');
    if (!searchInput) return;
    
    // 添加搜索建议容器
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'search-suggestions';
    searchInput.parentElement.appendChild(suggestionsContainer);
    
    // 热门搜索词
    const hotSearches = ['LLM', 'Agent', '测试', 'Python', 'FastAPI', '自动化测试', 'Prompt工程'];
    
    // 显示热门搜索
    function showHotSearches() {
      suggestionsContainer.innerHTML = '<div class="hot-searches"><span>热门搜索：</span>' +
        hotSearches.map(term => `<span class="hot-search-tag" data-term="${term}">${term}</span>`).join('') +
        '</div>';
      
      // 点击热门搜索
      suggestionsContainer.querySelectorAll('.hot-search-tag').forEach(tag => {
        tag.addEventListener('click', function() {
          searchInput.value = this.dataset.term;
          searchInput.dispatchEvent(new Event('input'));
          suggestionsContainer.style.display = 'none';
        });
      });
    }
    
    // 当输入框获得焦点时显示热门搜索
    searchInput.addEventListener('focus', function() {
      if (!this.value) {
        showHotSearches();
        suggestionsContainer.style.display = 'block';
      }
    });
    
    // 点击外部隐藏建议
    document.addEventListener('click', function(e) {
      if (!searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
        suggestionsContainer.style.display = 'none';
      }
    });
  }

  // ==================== 通知提示 ====================
  function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `blog-notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => {
        notification.remove();
      }, 300);
    }, 2000);
  }

  // ==================== 键盘快捷键 ====================
  function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
      // 按 / 键聚焦搜索框
      if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
        const activeElement = document.activeElement;
        if (activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
          const searchInput = document.querySelector('#local-search-input');
          if (searchInput) {
            e.preventDefault();
            searchInput.focus();
          }
        }
      }
      
      // ESC 键关闭搜索建议
      if (e.key === 'Escape') {
        const suggestions = document.querySelector('.search-suggestions');
        if (suggestions) {
          suggestions.style.display = 'none';
        }
      }
    });
  }

  // ==================== 系列文章导航增强 ====================
  function enhanceSeriesNavigation() {
    const seriesNav = document.querySelector('.card_post_series');
    if (!seriesNav) return;
    
    // 添加系列进度条
    const seriesPosts = seriesNav.querySelectorAll('a');
    if (seriesPosts.length > 0) {
      const currentUrl = window.location.pathname;
      let currentIndex = -1;
      
      seriesPosts.forEach((link, index) => {
        if (link.getAttribute('href') === currentUrl) {
          currentIndex = index;
          link.classList.add('current-series-post');
        }
      });
      
      if (currentIndex >= 0) {
        const progress = ((currentIndex + 1) / seriesPosts.length) * 100;
        const progressBar = document.createElement('div');
        progressBar.className = 'series-progress-bar';
        progressBar.innerHTML = `<div class="series-progress-fill" style="width: ${progress}%"></div>
          <div class="series-progress-text">${currentIndex + 1} / ${seriesPosts.length}</div>`;
        seriesNav.insertBefore(progressBar, seriesNav.firstChild);
      }
    }
  }

  // ==================== 初始化所有功能 ====================
  function init() {
    // DOM 加载完成后初始化
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
      return;
    }
    
    initReadingProgress();
    initBookmark();
    initReadingHistory();
    enhanceSearch();
    initKeyboardShortcuts();
    
    // 延迟初始化系列导航（等待主题渲染）
    setTimeout(enhanceSeriesNavigation, 500);
  }

  init();
})();

