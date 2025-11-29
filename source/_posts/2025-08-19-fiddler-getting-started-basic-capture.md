---
title: Fiddler 入门与基础抓包 🕵️‍♂️
subtitle: 从零开始，轻松掌握HTTP/HTTPS网络请求拦截与分析
date: 2025-08-19 21:48:21
tags:
  - Fiddler
  - 抓包工具
  - HTTP/HTTPS
  - 中间人代理
  - 网络调试
  - 接口测试
  - 移动端抓包
categories:
  - 项目实战与案例经验
  - 测试经验与落地
updated: {{current_date_time}}
keywords: Fiddler, 抓包工具, HTTP/HTTPS, 中间人代理, 网络调试, 接口测试, 移动端抓包
description: 'Fiddler 是一个功能强大的 HTTP/HTTPS 抓包工具，能拦截客户端和服务器之间的请求。本文将带你从零开始，详细掌握 Fiddler 抓包基础，让你快速上手。'
top_img: /img/fiddler-guide.png
cover: /img/fiddler-guide.png
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

# Fiddler 入门与基础抓包 🕵️‍♂️

在工作中，我们经常需要调试网络请求，查看接口返回是否正确，分析数据异常原因。Fiddler 是一款功能强大的 HTTP/HTTPS 抓包工具，既能抓取浏览器请求，也能抓取移动端 App 请求。本文将带你从零开始，详细掌握 Fiddler 抓包基础，让你快速上手。

---

## 一、Fiddler 是什么？

Fiddler 是一个 **中间人代理（Man-in-the-Middle Proxy）** 工具，能拦截客户端和服务器之间的 HTTP/HTTPS 请求。

它可以帮助你：

1. **抓包**：查看请求 URL、请求方法、Header、Body 以及响应内容
2. **分析**：判断接口是否返回正确，排查参数错误或异常数据
3. **调试**：模拟接口异常或修改请求参数测试系统容错
4. **统计性能**：查看请求耗时，定位性能瓶颈

> ⚡ 小贴士：理解原理很重要。Fiddler 会作为中间人，让你的请求先到 Fiddler，再由 Fiddler 转发到服务器，因此可以拦截并修改请求和响应。

---

## 二、安装与基础配置

### 1. 下载与安装

* 官网：[https://www.telerik.com/fiddler](https://www.telerik.com/fiddler)
* 支持 Windows 和 macOS
* 安装完成后，打开 Fiddler

### 2. 配置抓取 HTTPS 请求

默认情况下，Fiddler 只能抓 HTTP 请求，要抓 HTTPS，需要安装证书：

1. 菜单栏：**Tools → Options → HTTPS**
2. 勾选 **Decrypt HTTPS traffic**
3. 点击 **Actions → Install Fiddler Root Certificate**
4. 浏览器或系统信任证书

> 🔒 安全提示：抓 HTTPS 请求时会看到敏感信息，如账号密码，请在测试环境操作，避免泄露生产数据。

### 3. 配置抓取特定域名（可选）

* 打开 **Filters** 面板
* 勾选 **Use Filters**
* 设置：

  * **Show only if URL contains** → 只抓取包含关键字的请求
  * **Hide if URL contains** → 隐藏不关心的请求

> 💡 经验分享：初学者抓包时建议只抓一个模块的请求，否则 Session 列表太多会很乱。

---

## 三、基础抓包操作

### 1. 抓包步骤

1. 打开 Fiddler
2. 确保浏览器或 App 通过 Fiddler 代理（默认端口 8888）
3. 执行操作（如访问页面、点击按钮、发送请求）
4. Fiddler 左侧 Session 列表显示抓到的请求

### 2. 查看请求和响应

点击任意请求，在右侧 **Inspectors** 面板查看：

* **Headers**：请求和响应头
* **Raw**：原始请求和响应文本
* **WebForms**：POST 参数可视化显示
* **JSON / TextView**：解析 JSON 数据

> 📖 场景示例：
> 在调试登录接口时，返回 401 错误。打开 Inspectors，发现 Header 中缺少 Authorization Token，通过修改请求参数重新发送，问题解决。

### 3. 导出抓包数据

* 右键请求 → **Save → Selected Sessions**
* 保存为 SAZ 文件，可分享给团队或复盘

---

## 四、移动端抓包配置

### 1. 设置手机代理

* 手机与 Fiddler 所在电脑同一 Wi-Fi
* Wi-Fi 设置 → 配置代理 → 手动
* IP 填写电脑 IP，端口 8888

### 2. 安装信任证书

* 手机浏览器访问 [http://ipv4.fiddler:8888](http://ipv4.fiddler:8888)
* 下载并信任 Fiddler Root Certificate

### 3. 抓取 App 请求

* 打开 App 执行操作
* Fiddler 会抓取所有 HTTP/HTTPS 请求
* 可使用 Filters 或搜索关键字，只查看感兴趣接口

> 🔧 提示：部分 App 会使用证书 pinning，需要额外工具或调试环境才能抓到请求。

---

## 五、基础技巧与常用命令

### 1. 常用快捷操作

| 快捷键                     | 功能      |
| ----------------------- | ------- |
| CTRL+R                  | 重发请求    |
| CTRL+X                  | 清空会话列表  |
| F5                      | 刷新抓包    |
| Session 右键 → Breakpoint | 暂停请求或响应 |

### 2. 使用 Filters 管理请求

* Show only if URL contains → 精确抓取目标接口
* Hide if URL contains → 隐藏无关请求
* HTTP methods → 只显示 GET / POST 请求

### 3. 导出与分析

* 保存抓包结果为 SAZ 文件
* 团队复盘或问题排查可直接打开 SAZ 分析

---

## 六、实践经验

1. **明确抓包目标**

   * 先确定调试接口或模块，避免 Session 列表混乱

2. **记录分析步骤**

   * 遇到复杂问题，将抓包、修改、分析步骤写成笔记
   * 方便复盘或团队共享

3. **安全操作**

   * HTTPS 抓包涉及敏感数据
   * 修改请求和响应要在测试环境进行

4. **循序渐进**

   * 先抓浏览器请求
   * 再抓移动端 App
   * 逐步掌握 Filters、Breakpoint、AutoResponder 等高级功能

---

## 七、总结

通过本篇文章，你应该能够：

* 安装 Fiddler 并配置 HTTPS 抓包
* 抓取浏览器和移动端请求
* 查看请求 Header、Body、响应内容
* 使用 Filters 精确抓包
* 保存抓包记录，进行分析和复盘

> 💡 下一步建议：掌握基础抓包后，可以学习 **Fiddler 拦截与修改请求**，模拟异常接口、修改请求参数，提高测试覆盖率。


