---
title: 从 Fiddler 到 Charles：Windows 切换到 Mac 的抓包实践分享 🍎
date: 2025-12-25 18:00:00

tags:
  - Fiddler
  - Charles
  - 抓包工具
  - Mac
  - Windows
  - HTTPS
  - 工具迁移
categories:
  - 📡 抓包与网络调优：Fiddler & Charles 实战指南
  - 测试经验与落地
updated: {{current_date_time}}
keywords: Fiddler, Charles, 抓包工具, Mac, Windows, HTTPS, 工具迁移, 抓包实践
description: '从 Windows + Fiddler 切换到 Mac + Charles 的真实抓包迁移记录。实践路径 + 易踩坑点 + 工具差异理解，适合刚换 Mac、需要抓包的测试/开发同学。'
top_img: /img/fiddler-to-charles.png
cover: /img/fiddler-to-charles.png
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

# 从 Fiddler 到 Charles：Windows 切换到 Mac 的抓包实践分享 🍎

从 Windows + Fiddler 切换到 Mac + Charles 的一次真实抓包迁移记录。本文不追求"最全教程"，而是更偏向 **实践路径 + 易踩坑点 + 工具差异理解**，适合刚换 Mac、需要抓包的测试 / 开发同学。

> 💡 **本文适合谁？**
> * 从 Windows 切换到 Mac 的测试/开发同学
> * 熟悉 Fiddler，想快速上手 Charles 的读者
> * 在 Mac 上抓包遇到问题的同学

---

## 一、背景：从熟悉到不熟悉的工具迁移

在使用 Windows 期间，我一直用 **Fiddler** 进行抓包：

* 抓 HTTP / HTTPS 接口
* 查看请求参数、响应数据
* 辅助定位联调与线上问题

最近更换为 **Mac 电脑** 后，原有的工具链需要整体迁移。在 Mac 平台上，抓包工具的主流选择是 **Charles**，因此也开始了一轮新的学习过程。

这篇文章主要记录：

* Windows 与 Mac 在抓包使用上的一些差异
* Charles 的基础安装与核心配置
* HTTPS 抓包中最容易遇到的问题与理解误区

---

## 二、Windows vs Mac：抓包时最明显的几个差异

### 1️⃣ 抓包工具生态不同

| 平台      | 常用抓包工具                     |
| ------- | -------------------------- |
| Windows | Fiddler、Wireshark          |
| Mac     | Charles、Proxyman、Wireshark |

如果你之前长期使用 Fiddler：

* 在 Mac 上并不是不能用，但体验和维护成本都偏高
* Charles 是 Mac 平台上更成熟、稳定的选择

---

### 2️⃣ 查本机 IP 的方式不同（抓手机包时尤为重要）

抓手机包时，需要让手机的代理指向 **电脑的局域网 IP**。这一点在 Windows 和 Mac 上的操作方式差异比较明显。

#### Windows

```bash
ipconfig
```

通常直接查看：

* IPv4 Address

---

#### Mac（推荐方式）

**图形界面方式（最不容易出错）**：

```
系统设置 → 网络 → 当前连接的网络 → 详情
```

查看其中的 **IPv4 地址**，该地址就是手机代理需要填写的 IP。

---

#### Mac（命令行方式，工程师常用）

```bash
ifconfig | grep "inet"
```

**输出示例**：

```
inet 127.0.0.1 netmask 0xff000000
inet 192.168.1.100 netmask 0xffffff00 broadcast 192.168.1.255
```

需要注意：

* ❌ 忽略 `127.0.0.1`（回环地址，不能给手机使用）
* ✅ 选择局域网地址（如 `192.168.x.x`、`10.x.x.x`）
* ✅ 一般位于 `en0`（Wi‑Fi 网卡）下

这一点如果不加说明，很容易在配置手机代理时选错 IP。

> 💡 **小技巧**：如果连接了多个网络（如同时连接 Wi-Fi 和以太网），优先选择 Wi-Fi 的 IP 地址。

---

### 3️⃣ 证书信任机制的差异

这是从 Windows 切换到 Mac 后，**最容易踩坑的一点**：

* 在 Windows + Fiddler 环境下，HTTPS 抓包的证书配置相对"无感"
* 在 Mac + Charles 下，**证书必须手动设为"始终信任"**

如果证书未正确配置，常见现象包括：

* HTTPS 请求抓不到
* Charles 中请求显示为 `<unknown>`
* 浏览器或 App 报 SSL 错误

---

## 三、Charles 安装与基础配置流程

### 1️⃣ 安装 Charles

* 官网：[https://www.charlesproxy.com](https://www.charlesproxy.com)
* 提供 Mac / Windows / Linux 版本

安装完成后，启动 Charles，会看到一个空的抓包主界面。

---

### 2️⃣ 确认系统代理已生效

Charles 默认监听端口：

* HTTP Proxy：**8888**

启动 Charles 后，可在菜单中确认：

```
Proxy → macOS Proxy → Enabled
```

如果系统代理未生效，浏览器流量将不会经过 Charles。

---

### 3️⃣ HTTPS 抓包的关键：开启 SSL Proxying

新手最常见的问题是：

* 只能看到 `CONNECT` 请求
* 接口路径显示为 `<unknown>`

根本原因是：

> **HTTPS 流量未被 Charles 解密**

#### 配置方式

```
Proxy → SSL Proxying Settings
```

* 勾选：`Enable SSL Proxying`
* 在 Include 中添加需要抓包的域名，例如：

```
Host: dev.example.com
Port: 443
```

建议只添加实际需要抓的域名，而不是使用通配符 `*`。

---

### 4️⃣ 安装并信任 Charles 根证书（Mac 必做）

#### 安装证书

```
Help → SSL Proxying → Install Charles Root Certificate
```

证书会被安装到系统的「钥匙串访问」。

#### 设为"始终信任"

1. 打开「钥匙串访问」
2. 找到 `Charles Proxy CA`
3. 双击 → 展开「信任」
4. 设置为：**始终信任**

这是 HTTPS 能否成功解密的关键一步。

---

## 四、常见问题与实践中的踩坑点

### ❓ 请求为什么显示为 `<unknown>`？

* HTTPS 未开启 SSL Proxying
* 域名未加入 Include 列表

解决思路：

* 检查 SSL Proxying 是否开启
* 确认 Host / Port 配置正确

---

### ❓ 浏览器能访问，但 Charles 抓不到？

建议按以下顺序排查：

1. Charles 是否在运行
2. 系统代理是否生效
3. 是否被 VPN / 代理规则绕过

---

### ❓ 手机 App 抓不到包？

常见原因包括：

1. **手机未正确配置代理**
   * 检查手机 Wi-Fi 设置中的代理配置
   * 确认 IP 地址和端口（8888）正确

2. **手机未安装 / 信任 Charles 证书**
   * 在 Charles 中：`Help → SSL Proxying → Install Charles Root Certificate on a Mobile Device or Remote Browser`
   * 手机浏览器访问 `chls.pro/ssl` 下载证书
   * iOS：设置 → 通用 → 关于本机 → 证书信任设置 → 信任 Charles Proxy CA
   * Android：设置 → 安全 → 加密与凭据 → 从存储设备安装

3. **App 使用了 SSL Pinning**
   * 这是更高阶场景，需要额外处理（如使用 Xposed、Frida 等工具）

> 💡 **排查顺序**：先确认代理配置 → 再检查证书 → 最后考虑 SSL Pinning

---

## 五、从 Fiddler 到 Charles：使用体验上的变化

| 维度       | Fiddler | Charles   |
| -------- | ------- | --------- |
| 上手难度     | 较低      | 中等        |
| HTTPS 配置 | 相对自动    | 需要理解与手动配置 |
| 界面体验     | 偏工程化    | 更直观       |
| 跨平台能力    | 一般      | 较好        |

整体感受是：

* Fiddler 更"即插即用"
* Charles 更强调对 HTTPS 与代理机制的理解

一旦配置完成，Charles 在 Mac 环境下的稳定性和可控性都非常好。

---

## 六、参考资料与延伸阅读

在学习和配置 Charles 的过程中，我主要参考了以下资源，它们分别解决了不同层级的问题：

### 📖 配置与问题排查

* **Mac 下 Charles 抓包 HTTPS 详细配置与问题排查**（CSDN · ios_xumin）
  
  重点讲解 SSL Proxying、证书安装与信任，对理解 HTTPS 抓不到包、`<unknown>` 等问题非常有帮助。

### 🔬 原理深度解析

* **Charles 抓包原理与 HTTPS 解密机制解析**（博客园 · upstudy）
  
  从原理层解释 CONNECT 隧道、中间人证书与 TLS 解密流程，适合在"能用之后"补齐底层认知。

### 🛠️ 工具使用技巧

* **Mac 下使用 ifconfig 查看本机 IP 地址详解**（CSDN · gyueh）
  
  详细说明 `ifconfig` 输出中各类网卡与 IP 的含义，对抓手机包时避免误用 `127.0.0.1` 非常有参考价值。

### 📚 官方文档

* [Charles 官方文档](https://www.charlesproxy.com/documentation/)：Charles 的官方文档，包含完整的配置说明和 API 文档

---

## 七、结语

从 Windows 切换到 Mac，看似只是操作系统的变化，实际上也会带来一整套工具链和使用习惯的调整。

Charles 并不难，真正需要理解的是：

* HTTPS 为什么不能直接被看到
* 证书和代理在其中扮演的角色

当这些概念理清之后，抓包这件事会变得更加可控，也更有助于问题定位和沟通协作。

希望这篇从 **Fiddler 到 Charles** 的实践记录，能帮到同样处在迁移过程中的你。

---

## 📚 相关文章

如果你对抓包工具感兴趣，可以继续阅读：

* [Fiddler 入门与基础抓包 🕵️‍♂️](/项目实战与案例经验/测试经验与落地/2025-08-19-fiddler-getting-started-basic-capture/)
* [Fiddler 拦截与修改请求实战 🕵️‍♂️](/项目实战与案例经验/测试经验与落地/2025-08-22-fiddler-intercept-modify-requests/)
* [Fiddler 高级命令与过滤技巧 🚀](/项目实战与案例经验/测试经验与落地/2025-08-24-fiddler-advanced-commands-and-filters/)
* [Fiddler 移动端抓包与实战技巧 📱🕵️‍♂️](/项目实战与案例经验/测试经验与落地/2025-08-26-fiddler-mobile-capture-and-practical-tips/)

