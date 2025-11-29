/**
 * 首页增强脚本
 * 添加分类卡片、推荐区域等
 */

(function() {
  'use strict';

  function enhanceIndexPage() {
    // 检查是否在首页
    if (!document.querySelector('.recent-post-item, .post-item')) return;

    // 创建分类快速导航卡片
    function createCategoryCards() {
      const categoryCards = [
        {
          name: '测试基础与理论',
          icon: 'fa fa-flask',
          color: '#49b1f5',
          url: '/categories/测试基础与理论-Testing-Fundamentals/',
          description: '测试基础理论、测试方法与质量度量'
        },
        {
          name: '自动化测试与工具开发',
          icon: 'fa fa-cogs',
          color: '#00c4b6',
          url: '/categories/自动化测试与工具开发-Test-Automation-Tool-Development/',
          description: '自动化测试框架、工具开发与平台建设'
        },
        {
          name: '性能、安全与专项测试',
          icon: 'fa fa-shield-alt',
          color: '#ff7242',
          url: '/categories/性能、安全与专项测试-Performance-Security-Special-Testing/',
          description: '性能测试、安全测试与专项测试实践'
        },
        {
          name: '项目实战与案例经验',
          icon: 'fa fa-briefcase',
          color: '#f56c6c',
          url: '/categories/项目实战与案例经验-Testing-Practices-Case-Studies/',
          description: '项目实战经验、案例分析与问题解决'
        },
        {
          name: '技术学习与行业趋势',
          icon: 'fa fa-graduation-cap',
          color: '#95de64',
          url: '/categories/技术学习与行业趋势-Learning-Industry-Trends/',
          description: '技术学习、行业趋势与前沿技术探索'
        },
        {
          name: '职业成长与思考',
          icon: 'fa fa-heart',
          color: '#ff9a9e',
          url: '/categories/职业成长与思考-Career-Thoughts/',
          description: '职业规划、个人成长与生活思考'
        }
      ];

      const cardsContainer = document.createElement('div');
      cardsContainer.className = 'index-category-cards sidebar-category-cards';
      cardsContainer.innerHTML = `
        <h2 class="section-title sidebar-section-title">
          <i class="fa fa-th-large"></i>快速导航
        </h2>
        <div class="category-cards sidebar-category-cards-grid">
          ${categoryCards.map(cat => `
            <div class="category-card sidebar-category-card" onclick="window.location.href='${cat.url}'">
              <div class="category-card-icon" style="color: ${cat.color}">
                <i class="${cat.icon}"></i>
              </div>
              <div class="category-card-title">${cat.name}</div>
              <div class="category-card-description">${cat.description}</div>
            </div>
          `).join('')}
        </div>
      `;

      // 插入到文章列表上方（主内容区域）
      function insertToMainContent() {
        // 查找文章列表容器
        const postContainer = document.querySelector('#recent-posts, .recent-post, .post-list, #content-inner, #content');
        
        if (!postContainer) {
          console.log('未找到文章列表容器');
          return false;
        }

        // 查找第一个文章项
        const firstPost = postContainer.querySelector('.recent-post-item, .post-item, article, .post');
        
        if (firstPost && firstPost.parentElement) {
          // 插入到第一个文章之前
          firstPost.parentElement.insertBefore(cardsContainer, firstPost);
          console.log('成功插入到文章列表上方');
          return true;
        } else {
          // 如果没有找到文章项，插入到容器开头
          postContainer.insertBefore(cardsContainer, postContainer.firstChild);
          console.log('成功插入到内容容器开头');
          return true;
        }
      }

      // 尝试插入
      if (!insertToMainContent()) {
        // 延迟重试
        setTimeout(() => {
          if (!insertToMainContent()) {
            setTimeout(() => insertToMainContent(), 1000);
          }
        }, 500);
      }
    }

    // 创建推荐区域
    function createRecommendSection() {
      const recommendSection = document.createElement('div');
      recommendSection.className = 'index-recommend-section sidebar-recommend-section';
      recommendSection.innerHTML = `
        <h2 class="section-title sidebar-section-title">
          <i class="fa fa-star"></i>推荐内容
        </h2>
        <div class="recommend-grid sidebar-recommend-grid">
          <div class="recommend-card sidebar-recommend-card">
            <div class="recommend-card-title">📚 系列文章</div>
            <ul class="recommend-list">
              <li><a href="/series/LLM-Agent系列教程.html">LLM/Agent系列教程</a></li>
              <li><a href="/categories/技术学习与行业趋势-Learning-Industry-Trends/">更多系列...</a></li>
            </ul>
          </div>
          <div class="recommend-card sidebar-recommend-card">
            <div class="recommend-card-title">🔥 热门标签</div>
            <ul class="recommend-list">
              <li><a href="/tags/LLM/">LLM</a></li>
              <li><a href="/tags/Python/">Python</a></li>
              <li><a href="/tags/测试/">测试</a></li>
              <li><a href="/tags/">更多标签...</a></li>
            </ul>
          </div>
          <div class="recommend-card sidebar-recommend-card">
            <div class="recommend-card-title">📖 快速链接</div>
            <ul class="recommend-list">
              <li><a href="/categories/">所有分类</a></li>
              <li><a href="/tags/">所有标签</a></li>
              <li><a href="/archives/">文章归档</a></li>
              <li><a href="/series/">系列文章</a></li>
            </ul>
          </div>
        </div>
      `;

      // 插入到文章列表上方，在分类卡片之后
      function insertRecommendToMainContent() {
        const categoryCards = document.querySelector('.sidebar-category-cards, .index-category-cards');
        
        if (categoryCards && categoryCards.parentElement) {
          // 插入到分类卡片之后
          if (categoryCards.nextSibling) {
            categoryCards.parentElement.insertBefore(recommendSection, categoryCards.nextSibling);
          } else {
            categoryCards.parentElement.appendChild(recommendSection);
          }
          console.log('推荐内容插入到分类卡片之后');
          return true;
        }
        
        // 如果找不到分类卡片，插入到文章列表之前
        const postContainer = document.querySelector('#recent-posts, .recent-post, .post-list, #content-inner, #content');
        if (postContainer) {
          const firstPost = postContainer.querySelector('.recent-post-item, .post-item, article, .post');
          if (firstPost && firstPost.parentElement) {
            firstPost.parentElement.insertBefore(recommendSection, firstPost);
          } else {
            postContainer.insertBefore(recommendSection, postContainer.firstChild);
          }
          console.log('推荐内容插入到文章列表上方');
          return true;
        }
        
        return false;
      }

      // 尝试插入
      if (!insertRecommendToMainContent()) {
        setTimeout(() => {
          if (!insertRecommendToMainContent()) {
            setTimeout(() => insertRecommendToMainContent(), 1000);
          }
        }, 500);
      }
    }

    // 为文章列表添加标题
    function addPostListTitle() {
      const postContainer = document.querySelector('#recent-posts, .recent-post, .post-list, #content-inner, #content');
      if (!postContainer) return;
      
      const firstPost = postContainer.querySelector('.recent-post-item, .post-item, article, .post');
      if (!firstPost) return;
      
      // 检查是否已有标题
      if (postContainer.querySelector('.post-list-title')) return;
      
      const postTitle = document.createElement('h2');
      postTitle.className = 'post-list-title';
      postTitle.innerHTML = '<i class="fa fa-file-text"></i>最新文章';
      
      if (firstPost.parentElement) {
        firstPost.parentElement.insertBefore(postTitle, firstPost);
      }
    }

    // 初始化 - 延迟执行确保侧边栏已加载
    setTimeout(() => {
      createCategoryCards();
      setTimeout(() => {
        createRecommendSection();
        setTimeout(addPostListTitle, 200);
      }, 200);
    }, 300);
  }

  // 初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceIndexPage);
  } else {
    enhanceIndexPage();
  }
})();

