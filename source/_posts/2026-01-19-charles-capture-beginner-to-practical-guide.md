---
title: 🐢 Charles 抓包工具从入门到实战使用教程
date: 2026-01-19 10:00:00
series: 🕵️‍♂️ Fiddler 抓包实战全攻略
tags:
  - Charles
  - 抓包工具
  - HTTPS
  - 接口调试
  - Mock
  - 弱网
  - 问题定位
categories:
  - 项目实战与案例经验
  - 测试经验与落地
updated: {{current_date_time}}
keywords: Charles, 抓包, HTTPS, 代理, 接口调试, Breakpoints, Rewrite, Map Local, Map Remote, Throttle, DNS Spoofing
description: '一篇从界面认识到高频操作、再到实战排查的 Charles 抓包指南：抓得到、看得懂、改得动、能复现。'
top_img: /img/charles.png
cover: /img/charles.png
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

# 🐢 Charles 抓包工具从入门到实战使用教程

> 适合人群：
>
> - 测试工程师 / 测开
> - 后端 / 前端开发
> - 对网络请求、接口调试、问题定位感兴趣的同学

如果你在日常工作中遇到过下面这些问题：

- 🤔 接口到底有没有发请求？
- 🤔 请求参数对不对？
- 🤔 为什么前端/客户端显示异常，但后端说接口没问题？

那 **Charles** 基本是一个绕不开的工具。

这篇文章会从 **页面介绍 → 基础使用 → 常见操作 → 实战场景** 一步一步带你真正「用会」Charles，而不是只停留在“知道有这个工具”。

---

## 1️⃣ Charles 是什么？能解决什么问题？

**Charles 是一个 HTTP / HTTPS 抓包代理工具**，它可以：

- 捕获客户端发出的所有网络请求
- 查看请求 / 响应的详细内容
- 修改请求或响应（Mock / 调试神器）
- 重放请求、验证接口逻辑
- 模拟弱网、做“网络侧”的问题复现

📌 **一句话总结**：

> 只要是走网络的请求，理论上 Charles 都能看到。

---

## 2️⃣ Charles 的核心工作原理（先理解再使用）

在使用之前，先用一张“脑图”理解它的角色：

```
客户端  →  Charles（代理）  →  服务器
```

Charles 本质上是一个 **代理服务器（Proxy）**：

- 客户端把请求先发给 Charles
- Charles 再转发给真实服务器
- 响应返回时，再经过 Charles

📌 所以：

- **客户端必须配置代理**
- **HTTPS 需要额外的证书信任 + SSL Proxying 解密**

这一点非常重要，后面很多“抓不到包”的问题，本质都出在这里。

---

## 3️⃣ Charles 页面与功能区域详解（重点）

打开 Charles 后，你会看到这样一个界面，我们按区域来拆解。

### 3.1 顶部菜单栏（功能入口）

常用的几个菜单：

- **Proxy**
  - Proxy Settings（代理端口设置）
  - SSL Proxying Settings（HTTPS 抓包）
  - macOS Proxy / Windows Proxy（是否把系统代理切到 Charles）

- **Tools**
  - Rewrite（重写请求/响应）
  - Map Local / Map Remote（请求映射）
  - Breakpoints（断点/拦截）
  - DNS Spoofing（DNS 劫持到指定 IP）
  - Throttle Settings（弱网限速/延迟模拟）

- **Help**
  - SSL Proxying → Install Charles Root Certificate（安装根证书）
  - Install Charles Root Certificate on a Mobile Device…（手机/远程浏览器安装证书）

📌 初学阶段，你最常用的是：

> Proxy / Tools / Help

---

### 3.2 左侧区域（请求列表区）

左侧是 **抓到的所有请求列表**，默认以域名分类：

- 每一个域名 = 一个 Host
- 展开后是具体的请求路径

你可以在这里看到：

- 请求是否成功（状态码）
- 是否走 HTTPS
- 请求次数

📌 常见技巧：

- 请求太多时，可使用顶部 **Filter** 过滤关键词
- 右键 Host → `Focus`，只看一个域名（排查速度会快很多）

---

### 3.3 右侧区域（请求/响应详情区）

这是 **最核心、最常用** 的区域。

右侧一般分为两个大标签：

#### ▶ Request（请求）

- Method（GET / POST）
- URL
- Headers
- Query String / Body（重点看参数）

#### ▶ Response（响应）

- Status Code
- Headers
- Response Body（JSON / Text / 图片等）

📌 调试接口 80% 的时间，都在看这里。

---

## 4️⃣ 基础使用：抓 HTTP / HTTPS 请求

### 4.1 开启 Charles 代理

默认情况下，Charles 启动后代理是 **开启的**。

你可以在菜单栏确认：

> Proxy → macOS Proxy（或 Windows Proxy）

确保是勾选状态。

---

### 4.2 抓浏览器请求（最简单）

直接：

1. 打开 Charles
2. 用浏览器访问任意网站

如果左侧开始出现请求列表，说明抓包成功。

---

### 4.3 抓 HTTPS 请求（最容易卡住的部分）

很多同学第一次只能看到 `CONNECT`，或者请求路径显示 `<unknown>`，本质原因是 **HTTPS 没被解密**。

你之前那篇文章已经把安装、证书、移动端配置写得很完整，这里不再重复展开，建议先把“能抓到 HTTPS”这件事打通：

- [从 Fiddler 到 Charles：Windows 切换到 Mac 的抓包实践分享 🍎](/2025/12/25/2025-12-25-fiddler-to-charles-migration-guide/)

📌 快速记忆（只记结论）：

- **装并信任 Charles Root Certificate**
- **开启 SSL Proxying，并把目标域名加入 Include**

---

## 5️⃣ 抓包前的前置说明（已安装可跳过）

关于 **Charles 安装、证书配置、HTTPS 抓包原理**，你已经在之前的博客中写得非常完整，这里不再重复展开。

本文将 **重点放在「如何用 Charles 干活」** 上，而不是「怎么装」。

---

## 6️⃣ Charles 高频操作速查（按操作步骤整理）

本章开始 **不再解释功能背景**，只保留：

- 在哪点
- 怎么配
- 配完会看到什么

适合在真实调试场景中直接对照使用。

---

### 6.1 请求过滤（Filter）

#### ▶ 操作入口

- Charles 顶部工具栏 → `Filter`

#### ▶ 操作步骤

1. 点击 `Filter` 输入框
2. 输入域名或接口关键字，例如：

```
example.com
```

3. 回车

#### ▶ 操作结果

- 左侧请求列表只显示匹配的请求

---

### 6.2 Focus（只显示指定 Host / 请求）

#### ▶ 操作入口

- 左侧请求列表

#### ▶ 操作步骤

1. 在左侧找到目标 `Host` 或具体请求
2. 右键点击
3. 选择：`Focus`

#### ▶ 操作结果

- 左侧仅显示被 Focus 的请求

#### ▶ 取消 Focus

菜单栏：`View → Focused Host Only` 取消勾选

---

### 6.3 Breakpoints（拦截请求/响应）

#### ▶ 对单个请求加断点

1. 左侧找到目标请求
2. 右键 → `Breakpoints`

#### ▶ 断点触发后的操作

1. 客户端再次发起该请求
2. Charles 弹出拦截窗口
3. 在窗口中按需修改：
   - Query 参数
   - Request Body
   - Header（例如 token、traceId、tenant）
4. 点击 `Execute / Continue`

#### ▶ 常见注意点

- 请求“卡住”时，先检查是不是忘了关断点（尤其是对 Host 加了断点）
- 断点也可以用于 **拦截响应**（验证前端容错、模拟异常字段更直观）

---

### 6.4 Rewrite（自动修改请求 / 响应）

#### ▶ 新建 Rewrite 规则

1. `Tools → Rewrite`
2. 勾选 `Enable Rewrite`
3. 点击 `Add`

#### ▶ 配置 URL 匹配条件

1. 设置 `Host`（域名或 `*`）
2. 设置 `Path`（接口路径）
3. 保存

#### ▶ 配置修改内容

1. 选择 `Modify Request` 或 `Modify Response`
2. 选择修改位置（Header / Body 等）
3. 填写替换内容
4. 保存规则

📌 使用建议：

- 先用 Breakpoints 试验“改哪个字段有效”
- 再用 Rewrite 固化成自动规则（更稳定、更省时间）

---

### 6.5 Map Local / Map Remote（请求映射）

#### ▶ Map Local（映射本地文件，做本地 Mock）

1. 右键目标请求 → `Map Local`
2. 选择本地文件
3. 确认

#### ▶ Map Remote（转发到其他服务器，快速切环境）

1. 右键目标请求 → `Map Remote`
2. 输入目标服务器地址（如把 `api.prod.com` 映射到 `api.test.com`）
3. 保存

---

### 6.6 Block（屏蔽请求）

#### ▶ 操作步骤

1. 左侧请求列表中右键请求或 Host
2. 点击：`Block`

#### ▶ 操作结果

- 该请求后续将直接失败（用于验证“接口失败时前端/客户端怎么表现”）

---

### 6.7 Repeat / Repeat Advanced（重放请求，验证幂等与边界）

> 这是很多同学“会抓包但不会用”的分水岭功能：**能否把一次请求复现出来**。

#### ▶ 操作入口

- 左侧选中目标请求 → 右键菜单里 `Repeat` / `Repeat Advanced`（不同版本名称可能略有差异）

#### ▶ 操作步骤

1. 选中要重放的请求（建议选择业务接口，不要选静态资源）
2. 右键 `Repeat`（或 `Repeat Advanced`）

#### ▶ 操作结果

- Charles 会再次向服务器发起同样的请求
- 左侧会出现一条新的会话记录（方便对比响应差异）

#### ▶ 常见用途

- 验证接口 **幂等**（重复提交是否会创建重复订单）
- 验证 **token/签名** 是否过期
- 对比不同参数的响应差异（配合 Breakpoints 修改后再 Repeat）

---

### 6.8 Compose（手动构造请求，替代 Postman 的“临时场景”）

> 当你想“从抓到的请求出发，改一点字段就发出去”，Compose 特别顺手。

#### ▶ 操作入口

- 选中请求 → 右键 `Compose`

#### ▶ 操作步骤

1. 把抓到的请求发送到 Compose 面板
2. 修改 URL / Query / Headers / Body
3. 点击发送（不同版本按钮文案可能为 `Execute` / `Send`）

#### ▶ 操作结果

- Charles 会发送你手动构造的请求，并显示响应

#### ▶ 常见用途

- 快速验证“某字段改成 X 会怎样”
- 复现线上问题时，替换成测试环境域名（也可用 Map Remote）
- 模拟非法参数（空值、超长、特殊字符）看服务端兜底

---

### 6.9 Throttle（弱网模拟：限速/延迟/丢包感知）

> 非常适合排查“我这边加载很慢”“偶现白屏”“图片/接口超时”这类问题。

#### ▶ 操作入口

- `Proxy → Throttle Settings`（或 `Tools → Throttle Settings`，取决于版本）

#### ▶ 操作步骤

1. 勾选 `Enable Throttling`
2. 选择一个预设（如 3G/4G）或自定义带宽/延迟
3. 让业务重新走一遍

#### ▶ 操作结果

- 请求明显变慢，你可以观察：
  - 前端 loading 是否正确
  - 超时重试是否生效
  - 首屏是否有骨架/占位

#### ▶ 常见注意点

- 弱网模拟容易影响全局网络体验，用完记得关闭
- 建议配合 `Focus + Filter`，否则列表会刷得很快

---

### 6.10 DNS Spoofing（把域名“劫持”到指定 IP）

> 常用在：同域名切不同机房/不同环境、排查 DNS 污染、验证某台机器问题。

#### ▶ 操作入口

- `Tools → DNS Spoofing`

#### ▶ 操作步骤

1. 勾选 `Enable DNS Spoofing`
2. 添加规则：
   - Host：`api.example.com`
   - IP Address：`10.0.0.12`
3. 确认保存

#### ▶ 操作结果

- 当客户端访问 `api.example.com` 时，会被解析到你指定的 IP

#### ▶ 常见注意点

- 这是“强干预”功能，建议仅在测试环境/自用环境使用
- 如果你已经用 VPN/系统 Hosts 文件改过解析，优先统一管理方式，避免相互干扰

---

### 6.11 清理/保存/导出会话（便于复盘与协作）

> 抓包不是“抓完就结束”，真正有价值的是：**把证据带走**。

#### ▶ 清理会话

- 菜单栏：`Edit → Clear`（或工具栏的清空按钮）

#### ▶ 保存会话（用于复盘/发给同事）

1. 选中一条或多条会话（可按住 `Cmd/Ctrl` 多选）
2. 右键 `Save`（或 `File → Save Session`）

#### ▶ 操作结果

- 你会得到一个会话文件，可用于：
  - 复盘问题（对比请求/响应）
  - 团队协作（把“证据链”发给开发/后端/客户端）

---

## 7️⃣ 调试时的常用组合操作（更贴近干活）

### 组合一：Filter + Focus（把“噪音”降到最低）

1. 先使用 `Filter` 输入域名/关键字
2. 对目标 Host 右键 `Focus`

效果：你会感觉 Charles “突然变得很好用”。

---

### 组合二：Breakpoints → 验证 → Rewrite（从试验到固化）

1. 先用 Breakpoints 验证：改哪个参数/字段能复现或修复问题
2. 确认后使用 Rewrite 固化规则（省去每次手改）

---

### 组合三：Repeat + Throttle（复现“弱网/偶现”问题）

1. 先用 Repeat 确保请求可以稳定复现
2. 再开 Throttle 模拟弱网
3. 观察：超时、重试、loading、缓存、首屏等表现

---

### 组合四：Map Remote + DNS Spoofing（快速定位“环境/机器差异”）

1. Map Remote：把同一个请求打到不同环境
2. DNS Spoofing：把域名固定解析到某一台机器
3. 对比响应/耗时/错误率，快速缩小问题范围

---

## 8️⃣ 使用过程中的常见问题（更细一点）

- **请求卡住**：先检查是否开启了 Breakpoints（尤其是对 Host 级别加了断点）
- **看不到请求**：检查是否仍处于 Focus 模式、Filter 是否过于严格
- **Rewrite 不生效**：确认规则是否 `Enable`，以及 URL 匹配条件（Host/Path）是否真的匹配到了
- **只能看到 CONNECT / <unknown>**：检查 SSL Proxying 是否开启、目标域名是否加入 Include、证书是否“始终信任”
- **抓不到某些请求（尤其是浏览器）**：可能走了 HTTP/3/QUIC 或者有系统/浏览器代理绕过策略；可先临时关闭相关特性再验证（排查思路优先：代理是否生效 → HTTPS 是否解密 → 是否被绕过）

---

## 9️⃣ 总结

本文不覆盖安装与证书配置细节，仅聚焦 **Charles 的实际操作路径**：抓得到、看得懂、改得动、能复现。

建议你在真实调试过程中：

- 先用 `Filter + Focus` 把噪音降到最低
- 用 `Breakpoints` 验证“改什么有效”
- 用 `Rewrite / Map Local / Map Remote` 把规则沉淀下来
- 用 `Repeat / Compose / Throttle / DNS Spoofing` 把问题稳定复现、定位到可行动的结论

