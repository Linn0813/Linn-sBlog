---
title: 知识库问答
date: 2025-01-01
layout: page
permalink: /qa/
---

<!-- 先加载 CSS -->
<link rel="stylesheet" href="/qa/assets/index.DRzPa3M-.css">

<div id="app"></div>

<!-- 加载 Vue 应用 JS - 使用 defer 确保在 DOM 加载后执行 -->
<script type="module" crossorigin src="/qa/assets/index.BwXeKSfW.js" defer></script>

<script>
  // 确保在 DOM 加载完成后检查 Vue 应用
  document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM 加载完成，检查 #app 元素');
    const app = document.getElementById('app');
    console.log('#app 元素:', app);
    
    // 等待 Vue 应用挂载
    setTimeout(function() {
      if (app && (!app.innerHTML || app.innerHTML.trim() === '')) {
        console.warn('Vue 应用可能未正确挂载，检查控制台错误');
      } else {
        console.log('Vue 应用已挂载，内容:', app.innerHTML.substring(0, 100));
      }
    }, 1000);
  });
</script>

<style>
  /* 确保问答应用占满整个页面 */
  #app {
    width: 100%;
    min-height: 100vh;
  }
  
  /* 隐藏博客页面的默认样式，让问答系统完全控制 */
  .page {
    padding: 0 !important;
  }
  
  .page-title {
    display: none;
  }
</style>

