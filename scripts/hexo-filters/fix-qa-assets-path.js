/**
 * Hexo Filter: 修复 QA 页面的资源路径
 * 当设置了 root 路径时，自动修正 QA 页面中的 CSS/JS 资源路径
 */

hexo.extend.filter.register('after_render:html', function(str, data) {
  // 只处理 QA 页面
  if (!data.page || !data.page.path || !data.page.path.includes('qa')) {
    return str;
  }
  
  // 获取 root 配置
  const root = hexo.config.root || '/';
  
  // 如果 root 是 '/'，不需要修复
  if (root === '/') {
    return str;
  }
  
  // 移除 root 末尾的斜杠（如果有）
  const rootPath = root.replace(/\/$/, '');
  
  // 修复 CSS 路径
  str = str.replace(
    /href="\/qa\/assets\/([^"]+)"/g,
    `href="${rootPath}/qa/assets/$1"`
  );
  
  // 修复 JS 路径
  str = str.replace(
    /src="\/qa\/assets\/([^"]+)"/g,
    `src="${rootPath}/qa/assets/$1"`
  );
  
  return str;
});
