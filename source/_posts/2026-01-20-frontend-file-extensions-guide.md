---
title: "📄 一篇搞懂前端常见文件后缀：ts / tsc / jsx / tsx / scss"
date: 2026-01-20 16:00:00
updated: {{current_date_time}}

categories:
  - 🏗️ 测试平台开发实战手记
  - 前端开发
tags:
  - TypeScript
  - React
  - 前端工程化
  - SCSS
  - 技术科普
keywords: ts, tsc, jsx, tsx, scss, 前端后缀, TypeScript编译器, React语法, 前端基础
description: '很多刚接触前端工程化的人都会被后缀劝退。本文从浏览器运行机制出发，深度解析 ts、tsx、jsx、scss 等常见后缀的本质及其在项目中的分工。'
top_img: /img/frontend-file-extensions-guide.png
cover: /img/frontend-file-extensions-guide.png
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

> **这是[《🏗️ 测试平台开发实战手记》](/categories/🏗️-测试平台开发实战手记/)系列的工具篇**

# 一篇搞懂前端常见文件后缀

## —— ts / tsc / jsx / tsx / scss 全面知识汇总 📚

很多刚接触前端工程化的人，都会被一堆文件后缀劝退：`.ts`、`.tsx`、`.jsx`、`.scss`、`tsc` …… **它们到底是什么？谁依赖谁？在项目里分别负责什么？**

这篇文章**不假设你已经懂前端**，而是从**“浏览器到底认识什么”**开始，一步步把整条链路讲清楚。

---

## 一、先从一个根本问题开始：浏览器到底认识什么？🌍

这是理解所有前端工具的**起点**。

👉 **浏览器只认识三样东西**：
* **HTML**：页面结构
* **CSS**：页面样式
* **JavaScript（JS）**：页面逻辑

除此之外的东西（ts、tsx、jsx、scss），**浏览器一概不认识。**

那为什么我们还天天写这些？👉 因为：**它们是“给人写的”，不是给浏览器写的。**

---

## 二、ts 是什么？—— JavaScript 的“安全带” 🛡️

### 1️⃣ ts 的本质
> **ts（TypeScript）= 带类型的 JavaScript**
它不是一门全新的语言，而是 **JS 的超集**。

### 2️⃣ 为什么需要 ts？
在 JS 中，`add(1, "2")` 会得到 `"12"` 而不报错。在 TS 中：
```ts
function add(a: number, b: number): number {
  return a + b
}
add(1, "2") // ❌ 编译期直接报错
```
✅ **错误在你写代码时就被发现，而不是上线后。**

---

## 三、tsc 是什么？—— TypeScript 编译器 ⚙️

### 1️⃣ 一句话定义
> **tsc = TypeScript Compiler**
它负责把“人写的代码（ts/tsx）”编译成“浏览器能跑的代码（js）”。

### 2️⃣ 核心工作
1. **类型检查**：看你有没有写错类型。
2. **转换**：把高级语法降级成浏览器兼容的 JS。

---

## 四、jsx vs tsx：React 开发者的必选项 🧩

### 1️⃣ jsx（JavaScript XML）
让用户在 JS 里写“像 HTML 的东西”。
```jsx
const element = <h1>Hello World</h1>
```
本质会被编译成 `React.createElement(...)`。

### 2️⃣ tsx（TypeScript + JSX）
当你的 React 项目引入了 TypeScript 约束时，后缀必须是 `.tsx`。

### 3️⃣ 文件后缀选择原则
| 你在写什么 | 用什么 |
| :--- | :--- |
| **纯逻辑 / 工具函数 / 接口定义** | `.ts` |
| **React 页面 / UI 组件** | `.tsx` |
| **老旧 JS 项目页面** | `.jsx` |

---

## 五、scss 是什么？—— 给 CSS 加上“工程能力” 🎨

CSS 无法嵌套，没有变量。SCSS 解决了这些痛点：
```scss
$main-color: #49b1f5;

.button {
  color: $main-color;
  &:hover {
    color: blue;
  }
}
```
📌 **最终它会被编译成标准的 `.css` 文件。**

---

## 六、把它们放在一起：一整个网页是怎么“跑起来”的？ 🔗

```text
tsx（页面 + 逻辑）
 ├─ ts（类型约束）
 ├─ jsx（页面结构）
 └─ scss（样式）
        ↓
   构建工具（Vite / Webpack / tsc）
        ↓
      js + css
        ↓
     浏览器渲染
```

---

## 七、终极记忆版总结 🧠

*   **ts**：让 JS 更安全（加个类型）。
*   **tsc**：把 ts 变成 js（翻译官）。
*   **jsx**：在 JS 里画 UI。
*   **tsx**：在更安全的 TS 里画 UI。
*   **scss**：更好写的样式表。

---

## 📚 延伸阅读
* [🏗️ 测试平台开发实战：账号体系模块设计](/2025/06/08/2025-06-08-account-system/)
* [🧠 Python 操作 XMind：从“能读懂”到“能生成”的深度指南](/2026/01/20/2026-01-20-python-xmind-operation-guide/)
