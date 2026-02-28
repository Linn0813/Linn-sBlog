---
title: "同一 Wi‑Fi 下让别人访问你的本地前后端：完整操作指南"
date: 2026-01-26 10:00:00
updated: {{current_date_time}}
categories:
  - 🏗️ 测试平台开发实战手记
  - 技术科普
tags:
  - 网络
  - 本地开发
  - CORS
  - 前后端联调
keywords: localhost, 局域网访问, Wi-Fi, 0.0.0.0, CORS, 前后端联调, 本地开发, 网络模型, API 调用
description: '同一 Wi‑Fi 下，如何让别人访问你本地运行的前端页面，并能成功调用你本地运行的后端 API。本文提供完整操作步骤：网络配置、前后端监听、CORS 与 API 地址配置。'
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

> **在同一 Wi‑Fi 下，如何让别人访问你本地运行的前端页面，并能成功调用你本地运行的后端 API。**

典型场景：同事用手机打开你的本地开发地址，页面能正常加载，接口请求也能正确打到你的本地后端，而不是报错或请求失败。

* 先说明访问模型和必要前提
* 再给出前后端联调的完整操作步骤
* 最后列出常见失效位置（含 CORS、API 地址配置）

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

## 3. 前后端联调要做什么

当别人访问你的本地前端时，页面会发起 API 请求到后端。要让「访问 + 调用」都成功，需要同时满足：

| 步骤 | 配置项 | 说明 |
|-----|--------|------|
| 1 | 前端监听 `0.0.0.0` | 其他设备才能通过局域网 IP 打开你的前端页面 |
| 2 | 后端监听 `0.0.0.0` | 其他设备的浏览器才能把 API 请求发到你的后端 |
| 3 | 后端 CORS 放行前端 Origin | 前端地址从 `localhost:3000` 变为 `192.168.x.x:3000` 后，后端必须放行新的 Origin |
| 4 | 前端 API 地址指向正确 | 不能写死 `localhost:8080`，否则别人设备会请求他们自己的 localhost |

**第 4 步最容易忽略**：别人用 `http://192.168.1.10:3000` 打开你的前端时，如果前端请求的是 `http://localhost:8080/api/xxx`，浏览器会在**对方设备**上请求 localhost，而不是你的电脑。正确做法是使用 `http://192.168.1.10:8080` 或通过相对路径/环境变量动态配置。

---

## 4. 最小可行配置（MVP）

如果你只关心"如何尽快让别人访问到并能调通接口"，可以按以下路径配置：

1. 查到本机局域网 IP（如 `192.168.1.10`）
2. 前端、后端都监听 `0.0.0.0`
3. 后端 CORS 放行 `http://192.168.1.10:前端端口`
4. 前端 API 基础地址配置为 `http://192.168.1.10:后端端口`（或使用相对路径）
5. 使用 `http://192.168.1.10:前端端口` 访问

只要本机用该地址能打开页面且接口正常，其他设备在同一 Wi‑Fi 下通常也可以。

---

## 4.1 完整实操步骤（新手友好版）

下面以「Vite 前端 + Express 后端」为例，手把手走一遍前后端联调流程。

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

### Step 2：启动前端并监听 0.0.0.0

```bash
# 在前端项目目录
npm run dev -- --host
```

启动后应看到 `Network: http://192.168.1.10:5173/`。若只有 `Local` 没有 `Network`，说明未监听 `0.0.0.0`。

### Step 3：启动后端并监听 0.0.0.0，配置 CORS

```js
// Express 示例
const express = require('express');
const cors = require('cors');
const app = express();

// 关键：放行前端的 Origin（局域网 IP + 前端端口）
app.use(cors({
  origin: [
    'http://localhost:5173',
    'http://192.168.1.10:5173'  // 替换为你的实际 IP 和前端端口
  ]
}));

app.get('/api/hello', (req, res) => {
  res.json({ message: 'Hello' });
});

app.listen(8080, '0.0.0.0', () => {
  console.log('Backend on http://0.0.0.0:8080');
});
```

### Step 4：配置前端 API 基础地址

前端请求后端时，不能写死 `http://localhost:8080`。可用环境变量或构建时注入：

```ts
// 示例：Vite 环境变量
// .env.development
VITE_API_BASE=http://192.168.1.10:8080

// 或使用相对路径（若前端通过同一域名代理到后端）
// vite.config.ts 中配置 proxy 时，前端用 /api 即可
```

若使用代理，确保代理目标也是 `0.0.0.0` 或局域网 IP，否则其他设备访问时代理仍会指向错误地址。

### Step 5：在本机验证

在本机浏览器打开 `http://192.168.1.10:5173`，打开开发者工具 Network，确认：

* 页面能打开
* API 请求能成功返回（状态码 200，无 CORS 报错）

若本机用局域网 IP 打不开或接口报错，先解决本机问题再让其他人访问。

### Step 6：让其他设备访问

1. 确保手机/同事电脑和你连的是**同一个 Wi‑Fi**
2. 在对方浏览器输入：`http://192.168.1.10:5173`
3. 页面能打开且接口正常 → 成功

### 常见问题

**Q：本机用 `192.168.1.10:5173` 打不开？**

A：服务未监听 `0.0.0.0`。检查 Vite 是否加了 `--host`，Express 是否 `app.listen(8080, '0.0.0.0')`。

**Q：页面能打开，但接口报 CORS 错误？**

A：后端 CORS 未放行 `http://192.168.1.10:5173`。参考第 7 节配置。

**Q：接口请求发到了错误的地址（如对方设备的 localhost）？**

A：前端 API 基础地址配置错误，需改为局域网 IP 或相对路径。

**Q：本机正常，但手机打不开？**

A：按第 6 节排查：防火墙、同一 Wi‑Fi、设备隔离。

---

## 5. 常见技术栈的监听配置

下面仅列出**监听地址相关配置**，不涉及其他启动参数。

### 5.1 Vite

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

### 5.2 Create React App

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

### 5.3 Node / Express

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

### 5.4 Flask

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

### 5.5 Spring Boot

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

## 6. 常见失效位置与排查顺序

在真实环境中，问题通常集中在以下位置，且有明显优先级：

### 6.1 服务未对外监听（最高频）

特征：

* 本机 `localhost` 可访问
* 本机用局域网 IP 不可访问

结论：监听地址错误。

---

### 6.2 防火墙拦截端口

**特征：**

* 本机可访问
* 其他设备连接超时或被拒绝

**Windows 处理：**

1. 打开"Windows Defender 防火墙"
2. 点击"高级设置"
3. 选择"入站规则" → "新建规则"
4. 选择"端口" → TCP → 特定本地端口（输入端口号，前后端联调需同时放行前端端口如 `5173` 和后端端口如 `8080`）
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

### 6.3 局域网设备隔离（公司 / 访客 Wi‑Fi）

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

### 6.4 VPN / 代理改变路由

**特征：**

* 开 VPN 后访问失效
* 关闭 VPN 恢复正常

**解决：**

* 临时关闭 VPN 测试
* 或配置 VPN 的 split-tunnel（让局域网流量不走 VPN）

---

## 7. 前后端联调中的 CORS 与 API 地址

当别人能访问你的前端页面后，若接口报错，通常是 **CORS** 或 **API 地址配置** 问题。

### 7.1 CORS 发生在哪一层

* CORS 是浏览器行为
* 与服务是否可访问无关

以下情况即为跨域：

```
http://192.168.1.10:3000
http://192.168.1.10:8080
```

端口不同，即视为跨域。

---

### 7.2 后端 CORS 配置示例

**Express（cors 中间件）：**

```js
const cors = require('cors');
app.use(cors({
  origin: [
    'http://localhost:5173',
    'http://192.168.1.10:5173'  // 局域网访问时的前端地址
  ]
}));
```

**Flask：**

```python
from flask_cors import CORS
CORS(app, origins=['http://localhost:5173', 'http://192.168.1.10:5173'])
```

**Spring Boot：**

```java
@Configuration
public class CorsConfig {
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/api/**")
                    .allowedOrigins("http://localhost:5173", "http://192.168.1.10:5173");
            }
        };
    }
}
```

开发阶段也可临时放行所有 Origin（`*`），但生产环境务必限制。

### 7.3 前端 API 地址配置原则

* 别人用 `http://192.168.1.10:3000` 访问时，前端请求的 API 地址必须是 `http://192.168.1.10:8080`（或你的后端端口），不能是 `localhost`
* 推荐用环境变量：`VITE_API_BASE`、`REACT_APP_API_URL` 等，根据访问方式切换
* 若使用 Vite/Webpack 的 proxy，注意代理只在开发时对本机生效，其他设备访问时不会走代理，需直接配置后端地址

---

## 8. 访问边界与安全说明

监听 `0.0.0.0` 通常只会暴露在局域网内，但仍需注意：

* 仅用于开发调试
* 避免暴露敏感服务
* 必要时加简单鉴权

---

## 9. 本文不覆盖的场景

以下问题不属于"同一 Wi‑Fi 访问本地服务"的范畴：

* 外网访问
* 内网穿透
* 公网部署

它们属于**网络边界扩展问题**，需要额外的安全与部署设计。

---

## 10. 总结

要让别人在同一 Wi‑Fi 下访问你的本地前后端并成功调用接口，需要：

* **前端、后端都监听 `0.0.0.0`**，否则其他设备无法访问
* **后端 CORS 放行前端的 Origin**（含 `http://你的局域网IP:前端端口`）
* **前端 API 地址指向你的后端**，不能写死 `localhost`，否则会请求到对方设备

理解「访问模型 + CORS + API 地址」这三层，比记住配置命令更重要。

---
