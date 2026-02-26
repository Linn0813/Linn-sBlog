---
title: "前端常见文件后缀指南：ts / tsc / jsx / tsx / scss"
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
description: '从浏览器运行机制出发，系统解析 ts、tsx、jsx、scss 等常见后缀的本质、分工与适用场景。'
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

本文从浏览器运行机制出发，系统解析 `ts`、`tsc`、`jsx`、`tsx`、`scss` 等常见后缀的本质、分工与适用场景，帮助读者建立清晰的文件类型与工程实践认知。


---

## 一、前置认知：浏览器实际支持什么？

浏览器只认识三类资源：

| 类型 | 用途 |
|------|------|
| HTML | 结构 |
| CSS | 样式 |
| JavaScript | 逻辑 |

**核心结论**：`.ts`、`.tsx`、`.jsx`、`.scss` 均无法被浏览器直接执行，需经构建工具编译为 js/css 后使用。

**术语速查**：构建 = 将 ts/tsx/scss 编译为浏览器可执行的 js/css；PR = 代码合并请求；构建产物 = 最终打包出的 js、css 文件。

---

## 二、ts：带类型约束的 JavaScript

### 2.1 定义与本质

**ts = 带类型约束的 JavaScript**，本质是 JS 的超集，通过类型约束在编译阶段提前发现错误。

```ts
function add(a: number, b: number): number {
  return a + b
}

add(1, "2") // ❌ 编译阶段即被拦截
```

### 2.2 典型场景

接口字段类型变更时：

- **JS**：代码可运行，但类型不匹配分支可能静默失效，逻辑错误难以排查
- **TS**：类型声明后，tsc 在编译阶段报错，需修正类型后才能通过

示例：若 `userId` 从 `string` 改为 `number`，前端仍写 `if (userId === "123")`，TS 会直接报错。

### 2.3 错误 vs 正确

| 场景 | 错误 | 正确 |
|------|------|------|
| 接口返回 `{ count: 100 }`，误写 `count.toUpperCase()` | JS 运行时才报错 | TS 在编写时即红线提示「number 无 toUpperCase 方法」 |

**实践要点**：ts 的价值主要体现在类型错误提前暴露，避免将问题带入运行时。

---

## 三、tsc：类型检查与编译

### 3.1 职能

tsc（TypeScript Compiler）除将 ts 编译为 js 外，主要承担：

1. **类型检查**（核心）
2. 语法降级（兼容目标浏览器）
3. 决定代码是否可进入构建产物

### 3.2 典型报错示例

```text
// 代码：
const user = { name: "张三", age: 18 };
user.age.toUpperCase();

// tsc 报错：
// Property 'toUpperCase' does not exist on type 'number'.
```

关闭 tsc 后代码可运行，但 `age` 为数字时会在运行时崩溃。tsc 在编译阶段即可拦截此类问题。

### 3.3 错误 vs 正确

| 场景 | 错误 | 正确 |
|------|------|------|
| 遇到 tsc 报错 | 注释类型、关闭检查 | 修正类型或使用类型断言，使 tsc 通过 |

**实践要点**：tsc 报错不应通过关闭检查规避，应通过修正类型或合理断言解决。

---

## 四、jsx / tsx：语法与边界

### 4.1 jsx

jsx 是 React 引入的语法扩展，允许在 JS 中书写类似 HTML 的结构，编译后被转换为 `React.createElement` 调用：

```jsx
const element = <h1>Hello World</h1>
// 编译为：
// React.createElement('h1', null, 'Hello World')
```

### 4.2 tsx

**tsx = TypeScript + JSX**。若在 React 组件中同时使用 JSX 与类型约束，文件后缀必须为 `.tsx`。

### 4.3 错误 vs 正确

| 场景 | 错误 | 正确 |
|------|------|------|
| 在 `.ts` 中书写 `<Button />` | 报错：`JSX element implicitly has type 'any'` | 将文件改为 `.tsx` |

### 4.4 后缀选择原则

| 场景 | 推荐后缀 |
|------|----------|
| 纯逻辑 / utils / hooks | `.ts` |
| React 页面 / 组件 | `.tsx` |

**实践要点**：tsx 用于 UI 边界，纯逻辑、工具函数应使用 `.ts`，避免将工具函数混入 UI 层。

---

## 五、scss：变量、嵌套与维护

### 5.1 能力

| 能力 | 说明 |
|------|------|
| 变量 | 统一管理颜色、尺寸等 |
| 嵌套 | 按结构组织选择器 |
| 复用 | mixin、继承等 |

```scss
$main-color: #49b1f5;

.button {
  color: $main-color;
  &:hover {
    color: blue;
  }
}
```

### 5.2 嵌套深度规范

嵌套过深会导致选择器权重过高、难以维护。建议：

- **可接受**：3 层以内
- **需警惕**：超过 3 层

```scss
// ✅ 可接受
.card {
  .header { font-size: 16px; }
  .body { padding: 12px; }
}

// ❌ 失控：6 层嵌套，选择器权重爆炸
.page .layout .sidebar .menu .item .link {
  color: blue;
}
```

**实践要点**：scss 侧重可维护性，嵌套应控制在合理深度，避免「只敢改不敢删」的情况。

---

## 六、构建链路概览

```
tsx（页面 + UI）
 ├─ ts（逻辑 / 类型）
 ├─ jsx（结构）
 └─ scss（样式）
        ↓
   构建工具（Vite / Webpack 等）
        ↓
      js + css
        ↓
     浏览器渲染
```

前端工程化的本质是**将问题前移到构建阶段**，通过类型检查、编译与规范约束，降低运行时错误概率。

---

## 七、快速决策表

| 场景 | 后缀 | 说明 |
|------|------|------|
| 工具函数、hooks、类型定义 | `.ts` | 无 JSX，纯逻辑 |
| React 组件、页面（含 `<xxx />`） | `.tsx` | 有 JSX 必须用 tsx |
| `.ts` 中写入 `<Button />` 报错 | 改为 `.tsx` | 编译器不识别 ts 中的 JSX |
| tsc 报类型错误 | 修类型或加断言 | 不通过关闭检查规避 |
| scss 嵌套超过 3 层 | 拆分为多个类 | 减少嵌套深度 |

---

## 八、知识自测

1. **浏览器能否直接执行 `.tsx`？** → 不能，需先构建为 js
2. **文件中有 `<div>` 时，应使用 `.ts` 还是 `.tsx`？** → `.tsx`
3. **tsc 报错时，正确做法是？** → 修正类型或使用类型断言，而非关闭检查
4. **scss 嵌套几层应引起警惕？** → 3 层

---

## 九、总结

| 后缀/工具 | 核心作用 |
|------|----------|
| ts | 在提交前通过类型约束发现错误 |
| tsc | 拦截不符合类型规范的代码 |
| tsx | 明确 UI 边界，与纯逻辑区分 |
| scss | 提升样式可维护性，需控制嵌套深度 |

**实践建议**：明确 ts/tsx 边界、不规避 tsc 报错、scss 嵌套少即是多。理解这些比记忆定义更重要。
