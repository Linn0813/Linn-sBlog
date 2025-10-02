---
title: Fiddler 移动端抓包与实战技巧 📱🕵️‍♂️
date: 2025-08-26 21:49:29
tags:
  - Fiddler
  - 抓包工具
  - 实战技巧
  - 移动端抓包
categories:
- 技术学习 & 行业趋势（Learning & Industry Trends）
  - 网络工具
  - 抓包技术
updated: {{current_date_time}}
keywords: Fiddler, 移动端抓包, 实战技巧
description: 'Fiddler 是一个功能强大的 HTTP/HTTPS 抓包工具，能拦截客户端和服务器之间的请求。本文将带你从零开始，详细掌握 Fiddler 移动端抓包与实战技巧，让你快速上手。'
top_img: /img/fiddler-mobile.png
cover: /img/fiddler-mobile.png
comments: true
toc: true
toc_number: true
toc_style_simple: false
copyright: true
copyright_author: yuxiaoling
copyright_info: 版权所有，转载请注明出处。
mathjax: false
katex: false
abcjs: false
aplayer: false
highlight_shrink: false
aside: true
noticeOutdate: false
---

# Fiddler 移动端抓包与实战技巧 📱🕵️‍♂️

前面三篇文章，我们学习了 Fiddler 的基础抓包、拦截修改请求以及高级命令与过滤技巧。本篇将深入讲解 **移动端抓包配置、HTTPS 抓包原理、App 请求调试、证书问题处理、性能分析及实战经验**，帮助你在实际工作中快速定位问题。

---

## 一、移动端抓包原理

移动端抓包与 PC 端类似，都是通过 **中间人代理（MITM）** 拦截请求与响应，但涉及移动端特有的 HTTPS、App 签名和证书 pinning 问题。

### 1. MITM 工作原理

1. 手机发起请求 → Fiddler 代理接收
2. Fiddler 解密 HTTPS（需安装根证书）
3. 可在 Fiddler 内修改请求或响应
4. 请求被转发到服务器 → 响应返回 Fiddler → 手机接收

> 🔍 注意：HTTPS 抓包必须安装 Fiddler 根证书，否则无法查看加密数据。

### 2. 常见抓包问题

* **证书 pinning**：部分 App 会验证证书，直接拒绝抓包请求
* **缓存干扰**：App 缓存可能导致抓包内容不更新
* **网络环境**：手机和 Fiddler 电脑必须在同一局域网

---

## 二、移动端抓包配置

### 1. 手机代理设置

1. 确保手机与电脑在同一 Wi-Fi
2. Wi-Fi → 配置代理 → 手动
3. IP 填写电脑 IP，端口 8888
4. 确保 Fiddler 开启 **允许远程连接**

### 2. 安装和信任证书

1. 手机浏览器访问 [http://ipv4.fiddler:8888](http://ipv4.fiddler:8888)
2. 下载并安装根证书
3. 系统设置 → 信任该证书

### 3. 注意事项

* iOS 系统需要在设置中启用完整信任
* Android 7+ 需要 App 信任用户证书
* 证书 pinning App 需要使用测试环境或关闭 pinning

> 💡 小技巧：安装证书前，先关闭 VPN 或代理，以避免网络冲突

---

## 三、抓包与分析移动端请求

1. 打开 App 执行操作
2. Fiddler 左侧 Session 列表显示请求
3. 使用 **Filters** 精准显示目标接口
4. 点击请求 → **Inspectors** 查看 Header、Body 和响应

### 实战示例

* 登录接口调试：POST 请求检查 Token
* 支付接口调试：验证请求参数和返回数据
* 异常接口测试：结合 Breakpoint 修改请求或响应

> 📖 场景分享：
> 调试支付模块时，发现某些请求返回空 Body，通过 Filters 精准筛选支付接口，结合 Breakpoint 修改 Header 测试权限，快速定位问题。

---

## 四、Breakpoint 与 AutoResponder 移动端应用

### 1. Breakpoint

* Session 右键 → **Break on Request / Response**
* 修改 Header 或 Body
* 点击 **Run to Completion** 发送请求

### 2. AutoResponder

* 添加规则匹配移动端接口 URL
* 返回本地 Mock 文件或自定义 JSON
* 支持延迟返回，模拟慢接口
* 支持正则匹配，精确控制生效请求

> 💡 实战技巧：
>
> * 模拟支付接口异常或慢接口
> * 模拟登录接口异常 JSON，验证 App 弹窗和重试逻辑
> * 团队统一测试数据，保证不同设备环境一致

---

## 五、Filters 高级技巧

### 1. 正则匹配 URL

* `.*login.*` 匹配登录接口
* `.*\.(jpg|png|css|js)$` 隐藏静态资源

### 2. 请求参数过滤

* Filters → Request Headers → Contains / Does not contain
* 精确抓取 POST Body 中包含关键字段的请求

### 3. 分场景过滤

* 配合 Breakpoint，先过滤目标接口，再修改数据
* 避免大量无关请求干扰

> 🔧 小技巧：
>
> * 调试支付模块只抓支付接口
> * 调试登录异常时使用正则匹配 URL

---

## 六、性能分析与优化

1. **Timeline 查看请求耗时**

   * 菜单栏 → Rules → Performance → Show Timeline
   * 识别慢请求，优化性能

2. **Filters 精准分析**

   * 排除静态资源干扰
   * 比较不同请求耗时，定位性能瓶颈

3. **Replay 重发请求**

   * 修改参数或 Header
   * 模拟不同场景下的耗时变化

> 📖 场景分享：
> 在移动端 App 性能调试中，通过 Timeline 和 Replay 发现某接口慢 2 秒，定位到数据库查询未加索引，最终优化接口响应。

---

## 七、团队协作与复盘

1. **导出抓包记录**

   * Session → Save → Selected Sessions → SAZ 文件
   * 便于同事复盘问题

2. **共享规则**

   * Filters 与 AutoResponder 可导出规则
   * 团队统一规则，提高调试一致性

3. **文档记录**

   * 每次操作记录 URL、请求参数、修改结果、问题原因
   * 形成团队知识库，降低新人上手成本

> 💡 建议：
>
> * 定期整理抓包经验和场景
> * 新人先学习团队共享规则，再进行实战

---

## 八、常见问题与解决方案

| 问题              | 解决方案                                |
| --------------- | ----------------------------------- |
| HTTPS 抓不到内容     | 安装 Fiddler 根证书，并信任                  |
| 证书 pinning 拦截失败 | 使用测试环境 App 或关闭 pinning              |
| 抓包过多杂乱          | 使用 Filters 精准匹配 URL / Host / Method |
| 请求被缓存           | 清理 App 缓存或使用 Replay 重发              |

---

## 九、总结与实践建议

通过本篇文章，你将掌握：

* 移动端抓包原理与代理配置
* HTTPS 抓包与证书安装方法
* Breakpoint 与 AutoResponder 移动端应用
* Filters 精准过滤和正则匹配技巧
* 性能分析与 Replay 测试
* 实战场景：登录、支付、权限调试
* 团队协作与复盘方法

> 🚀 系列总结：
>
> * 文章 1：Fiddler 基础抓包
> * 文章 2：拦截与修改请求
> * 文章 3：高级命令与过滤技巧
> * 文章 4：移动端抓包与实战技巧

结合四篇文章，你可以形成完整 Fiddler 技能体系，无论是 PC 端、移动端、接口调试、性能分析还是团队协作，都能高效完成抓包与调试工作。


