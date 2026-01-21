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

# 📄 一篇真正从工程里搞懂前端常见文件后缀

> **写在前面**：
>
> 这篇文章并不是我一开始就想写的。
>
> 在给测试平台补前端页面的时候，我连续踩了几个看似“很基础”的坑：
>
> * 有的文件明明只是加了个组件，却必须从 `.ts` 改成 `.tsx`
> * scss 嵌套一多，样式开始完全不受控
> * tsc 报错时，新人第一反应是「关掉它」
>
> 回头一看才发现，本质问题只有一个：**我并没有真正理解这些文件后缀在工程里的分工**。
>
> 所以有了这篇文章 —— 不是从定义开始，而是从**真实工程视角**，把 `ts / tsc / jsx / tsx / scss` 一次讲清楚。

---

## 一、先统一一个认知：浏览器到底认识什么？

这是所有前端工程化问题的起点，也是很多混乱的源头。

**浏览器只认识三样东西**：

* HTML（结构）
* CSS（样式）
* JavaScript（逻辑）

👉 结论很残酷但很重要：

> **`.ts`、`.tsx`、`.jsx`、`.scss`，浏览器一个都不认识。**

那问题来了：

> 既然浏览器不认识，为什么真实项目里却几乎都在用？

答案只有一句话：

> **这些文件，是给「人 + 工程」用的，不是给浏览器用的。**

---

## 二、ts：它不是为了“高级”，而是为了“不出事”

### 我是在什么时候真正理解 ts 的价值的？

不是学语法的时候，而是**线上出过一次低级 bug 之后**。

当时一个接口字段从 `string` 改成了 `number`：

* JS 版本：代码能跑，页面能渲染，直到某个分支逻辑 silently 出错
* TS 版本：**构建阶段直接报错，PR 合不上**

那一刻我才意识到：

> **ts 不是让你代码写得“更酷”，而是让错误更早暴露。**

### ts 的本质到底是什么？

一句工程化理解就够了：

> **ts = 带类型约束的 JavaScript**

它不是新语言，而是 JS 的「安全带」。

```ts
function add(a: number, b: number): number {
  return a + b
}

add(1, "2") // ❌ 在你提交代码之前就会被拦下
```

📌 工程经验总结：

* ts 的价值，**80% 体现在“你不小心写错的时候”**
* 如果你觉得 ts 很烦，通常说明：你还没被它救过

---

## 三、tsc：它更像“守门员”，而不是翻译官

### 新人常见误解

> tsc 不就是把 ts 变成 js 吗？

**对，但只说对了一半。**

### 在真实工程里，tsc 干了三件事

1. **类型检查（最重要）**
2. 语法降级（兼容浏览器）
3. 决定这段代码**有没有资格进入构建产物**

在测试平台项目中，我们有一个共识：

> **tsc 报错的代码，宁可不合，也不要“先跑起来再说”。**

📌 实战建议：

* 不要为了“快”而关掉 tsc
* 它拦下的，往往是未来最难查的 bug

---

## 四、jsx / tsx：真正让人困惑的不是语法，而是边界

### jsx：为什么 JS 里能写“像 HTML 的东西”？

```jsx
const element = <h1>Hello World</h1>
```

这是 React 引入的 JSX 语法糖，本质会被编译成：

```js
React.createElement('h1', null, 'Hello World')
```

### 那 tsx 是什么？

> **tsx = TypeScript + JSX**

一旦你在 React 组件里：

* 写 JSX
* 又想要类型约束

👉 后缀只能是 `.tsx`，没有第二种选择。

### 工程里最容易踩的一个坑

> 「反正是 React 项目，我全用 `.tsx` 不就好了？」

在小项目里，这么干问题不大；
但在中大型项目中，后果通常是：

* 工具函数混进 UI 层
* 类型边界变得模糊
* 组件依赖关系越来越乱

📌 一个被反复验证的实践原则：

| 场景                  | 推荐后缀   |
| ------------------- | ------ |
| 纯逻辑 / utils / hooks | `.ts`  |
| React 页面 / 组件       | `.tsx` |

> **tsx 是 UI 边界，不是默认选择。**

---

## 五、scss：它让样式“好写”，也让样式“更容易失控”

### scss 解决了什么问题？

* 变量
* 嵌套
* 复用（mixin）

```scss
$main-color: #49b1f5;

.button {
  color: $main-color;
  &:hover {
    color: blue;
  }
}
```

### 但工程里真正的坑在这

> **scss 的嵌套是没有“刹车”的。**

我见过最夸张的情况：

* 6 层嵌套
* 样式只敢改，不敢删
* 最后只能推倒重来

📌 实战建议：

* scss 解决的是“可维护性”，不是“写着爽”
* 嵌套超过 3 层，就该警惕了

---

## 六、把它们串起来：一个页面是怎么真正跑起来的？

```text
tsx（页面 + UI）
 ├─ ts（逻辑 / 类型）
 ├─ jsx（结构）
 └─ scss（样式）
        ↓
   构建工具（Vite / Webpack / tsc）
        ↓
      js + css
        ↓
     浏览器渲染
```

理解这条链路后，你会发现：

> **前端工程化的复杂度，本质是“把问题前移”。**

---

## 七、工程视角下的终极总结（不是定义版）

* **ts**：让我在提交代码前发现问题
* **tsc**：帮我挡掉不合格的代码
* **tsx**：明确 UI 边界，而不是滥用
* **scss**：提高效率，但必须有约束

> 如果你是在做一个内部平台 / 中小型系统：
>
> * 先把 ts / tsx 的边界立清楚
> * tsc 报错不要逃
> * scss 少即是多

这些，往往比“记住定义”更重要。
