---
title: 文章归档
date: 2024-01-01 00:00:00
type: "archives"
---

# 文章归档

<div class="archives-group">
  {% set currentYear = '' %}
  {% set currentMonth = '' %}
  {% for post in site.posts %}
    {% set postYear = post.date.format('YYYY') %}
    {% set postMonth = post.date.format('MM') %}
    
    {% if postYear != currentYear %}
      {% set currentYear = postYear %}
      {% set currentMonth = '' %}
      <h3 class="archives-year">{{ currentYear }}</h3>
    {% endif %}
    
    {% if postMonth != currentMonth %}
      {% set currentMonth = postMonth %}
      <h4 class="archives-month">{{ currentYear }}-{{ currentMonth }}</h4>
    {% endif %}
    
    <div class="archive-item">
      <time class="archive-date">{{ post.date.format('MM-DD') }}</time>
      <a href="{{ url_for(post.path) }}" class="archive-title">{{ post.title }}</a>
    </div>
  {% endfor %}
</div>

<style>
.archives-group {
  max-width: 800px;
  margin: 0 auto;
}
.archives-year {
  font-size: 1.8rem;
  color: #333;
  margin-top: 2rem;
  margin-bottom: 1rem;
  border-left: 4px solid #3eaf7c;
  padding-left: 10px;
}
.archives-month {
  font-size: 1.4rem;
  color: #666;
  margin-top: 1.5rem;
  margin-bottom: 0.8rem;
  padding-left: 14px;
}
.archive-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}
.archive-date {
  width: 80px;
  color: #999;
  font-size: 0.9rem;
  flex-shrink: 0;
}
.archive-title {
  color: #333;
  text-decoration: none;
  flex-grow: 1;
  padding-left: 1rem;
  transition: color 0.3s;
}
.archive-title:hover {
  color: #3eaf7c;
}
</style>