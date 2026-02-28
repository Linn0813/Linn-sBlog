# encoding: utf-8
"""
博客文章加载器，用于从 Hexo 博客加载文章内容。
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime
import yaml

from shared.logger import log


class BlogDocumentLoader:
    """博客文章加载器，用于获取和处理博客文章内容。"""

    def __init__(self, blog_posts_dir: Optional[str] = None):
        """
        初始化博客文章加载器。

        Args:
            blog_posts_dir: 博客文章目录路径，如果不提供则使用默认路径
        """
        if blog_posts_dir is None:
            # 默认路径：qa-service/backend/infrastructure/external/blog/loader.py
            # 向上6级到 Blog 目录：blog -> external -> infrastructure -> backend -> qa-service -> Blog
            current_file = Path(__file__).resolve()
            # blog (1) -> external (2) -> infrastructure (3) -> backend (4) -> qa-service (5) -> Blog (6)
            blog_root = current_file.parent.parent.parent.parent.parent.parent
            blog_posts_dir = blog_root / 'source' / '_posts'
            
            # 如果路径不存在，尝试从环境变量获取
            if not blog_posts_dir.exists():
                import os
                blog_root_env = os.getenv('BLOG_ROOT')
                if blog_root_env:
                    blog_posts_dir = Path(blog_root_env) / 'source' / '_posts'
        
        self.blog_posts_dir = Path(blog_posts_dir)
        if not self.blog_posts_dir.exists():
            # 不抛出异常，允许后续处理
            log.warning(f"博客文章目录不存在: {self.blog_posts_dir}")

    def load_all_posts(self) -> List[Dict[str, Any]]:
        """
        加载所有博客文章。

        Returns:
            文章列表，每个文章包含内容和元信息
        """
        documents = []
        
        if not self.blog_posts_dir.exists():
            log.warning(f"博客文章目录不存在: {self.blog_posts_dir}")
            return documents

        # 遍历所有 Markdown 文件
        for post_file in self.blog_posts_dir.glob("*.md"):
            try:
                doc = self._load_post(post_file)
                if doc:
                    documents.append(doc)
            except Exception as e:
                log.error(f"加载文章失败 {post_file}: {e}")
                continue

        log.info(f"成功加载 {len(documents)} 篇博客文章")
        return documents

    def _load_post(self, post_file: Path) -> Optional[Dict[str, Any]]:
        """
        加载单篇博客文章。

        Args:
            post_file: 文章文件路径

        Returns:
            文章字典，包含内容和元信息
        """
        try:
            # 读取文件内容
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析 front matter
            metadata, body = self._parse_frontmatter(content)

            # 提取文章信息
            title = metadata.get('title', post_file.stem)
            date = metadata.get('date')
            if isinstance(date, datetime):
                date = date.timestamp()
            elif isinstance(date, str):
                try:
                    date = datetime.fromisoformat(date.replace('Z', '+00:00')).timestamp()
                except (ValueError, AttributeError) as date_error:
                    log.debug(f"无法解析日期格式 '{date}': {date_error}，使用文件修改时间")
                    date = post_file.stat().st_mtime

            # 生成文章 URL（基于 Hexo permalink 规则）
            url = self._generate_post_url(post_file, metadata)

            # 清理内容：移除 Markdown 语法，保留纯文本
            clean_content = self._clean_markdown(body)

            if not clean_content.strip():
                log.warning(f"文章内容为空: {post_file}")
                return None

            return {
                "id": post_file.stem,
                "content": clean_content,
                "metadata": {
                    "title": title,
                    "url": url,
                    "date": date,
                    "categories": metadata.get('categories', []),
                    "tags": metadata.get('tags', []),
                    "description": metadata.get('description', ''),
                    "source": "blog",
                    "source_file": str(post_file.relative_to(self.blog_posts_dir.parent.parent)),
                }
            }
        except Exception as e:
            log.error(f"解析文章失败 {post_file}: {e}")
            return None

    def _generate_post_url(self, post_file: Path, metadata: Dict[str, Any]) -> str:
        """
        生成文章 URL。

        Args:
            post_file: 文章文件路径
            metadata: 文章元数据

        Returns:
            文章 URL
        """
        # 优先使用 front matter 中的 permalink（如果存在）
        if metadata.get("permalink"):
            permalink = metadata["permalink"]
            # 确保 permalink 以 / 开头
            if not permalink.startswith("/"):
                permalink = "/" + permalink
            # 确保 permalink 以 / 结尾
            if not permalink.endswith("/"):
                permalink = permalink + "/"
            return permalink
        
        # Hexo permalink 规则: :title/
        # Hexo 的 :title 使用的是完整的文件名（去掉扩展名），而不是只提取标题部分
        # 例如：2026-01-26-localhost-wifi-access-guide.md -> /2026-01-26-localhost-wifi-access-guide/
        filename = post_file.stem  # 去掉扩展名，例如：2026-01-26-localhost-wifi-access-guide
        return f"/{filename}/"

    def _clean_markdown(self, content: str) -> str:
        """
        清理 Markdown 内容，转换为纯文本。

        Args:
            content: Markdown 内容

        Returns:
            清理后的纯文本
        """
        # 移除代码块
        content = re.sub(r'```[\s\S]*?```', '', content)
        content = re.sub(r'`[^`]+`', '', content)
        
        # 移除链接但保留文本 [text](url) -> text
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        
        # 移除图片 ![alt](url) -> alt
        content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', content)
        
        # 移除标题标记
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
        
        # 移除粗体和斜体标记
        content = re.sub(r'\*\*([^\*]+)\*\*', r'\1', content)
        content = re.sub(r'\*([^\*]+)\*', r'\1', content)
        content = re.sub(r'__([^_]+)__', r'\1', content)
        content = re.sub(r'_([^_]+)_', r'\1', content)
        
        # 移除列表标记
        content = re.sub(r'^\s*[-*+]\s+', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*\d+\.\s+', '', content, flags=re.MULTILINE)
        
        # 移除引用标记
        content = re.sub(r'^>\s+', '', content, flags=re.MULTILINE)
        
        # 移除水平线
        content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)
        
        # 清理多余的空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content.strip()

    def _parse_frontmatter(self, content: str) -> tuple[Dict[str, Any], str]:
        """
        解析 Markdown 文件的 front matter。

        Args:
            content: 文件内容

        Returns:
            (metadata, body) 元组
        """
        # 检查是否有 front matter（以 --- 开头）
        if not content.startswith('---'):
            return {}, content

        # 查找第二个 ---
        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content

        frontmatter_text = parts[1].strip()
        body = parts[2].strip()

        # 清理模板变量（如 {{current_date_time}}）
        frontmatter_text = re.sub(r'\{\{[^}]+\}\}', '', frontmatter_text)

        # 解析 YAML
        try:
            metadata = yaml.safe_load(frontmatter_text) or {}
        except Exception as e:
            log.warning(f"解析 frontmatter 失败: {e}")
            metadata = {}

        return metadata, body

    def get_blog_categories(self) -> List[Dict[str, Any]]:
        """
        获取博客分类列表（用于兼容 get_wiki_spaces API）。

        Returns:
            分类列表
        """
        categories = set()
        
        if not self.blog_posts_dir.exists():
            return []

        # 遍历所有 Markdown 文件，收集分类
        for post_file in self.blog_posts_dir.glob("*.md"):
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                metadata, _ = self._parse_frontmatter(content)
                post_categories = metadata.get('categories', [])
                
                # 处理嵌套分类（如 ["技术学习与行业趋势", "学习与工具"]）
                if isinstance(post_categories, list):
                    for cat in post_categories:
                        if isinstance(cat, str):
                            categories.add(cat)
                        elif isinstance(cat, list):
                            categories.update(cat)
            except Exception:
                continue

        # 转换为列表格式，兼容 WikiSpacesResponse
        return [
            {
                "space_id": cat,
                "name": cat,
                "description": f"博客分类: {cat}",
            }
            for cat in sorted(categories)
        ]

