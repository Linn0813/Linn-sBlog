---
title: 🧩 前端工程实战：HTTP 请求拦截与错误处理的正确姿势
date: 2025-06-30 16:05:38
tags:
  - HTTP拦截器
  - 请求拦截
  - 响应拦截
  - 错误处理
  - axios
categories:
- 项目实战 & 测试经验（Testing Practices & Case Studies）
  - 前端实践
  - 错误处理
updated: {{current_date_time}}
keywords: HTTP拦截器, 请求拦截, 响应拦截, 错误处理, axios
description: '通过 axios 示例，讲解前端 HTTP 请求拦截与响应拦截机制，以及统一处理异常、提升用户体验与开发效率的方法！'
top_img: /img/http-interceptor-error-handling.png
cover: /img/http-interceptor-error-handling.png
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


# 🧩 前端工程实战：HTTP 请求拦截与错误处理的正确姿势

> “接口请求失败了？怎么都没提示！”
> “后端 401 了我还在页面继续点……”
>
> 如果你也在项目中遇到过类似的尴尬场面，那你可能需要好好了解一下前端的 **HTTP 请求拦截与错误处理机制**。

在 Vue/React 等现代前端项目中，接口请求是日常开发的核心。而如何在全局优雅地管理这些请求 —— 包括统一加 token、统一错误弹窗、自动跳转登录、捕获网络异常 —— 是项目健壮性的重要保障。

本文将通过 `axios` 为例，讲解如何**拦截请求与响应、集中处理异常、提升用户体验与开发效率**。

---

## 📦 什么是请求拦截与响应拦截？

使用 `axios` 时，可以通过拦截器为每个请求/响应 **统一加料或做处理**，如同为接口套上中间件。

```ts
// 请求拦截器
axios.interceptors.request.use(config => {
  // 在发送请求前统一加上 token
  config.headers.Authorization = getToken();
  return config;
}, error => Promise.reject(error));

// 响应拦截器
axios.interceptors.response.use(response => {
  // 成功返回的数据可以在这里预处理
  return response.data;
}, error => {
  // 统一错误处理
  handleError(error);
  return Promise.reject(error);
});
```

---

## ✨ 请求拦截：统一处理请求前的操作

请求拦截通常用于：

| 用途                     | 示例                     |
| ---------------------- | ---------------------- |
| 添加鉴权 token             | 加入 `Authorization` 请求头 |
| 加统一前缀或 baseUrl         | 适配代理或环境                |
| 发起 loading 状态          | 显示页面 loading 动效        |
| 加入 traceId / sessionId | 后端日志定位、流程追踪            |

示例代码：

```ts
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  // 可添加其他 headers
  config.headers['X-Request-Id'] = generateUUID();
  return config;
}, error => {
  return Promise.reject(error);
});
```

---

## ⚠ 响应拦截：统一处理返回结果和错误

响应拦截可以做两件事：

### ✅ 1. 数据格式统一处理

很多接口返回格式如：

```json
{ "code": 0, "data": { ... }, "msg": "成功" }
```

可以统一处理成：

```ts
axios.interceptors.response.use(response => {
  const { code, data, msg } = response.data;
  if (code === 0) {
    return data;
  } else {
    ElMessage.error(msg || '请求失败');
    return Promise.reject(new Error(msg));
  }
});
```

这样组件中就能直接使用：

```ts
const res = await api.getUser(); // 返回 data
```

### ❌ 2. 错误处理（401、500、断网等）

```ts
axios.interceptors.response.use(
  res => res,
  error => {
    const status = error.response?.status;
    if (status === 401) {
      ElMessage.warning('登录已失效，请重新登录');
      router.push('/login');
    } else if (status === 500) {
      ElMessage.error('服务器开小差了，请稍后重试');
    } else if (!error.response) {
      ElMessage.error('网络异常，请检查网络连接');
    } else {
      ElMessage.error(error.response.data?.msg || '请求失败');
    }
    return Promise.reject(error);
  }
);
```

---

## 🛠 实战推荐策略

在实际项目中，我们建议这样组织 HTTP 拦截与错误处理逻辑：

### ✅ 拦截器注册模块化封装

```ts
// http.ts
import axios from 'axios';
import { ElMessage } from 'element-plus';

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

// 请求拦截器
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) config.headers['Authorization'] = `Bearer ${token}`;
  return config;
});

// 响应拦截器
instance.interceptors.response.use(
  res => {
    const { code, data, msg } = res.data;
    if (code === 0) return data;
    ElMessage.error(msg || '请求失败');
    return Promise.reject(new Error(msg));
  },
  error => {
    const status = error.response?.status;
    if (status === 401) {
      ElMessage.warning('登录过期，请重新登录');
      location.href = '/login';
    } else {
      ElMessage.error('网络错误或服务异常');
    }
    return Promise.reject(error);
  }
);

export default instance;
```

### ✅ API 调用示例

```ts
// api/user.ts
import request from '@/utils/http';

export function getUserInfo() {
  return request.get('/user/info');
}
```

---

## 📌 常见错误场景处理建议

| 错误类型       | 建议做法                       |
| ---------- | -------------------------- |
| 401 未授权    | 清 token，跳转登录页              |
| 403 权限不足   | 弹出提示，无跳转                   |
| 404 接口不存在  | 提示后上报错误日志                  |
| 500 后端异常   | 弹窗提示、允许用户重试                |
| 网络超时 / 断网  | 提示网络问题，可选 loading fallback |
| code !== 0 | 按后端定义规则提示用户                |

---

## 🎯 总结

* ✅ 使用请求拦截器统一加 token、traceId；
* ✅ 使用响应拦截器统一处理 code 判断与异常提示；
* ✅ 错误处理应清晰有反馈，不让用户“黑盒使用”；
* ✅ 拦截器逻辑推荐模块化封装，避免重复代码；
* ✅ 项目越大，统一错误处理带来的收益越明显。

---

你还可以进一步引入：

* 🔍 `Sentry` 等错误监控工具，记录异常
* ⏱ loading 状态统一处理（如配合全局 loading 管理器）
* 🚥 请求取消功能（如路由切换时中断无用请求）

---

> 你项目中是如何处理 HTTP 请求与错误的？欢迎留言分享经验！


