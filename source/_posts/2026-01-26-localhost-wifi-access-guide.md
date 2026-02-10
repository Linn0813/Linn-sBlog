---
title: "同一 Wi‑Fi 访问本地服务：网络模型、配置方式与边界说明"
date: 2026-01-26 10:00:00
updated: {{current_date_time}}
permalink: 2026/01/26/localhost-wifi-access-guide/
categories:
  - 🏗️ 测试平台开发实战手记
  - 技术科普
tags:
  - 网络
  - 本地开发
  - CORS
  - 前后端联调
keywords: localhost, 局域网访问, Wi-Fi, 0.0.0.0, CORS, 前后端联调, 本地开发, 网络模型
description: '本文说明在同一 Wi‑Fi（同一局域网）内，其他设备如何访问你本机启动的 Web 服务，以及这件事在网络层面如何成立。先说明访问模型和地址角色，再给出最小可行配置，最后列出常见失效位置与边界问题（含 CORS）。'
top_img: /img/localhost-wifi-access-guide.png
cover: /img/localhost-wifi-access-guide.png
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
noticeOutdate: false
---

本文解决：

> **在同一 Wi‑Fi（同一局域网）内，其他设备如何访问你本机启动的 Web 服务，以及这件事在网络层面到底是如何成立的。**

* 先说明访问模型和地址角色
* 再给出最小可行配置
* 最后列出常见失效位置与边界问题（含 CORS）

---

## 1. 本地服务的访问模型

### 1.1 回环地址（localhost / 127.0.0.1）

`localhost`（`127.0.0.1`）是**回环地址**，含义只有一个：

> **当前这台机器自己。**

访问回环地址时，请求不会经过网卡，也不会进入局域网。

因此：

* 你在电脑上访问 `localhost:3000` → 访问的是你自己的电脑
* 其他设备访问 `localhost:3000` → 访问的是它们自己

结论：**回环地址天生不支持跨设备访问。**

---

### 1.2 对外监听地址（0.0.0.0）

`0.0.0.0` 不是一个真实 IP，而是一个**监听语义**：

> **监听当前机器上的所有网络接口。**

当服务监听在 `0.0.0.0` 上时，才有可能：

* 通过局域网 IP 被其他设备访问
* 被端口转发、内网穿透等机制使用

如果服务只监听在 `127.0.0.1`，即使你知道局域网 IP，外部设备也无法访问。

---

### 1.3 局域网 IP（192.168.x.x / 10.x.x.x）

局域网 IP 是：

> **其他设备在同一 Wi‑Fi 中找到你的"地址"。**

在同一网段内，访问路径始终是：

```
其他设备 → 你的局域网 IP → 端口 → 本地服务
```

---

## 2. 同一 Wi‑Fi 访问成立的必要条件

在工程实践中，要让"同一 Wi‑Fi 访问本地服务"成立，必须同时满足以下条件：

1. 服务监听在 `0.0.0.0`
2. 访问使用的是本机的局域网 IP + 端口
3. 两台设备在同一网段，且未开启设备隔离
4. 本机防火墙允许端口入站

其中，**监听地址错误**是最常见的问题来源。

---

## 3. 最小可行配置（MVP）

如果你只关心"如何尽快让别人访问到"，可以按以下最小路径配置：

1. 查到本机局域网 IP（如 `192.168.1.10`）
2. 启动服务时监听 `0.0.0.0`
3. 使用 `http://192.168.1.10:端口` 访问

只要本机用该地址能访问成功，其他设备在同一 Wi‑Fi 下通常也可以访问。

---

## 3.1 完整实操步骤（新手友好版）

下面用一个完整的例子，手把手走一遍流程。

### Step 1：查看本机局域网 IP

#### Windows

1. 按 `Win + R`，输入 `cmd`，回车
2. 在命令行输入：`ipconfig`
3. 找到 `无线局域网适配器 WLAN` 或 `以太网适配器` 下的 `IPv4 地址`
4. 记下这个 IP，例如 `192.168.1.10`

#### macOS

1. 打开终端（Terminal）
2. 输入：`ipconfig getifaddr en0`（Wi-Fi）或 `ipconfig getifaddr en1`（有线）
3. 记下输出的 IP，例如 `192.168.1.10`

#### Linux

1. 打开终端
2. 输入：`ip a` 或 `ifconfig`
3. 找到 `wlan0`（Wi-Fi）或 `eth0`（有线）下的 `inet` 地址
4. 记下 IP，例如 `192.168.1.10`

### Step 2：启动服务并监听 0.0.0.0

以 Vite 项目为例：

```bash
npm run dev -- --host
```

启动后，你应该能看到类似输出：

```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.1.10:5173/
```

注意：如果只看到 `Local` 而没有 `Network`，说明没有监听 `0.0.0.0`。

### Step 3：在本机验证

**关键验证步骤**：在本机浏览器打开 `http://192.168.1.10:5173`（用你实际的 IP 和端口）。

* 如果本机能打开 → 说明监听配置正确，可以继续
* 如果本机打不开 → 说明监听地址还是 `127.0.0.1`，需要检查配置

### Step 4：让其他设备访问

1. 确保手机/同事电脑和你连的是**同一个 Wi‑Fi**
2. 在手机浏览器输入：`http://192.168.1.10:5173`（用你实际的 IP 和端口）
3. 如果能看到页面，说明成功了

### 常见问题

**Q：本机用 `192.168.1.10:5173` 打不开怎么办？**

A：说明服务没有监听 `0.0.0.0`。检查：
* Vite：确认加了 `--host` 参数
* Express：确认 `app.listen(3000, '0.0.0.0')` 而不是 `app.listen(3000)`
* 其他框架：参考第 4 节的配置

**Q：本机能打开，但手机打不开？**

A：按第 5 节的排查顺序检查：
1. 防火墙是否拦截（最常见）
2. 是否在同一 Wi‑Fi
3. 是否有设备隔离

---

## 4. 常见技术栈的监听配置

下面仅列出**监听地址相关配置**，不涉及其他启动参数。

### 4.1 Vite

**方式 1：命令行参数**

```bash
npm run dev -- --host
```

**方式 2：配置文件**

在 `vite.config.ts` 中：

```ts
export default {
  server: {
    host: '0.0.0.0',
    port: 3000
  }
}
```

**验证**：启动后应该能看到 `Network: http://192.168.x.x:3000/` 的输出。

---

### 4.2 Create React App

**macOS / Linux：**

```bash
HOST=0.0.0.0 npm start
```

**Windows PowerShell：**

```powershell
$env:HOST="0.0.0.0"; npm start
```

**Windows CMD：**

```cmd
set HOST=0.0.0.0 && npm start
```

**验证**：启动后应该能看到类似 `On Your Network: http://192.168.x.x:3000` 的输出。

---

### 4.3 Node / Express

```js
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World');
});

// 关键：第二个参数指定监听地址
app.listen(3000, '0.0.0.0', () => {
  console.log('Server running on http://0.0.0.0:3000');
});
```

**验证**：在本机浏览器访问 `http://你的局域网IP:3000`，应该能打开。

---

### 4.4 Flask

**方式 1：命令行**

```bash
flask run --host=0.0.0.0 --port=5000
```

**方式 2：代码中**

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**验证**：启动后应该能看到类似 `Running on http://0.0.0.0:5000` 的输出。

---

### 4.5 Spring Boot

默认监听所有网卡（`0.0.0.0`），一般无需额外配置。

如果曾修改过 `application.properties` 或 `application.yml`，检查是否有：

```properties
# 错误示例（只监听本机）
server.address=127.0.0.1

# 正确：删除这行或改为 0.0.0.0
server.address=0.0.0.0
```

**验证**：启动日志中应该能看到 `Tomcat started on port(s): 8080 (http)`，而不是 `127.0.0.1:8080`。

---

## 5. 常见失效位置与排查顺序

在真实环境中，问题通常集中在以下位置，且有明显优先级：

### 5.1 服务未对外监听（最高频）

特征：

* 本机 `localhost` 可访问
* 本机用局域网 IP 不可访问

结论：监听地址错误。

---

### 5.2 防火墙拦截端口

**特征：**

* 本机可访问
* 其他设备连接超时或被拒绝

**Windows 处理：**

1. 打开"Windows Defender 防火墙"
2. 点击"高级设置"
3. 选择"入站规则" → "新建规则"
4. 选择"端口" → TCP → 特定本地端口（输入你的端口号，如 `3000`）
5. 允许连接 → 完成

**macOS 处理：**

1. 系统设置 → 网络 → 防火墙
2. 点击"选项"
3. 如果有应用被阻止，点击"允许入站连接"

**Linux 处理：**

```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 3000/tcp

# CentOS/RHEL (firewalld)
sudo firewall-cmd --add-port=3000/tcp --permanent
sudo firewall-cmd --reload
```

---

### 5.3 局域网设备隔离（公司 / 访客 Wi‑Fi）

**特征：**

* 同一 Wi‑Fi
* 设备之间无法互相访问

**验证方法：**

在手机上 ping 电脑 IP（需要安装网络工具 App）：

```bash
# 如果 ping 不通，可能是设备隔离
ping 192.168.1.10
```

**解决：**

* 换到非访客 Wi‑Fi
* 联系网管关闭 AP Isolation（需要路由器权限）

---

### 5.4 VPN / 代理改变路由

**特征：**

* 开 VPN 后访问失效
* 关闭 VPN 恢复正常

**解决：**

* 临时关闭 VPN 测试
* 或配置 VPN 的 split-tunnel（让局域网流量不走 VPN）

---

## 6. 前后端联调中的 CORS 边界

当访问模型成立后，前后端联调常见的下一层问题是 **CORS**。

### 6.1 CORS 发生在哪一层

* CORS 是浏览器行为
* 与服务是否可访问无关

以下情况即为跨域：

```
http://192.168.1.10:3000
http://192.168.1.10:8080
```

端口不同，即视为跨域。

---

### 6.2 工程原则

* 前端地址变化（localhost → 局域网 IP）
* 后端必须同步放行对应 Origin

CORS 不应通过前端绕过，而应由后端明确配置。

---

## 7. 访问边界与安全说明

监听 `0.0.0.0` 通常只会暴露在局域网内，但仍需注意：

* 仅用于开发调试
* 避免暴露敏感服务
* 必要时加简单鉴权

---

## 8. 本文不覆盖的场景

以下问题不属于"同一 Wi‑Fi 访问本地服务"的范畴：

* 外网访问
* 内网穿透
* 公网部署

它们属于**网络边界扩展问题**，需要额外的安全与部署设计。

---

## 9. 总结

* `localhost` 是回环地址，只能本机访问
* 对外访问的前提是监听 `0.0.0.0`
* 局域网访问依赖本机 IP + 端口
* 监听地址错误是最常见问题
* CORS 是访问成立之后的下一层问题

理解访问模型，比记住配置命令更重要。

---
