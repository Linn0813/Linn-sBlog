---
title: 🧩【前端实践】环境变量 vs Vite 代理：API 地址配置的最佳实践
date: 2025-06-30 15:51:30
tags:
  - API地址配置
  - 环境变量
  - Vite代理
  - 前后端分离
  - 开发配置
categories:
- 项目实战 & 测试经验（Testing Practices & Case Studies）
  - 前端实践
  - 开发配置
updated: {{current_date_time}}
keywords: API地址配置, 环境变量, Vite代理, 前后端分离, 开发配置
description: '分享前后端分离项目中 API 请求地址的两种配置方案：使用环境变量（baseUrl）和 Vite 代理，对比其优缺点并给出最佳实践建议！'
top_img: /img/api-baseurl-vs-vite-proxy.png
cover: /img/api-baseurl-vs-vite-proxy.png
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
noticeOutdate: falsetags
---


# 🧩【前端实践】环境变量 vs Vite 代理：API 地址配置的最佳实践

在前后端分离项目中，**如何优雅配置 API 请求地址**，既能本地开发方便调试、又能线上部署稳定切换，是一个绕不过去的问题。

今天我们聊聊两种常见方案：

* ✅ 使用环境变量（`baseUrl`）
* ✅ 使用 Vite 的代理配置

它们看似相似，实则**适用场景、优缺点完全不同**。掌握它们的使用原则，将大大提升项目的可维护性与环境适配能力。

---

## ☁ 场景介绍：前端如何请求后端接口？

我们以一个典型的 Vue + Vite 项目为例，调用接口的方式有两种：

---

## 1️⃣ 使用环境变量（baseUrl）

### ✅ 写法示例：

```js
const baseUrl = import.meta.env.VITE_API_BASE_URL;
axios.post(`${baseUrl}/api/xxx`, {...})
```

### ✅ 优点：

* ✅ **多环境切换灵活**：只需修改 `.env` 文件，不需改动代码。
* ✅ **适配生产环境**：部署时，前端可直接请求真实后端地址（无需代理）。
* ✅ **利于前后端分开部署**：如前端在 CDN、后端在独立服务器，适配性强。

### ⚠ 缺点：

* ⚠ **开发时会遇到跨域（CORS）**：需要后端设置允许跨域。
* ⚠ **需要为每个环境维护一份 `.env` 文件**：如 `.env.development`、`.env.test`、`.env.production` 等。

---

## 2️⃣ 使用 Vite 的代理功能

### ✅ 写法示例：

```js
// axios 请求
axios.post('/api/xxx', {...})

// vite.config.ts 配置
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
})
```

### ✅ 优点：

* ✅ **开发环境免跨域**：Vite 自带代理功能，前端请求会被重定向到本地后端服务。
* ✅ **接口调用路径统一简洁**：代码中只写 `/api/xxx`，无需处理不同环境的域名。

### ⚠ 缺点：

* ⚠ **只适用于开发环境**：生产环境部署时没有 Vite 代理功能。
* ⚠ **线上部署还需 nginx 或其它反向代理配置**：否则路径 `/api/xxx` 无法找到目标。

---

## ✅ 推荐实践：开发用代理，部署用环境变量

经过多项目实践，我们总结出一套稳定可复用的做法：

| 阶段      | API配置                         | 推荐方式                          |
| ------- | ----------------------------- | ----------------------------- |
| 🧪 开发环境 | `/api/xxx` + Vite代理           | 使用 Vite `server.proxy` 解决跨域   |
| 🚀 生产环境 | `https://api.xxx.com/api/xxx` | 使用环境变量 + 后端 CORS 设置或 nginx 代理 |

---

## 📌 示例配置模板

### 📂 `.env.development`

```bash
VITE_API_BASE_URL=/api
```

### 📂 `.env.production`

```bash
VITE_API_BASE_URL=https://api.xxx.com
```

### 📂 `vite.config.ts`

```ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
    }
  }
}
```

### 📂 axios 请求代码（统一写法）

```ts
const baseUrl = import.meta.env.VITE_API_BASE_URL;
axios.post(`${baseUrl}/api/xxx`, data);
```

这样的写法有三个好处：

1. 📦 **前端代码不变**，只依赖环境变量。
2. 🔁 **支持所有环境自由切换**，不用到处改路径。
3. 🧩 **适配代理 / 非代理统一路径结构**。

---

## 🧠 小结建议

| 项目需求          | 推荐方式                     | 说明                |
| ------------- | ------------------------ | ----------------- |
| 本地调试便捷        | Vite Proxy               | 本地无跨域问题，前后端联调快速   |
| 多环境部署灵活       | 环境变量 `VITE_API_BASE_URL` | 替换地址即可适配不同部署      |
| 路径统一          | axios 基于 `baseUrl` 拼接    | 减少 if/else 或魔法字符串 |
| 分开部署 / CDN 发布 | 使用绝对后端地址                 | 无代理支持时只能走后端接口地址   |

---

## 🔚 最佳实践总结

* 本地开发推荐 **使用 Vite 代理**，无需处理跨域，开发体验更顺滑；
* 生产环境推荐 **使用环境变量配置 baseUrl**，便于部署和管理；
* 推荐统一使用：

  ```js
  axios.post(`${baseUrl}/api/xxx`, ...)
  ```

  让环境切换只需改 `.env` 文件，无需动代码。

