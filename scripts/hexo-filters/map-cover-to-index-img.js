/**
 * 将 Butterfly 主题的 cover 字段映射到 Fluid 主题的 index_img 字段
 * 这样可以在 Fluid 主题中显示文章封面图
 */

'use strict';

hexo.extend.filter.register('template_locals', function(locals) {
  if (locals.page && locals.page.posts) {
    // 处理文章列表
    locals.page.posts.forEach(function(post) {
      if (post.cover && !post.index_img) {
        post.index_img = post.cover;
      }
      // 如果同时有 top_img，优先使用 top_img
      if (post.top_img && !post.index_img) {
        post.index_img = post.top_img;
      }
    });
  }
  
  // 处理单个文章页面
  if (locals.page && locals.page.cover && !locals.page.index_img) {
    locals.page.index_img = locals.page.cover;
  }
  if (locals.page && locals.page.top_img && !locals.page.index_img) {
    locals.page.index_img = locals.page.top_img;
  }
  
  return locals;
});
