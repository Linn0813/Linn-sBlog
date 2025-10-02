---
title: Fiddler 高级命令与过滤技巧 🚀
date: 2025-08-24 21:49:14
tags:
  - Fiddler
  - 抓包工具
  - 高级命令
  - 过滤技巧
  - 正则匹配
  - 团队协作
  - 实战思路
categories:
- 技术学习 & 行业趋势（Learning & Industry Trends）
  - 网络工具
  - 抓包技术
updated: {{current_date_time}}
keywords: Fiddler, 高级命令, 过滤技巧, 正则匹配, 团队协作, 实战思路
description: 'Fiddler 是一个功能强大的 HTTP/HTTPS 抓包工具，能拦截客户端和服务器之间的请求。本文将带你从零开始，详细掌握 Fiddler 高级命令与过滤技巧，让你快速上手。'
top_img: /img/fiddler-advanced.png
cover: /img/fiddler-advanced.png
comments: true
toc: true
toc_number: true
toc_style_simple: false
copyright: true
copyright_author: yuxiaoling
copyright_info: 版权所有，转载请注明出处。
mathjax: false
katex: false
aplayer: false
highlight_shrink: false
aside: true
abcjs: false
noticeOutdate: false
---

# Fiddler 高级命令与过滤技巧 🚀

前两篇文章，我们学习了 Fiddler 的安装、基础抓包和拦截修改请求的操作。本篇将带你深入探索 **Fiddler 的高级命令、过滤技巧、正则匹配、团队协作方法和实战思路**，让抓包工作更高效、更系统化。

---

## 一、Fiddler 高级命令原理与作用

Fiddler 的高级命令不仅是快捷操作，更隐藏着抓包原理和调试逻辑：

| 快捷键 / 功能                              | 用途              | 原理/场景                           |
| ------------------------------------- | --------------- | ------------------------------- |
| CTRL+R                                | 重发请求            | 请求被重新发送到服务器，可修改后再次发送测试接口容错或权限问题 |
| CTRL+X                                | 清空会话列表          | 清理历史抓包记录，避免干扰分析                 |
| F5                                    | 刷新抓包            | 刷新显示最新抓包数据                      |
| CTRL+T                                | 打开 Filters 面板   | 快速定位过滤面板，提高抓包精确度                |
| CTRL+SHIFT+R                          | Replay 重发请求并可修改 | 用于批量调试请求或回放场景                   |
| Session 右键 → Breakpoint               | 拦截请求或响应         | 在请求或响应到达前暂停，便于修改数据              |
| Session 右键 → Unlock for Editing       | 解锁请求以修改         | 允许修改请求参数、Header 或 Body          |
| Session 右键 → Save → Selected Sessions | 导出抓包记录          | 便于团队共享或复盘                       |

> 🔍 小技巧：理解命令背后的原理比记快捷键更重要。例如 Breakpoint 是暂停数据流，而 AutoResponder 是自动替换响应，两者组合可模拟复杂业务场景。

---

## 二、Filters 高级用法

Filters 是 Fiddler 的核心功能之一，可以精准控制抓包结果，提升分析效率。

### 1. 基础过滤

* **Show only if URL contains** → 只显示关键接口
* **Hide if URL contains** → 隐藏无关请求
* **HTTP methods** → 只显示 GET / POST / PUT / DELETE
* **Hosts** → 指定域名抓包

### 2. 高级过滤技巧

* **正则匹配 URL**

  * 支持复杂规则：如 `.*login.*` 匹配 URL 包含 login 的请求
  * 示例：`.*\.(jpg|png|css|js)$` 隐藏静态资源
* **请求参数过滤**

  * Filters → Request Headers → Contains / Does not contain
  * 精确抓取 POST Body 中包含关键字段的请求
* **分场景过滤**

  * 结合 Breakpoint，先过滤目标接口，再拦截修改数据

> 📖 场景分享：
>
> * 在调试支付模块时，只抓取支付接口 URL，隐藏图片、JS、广告请求
> * 调试登录异常，使用正则匹配 URL，快速定位异常接口

---

## 三、AutoResponder 高级技巧

AutoResponder 可自动修改响应或重定向请求，常用于模拟各种测试场景：

1. **正则匹配 URL**

   * `.*api/v1/orders.*` 匹配所有订单接口
2. **重定向请求**

   * 可将请求重定向到本地 Mock 文件或测试服务器
3. **延迟响应**

   * 模拟慢接口，测试前端加载动画、重试逻辑
4. **条件生效**

   * 结合 Filters 使用，只在特定模块启用 AutoResponder

> 💡 实战示例：
>
> * 模拟支付接口延迟 5 秒
> * 模拟登录接口返回异常 JSON，验证前端异常提示
> * 团队统一测试数据，确保环境一致

---

## 四、团队协作与复盘技巧

1. **导出抓包记录**

   * Session → Save → Selected Sessions → SAZ 文件
   * 团队共享，便于问题复盘
2. **共享规则**

   * Filters 和 AutoResponder 可导出规则
   * 团队统一规则，提高调试一致性
3. **文档记录**

   * 记录抓包操作步骤、修改参数、模拟响应
   * 形成团队知识库，降低新人上手成本

> 🔧 小技巧：
>
> * 每次调试记录 URL、请求参数和修改结果
> * 团队共享 AutoResponder 文件，实现统一 Mock 场景

---

## 五、实战场景分享

1. **模拟异常接口**

   * 使用 AutoResponder 返回 HTTP 500 或自定义 JSON
   * 测试前端弹窗、重试逻辑和容错
2. **移动端权限调试**

   * 手机代理连接 Fiddler
   * Breakpoint 拦截请求，修改 Header 权限字段
   * 验证不同用户角色接口返回是否正确
3. **性能分析**

   * 使用 Timeline 查看请求耗时
   * 配合 Filters 精准分析慢接口
   * 排查网络瓶颈和前端渲染问题


---

## 六、实用技巧与注意事项

1. **精准抓包**：先确定目标接口，避免大量无关请求干扰
2. **组合使用**：Filters + Breakpoint + AutoResponder 提高调试效率
3. **安全操作**：HTTPS 抓包涉及敏感信息，建议在测试环境操作
4. **团队共享**：导出规则和抓包记录，形成知识沉淀
5. **文档记录**：每次操作写笔记，便于复盘和新人学习

---

## 七、总结

通过本篇文章，你将掌握：

* Fiddler 高级命令和快捷操作，提高抓包效率
* Filters 高级用法，正则匹配和分场景过滤
* AutoResponder 高级技巧，模拟异常和延迟响应
* 团队协作方法，共享规则与抓包记录
* 实战场景分析，结合前两篇形成完整 Fiddler 技能体系

> 💡 下一步建议：结合文章 1-3 技能，进入 **移动端抓包与实战技巧**，解决 App 抓包、证书 pinning、性能分析等高级问题，形成全方位调试能力。
