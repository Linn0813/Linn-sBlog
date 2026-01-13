#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 sitemap.xml 中的重复 URL（.html 和 /index.html 版本）
在 hexo generate 后自动运行
"""

import xml.etree.ElementTree as ET
import sys
import os

sitemap_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'public', 'sitemap.xml')

if not os.path.exists(sitemap_path):
    print('sitemap.xml 不存在，跳过修复')
    sys.exit(0)

print('正在修复 sitemap.xml 中的重复 URL...')

try:
    # 读取 sitemap
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    original_count = len(urls)

    # 提取所有 URL
    url_elements = []
    for url in urls:
        loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        if loc is not None:
            url_elements.append((loc.text, url))

    # 找出重复的 URL（.html 和 /index.html）
    to_remove = set()
    url_texts = [url_text for url_text, _ in url_elements]

    for url_text, url_elem in url_elements:
        # 如果是 .html 结尾（但不是 /index.html），检查是否有对应的 /index.html 版本
        if url_text.endswith('.html') and not url_text.endswith('/index.html'):
            base = url_text.replace('.html', '')
            index_version = base + '/index.html'
            # 如果存在 /index.html 版本，标记 .html 版本为删除
            if index_version in url_texts:
                to_remove.add(url_text)

    # 移除重复的 URL，并重新创建标准格式的元素
    new_root = ET.Element('urlset')
    new_root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    kept_count = 0
    for url_text, url_elem in url_elements:
        if url_text not in to_remove:
            # 创建新的 URL 元素（不使用命名空间前缀）
            new_url = ET.SubElement(new_root, 'url')
            
            # 复制子元素
            loc = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc is not None:
                ET.SubElement(new_url, 'loc').text = loc.text
            
            lastmod = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
            if lastmod is not None:
                ET.SubElement(new_url, 'lastmod').text = lastmod.text
            
            changefreq = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}changefreq')
            if changefreq is not None:
                ET.SubElement(new_url, 'changefreq').text = changefreq.text
            
            priority = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}priority')
            if priority is not None:
                ET.SubElement(new_url, 'priority').text = priority.text
            
            kept_count += 1

    # 保存新的 sitemap
    new_tree = ET.ElementTree(new_root)
    ET.indent(new_tree, space='  ')

    # 写入文件（使用正确的 XML 声明）
    with open(sitemap_path, 'wb') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode('utf-8'))
        ET.indent(new_tree, space='  ')
        new_tree.write(f, encoding='utf-8', xml_declaration=False)

    print(f'✓ 已修复 sitemap.xml')
    print(f'  - 原始 URL 数量: {original_count}')
    print(f'  - 删除重复 URL: {len(to_remove)}')
    print(f'  - 保留 URL 数量: {kept_count}')

except Exception as e:
    print(f'✗ 修复失败: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)

